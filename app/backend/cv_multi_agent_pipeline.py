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
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from generate_cv_from_kb import generate_cv_from_kb
from cv_auto_review_iterate import extract_text_from_pdf, iterate_cv_from_pdf_jd


def _parse_json_object(raw: str) -> Dict[str, Any]:
    s = (raw or "").strip()
    try:
        return json.loads(s)
    except Exception:
        pass
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", s)
    if m:
        return json.loads(m.group(1).strip())
    m2 = re.search(r"(\{[\s\S]*\})\s*$", s)
    if m2:
        return json.loads(m2.group(1))
    raise ValueError(f"Invalid JSON response: {s[:300]!r}")


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
    return _parse_json_object(content)


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


def _collect_str_list(v: Any) -> List[str]:
    if isinstance(v, str) and v.strip():
        return [v.strip()]
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return []


def _apply_pre_consensus(
    pre_outputs: List[Dict[str, Any]],
    jd_keywords: List[str],
    max_projects: int,
    min_jd_match_pct: float,
) -> Tuple[List[str], int, float]:
    kw_votes: Dict[str, int] = {k: 0 for k in jd_keywords}
    long_risk_count = 0
    coverage_push_count = 0

    for out in pre_outputs:
        for key in ("keyword_priority", "must_cover", "focus", "risks"):
            for item in _collect_str_list(out.get(key)):
                li = item.lower()
                for kw in jd_keywords:
                    if kw.lower() in li:
                        kw_votes[kw] = kw_votes.get(kw, 0) + 1
                if any(t in li for t in ["too long", "page", "dense", "verbosity", "length"]):
                    long_risk_count += 1
                if any(t in li for t in ["coverage", "ats", "keyword", "must cover"]):
                    coverage_push_count += 1

    sorted_kws = sorted(jd_keywords, key=lambda k: (-kw_votes.get(k, 0), k.lower()))
    tuned_max_projects = max_projects
    tuned_min_cov = float(min_jd_match_pct)

    if long_risk_count >= 2:
        tuned_max_projects = max(4, min(max_projects, 6))
    if coverage_push_count >= 2:
        tuned_min_cov = max(tuned_min_cov, 88.0)

    return sorted_kws, tuned_max_projects, tuned_min_cov


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
    if not jd_text.strip() and not jd_keywords:
        raise RuntimeError("cv-best requires JD context: provide jd_text or jd_keywords.")

    # 1) Pre-generation discussion
    pre_payload = _build_pre_payload(role_type, company_name, target_role_title, jd_text, jd_keywords)
    pre_outputs: List[Dict[str, Any]] = []
    for name, sp in PRE_AGENT_PROMPTS:
        out = _openai_chat_json(sp, pre_payload, use_model, api_key, base_url)
        out["_agent"] = name
        pre_outputs.append(out)
    jd_keywords, max_projects, min_jd_match_pct = _apply_pre_consensus(
        pre_outputs=pre_outputs,
        jd_keywords=jd_keywords,
        max_projects=max_projects,
        min_jd_match_pct=min_jd_match_pct,
    )

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

    async def _run_post_round(pdf_for_review: Path, round_name: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        round_post_check = _read_if_exists(pdf_for_review.with_name(f"{pdf_for_review.stem}_POST_CHECK.md"))
        round_quality = _read_if_exists(pdf_for_review.with_name(f"{pdf_for_review.stem}_QUALITY.md"))
        round_cv_text = extract_text_from_pdf(pdf_for_review)
        round_payload = _build_post_payload(
            role_type,
            jd_keywords,
            round_cv_text,
            round_post_check,
            round_quality,
        )
        post_outputs_local: List[Dict[str, Any]] = []
        for name, sp in POST_AGENT_PROMPTS:
            out = _openai_chat_json(sp, round_payload, use_model, api_key, base_url)
            out["_agent"] = name
            out["_round"] = round_name
            post_outputs_local.append(out)
        arb_payload_local = json.dumps(
            {
                "pre_discussion": pre_outputs,
                "post_reviews": post_outputs_local,
                "round": round_name,
                "post_check_path": str(pdf_for_review.with_name(f"{pdf_for_review.stem}_POST_CHECK.md")),
                "quality_path": str(pdf_for_review.with_name(f"{pdf_for_review.stem}_QUALITY.md")),
            },
            ensure_ascii=False,
        )
        arb_local = _openai_chat_json(ARBITER_PROMPT, arb_payload_local, use_model, api_key, base_url)
        return post_outputs_local, arb_local

    # 3) Post-generation review (round-1)
    post_outputs, arb = await _run_post_round(pdf_path, "round-1")

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
            # Re-review refined output so gate/score reflect final artifact.
            post_outputs, arb = await _run_post_round(Path(final_pdf), "round-2")
            decision = str(arb.get("decision", "")).strip().lower()
            gate_pass = bool(arb.get("gate_pass", False))
            final_score = float(arb.get("final_score", 0.0) or 0.0)

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

