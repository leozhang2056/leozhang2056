#!/usr/bin/env python3
"""
Post-generation CV checks: fluency heuristics, HTML layout signals, JD keyword coverage breakdown.

Runs on the English HTML after PDF generation (cheap, no extra Playwright pass).
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import List, Optional, Tuple

try:
    from cv_quality_validator import extract_sections, extract_text_from_html
except ImportError:
    from app.backend.cv_quality_validator import extract_sections, extract_text_from_html

FLUENCY_MIN_SCORE = 78.0
LAYOUT_MIN_SCORE = 82.0
SUMMARY_MIN_KW_HITS = 2
SKILLS_MIN_KW_HITS = 2


@dataclass
class PostGenerationCheck:
    fluency_score: float
    fluency_notes: List[str]
    layout_score: float
    layout_notes: List[str]
    jd_coverage_pct: float
    jd_hit_count: int
    jd_total: int
    jd_misses: List[str]
    summary_kw_hits: int
    skills_kw_hits: int
    bullets_kw_hits: int


@dataclass
class PostGenerationThresholdResult:
    overall_pass: bool
    checks: List[Tuple[str, bool, str]]


def _sentence_split(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _bigram_repetition_score(words: List[str]) -> Tuple[float, List[str]]:
    """Penalize repeated adjacent word pairs (fluency / redundancy)."""
    if len(words) < 6:
        return 100.0, []
    bigrams = [f"{words[i]} {words[i + 1]}" for i in range(len(words) - 1)]
    ctr = Counter(bigrams)
    top = ctr.most_common(5)
    notes: List[str] = []
    score = 100.0
    for bg, c in top:
        if c >= 4 and len(bg) > 4:
            score -= min(25.0, (c - 3) * 5.0)
            notes.append(f'Repeated phrase "{bg}" ×{c}')
    return max(0.0, score), notes[:5]


def analyze_fluency(html: str) -> Tuple[float, List[str]]:
    text = extract_text_from_html(html)
    sentences = _sentence_split(text)
    notes: List[str] = []
    score = 100.0

    if not sentences:
        return 40.0, ["Very little readable text extracted from HTML"]

    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    if avg > 38:
        score -= 18
        notes.append(f"Average sentence length high (~{avg:.0f} words); consider shorter sentences")
    elif avg > 28:
        score -= 8
        notes.append(f"Some long sentences (avg ~{avg:.0f} words)")
    if avg < 10 and len(sentences) > 3:
        score -= 5
        notes.append("Very short sentences; check flow between ideas")

    words = re.findall(r"[A-Za-z0-9+.#]+", text.lower())
    rep_score, rep_notes = _bigram_repetition_score(words)
    score = score * 0.5 + rep_score * 0.5
    notes.extend(rep_notes)

    return max(0.0, min(100.0, score)), notes[:8]


def analyze_layout(html: str) -> Tuple[float, List[str]]:
    notes: List[str] = []
    score = 100.0

    if 'class="cv-summary"' not in html and "cv-summary" not in html:
        score -= 25
        notes.append("Missing cv-summary block (unexpected template output)")
    if 'class="cv-skills"' not in html and "cv-skills" not in html:
        score -= 20
        notes.append("Missing cv-skills block")

    summary_m = re.search(r'class="cv-summary"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if summary_m:
        inner = extract_text_from_html(summary_m.group(1))
        wc = len(inner.split())
        if wc < 40:
            score -= 12
            notes.append(f"Summary looks short ({wc} words); check 4–5 line target")
        if wc > 220:
            score -= 10
            notes.append(f"Summary is long ({wc} words); may affect page balance")

    li_count = len(re.findall(r"<li[^>]*>", html, re.IGNORECASE))
    if li_count < 8:
        score -= 8
        notes.append(f"Few list items ({li_count}); experience may look thin")

    empty_li = len(re.findall(r"<li[^>]*>\s*</li>", html, re.DOTALL | re.IGNORECASE))
    if empty_li:
        score -= 15
        notes.append(f"Found {empty_li} empty <li> (layout/ATS risk)")

    if "page-break-inside: avoid" in html and "job-employer" in html:
        notes.append("Large employer block uses avoid breaks; verify PDF has no huge end-of-page gaps")

    return max(0.0, min(100.0, score)), notes[:8]


def analyze_keyword_distribution(
    html: str,
    jd_keywords: Optional[List[str]],
) -> Tuple[int, int, int]:
    """How many distinct JD terms appear in summary / skills / bullets (best-effort)."""
    if not jd_keywords:
        return 0, 0, 0
    sections = extract_sections(html)
    summary = sections.get("summary") or ""
    skills = sections.get("skills") or ""
    bullets = sections.get("bullets") or []
    bullet_text = " ".join(bullets) if isinstance(bullets, list) else str(bullets)

    def hits(txt: str) -> int:
        return sum(1 for kw in jd_keywords if kw and kw.lower() in txt.lower())

    return hits(summary), hits(skills), hits(bullet_text)


def evaluate_thresholds(
    report: PostGenerationCheck,
    min_target_pct: float,
) -> PostGenerationThresholdResult:
    checks: List[Tuple[str, bool, str]] = []

    fluency_ok = report.fluency_score >= FLUENCY_MIN_SCORE
    checks.append(("Fluency score", fluency_ok, f"{report.fluency_score:.0f} >= {FLUENCY_MIN_SCORE:.0f}"))

    layout_ok = report.layout_score >= LAYOUT_MIN_SCORE
    checks.append(("Layout score", layout_ok, f"{report.layout_score:.0f} >= {LAYOUT_MIN_SCORE:.0f}"))

    coverage_target = max(0.0, min_target_pct)
    if report.jd_total > 0 and coverage_target > 0:
        cov_ok = report.jd_coverage_pct >= coverage_target
        checks.append(("JD coverage", cov_ok, f"{report.jd_coverage_pct:.1f}% >= {coverage_target:.0f}%"))
    else:
        checks.append(("JD coverage", True, "No JD keywords / target disabled"))

    if report.jd_total > 0:
        summary_ok = report.summary_kw_hits >= SUMMARY_MIN_KW_HITS
        skills_ok = report.skills_kw_hits >= SKILLS_MIN_KW_HITS
        bullets_target = max(3, int(report.jd_total * 0.35))
        bullets_ok = report.bullets_kw_hits >= bullets_target
        miss_limit = max(2, int(report.jd_total * 0.25))
        misses_ok = len(report.jd_misses) <= miss_limit

        checks.append(("Summary keyword hits", summary_ok, f"{report.summary_kw_hits} >= {SUMMARY_MIN_KW_HITS}"))
        checks.append(("Skills keyword hits", skills_ok, f"{report.skills_kw_hits} >= {SKILLS_MIN_KW_HITS}"))
        checks.append(("Bullets keyword hits", bullets_ok, f"{report.bullets_kw_hits} >= {bullets_target}"))
        checks.append(("JD misses upper bound", misses_ok, f"{len(report.jd_misses)} <= {miss_limit}"))
    else:
        checks.append(("Keyword distribution", True, "No JD keywords provided"))

    return PostGenerationThresholdResult(overall_pass=all(ok for _, ok, _ in checks), checks=checks)


def build_post_check_markdown(report: PostGenerationCheck, min_target_pct: float) -> str:
    th = evaluate_thresholds(report, min_target_pct)
    lines = [
        "# CV Post-Generation Check",
        "",
        f"- **Fluency (heuristic)**: `{report.fluency_score:.0f}/100`",
        f"- **Layout (HTML signals)**: `{report.layout_score:.0f}/100`",
        f"- **JD keyword coverage**: `{report.jd_coverage_pct:.1f}%` ({report.jd_hit_count}/{report.jd_total})",
        f"- **Gate status**: `{'PASS' if th.overall_pass else 'FAIL'}`",
        "",
        "## Quantitative Gate",
    ]
    for name, ok, detail in th.checks:
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] **{name}**: {detail}")
    lines.extend(
        [
        "",
        "## Fluency notes",
        ]
    )
    if report.fluency_notes:
        for n in report.fluency_notes:
            lines.append(f"- {n}")
    else:
        lines.append("- (no major issues detected)")
    lines.extend(["", "## Layout notes"])
    if report.layout_notes:
        for n in report.layout_notes:
            lines.append(f"- {n}")
    else:
        lines.append("- (no major issues detected)")
    lines.extend(
        [
            "",
            "## Keyword coverage",
            f"- Target: **≥ {min_target_pct:.0f}%** (when JD keywords provided)",
            f"- Misses: `{', '.join(report.jd_misses) if report.jd_misses else 'none'}`",
            f"- Distribution (term hits by section): Summary `{report.summary_kw_hits}`, Key Skills `{report.skills_kw_hits}`, Experience bullets `{report.bullets_kw_hits}` (counts are non-exclusive)",
            "",
        ]
    )
    return "\n".join(lines)


def run_post_generation_check(
    html: str,
    jd_keywords: Optional[List[str]],
    hits: List[str],
    misses: List[str],
    coverage_pct: float,
    min_target_pct: float,
) -> PostGenerationCheck:
    fluency_score, fluency_notes = analyze_fluency(html)
    layout_score, layout_notes = analyze_layout(html)
    total = len(jd_keywords) if jd_keywords else 0
    hit_count = len(hits)
    sk, skk, bk = analyze_keyword_distribution(html, jd_keywords)

    return PostGenerationCheck(
        fluency_score=fluency_score,
        fluency_notes=fluency_notes,
        layout_score=layout_score,
        layout_notes=layout_notes,
        jd_coverage_pct=coverage_pct,
        jd_hit_count=hit_count,
        jd_total=total,
        jd_misses=misses,
        summary_kw_hits=sk,
        skills_kw_hits=skk,
        bullets_kw_hits=bk,
    )


def print_post_check_summary(
    report: PostGenerationCheck,
    min_target_pct: float,
) -> None:
    th = evaluate_thresholds(report, min_target_pct)
    cov_ok = report.jd_total == 0 or report.jd_coverage_pct >= min_target_pct or min_target_pct <= 0
    cov_flag = "OK" if cov_ok else "BELOW TARGET"
    print("")
    print("  --- Post-generation check (fluency / layout / keywords) ---")
    print(f"  Gate status            → {'PASS' if th.overall_pass else 'FAIL'}")
    print(f"  Fluency (heuristic)  → {report.fluency_score:.0f}/100")
    if report.fluency_notes:
        print(f"    Notes: {'; '.join(report.fluency_notes[:3])}")
    print(f"  Layout (HTML signals) → {report.layout_score:.0f}/100")
    if report.layout_notes:
        print(f"    Notes: {'; '.join(report.layout_notes[:3])}")
    print(
        f"  JD coverage            → {report.jd_coverage_pct:.1f}% ({report.jd_hit_count}/{report.jd_total}) [{cov_flag}]"
    )
    if report.jd_misses and min_target_pct > 0:
        show = ", ".join(report.jd_misses[:8])
        if len(report.jd_misses) > 8:
            show += "..."
        print(f"    Misses: {show}")
    print(
        f"  KW by section (hits)   → Summary {report.summary_kw_hits}, Skills {report.skills_kw_hits}, Bullets {report.bullets_kw_hits}"
    )
    for name, ok, detail in th.checks:
        print(f"  {'[PASS]' if ok else '[FAIL]'} {name}: {detail}")
    print("  --- end post-generation check ---")
    print("")
