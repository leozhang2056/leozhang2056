#!/usr/bin/env python3
"""
LinkedIn Saved Jobs Fetcher — Playwright + Chrome automation.

Connects to your existing Chrome (via CDP) or launches a fresh instance,
scrapes LinkedIn saved jobs, lets you pick one (or auto-select), fetches
the full JD text, saves it to jd_archive/, then optionally triggers the CV
generation pipeline.

Usage:
    python generate.py li-jd                           # interactive
    python generate.py li-jd --port 9222                # custom CDP port
    python generate.py li-jd --auto 0 --no-generate     # auto-pick first, fetch only
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
JD_ARCHIVE_DIR = REPO_ROOT / "jd_archive"
DEFAULT_CDP_PORT = 9222


# ---------------------------------------------------------------------------
# Chrome discovery (Windows)
# ---------------------------------------------------------------------------
def _chrome_default_profile() -> Optional[str]:
    """Return the default Chrome user-data-dir on Windows, or None."""
    local = os.environ.get("LOCALAPPDATA", "")
    if not local:
        return None
    candidate = Path(local) / "Google" / "Chrome" / "User Data"
    return str(candidate) if candidate.is_dir() else None


def _find_chrome_exe() -> Optional[str]:
    """Locate the Chrome executable on Windows."""
    candidates = [
        os.environ.get("CHROME_PATH", ""),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def _launch_chrome_with_debug(port: int = DEFAULT_CDP_PORT) -> Optional[subprocess.Popen]:
    """
    Launch Chrome with --remote-debugging-port using the default user profile.
    Returns the Popen handle, or None on failure.
    """
    exe = _find_chrome_exe()
    if not exe:
        print("Could not locate Chrome. Please install Chrome or start it manually with:")
        print(f"  chrome --remote-debugging-port={port}")
        return None
    profile = _chrome_default_profile()
    args = [
        exe,
        f"--remote-debugging-port={port}",
    ]
    if profile:
        args.append(f'--user-data-dir="{profile}"')
    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"Launched Chrome (PID {proc.pid}) on port {port}.")
        return proc
    except Exception as e:
        print(f"Failed to launch Chrome: {e}")
        return None


# ---------------------------------------------------------------------------
# Browser connection
# ---------------------------------------------------------------------------
async def _ensure_browser(port: int = DEFAULT_CDP_PORT, keep_chrome: bool = False):
    """
    Return an (async_playwright, browser) tuple.

    Strategy:
    1. Try connecting to an existing Chrome via CDP (--remote-debugging-port).
    2. If fails and keep_chrome=False: kill running Chrome, relaunch with
       --remote-debugging-port so we connect to **your real Chrome**.
    3. If keep_chrome=True or step 2 fails: use Playwright's bundled Chromium.

    Usage:
        p, browser = await _ensure_browser(port)
        page = await browser.new_page()
        ...
        await browser.close()
        await p.stop()
    """
    from playwright.async_api import async_playwright

    p = await async_playwright().__aenter__()

    # ── 1. CDP (user already has Chrome with --remote-debugging-port) ──────
    cdp_url = f"http://127.0.0.1:{port}"
    try:
        browser = await p.chromium.connect_over_cdp(cdp_url, timeout=5000)
        print(f"Connected to existing Chrome via CDP ({cdp_url}).")
        return p, browser
    except Exception:
        pass

    # ── 2. Kill running Chrome, restart with debug port ───────────────────
    if keep_chrome:
        _safe_print("--keep-chrome set. Falling back to Playwright Chromium.")
        browser = await p.chromium.launch(headless=False)
        return p, browser

    exe = _find_chrome_exe()
    if not exe:
        _safe_print("Chrome not found. Falling back to Playwright Chromium.")
        browser = await p.chromium.launch(headless=False)
        return p, browser

    # Running Chrome blocks the debug port, so kill it first
    _safe_print(f"Restarting Chrome with debug port (--remote-debugging-port={port})...")
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "chrome.exe"],
            capture_output=True, timeout=10,
        )
        await asyncio.sleep(3)
    except Exception:
        pass

    # Launch Chrome with debug port + default user profile
    profile_dir = _chrome_default_profile()
    launch_args = [exe, f"--remote-debugging-port={port}"]
    if profile_dir:
        launch_args.append(f'--user-data-dir="{profile_dir}"')
    _safe_print("Starting Chrome...")
    try:
        subprocess.Popen(launch_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as exc:
        _safe_print(f"  Failed to start Chrome: {_safe_str(exc)}. "
                     "Falling back to Playwright Chromium.")
        browser = await p.chromium.launch(headless=False)
        return p, browser

    # Wait for Chrome to be ready
    for _ in range(45):
        await asyncio.sleep(1)
        try:
            browser = await p.chromium.connect_over_cdp(cdp_url, timeout=3000)
            _safe_print("Connected to Chrome via CDP.")
            return p, browser
        except Exception:
            continue

    _safe_print("Timed out waiting for Chrome debug port. Falling back to Playwright Chromium.")
    browser = await p.chromium.launch(headless=False)
    return p, browser


# ---------------------------------------------------------------------------
# Safe I/O helpers (avoid GBK/UnicodeEncodeError on Windows)
# ---------------------------------------------------------------------------
def _safe_str(text: object) -> str:
    return str(text).encode("ascii", errors="replace").decode("ascii")

def _safe_print(*args, **kw) -> None:
    text = " ".join(str(a) for a in args)
    try:
        print(text, **kw)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"), **kw)


# ---------------------------------------------------------------------------
# LinkedIn scraper
# ---------------------------------------------------------------------------
SAVED_JOBS_URL = "https://www.linkedin.com/my-items/saved-jobs/"


LOGIN_TIMEOUT = 300  # seconds (5 minutes)


async def _wait_for_login(page) -> None:
    """Wait until the user is logged into LinkedIn.  Returns when logged in,
    or raises TimeoutError after LOGIN_TIMEOUT seconds."""
    # Quick check: already logged in?
    try:
        has_nav = await page.evaluate(
            "() => !!document.querySelector('nav.global-nav__nav, "
            ".global-nav__nav, [data-global-nav]')"
        )
        if has_nav:
            return
    except Exception:
        pass

    print("LinkedIn login required. Please log in in the browser window...")
    # Navigate to login page (only if not already there)
    try:
        if "login" not in page.url:
            await page.goto("https://www.linkedin.com/login",
                            wait_until="domcontentloaded", timeout=15000)
    except Exception:
        pass  # page may already be closing

    deadline = asyncio.get_event_loop().time() + LOGIN_TIMEOUT
    print("Waiting for you to log in...", end="", flush=True)
    while asyncio.get_event_loop().time() < deadline:
        await asyncio.sleep(2)
        try:
            current_url = page.url
            if "/feed" in current_url or "/my-items" in current_url or "/jobs" in current_url:
                print(" OK")
                return
            has_nav = await page.evaluate(
                "() => !!document.querySelector('nav.global-nav__nav, "
                ".global-nav__nav, [data-global-nav]')"
            )
            if has_nav:
                print(" OK")
                return
        except Exception:
            # Page/browser was closed — give a clear message
            print("\nBrowser window was closed. Exiting.")
            raise SystemExit(1)
        print(".", end="", flush=True)

    print("\nLogin timed out after 5 minutes. Please try again.")
    raise SystemExit(1)


async def _extract_job_cards(page) -> list[dict]:
    """
    Extract job cards from the current saved-jobs page via JavaScript.
    Returns [{title, company, location, url}, ...].
    """
    return await page.evaluate("""() => {
        const results = [];

        // Try multiple selector strategies
        const cardSelectors = [
            'li.job-card-list', 'li[data-urn*="job"]', '.job-card-container',
            'article.job-card', '[data-job-id]', '.ember-view > li',
        ];

        let cards = [];
        for (const sel of cardSelectors) {
            const found = document.querySelectorAll(sel);
            if (found.length > 0) { cards = found; break; }
        }

        // If no cards found via selectors, try finding job links directly
        if (cards.length === 0) {
            const links = document.querySelectorAll('a[href*="/jobs/view/"]');
            const processed = new Set();
            links.forEach(a => {
                const href = a.href;
                if (processed.has(href)) return;
                processed.add(href);
                const card = a.closest('li, article, div[class*="card"], div[class*="item"]') || a.parentElement;
                results.push({
                    title: (a.innerText || a.textContent || '').trim(),
                    company: '',
                    location: '',
                    url: href,
                    rawHtml: card ? card.innerHTML.substring(0, 300) : '',
                });
            });
            return results;
        }

        cards.forEach(card => {
            const link = card.querySelector('a[href*="/jobs/view/"]');
            if (!link) return;
            const url = link.href;
            const title = (link.innerText || link.textContent || '').trim();
            if (!title) return;

            // Find company name
            const companyEl = card.querySelector(
                '.job-card-container__primary-description, ' +
                '[class*="company-name"], [class*="company"], ' +
                '.artdeco-entity-lockup__subtitle, ' +
                'span[class*="primary-description"]'
            );
            const company = companyEl ? (companyEl.innerText || companyEl.textContent || '').trim() : '';

            // Find location
            const locationEl = card.querySelector(
                '.job-card-container__metadata-item, ' +
                '[class*="location"], ' +
                'li[class*="metadata"], ' +
                'span[class*="secondary-description"]'
            );
            const location = locationEl ? (locationEl.innerText || locationEl.textContent || '').trim() : '';

            results.push({ title, company, location, url });
        });

        return results;
    }""")


async def _extract_jd_text(page) -> str:
    """
    Extract the job description text from a LinkedIn job page.
    Handles 'Show more' / 'Show less' expanders.
    """
    # Click "Show more" if present
    try:
        show_more = page.locator('button:has-text("Show more"), button:has-text("show more"), a:has-text("Show more")')
        if await show_more.is_visible(timeout=2000):
            await show_more.click()
            await asyncio.sleep(0.5)
    except Exception:
        pass

    jd_text = await page.evaluate("""() => {
        // Collect text from common JD containers
        const selectors = [
            '.jobs-description-content',
            '.jobs-box__box',
            '.job-view-layout',
            '.description__text',
            '.show-more-less-html__markup',
            'div[class*="job-details"]',
            'div[class*="description"]',
            'section[class*="description"]',
            '#job-details',
            '[data-job-description]',
        ];
        let texts = [];
        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el && el.innerText && el.innerText.length > 100) {
                texts.push(el.innerText.trim());
            }
        }
        // Fallback: get all visible text from the main area
        if (texts.length === 0) {
            const main = document.querySelector('main, .job-view-layout, [role="main"]');
            if (main) {
                // Filter out navigation/header noise
                const clone = main.cloneNode(true);
                const noise = clone.querySelectorAll('nav, header, [role="navigation"], .global-nav, .banner');
                noise.forEach(n => n.remove());
                texts.push(clone.innerText.trim());
            }
        }
        return texts.join('\\n\\n');
    }""")

    # Clean up whitespace
    lines = [ln.strip() for ln in jd_text.splitlines() if ln.strip()]
    return "\n".join(lines)


async def fetch_saved_jobs(page) -> list[dict]:
    """
    Navigate to LinkedIn saved jobs, scroll to load all, extract job cards.
    Returns [{title, company, location, url}, ...].
    """
    print("Opening LinkedIn... (log in if prompted)")
    # Use domcontentloaded for initial navigation (avoids hanging on auth redirect)
    await page.goto("https://www.linkedin.com", wait_until="domcontentloaded", timeout=30000)

    # Ensure we're logged in (waits for manual login if needed)
    await _wait_for_login(page)

    # Now navigate to saved jobs
    print("Navigating to saved jobs...")
    await page.goto(SAVED_JOBS_URL, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(3)

    # Scroll to load all saved jobs (LinkedIn lazy-loads)
    print("Loading saved jobs (scrolling)...", end="", flush=True)
    prev_count = 0
    for _ in range(30):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1.5)
        jobs = await _extract_job_cards(page)
        if len(jobs) == prev_count:
            break
        prev_count = len(jobs)
        print(".", end="", flush=True)
    print(f" found {len(jobs)} saved job(s).")

    return jobs


async def fetch_jd_text(page, job_url: str) -> str:
    """
    Navigate to a specific LinkedIn job posting and extract the full JD text.
    """
    print(f"  Fetching JD: {job_url}")
    try:
        await page.goto(job_url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)
    except Exception as e:
        _safe_print(f"  Failed to load page: {_safe_str(e)}")
        return ""
    # Give JS-rendered content time to appear
    await asyncio.sleep(1)
    jd = await _extract_jd_text(page)
    if len(jd) < 50:
        print(f"  Warning: short JD text ({len(jd)} chars), page may not have loaded correctly.")
    return jd


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------
def _slugify(text: str, max_len: int = 48) -> str:
    """Create a safe, compact filename token from arbitrary text."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return s[:max_len] if s else "unknown"


