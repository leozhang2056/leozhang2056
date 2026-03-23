#!/usr/bin/env python3
"""
Generate a simple one-page portfolio PDF with clickable links.
"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path

from generate_cv_html_to_pdf import html_to_pdf


def build_html(title: str, portfolio_url: str, github_url: str, linkedin_url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    @page {{
      size: A4;
      margin: 18mm;
    }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      color: #111827;
      line-height: 1.5;
      margin: 0;
    }}
    .card {{
      border: 1px solid #d1d5db;
      border-radius: 10px;
      padding: 22px;
    }}
    h1 {{
      margin: 0 0 8px 0;
      color: #0f172a;
      font-size: 22px;
    }}
    p {{
      margin: 0 0 14px 0;
      font-size: 12.5pt;
    }}
    .link-box {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 14px;
      margin: 12px 0;
      word-break: break-all;
    }}
    .label {{
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 4px;
      display: block;
    }}
    a {{
      color: #1d4ed8;
      text-decoration: none;
      font-size: 12pt;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .hint {{
      margin-top: 18px;
      font-size: 10.5pt;
      color: #475569;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>{title}</h1>
    <p>
      This document provides direct links to Leo Zhang's portfolio and profiles.
      All links below are clickable in PDF readers.
    </p>

    <div class="link-box">
      <span class="label">Portfolio (GitHub Repository)</span>
      <a href="{portfolio_url}">{portfolio_url}</a>
    </div>

    <div class="link-box">
      <span class="label">GitHub Profile</span>
      <a href="{github_url}">{github_url}</a>
    </div>

    <div class="link-box">
      <span class="label">LinkedIn</span>
      <a href="{linkedin_url}">{linkedin_url}</a>
    </div>

    <p class="hint">
      Tip: if your PDF viewer blocks clicks, copy and paste the URL into your browser.
    </p>
  </div>
</body>
</html>"""


def default_output_path(repo_root: Path) -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    stamp = datetime.now().strftime("%Y%m%d")
    out_dir = repo_root / "outputs" / today
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"Portfolio_Leo_Zhang_{stamp}.pdf"


async def run() -> None:
    parser = argparse.ArgumentParser(description="Generate clickable portfolio link PDF")
    parser.add_argument(
        "--title",
        default="Leo Zhang Portfolio Links",
        help="Document title",
    )
    parser.add_argument(
        "--portfolio-url",
        default="https://github.com/leozhang2056/leozhang2056",
        help="Main portfolio URL",
    )
    parser.add_argument(
        "--github-url",
        default="https://github.com/leozhang2056",
        help="GitHub profile URL",
    )
    parser.add_argument(
        "--linkedin-url",
        default="https://www.linkedin.com/in/leo-zhang-305626280/",
        help="LinkedIn URL",
    )
    parser.add_argument(
        "--output",
        default="",
        help="PDF output path (optional)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    output_path = Path(args.output) if args.output else default_output_path(repo_root)

    html = build_html(
        title=args.title.strip(),
        portfolio_url=args.portfolio_url.strip(),
        github_url=args.github_url.strip(),
        linkedin_url=args.linkedin_url.strip(),
    )
    await html_to_pdf(html, str(output_path))
    print(str(output_path))


if __name__ == "__main__":
    asyncio.run(run())
