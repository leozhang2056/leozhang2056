#!/usr/bin/env python3
"""
HTML to PDF conversion utility using Playwright.

This module provides the `html_to_pdf()` function used by the CV and cover letter
generation pipeline. For actual resume generation, use the unified CLI:

    python generate.py cv --role android
    python generate.py cl --role backend --company "Acme"
"""

from __future__ import annotations

from pathlib import Path
import asyncio
import time


class PdfRenderError(RuntimeError):
    """Raised when HTML-to-PDF rendering fails with actionable context."""


def _playwright_install_hint(exc: Exception) -> str:
    msg = str(exc).lower()
    if "executable doesn't exist" in msg or "browser" in msg and "install" in msg:
        return (
            "Playwright browser executable is missing. "
            "Install it with `python -m playwright install chromium`."
        )
    return "Verify that Playwright and Chromium are installed and available in this environment."


async def _render_with_playwright(html_content: str, output: Path) -> None:
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError
    from playwright.async_api import async_playwright

    browser = None
    t0 = time.perf_counter()
    try:
        async with async_playwright() as p:
            try:
                browser = await asyncio.wait_for(
                    p.chromium.launch(
                        args=["--disable-gpu", "--no-sandbox"],
                    ),
                    timeout=15,
                )
            except Exception as exc:
                raise PdfRenderError(_playwright_install_hint(exc)) from exc

            page = await browser.new_page()
            await asyncio.wait_for(
                page.set_content(html_content, wait_until="domcontentloaded", timeout=20000),
                timeout=22,
            )
            # Keep a short stabilization wait only.
            await page.wait_for_timeout(150)
            await asyncio.wait_for(
                page.pdf(
                    path=str(output),
                    format="A4",
                    margin={
                        "top": "15mm",
                        "right": "15mm",
                        "bottom": "15mm",
                        "left": "15mm",
                    },
                    print_background=True,
                ),
                timeout=22,
            )
    except PlaywrightTimeoutError as exc:
        raise PdfRenderError("Timed out while rendering HTML to PDF.") from exc
    except asyncio.TimeoutError as exc:
        raise PdfRenderError("Timed out while launching Chromium or writing PDF.") from exc
    except PdfRenderError:
        raise
    except Exception as exc:
        raise PdfRenderError(f"Failed to render PDF to `{output}`: {exc}") from exc
    finally:
        if browser is not None:
            await browser.close()
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"  PDF render elapsed: {elapsed:.0f} ms")


async def html_to_pdf(html_content: str, output_path: str) -> None:
    """
    Convert HTML content to PDF using Playwright Chromium.
    
    Args:
        html_content: Full HTML document as a string.
        output_path: Destination path for the generated PDF.
    """
    try:
        # Validate dependency early; actual rendering is delegated.
        import playwright  # type: ignore  # noqa: F401
    except ImportError as exc:
        raise PdfRenderError(
            "Playwright is not installed. Install dependencies from `requirements.txt` "
            "and then run `python -m playwright install chromium`."
        ) from exc

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    await _render_with_playwright(html_content, output)