def save_jd_to_file(company: str, title: str, jd_text: str, job_url: str) -> Path:
    """
    Write JD text to jd_archive/JD__<company>_<title>.txt.
    Includes source URL as a comment line.
    Returns the file path.
    """
    JD_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    slug = f"{_slugify(company)}_{_slugify(title)}".strip("_")
    filename = f"JD__{slug}.txt"
    path = JD_ARCHIVE_DIR / filename

    # Header with metadata
    header = (
        f"# Source: {job_url}\n"
        f"# Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"# Company: {company}\n"
        f"# Title: {title}\n"
        f"{'#' * 60}\n\n"
    )
    path.write_text(header + jd_text, encoding="utf-8")
    print(f"  Saved to: {path.resolve()}")
    return path


# ---------------------------------------------------------------------------
# Interactive selection
# ---------------------------------------------------------------------------
def _print_jobs(jobs: list[dict]) -> None:
    """Print a numbered list of saved jobs."""
    print(f"\n{'=' * 72}")
    print(f"  LinkedIn Saved Jobs ({len(jobs)} total)")
    print(f"{'=' * 72}")
    for i, job in enumerate(jobs):
        title = job.get("title", "?") or "?"
        company = job.get("company", "?") or "?"
        location = job.get("location", "") or ""
        loc_suffix = f" — {location}" if location else ""
        print(f"  [{i:2d}] {title} @ {company}{loc_suffix}")
    print()


