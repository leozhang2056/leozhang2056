#!/usr/bin/env python3
"""
Post-generation Cover Letter checks: word count, paragraph structure, tone, JD keyword coverage.

Advisory only — does not block PDF generation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
CL_WORD_COUNT_MIN = 250
CL_WORD_COUNT_MAX = 400
CL_PARAGRAPH_MIN = 3
CL_PARAGRAPH_MAX = 5
CL_SENTENCE_AVG_MAX = 35  # words per sentence

AI_TONE_PATTERNS = [
    (r"\bpassionate about\b", "AI tone: 'passionate about'"),
    (r"\bworld[- ]class\b", "AI tone: 'world-class'"),
    (r"\bcutting[- ]edge\b", "AI tone: 'cutting-edge'"),
    (r"\bseamlessly\b", "AI tone: 'seamlessly'"),
    (r"\brobust and scalable\b", "AI tone: 'robust and scalable'"),
    (r"\bleverage\b", "AI tone: 'leverage'"),
    (r"\bI am writing to express\b", "Template phrase: 'I am writing to express'"),
    (r"\bI am excited to apply\b", "Template phrase: 'I am excited to apply'"),
    (r"\bI would like to apply\b", "Template phrase: 'I would like to apply'"),
]

TEMPLATE_PHRASES = [
    (r"\bproven track record\b", "Template phrase: 'proven track record'"),
    (r"\bresults[- ]driven\b", "Template phrase: 'results-driven'"),
    (r"\bhighly motivated\b", "Template phrase: 'highly motivated'"),
    (r"\bstrong fit\b", "Template phrase: 'strong fit'"),
    (r"\bI am confident that\b", "Template phrase: 'I am confident that'"),
    (r"\bI am writing to apply\b", "Template phrase: 'I am writing to apply'"),
    (r"\bI believe my skills\b", "Template phrase: 'I believe my skills'"),
    (r"\bI would be a valuable\b", "Template phrase: 'I would be a valuable'"),
    (r"\bI am eager to contribute\b", "Template phrase: 'I am eager to contribute'"),
    (r"\bI am writing to express\b", "Template phrase: 'I am writing to express'"),
    (r"\bI am excited to apply\b", "Template phrase: 'I am excited to apply'"),
    (r"\bI would like to apply\b", "Template phrase: 'I would like to apply'"),
]


# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------
@dataclass
class CLQualityReport:
    word_count: int = 0
    word_count_ok: bool = True
    paragraph_count: int = 0
    paragraph_ok: bool = True
    sentence_count: int = 0
    sentence_avg_length: float = 0.0
    sentence_avg_ok: bool = True
    has_salutation: bool = False
    has_closing: bool = False
    tone_flags: List[str] = field(default_factory=list)
    jd_keyword_hits: List[str] = field(default_factory=list)
    jd_keyword_misses: List[str] = field(default_factory=list)
    jd_coverage_pct: float = 100.0
    overall_ok: bool = True
    notes: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _strip_html(text: str) -> str:
    """Remove HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _count_words(text: str) -> int:
    return len(text.split())


def _extract_sentences(text: str) -> List[str]:
    """Split text into sentences (simple regex split)."""
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in parts if s.strip()]


def _extract_paragraphs(html: str) -> List[str]:
    """Extract text content of <p> tags from HTML."""
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    return [_strip_html(p) for p in paragraphs if _strip_html(p)]


