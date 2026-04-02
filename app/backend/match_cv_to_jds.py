#!/usr/bin/env python3
"""
Compare CV match scores across multiple JDs.

Usage examples:
  python app/backend/match_cv_to_jds.py --role auto --jd-file jd1.txt --jd-file jd2.txt
  python app/backend/match_cv_to_jds.py --role backend --jd-url "https://example.com/job/1"
"""

from __future__ import annotations

# Ensure sibling imports work regardless of invocation method
from _path_setup import setup_backend_path
setup_backend_path()

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from generate_cv_from_kb import (
    _filter_jd_keywords_by_kb_evidence,
    _keyword_hits_in_text,
    _normalize_keywords,
    _strip_html_tags,
    generate_html_from_kb,
)
from jd_fetch import derive_keywords_from_url, extract_keywords_from_text, load_jd_text_from_file
from role_inference import infer_role_from_text


def _load_jd_input(url: Optional[str], file_path: Optional[str], max_keywords: int) -> Tuple[str, List[str], str]:
    if url:
        text, kws = derive_keywords_from_url(url, max_keywords=max_keywords)
        return text, kws, url
    if file_path:
        text = load_jd_text_from_file(file_path)
        kws = extract_keywords_from_text(text, max_keywords=max_keywords) if text else []
        return text, kws, file_path
    return "", [], "manual_keywords"


def _score_one_jd(
    role_type: str,
    raw_keywords: List[str],
    max_projects: int,
) -> Dict[str, object]:
    repo_root = Path(__file__).parent.parent.parent
    supported, filtered = _filter_jd_keywords_by_kb_evidence(raw_keywords, repo_root)
    html = generate_html_from_kb(
        role_type=role_type,
        lang="en",
        jd_keywords=supported,
        max_projects=max_projects,
    )
    cv_text = _strip_html_tags(html)
    norm_supported = _normalize_keywords(supported)
    hits = sorted(set(_keyword_hits_in_text(cv_text, norm_supported)))
    misses = [k for k in norm_supported if k not in hits]
    coverage = (len(hits) / len(norm_supported) * 100.0) if norm_supported else 0.0
    return {
        "supported_keywords": norm_supported,
        "filtered_keywords": filtered,
        "hits": hits,
        "misses": misses,
        "coverage": coverage,
    }


