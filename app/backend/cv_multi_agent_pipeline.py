#!/usr/bin/env python3
"""
Multi-agent CV pipeline:
1) Pre-generation multi-agent discussion
2) CV generation
3) Post-generation multi-agent review + arbitration
4) Optional one-round auto refine via cv-iterate
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from generate_cv_from_kb import generate_cv_from_kb
from cv_auto_review_iterate import extract_text_from_pdf, iterate_cv_from_pdf_jd


def _openai_chat_json(
    system_prompt: str,
    user_payload: str,
    model: str,
    api_key: str,
    base_url: str,
) -> Dict[str, Any]:
    import requests

    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    resp = requests.post(url, headers=headers, json=body, timeout=180)
    if not resp.ok:
        body.pop("response_format", None)
        resp = requests.post(url, headers=headers, json=body, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


PRE_AGENT_PROMPTS = [
    (
        "ATS Strategist",
        "You optimize ATS and keyword alignment. Return JSON with keys: focus, risks, must_cover, keyword_priority.",
    ),
    (
        "Hiring Manager",
        "You optimize business fit and impact narrative. Return JSON with keys: focus, risks, must_cover, wording_style.",
    ),
    (
        "Tech Lead Reviewer",
        "You optimize technical credibility and architecture signals. Return JSON with keys: focus, risks, must_cover, technical_emphasis.",
    ),
]


POST_AGENT_PROMPTS = [
    (
        "Fluency Reviewer",
        "Score writing fluency and clarity. Return JSON: score(0-100), verdict, top_issues, top_fixes.",
    ),
    (
        "Layout Reviewer",
        "Score layout/readability with provided checks. Return JSON: score(0-100), verdict, top_issues, top_fixes.",
    ),
    (
        "Coverage Reviewer",
        "Score JD keyword coverage and relevance. Return JSON: score(0-100), verdict, top_issues, top_fixes.",
    ),
]


ARBITER_PROMPT = """
You are the final arbiter. Merge multiple reviewer outputs.
Return JSON:
{
  "final_score": <0-100>,
  "gate_pass": <true|false>,
  "decision": "accept|needs_refine",
  "reasons": ["..."],
  "must_fix": ["..."],
  "suggested_next_action": "..."
}
Gate pass requires final_score >= 85 and no critical blockers.
"""


@dataclass
class MultiAgentResult:
    final_pdf: str
    report_md: str
    gate_pass: bool
    final_score: float


def _safe_get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _build_pre_payload(
    role_type: str,
    company: Optional[str],
    title: Optional[str],
    jd_text: str,
    jd_keywords: List[str],
) -> str:
    return "\n".join(
        [
            f"ROLE: {role_type}",
            f"COMPANY: {company or 'n/a'}",
            f"TITLE: {title or 'n/a'}",
            f"JD_KEYWORDS: {jd_keywords}",
            f"JD_TEXT:\n{jd_text[:100000]}",
        ]
    )


def _build_post_payload(
    role_type: str,
    jd_keywords: List[str],
    cv_text: str,
    post_check_text: str,
    quality_text: str,
) -> str:
    return "\n".join(
        [
            f"ROLE: {role_type}",
            f"JD_KEYWORDS: {jd_keywords}",
            "POST_CHECK_MARKDOWN:",
            post_check_text[:60000],
            "QUALITY_MARKDOWN:",
            quality_text[:60000],
            "CV_TEXT:",
            cv_text[:100000],
        ]
    )


def _read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


async def run_cv_best_pipeline(
    *,
    role_type: str,
    company_name: Optional[str],
    target_role_title: Optional[str],
    jd_text: str,
    jd_keywords: List[str],
    max_projects: int,
    output_path: Optional[str],
    min_jd_match_pct: float,
    model: Optional[str],
    auto_refine: bool,
) -> MultiAgentResult:
    api_key = _safe_get_env("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for cv-best.")
    base_url = _safe_get_env("OPENAI_BASE_URL", "https://api.openai.com/v1")
    use_model = (model or _safe_get_env("OPENAI_MODEL", "gpt-4o-mini")) or "gpt-4o-mini"

    # 1) Pre-generation discussion
    pre_payload = _build_pre_payload(role_type, company_name, target_role_title, jd_text, jd_keywords)
    pre_outputs: List[Dict[str, Any]] = []
    for name, sp in PRE_AGENT_PROMPTS:
        out = _openai_chat_json(sp, pre_payload, use_model, api_key, base_url)
        out["_agent"] = name
        pre_outputs.append(out)

    # 2) Generate CV using existing pipeline (with all checks)
    en_path, _zh, _ann = await generate_cv_from_kb(
        output_path=output_path,
        role_type=role_type,
        jd_keywords=jd_keywords,
        max_projects=max_projects,
        company_name=company_name,
        target_role_title=target_role_title,
        generate_zh=False,
        generate_quality_report=True,
        generate_jd_annotated_pdf=False,
        min_jd_match_pct=min_jd_match_pct,
        write_review_bundle=True,
        keep_html=False,
        strict_kb=True,
        run_post_check=True,
    )

    pdf_path = Path(en_path)
    post_check_path = pdf_path.with_name(f"{pdf_path.stem}_POST_CHECK.md")
    quality_path = pdf_path.with_name(f"{pdf_path.stem}_QUALITY.md")

    post_check_text = _read_if_exists(post_check_path)
    quality_text = _read_if_exists(quality_path)
    cv_text = extract_text_from_pdf(pdf_path)

    # 3) Post-generation review
    post_payload = _build_post_payload(role_type, jd_keywords, cv_text, post_check_text, quality_text)
    post_outputs: List[Dict[str, Any]] = []
    for name, sp in POST_AGENT_PROMPTS:
        out = _openai_chat_json(sp, post_payload, use_model, api_key, base_url)
        out["_agent"] = name
        post_outputs.append(out)

    arb_payload = json.dumps(
        {
            "pre_discussion": pre_outputs,
            "post_reviews": post_outputs,
            "post_check_path": str(post_check_path),
            "quality_path": str(quality_path),
        },
        ensure_ascii=False,
    )
    arb = _openai_chat_json(ARBITER_PROMPT, arb_payload, use_model, api_key, base_url)

    final_pdf = en_path
    decision = str(arb.get("decision", "")).strip().lower()
    gate_pass = bool(arb.get("gate_pass", False))
    final_score = float(arb.get("final_score", 0.0) or 0.0)

    # 4) Optional one-round refine when needs_refine
    if auto_refine and (not gate_pass or decision == "needs_refine"):
        refined = await iterate_cv_from_pdf_jd(
            repo_root=Path(__file__).resolve().parents[2],
            pdf_path=pdf_path,
            jd_text=jd_text,
            jd_keywords=jd_keywords,
            role_type=role_type,
            company_name=company_name,
            target_role_title=target_role_title,
            max_projects=max_projects,
            model=use_model,
            dry_run=False,
            output_pdf=str(pdf_path.with_name(f"{pdf_path.stem}_BEST.pdf")),
            min_jd_match_pct=min_jd_match_pct,
            write_review_bundle=True,
        )
        if refined:
            final_pdf = refined

    report_path = Path(final_pdf).with_name(f"{Path(final_pdf).stem}_MULTI_AGENT_REVIEW.md")
    md_lines: List[str] = [
        "# Multi-Agent CV Orchestration Report",
        "",
        f"- Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- Model: `{use_model}`",
        f"- Role: `{role_type}`",
        f"- Company: `{company_name or 'n/a'}`",
        f"- Final PDF: `{final_pdf}`",
        f"- Gate pass: `{'PASS' if gate_pass else 'FAIL'}`",
        f"- Final score: `{final_score:.1f}`",
        "",
        "## Pre-generation discussion",
        "```json",
        json.dumps(pre_outputs, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Post-generation reviews",
        "```json",
        json.dumps(post_outputs, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Arbiter decision",
        "```json",
        json.dumps(arb, ensure_ascii=False, indent=2),
        "```",
    ]
    report_path.write_text("\n".join(md_lines), encoding="utf-8")

    return MultiAgentResult(
        final_pdf=final_pdf,
        report_md=str(report_path),
        gate_pass=gate_pass,
        final_score=final_score,
    )

