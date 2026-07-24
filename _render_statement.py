#!/usr/bin/env python3
"""Render election supporting statement to PDF."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "app" / "backend"))
from generate_cv_html_to_pdf import html_to_pdf

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { font-family: Arial, sans-serif; font-size: 12pt; line-height: 1.6; color: #000; padding: 40px; }
p { margin-bottom: 12px; }
</style>
</head>
<body>
<h1>Tell us about yourself</h1>
<p>I recently completed a Master of Computer and Information Sciences at Auckland University of Technology (First Class Honours), where I developed strong attention to detail, problem-solving skills, and the ability to learn and follow new processes quickly.</p>
<p>I am confident using technology, including Microsoft Office, data entry systems, and digital tools. Through my background in software engineering and customer-facing roles, I have strong communication skills and experience working with people from diverse backgrounds. I am organised, reliable, and able to remain calm and professional in busy environments.</p>
<p>I am looking for casual election work on the North Shore because I want to contribute to my local community and support New Zealand's democratic process.</p>
</body>
</html>
"""


async def main():
    out_dir = Path("outputs") / "2026-07-21"
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = out_dir / "Election_Statement_Leo_Zhang_20260721.pdf"
    await html_to_pdf(HTML_CONTENT, str(pdf_path))
    print(f"PDF -> {pdf_path}  ({pdf_path.stat().st_size} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