def build_match_report(
    role_type: str,
    jd_items: List[Dict[str, str]],
    manual_keywords: Optional[List[str]] = None,
    max_projects: int = 6,
    max_keywords: int = 24,
) -> str:
    rows: List[Dict[str, object]] = []
    for item in jd_items:
        text, raw_kws, source = _load_jd_input(
            item.get("url"),
            item.get("file"),
            max_keywords=max_keywords,
        )
        if manual_keywords:
            raw_kws = list(manual_keywords)

        inferred = infer_role_from_text(text)
        effective_role = inferred if role_type == "auto" else role_type
        scored = _score_one_jd(effective_role, raw_kws, max_projects=max_projects)
        rows.append(
            {
                "source": source,
                "effective_role": effective_role,
                "raw_keywords": raw_kws,
                **scored,
            }
        )

    rows_sorted = sorted(rows, key=lambda x: float(x["coverage"]), reverse=True)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = []
    lines.append("# Multi-JD Match Report")
    lines.append("")
    lines.append(f"- Generated at: `{now_str}`")
    lines.append(f"- Role mode: `{role_type}`")
    lines.append(f"- Compared JDs: `{len(rows_sorted)}`")
    lines.append("")
    lines.append("## Ranking")
    for i, row in enumerate(rows_sorted, start=1):
        src = str(row["source"])
        cov = float(row["coverage"])
        hits = len(row["hits"])  # type: ignore[arg-type]
        total = len(row["supported_keywords"])  # type: ignore[arg-type]
        lines.append(f"{i}. `{src}` -> `{cov:.1f}%` ({hits}/{total}), role `{row['effective_role']}`")
    lines.append("")

    for row in rows_sorted:
        src = str(row["source"])
        lines.append(f"## JD: `{src}`")
        lines.append(f"- Effective role: `{row['effective_role']}`")
        lines.append(f"- Raw keywords: `{', '.join(row['raw_keywords']) if row['raw_keywords'] else 'none'}`")
        lines.append(
            f"- Supported keywords: `{', '.join(row['supported_keywords']) if row['supported_keywords'] else 'none'}`"
        )
        lines.append(f"- Filtered keywords: `{', '.join(row['filtered_keywords']) if row['filtered_keywords'] else 'none'}`")
        lines.append(f"- Hit keywords: `{', '.join(row['hits']) if row['hits'] else 'none'}`")
        lines.append(f"- Miss keywords: `{', '.join(row['misses']) if row['misses'] else 'none'}`")
        lines.append(f"- Match score: `{float(row['coverage']):.1f}%`")
        lines.append("")

    if rows_sorted:
        top = rows_sorted[0]
        lines.append("## Recommendation")
        lines.append(
            f"- Prioritize applying to `{top['source']}` first (highest match `{float(top['coverage']):.1f}%`)."
        )
        low = [r for r in rows_sorted if float(r["coverage"]) < 60.0]
        if low:
            low_sources = ", ".join(str(r["source"]) for r in low)
            lines.append(f"- Lower-match JDs (<60%): `{low_sources}`; refine JD keywords or generate role-specific CV.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def generate_match_report_file(
    role_type: str = "auto",
    jd_urls: Optional[List[str]] = None,
    jd_files: Optional[List[str]] = None,
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = 6,
    max_keywords: int = 24,
    output_path: Optional[str] = None,
) -> str:
    today = datetime.now().strftime("%Y%m%d")
    today_dir = datetime.now().strftime("%Y-%m-%d")
    repo_root = Path(__file__).parent.parent.parent
    outputs_dir = repo_root / "outputs" / today_dir
    outputs_dir.mkdir(parents=True, exist_ok=True)

    if not output_path:
        output_path = str(outputs_dir / f"JD_Match_Report_{today}.md")

    items: List[Dict[str, str]] = []
    for u in (jd_urls or []):
        items.append({"url": u, "file": ""})
    for f in (jd_files or []):
        items.append({"url": "", "file": f})
    if not items and jd_keywords:
        items.append({"url": "", "file": ""})
    if not items:
        raise ValueError("No JD inputs. Provide --jd-url / --jd-file / --jd-keywords.")

    report = build_match_report(
        role_type=role_type,
        jd_items=items,
        manual_keywords=jd_keywords,
        max_projects=max_projects,
        max_keywords=max_keywords,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare CV match score across multiple JDs")
    parser.add_argument(
        "--role",
        default="auto",
        choices=["auto", "android", "ai", "backend", "fullstack"],
        help="Role mode (auto infers per JD)",
    )
    parser.add_argument("--jd-url", action="append", dest="jd_urls", help="JD URL (can repeat)")
    parser.add_argument("--jd-file", action="append", dest="jd_files", help="JD file path (can repeat)")
    parser.add_argument("--jd-keywords", nargs="*", dest="jd_keywords", help="Manual JD keywords")
    parser.add_argument("--max-projects", type=int, default=6, help="Max projects when generating CV for scoring")
    parser.add_argument("--max-keywords", type=int, default=24, help="Max extracted keywords per JD")
    parser.add_argument("--output", default=None, help="Output report path")
    args = parser.parse_args()

    out = generate_match_report_file(
        role_type=args.role,
        jd_urls=args.jd_urls,
        jd_files=args.jd_files,
        jd_keywords=args.jd_keywords,
        max_projects=args.max_projects,
        max_keywords=args.max_keywords,
        output_path=args.output,
    )
    print(f"Match report generated: {out}")


if __name__ == "__main__":
    main()
