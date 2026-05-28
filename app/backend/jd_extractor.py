#!/usr/bin/env python3
"""
JD Text Extractor — cleans LinkedIn markdown page dumps to extract pure JD text.

Typical input: a .md file saved from a LinkedIn job posting (with YAML front
matter, premium upsells, tracking URLs, etc.).  Output: clean JD text suitable
for keyword extraction and CV generation.
"""

from __future__ import annotations

import re
from pathlib import Path


# Headings that signal the START of real JD content
_JD_START_HEADINGS = re.compile(
    r"^##\s+(About the job|Job description|Description|The role|"
    r"About the opportunity|About this job|Job details|"
    r" Responsibilities|Requirements|What you.ll do)",
    re.IGNORECASE | re.MULTILINE,
)

# Headings that signal the END of real JD content (post-JD noise)
_JD_END_HEADINGS = re.compile(
    r"^##\s+(Set alert|About the company|Company photos|More jobs|"
    r"People you can reach|Use AI to assess|"
    r"Job search faster|Seniority level|Employment type|"
    r"Job function|Industries|Referrals|Similar jobs)",
    re.IGNORECASE | re.MULTILINE,
)


def extract_jd_text(raw: str) -> str:
    """
    Extract clean JD text from a LinkedIn markdown page dump.

    Steps:
      1. Strip YAML front matter (--- ... ---).
      2. Find the real JD starting section (## About the job etc.).
      3. Cut off at post-JD noise sections.
      4. Remove markdown link syntax, tracking URLs, and empty lines.
    """
    text = raw

    # 1. Strip YAML front matter
    text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)

    # 2. Find starter heading
    start_match = _JD_START_HEADINGS.search(text)
    if not start_match:
        # No known heading found — try to use everything after first heading
        first_h2 = re.search(r"^##\s+", text, re.MULTILINE)
        if first_h2:
            start = first_h2.start()
            text = text[start:]
        # otherwise use whole text as-is
    else:
        start = start_match.start()
        text = text[start:]

    # 3. Cut off at end-of-JD headings
    end_match = _JD_END_HEADINGS.search(text)
    if end_match:
        text = text[: end_match.start()]

    # 4. Clean up markdown / LinkedIn noise
    # Remove inline markdown links: [text](url) -> text
    text = re.sub(r"\[([^\]]*?)\]\([^)]+\)", r"\1", text)
    # Remove bare URLs
    text = re.sub(r"https?://\S+", "", text)
    # Remove bold markers
    text = text.replace("**", "")
    # Remove bullet markers
    text = text.replace("* ", "• ")
    # Remove horizontal rules
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace per line
    lines = [ln.strip() for ln in text.splitlines()]
    text = "\n".join(ln for ln in lines if ln)

    return text.strip()


def extract_jd_from_file(path: str | Path) -> str | None:
    """
    Read a JD file, extract clean JD text.
    Returns None if the file can't be read.
    """
    try:
        raw = Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    if not raw.strip():
        return None
    return extract_jd_text(raw)
