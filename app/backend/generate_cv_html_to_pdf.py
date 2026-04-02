#!/usr/bin/env python3
"""
HTML to PDF conversion utility using Playwright.

This module provides the `html_to_pdf()` function used by the CV and cover letter
generation pipeline. For actual resume generation, use the unified CLI:

    python generate.py cv --role android
    python generate.py cl --role backend --company "Acme"
"""

import asyncio
from playwright.async_api import async_playwright


async def html_to_pdf(html_content: str, output_path: str) -> None:
    """
    Convert HTML content to PDF using Playwright Chromium.
    
    Args:
        html_content: Full HTML document as a string.
        output_path: Destination path for the generated PDF.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load HTML content (wait_until='load' ensures rendering is complete)
        await page.set_content(html_content, wait_until='load')
        
        # Wait for layout to stabilize
        await page.wait_for_timeout(1000)
        
        # Generate PDF
        await page.pdf(
            path=output_path,
            format='A4',
            margin={
                'top': '15mm',
                'right': '15mm',
                'bottom': '15mm',
                'left': '15mm'
            },
            print_background=True
        )
        
        await browser.close()
