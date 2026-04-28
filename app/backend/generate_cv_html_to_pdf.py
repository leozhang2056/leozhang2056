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


async def html_to_pdf(html_content: str, output_path: str) -> None:
    """
    Convert HTML content to PDF using Playwright Chromium.
    
    Args:
        html_content: Full HTML document as a string.
        output_path: Destination path for the generated PDF.
    """
    try:
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise PdfRenderError(
            "Playwright is not installed. Install dependencies from `requirements.txt` "
            "and then run `python -m playwright install chromium`."
        ) from exc

    browser = None
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch()
            except Exception as exc:
                raise PdfRenderError(_playwright_install_hint(exc)) from exc

            page = await browser.new_page()

            # Load HTML content (wait_until='load' ensures rendering is complete)
            await page.set_content(html_content, wait_until="load", timeout=30000)

            # Wait for layout to stabilize
            await page.wait_for_timeout(1000)

            # Generate PDF
            await page.pdf(
                path=str(output),
                format="A4",
                margin={
                    "top": "15mm",
                    "right": "15mm",
                    "bottom": "15mm",
                    "left": "15mm",
                },
                print_background=True,
            )
    except PlaywrightTimeoutError as exc:
        raise PdfRenderError("Timed out while rendering HTML to PDF.") from exc
    except PdfRenderError:
        raise
    except Exception as exc:
        raise PdfRenderError(f"Failed to render PDF to `{output}`: {exc}") from exc
    finally:
        if browser is not None:
            await browser.close()