def _keyword_hits(text: str, keywords: List[str]) -> List[str]:
    """Return keywords found in text (case-insensitive, with word boundary matching)."""
    text_lower = text.lower()
    return [kw for kw in keywords if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower)]


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------
def run_cl_quality_check(
    html: str,
    jd_keywords: Optional[List[str]] = None,
) -> CLQualityReport:
    """Run quality checks on CL HTML output. Advisory only."""
    report = CLQualityReport()
    plain = _strip_html(html)
    paragraphs = _extract_paragraphs(html)

    # Word count
    report.word_count = _count_words(plain)
    report.word_count_ok = CL_WORD_COUNT_MIN <= report.word_count <= CL_WORD_COUNT_MAX

    # Paragraph count
    report.paragraph_count = len(paragraphs)
    report.paragraph_ok = CL_PARAGRAPH_MIN <= report.paragraph_count <= CL_PARAGRAPH_MAX

    # Sentence analysis
    sentences = _extract_sentences(plain)
    report.sentence_count = len(sentences)
    if sentences:
        lengths = [len(s.split()) for s in sentences]
        report.sentence_avg_length = sum(lengths) / len(lengths)
        report.sentence_avg_ok = report.sentence_avg_length <= CL_SENTENCE_AVG_MAX

    # Salutation and closing
    report.has_salutation = bool(re.search(r"Dear\s+\w+", html, re.IGNORECASE))
    report.has_closing = bool(re.search(r"(?:Kind regards|Sincerely|Best regards)", html, re.IGNORECASE))

    # Tone check
    for pattern, msg in AI_TONE_PATTERNS + TEMPLATE_PHRASES:
        if re.search(pattern, plain, re.IGNORECASE):
            report.tone_flags.append(msg)

    # JD keyword coverage
    if jd_keywords:
        report.jd_keyword_hits = _keyword_hits(plain, jd_keywords)
        report.jd_keyword_misses = sorted(set(jd_keywords) - set(report.jd_keyword_hits))
        total = len(jd_keywords)
        report.jd_coverage_pct = (len(report.jd_keyword_hits) / total * 100) if total else 100.0

    # Overall
    report.overall_ok = (
        report.word_count_ok
        and report.paragraph_ok
        and report.sentence_avg_ok
        and len(report.tone_flags) <= 2  # allow minor flags
    )

    # Notes
    if not report.word_count_ok:
        report.notes.append(f"Word count {report.word_count} outside {CL_WORD_COUNT_MIN}-{CL_WORD_COUNT_MAX} range (target: 250-400)")
    if not report.paragraph_ok:
        report.notes.append(f"Paragraph count {report.paragraph_count} outside {CL_PARAGRAPH_MIN}-{CL_PARAGRAPH_MAX} range (target: 3-5)")
    if not report.has_salutation:
        report.notes.append("Missing salutation (e.g., 'Dear Hiring Manager')")
    if not report.has_closing:
        report.notes.append("Missing closing (e.g., 'Kind regards')")

    return report


def build_cl_check_markdown(report: CLQualityReport) -> str:
    """Build a Markdown summary of CL quality check results."""
    status = "PASS" if report.overall_ok else "NEEDS ATTENTION"
    lines = [
        f"# Cover Letter Quality Check — {status}",
        "",
        f"- Word count: {report.word_count} ({'OK' if report.word_count_ok else 'OUT OF RANGE'})",
        f"- Paragraphs: {report.paragraph_count} ({'OK' if report.paragraph_ok else 'OUT OF RANGE'})",
        f"- Sentences: {report.sentence_count} (avg {report.sentence_avg_length:.1f} words)",
        f"- Salutation: {'Yes' if report.has_salutation else 'No'}",
        f"- Closing: {'Yes' if report.has_closing else 'No'}",
    ]

    if report.tone_flags:
        lines.append(f"- Tone flags ({len(report.tone_flags)}):")
        for flag in report.tone_flags:
            lines.append(f"  - {flag}")

    if report.jd_keyword_hits or report.jd_keyword_misses:
        lines.append(f"- JD coverage: {report.jd_coverage_pct:.0f}% ({len(report.jd_keyword_hits)}/{len(report.jd_keyword_hits) + len(report.jd_keyword_misses)})")
        if report.jd_keyword_misses:
            lines.append(f"  - Missed: {', '.join(report.jd_keyword_misses)}")

    if report.notes:
        lines.append("")
        lines.append("## Notes")
        for note in report.notes:
            lines.append(f"- {note}")

    return "\n".join(lines)