async def select_and_generate(
    page,
    jobs: list[dict],
    auto_idx: Optional[int] = None,
    no_generate: bool = False,
    role: str = "auto",
) -> None:
    """
    Interactive job selection → fetch JD → save → (optionally) generate CV.
    """
    _print_jobs(jobs)

    if not jobs:
        print("No saved jobs found on LinkedIn.")
        return

    # Determine selection
    if auto_idx is not None:
        indices = [auto_idx]
    else:
        raw = input(f"Select job index [0-{len(jobs) - 1}]: ").strip()
        try:
            indices = [int(raw)]
        except ValueError:
            print("Invalid input.")
            return

    for idx in indices:
        if idx < 0 or idx >= len(jobs):
            print(f"Index {idx} out of range. Skipping.")
            continue

        job = jobs[idx]
        title = job.get("title", "Unknown Title")
        company = job.get("company", "Unknown Company")
        job_url = job.get("url", "")

        print(f"\n--- Selected: {title} @ {company} ---")

        if not job_url:
            print("  No URL available for this job. Skipping.")
            continue

        # Fetch JD
        jd_text = await fetch_jd_text(page, job_url)
        if not jd_text:
            print("  Failed to retrieve JD text.")
            continue

        # Save
        jd_path = save_jd_to_file(company, title, jd_text, job_url)
        print(f"  JD length: {len(jd_text)} characters.")

        # Generate CV
        if not no_generate:
            print("\n  Generating CV for this JD...")
            # Extract keywords from the JD text
            try:
                from jd_fetch import extract_keywords_from_text
            except ImportError:
                from app.backend.jd_fetch import extract_keywords_from_text
            keywords = extract_keywords_from_text(jd_text, max_keywords=20)
            if keywords:
                print(f"  Extracted keywords: {keywords}")

            # Import and run CV generation
            sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))
            try:
                from generate_cv_from_kb import generate_cv_from_kb
            except ImportError:
                from app.backend.generate_cv_from_kb import generate_cv_from_kb

            en_path, zh_path, annotated_path = await generate_cv_from_kb(
                output_path=None,
                role_type=role,
                jd_keywords=keywords or [],
                max_projects=6,
                company_name=company,
                target_role_title=title,
                generate_zh=False,
            )
            print(f"\n  CV generated successfully!")
            print(f"    EN: {en_path}")
        else:
            print("  Skipping CV generation (--no-generate).")


async def run_linkedin_workflow(
    port: int = DEFAULT_CDP_PORT,
    auto_idx: Optional[int] = None,
    no_generate: bool = False,
    role: str = "auto",
    keep_chrome: bool = False,
) -> None:
    """
    Main entry point:
    1. Connect to Chrome
    2. Scrape LinkedIn saved jobs
    3. Let user select a job (or auto-select)
    4. Fetch JD text
    5. Save to jd_archive/
    6. Optionally trigger CV generation
    """
    p = browser = page = None
    try:
        p, browser = await _ensure_browser(port, keep_chrome=keep_chrome)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        jobs = await fetch_saved_jobs(page)
        await select_and_generate(page, jobs, auto_idx=auto_idx, no_generate=no_generate, role=role)

    except Exception as e:
        _safe_print(f"\nError: {_safe_str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if p and browser:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass
            try:
                await p.stop()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Standalone entry point (for testing)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Quick test: python -m app.backend.linkedin_jd_fetcher
    asyncio.run(run_linkedin_workflow(auto_idx=0, no_generate=True, keep_chrome=True))
