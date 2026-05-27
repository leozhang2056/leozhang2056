#!/usr/bin/env python3
"""
Batch CV Generator — reads all JD files from Interview/NewJobs/ and
generates a tailored CV for each one.

Usage:
    python generate.py batch-cv
    python generate.py batch-cv --input Interview/NewJobs --dry-run
"""

from __future__ import annotations

import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Safe print for Windows GBK terminals
def _sp(*args, **kw):
    text = " ".join(str(a) for a in args)
    try:
        print(text, **kw)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"), **kw)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT_DIR = REPO_ROOT / "Interview" / "NewJobs"
PROCESSED_SUBDIR = "_processed"

SKIP_NAMES = {PROCESSED_SUBDIR, "_failed", "_archive"}


def _parse_filename(path: Path) -> tuple[str, str]:
    """
    Heuristically extract company name and job title from a filename.
    Returns (company, title).

    Pattern precedence:
      1. JD__ prefix stripped
      2. "Title @ Company": split on @
      3. "Title  Company" (double-space before company token)
      4. "Company - Title" or "Title - Company": split on first dash
      5. "Company_Title": split on first _
      6. Fallback: whole stem as title
    """
    stem = path.stem
    if stem.startswith("JD__"):
        stem = stem[4:]

    # "Title @ Company"
    if "@" in stem:
        parts = stem.split("@", 1)
        return parts[1].strip(), parts[0].strip()

    # "Title  Company" — double space before the last word(s)
    m = re.search(r"\s{2,}(\S[\w\s]*)$", stem)
    if m:
        return m.group(1).strip(), stem[:m.start()].strip()

    # "Company - Title" or "Title - Company" (first dash)
    m = re.match(r"^(.+?)\s*[–\-—]\s*(.+)$", stem)
    if m:
        return m.group(1).strip(), m.group(2).strip()

    # "Company_Title" (first underscore)
    parts = re.split(r"[_]", stem, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip().replace("_", " ")

    return "Unknown", stem.replace("_", " ")


def _read_jd_file(path: Path) -> Optional[str]:
    """Read a JD text file, stripping metadata header lines (starting with #)."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"  Error reading {path.name}: {e}")
        return None
    # Skip comment/metadata lines at the top
    lines = text.splitlines()
    body = [ln for ln in lines if not ln.startswith("#")]
    return "\n".join(body).strip()


async def run_batch_cv(
    input_dir: str | None = None,
    dry_run: bool = False,
    role: str = "auto",
    max_projects: int = 6,
) -> None:
    """
    Scan input_dir for JD files, generate a CV for each.

    Args:
        input_dir:  Path to directory containing JD files (default: Interview/NewJobs)
        dry_run:    If True, only list what would be processed without generating
        role:       Role type for CV generation (default: auto, inferred from JD)
        max_projects: Max projects to include in CV (default: 6)
    """
    scan_dir = Path(input_dir).resolve() if input_dir else DEFAULT_INPUT_DIR
    if not scan_dir.is_dir():
        _sp(f"Error: input directory not found: {scan_dir}")
        _sp("Create it and save JD .txt or .md files there.")
        return

    processed_dir = scan_dir / PROCESSED_SUBDIR
    processed_dir.mkdir(exist_ok=True)

    # Gather JD files (skip subdirectories starting with _)
    files = sorted(
        [p for p in scan_dir.iterdir()
         if p.is_file() and p.suffix.lower() in {".txt", ".md", ".html"}
         and p.stem not in SKIP_NAMES
         and not p.stem.startswith("_")],
        key=lambda p: p.name,
    )

    if not files:
        print(f"No JD files found in {scan_dir}")
        print("Save job descriptions as .txt or .md files there and re-run.")
        return

    _sp(f"\n{'=' * 70}")
    _sp(f"  Batch CV Generator - {len(files)} JD file(s) found")
    _sp(f"  Input: {scan_dir}")
    _sp(f"{'=' * 70}\n")

    results: list[dict] = []

    for idx, jd_path in enumerate(files):
        company, title = _parse_filename(jd_path)
        jd_text = _read_jd_file(jd_path)

        _sp(f"[{idx + 1}/{len(files)}] {company} - {title}")
        if not jd_text:
            _sp("  Skipping (empty or unreadable)")
            results.append({"file": jd_path.name, "status": "SKIP", "company": company, "title": title})
            continue

        if len(jd_text) < 50:
            _sp(f"  Skipping (too short: {len(jd_text)} chars)")
            results.append({"file": jd_path.name, "status": "SKIP_SHORT", "company": company, "title": title})
            continue

        _sp(f"  JD length: {len(jd_text):,} chars")

        if dry_run:
            _sp(f"  [DRY RUN] Would generate CV for: {company} - {title}")
            results.append({"file": jd_path.name, "status": "DRY_RUN", "company": company, "title": title})
            # In dry-run mode, don't move the file
            continue

        # --- Generate CV ---
        try:
            from jd_fetch import extract_keywords_from_text
            from generate_cv_from_kb import generate_cv_from_kb
        except ImportError:
            sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))
            from jd_fetch import extract_keywords_from_text
            from generate_cv_from_kb import generate_cv_from_kb

        keywords = extract_keywords_from_text(jd_text, max_keywords=20)
        _sp(f"  Keywords: {', '.join(keywords[:10])}{'...' if len(keywords) > 10 else ''}")

        try:
            en_path, zh_path, annotated_path = await generate_cv_from_kb(
                output_path=None,
                role_type=role,
                jd_keywords=keywords or [],
                max_projects=max_projects,
                company_name=company,
                target_role_title=title,
                generate_zh=False,
            )
            _sp(f"  [OK] CV generated: {Path(en_path).resolve()}")
            results.append({
                "file": jd_path.name,
                "status": "OK",
                "company": company,
                "title": title,
                "pdf": str(en_path),
            })

            # Move processed file to _processed/
            dest = processed_dir / jd_path.name
            counter = 1
            while dest.exists():
                dest = processed_dir / f"{jd_path.stem}_{counter}{jd_path.suffix}"
                counter += 1
            jd_path.rename(dest)
            _sp(f"  Moved to: {dest.name}")

        except Exception as e:
            _sp(f"  FAILED: {e}")
            results.append({
                "file": jd_path.name,
                "status": "FAIL",
                "company": company,
                "title": title,
                "error": str(e),
            })

        _sp()  # blank line between files

    # --- Summary ---
    _sp(f"{'=' * 70}")
    _sp("  Batch Summary")
    _sp(f"{'=' * 70}")
    ok = [r for r in results if r["status"] == "OK"]
    failed = [r for r in results if r["status"] == "FAIL"]
    skipped = [r for r in results if r["status"] in ("SKIP", "SKIP_SHORT")]
    dry = [r for r in results if r["status"] == "DRY_RUN"]
    _sp(f"  Total: {len(results)}")
    _sp(f"  Generated: {len(ok)}")
    _sp(f"  Failed: {len(failed)}")
    _sp(f"  Skipped: {len(skipped)}")
    if dry:
        _sp(f"  Dry-run: {len(dry)}")
    if failed:
        _sp("  Failures:")
        for r in failed:
            _sp(f"    - {r['file']}: {r.get('error', '')}")
    if ok:
        _sp("  Generated PDFs:")
        for r in ok:
            _sp(f"    - {r['pdf']}")
    _sp()
