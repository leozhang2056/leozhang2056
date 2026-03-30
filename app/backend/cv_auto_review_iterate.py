#!/usr/bin/env python3
"""
Second-AI style CV review + automatic KB patches + regenerate PDF.

Requires:
  - OPENAI_API_KEY
  - Optional: OPENAI_MODEL (default gpt-4o-mini), OPENAI_BASE_URL (OpenAI-compatible endpoint)

Flow:
  1) Extract text from the current CV PDF
  2) Load JD text (URL / file / keywords-only fallback)
  3) Call chat model with strict JSON output
  4) Backup touched YAML files under outputs/<date>/kb_backup_auto_<stamp>/
  5) Apply edits to kb/profile.yaml and projects/*/facts.yaml
  6) Regenerate CV PDF (same options as generate.py cv)

This does not send raw PDF bytes to the model by default (text extraction only).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from jd_fetch import (
    _get_linkedin_cookies,
    extract_keywords_from_text,
    fetch_jd_text_from_url,
    load_jd_text_from_file,
)
from generate_cv_from_kb import generate_cv_from_kb

# ---------------------------------------------------------------------------
# PDF → text
# ---------------------------------------------------------------------------


def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "pypdf is required for PDF text extraction. Run: pip install pypdf"
        ) from e
    reader = PdfReader(str(pdf_path))
    parts: List[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return re.sub(r"\s+\n", "\n", "\n".join(parts)).strip()


# ---------------------------------------------------------------------------
# Project IDs
# ---------------------------------------------------------------------------


def _list_valid_project_ids(repo_root: Path) -> List[str]:
    root = repo_root / "projects"
    if not root.is_dir():
        return []
    return sorted(
        p.name
        for p in root.iterdir()
        if p.is_dir() and (p / "facts.yaml").exists()
    )


# ---------------------------------------------------------------------------
# OpenAI-compatible JSON call
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert technical CV editor for software engineering roles.

You receive:
1) Plain text extracted from the candidate's current CV PDF  
2) A job description (full text and/or keywords)  
3) Target role type (android | ai | backend | fullstack)  
4) The list of valid project folder IDs that may receive extra highlight bullets  

Rules:
- Do NOT invent employers, titles, dates, degrees, visa status, or quantified metrics that are not clearly supported by the CV text.
- You MAY tighten wording, reorder emphasis, align language to the JD, remove vague phrasing, and add non-numeric formulations of skills already implied.
- You MAY append new highlight bullets only when they strictly paraphrase or combine facts already present in the CV (no new companies, products, or metrics).
- Prefer editing the role-relevant English summary key: android→android_focus, ai→ai_focus, backend→java_focus, fullstack→default. You may also set summary_variants_zh for Chinese if you output zh fields.

Respond with a single JSON object ONLY (no markdown fences), exact shape:
{
  "analysis": "short rationale",
  "edits": {
    "summary_variants_en": {
      "android_focus": null,
      "ai_focus": null,
      "java_focus": null,
      "default": null
    },
    "summary_variants_zh": {
      "android_focus": null,
      "ai_focus": null,
      "java_focus": null,
      "default": null
    },
    "project_highlights_append": {
      "example-project-id": ["Optional bullet in English; omit empty lists."]
    }
  }
}

Use null or omit a key to mean \"no change\". For project_highlights_append, only use IDs from the provided valid list; omit unknown IDs entirely. Keep bullets short (one line each).
"""


def _parse_json_object(raw: str) -> Dict[str, Any]:
    s = raw.strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", s)
    if m:
        return json.loads(m.group(1).strip())
    m2 = re.search(r"(\{[\s\S]*\})\s*$", s)
    if m2:
        return json.loads(m2.group(1))
    raise ValueError(f"Model did not return valid JSON: {s[:400]!r}...")


def _openai_chat_json(
    user_payload: str,
    model: str,
    api_key: str,
    base_url: str,
) -> Dict[str, Any]:
    try:
        import requests
    except ImportError as e:
        raise RuntimeError("requests is required for cv-iterate") from e

    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_payload},
        ],
        "temperature": 0.25,
        "response_format": {"type": "json_object"},
    }

    resp = requests.post(url, headers=headers, json=body, timeout=180)
    if not resp.ok:
        body_fallback = {k: v for k, v in body.items() if k != "response_format"}
        resp = requests.post(url, headers=headers, json=body_fallback, timeout=180)
    resp.raise_for_status()

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response: {data!r}") from e
    return _parse_json_object(content)


# ---------------------------------------------------------------------------
# Apply edits to KB
# ---------------------------------------------------------------------------


def _fold_block_scalar(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def _backup_files(repo_root: Path, files: Set[Path], backup_root: Path) -> None:
    backup_root.mkdir(parents=True, exist_ok=True)
    for fp in sorted(files):
        if not fp.is_file():
            continue
        rel = fp.relative_to(repo_root)
        dest = backup_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fp, dest)


def _build_change_summary(
    en_patch: Dict[str, Any],
    zh_patch: Dict[str, Any],
    project_append: Dict[str, Any],
    modified_labels: List[str],
) -> str:
    en_keys = [k for k, v in (en_patch or {}).items() if isinstance(v, str) and v.strip()]
    zh_keys = [k for k, v in (zh_patch or {}).items() if isinstance(v, str) and v.strip()]
    appended = {
        str(pid): len([b for b in (bullets or []) if isinstance(b, str) and b.strip()])
        for pid, bullets in (project_append or {}).items()
    }
    appended = {pid: cnt for pid, cnt in appended.items() if cnt > 0}

    lines = ["\n--- KB change summary ---"]
    lines.append(f"- Files changed: {len(modified_labels)}")
    lines.append(f"- EN summary variants updated: {', '.join(en_keys) if en_keys else 'none'}")
    lines.append(f"- ZH summary variants updated: {', '.join(zh_keys) if zh_keys else 'none'}")
    if appended:
        parts = [f"{pid} (+{cnt} bullet{'s' if cnt > 1 else ''})" for pid, cnt in sorted(appended.items())]
        lines.append(f"- Project highlights appended: {', '.join(parts)}")
    else:
        lines.append("- Project highlights appended: none")
    return "\n".join(lines)


def _print_rollback_hint(repo_root: Path, backup_dir: Path, modified_labels: List[str]) -> None:
    if not modified_labels:
        return
    print("\n--- Rollback hint ---")
    print(f"Backup root: {backup_dir}")
    print("To rollback manually, copy files from backup back to repository paths:")
    for rel in modified_labels:
        src = backup_dir / rel
        dst = repo_root / rel
        print(f"  - {src}  ->  {dst}")


def _apply_profile_summary_edits(
    repo_root: Path,
    en_patch: Dict[str, Any],
    zh_patch: Dict[str, Any],
) -> bool:
    profile_path = repo_root / "kb" / "profile.yaml"
    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    career = data.setdefault("career_identity", {})
    sve = career.setdefault("summary_variants", {})
    svz = career.setdefault("summary_variants_zh", {})

    changed = False
    for k, v in (en_patch or {}).items():
        if v is None:
            continue
        if isinstance(v, str) and v.strip():
            sve[str(k)] = _fold_block_scalar(v)
            changed = True
    for k, v in (zh_patch or {}).items():
        if v is None:
            continue
        if isinstance(v, str) and v.strip():
            svz[str(k)] = _fold_block_scalar(v)
            changed = True

    if changed:
        with open(profile_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return changed


def _apply_project_highlights(
    repo_root: Path,
    append_map: Dict[str, Any],
    valid_ids: Set[str],
) -> List[Path]:
    touched: List[Path] = []
    for pid, bullets in (append_map or {}).items():
        sid = str(pid)
        if sid not in valid_ids:
            print(f"  Warning: skip unknown project_id in LLM output: {sid}")
            continue
        if not bullets:
            continue
        facts_path = repo_root / "projects" / sid / "facts.yaml"
        if not facts_path.is_file():
            continue
        with open(facts_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        hl = data.get("highlights")
        if hl is None:
            hl = []
        if not isinstance(hl, list):
            hl = []
        for b in bullets:
            if not isinstance(b, str):
                continue
            t = _fold_block_scalar(b)
            if t and t not in hl:
                hl.append(t)
        data["highlights"] = hl
        with open(facts_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        touched.append(facts_path)
    return touched


def run_llm_review_and_apply(
    repo_root: Path,
    cv_text: str,
    jd_text: str,
    role_type: str,
    valid_project_ids: List[str],
    model: str,
    dry_run: bool,
) -> Tuple[Dict[str, Any], List[str]]:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it before running cv-iterate."
        )
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()

    user_msg = "\n\n".join(
        [
            f"TARGET_ROLE_TYPE: {role_type}",
            f"VALID_PROJECT_IDS: {', '.join(valid_project_ids)}",
            f"JOB_DESCRIPTION:\n{jd_text[:120_000]}",
            f"CV_TEXT_FROM_PDF:\n{cv_text[:120_000]}",
        ]
    )

    print(
        f"\nCalling model {model!r} (JD {len(jd_text)} chars, CV {len(cv_text)} chars)…"
    )
    result = _openai_chat_json(user_msg, model=model, api_key=api_key, base_url=base_url)
    print("\n--- LLM analysis ---\n")
    print(result.get("analysis", "(none)"))
    print("\n--- LLM edits (raw) ---\n")
    print(json.dumps(result.get("edits", {}), ensure_ascii=False, indent=2))

    edits = result.get("edits") or {}
    en_patch = edits.get("summary_variants_en") or {}
    zh_patch = edits.get("summary_variants_zh") or {}
    pha = edits.get("project_highlights_append") or {}

    modified_labels: List[str] = []

    if dry_run:
        print("\n[Dry-run] KB not modified; PDF not regenerated.")
        return result, modified_labels

    today = datetime.now().strftime("%Y-%m-%d")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = repo_root / "outputs" / today / f"kb_backup_auto_{stamp}"

    to_backup: Set[Path] = {repo_root / "kb" / "profile.yaml"}
    valid = set(valid_project_ids)
    for pid in pha.keys():
        sid = str(pid)
        if sid in valid:
            to_backup.add(repo_root / "projects" / sid / "facts.yaml")

    _backup_files(repo_root, to_backup, backup_dir)
    print(f"\nKB backup → {backup_dir}")

    if _apply_profile_summary_edits(repo_root, en_patch, zh_patch):
        print("  Updated kb/profile.yaml (summary variants)")
        modified_labels.append("kb/profile.yaml")

    touched = _apply_project_highlights(repo_root, pha, valid)
    for p in touched:
        print(f"  Updated {p.relative_to(repo_root)}")
        modified_labels.append(str(p.relative_to(repo_root)))

    if not modified_labels:
        print("  No KB files changed (LLM returned empty edits).")
    else:
        print(_build_change_summary(en_patch, zh_patch, pha, modified_labels))
        _print_rollback_hint(repo_root, backup_dir, modified_labels)

    return result, modified_labels


async def iterate_cv_from_pdf_jd(
    *,
    repo_root: Path,
    pdf_path: Path,
    jd_text: str,
    jd_keywords: List[str],
    role_type: str,
    company_name: Optional[str],
    target_role_title: Optional[str],
    max_projects: int,
    model: str,
    dry_run: bool,
    output_pdf: Optional[str],
    min_jd_match_pct: float,
    write_review_bundle: bool,
) -> str:
    cv_text = extract_text_from_pdf(pdf_path)
    if len(cv_text) < 80:
        raise RuntimeError(
            "Very little text extracted from PDF. The file may be image-based or corrupted."
        )

    valid_ids = _list_valid_project_ids(repo_root)

    run_llm_review_and_apply(
        repo_root=repo_root,
        cv_text=cv_text,
        jd_text=jd_text,
        role_type=role_type,
        valid_project_ids=valid_ids,
        model=model,
        dry_run=dry_run,
    )

    if dry_run:
        return ""

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_pdf:
        out_path = output_pdf
    else:
        out_dir = pdf_path.parent
        out_path = str(out_dir / f"{pdf_path.stem}_AUTO_{stamp}.pdf")

    en_path, _zh, _ann = await generate_cv_from_kb(
        output_path=out_path,
        role_type=role_type,
        jd_keywords=jd_keywords,
        max_projects=max_projects,
        company_name=company_name,
        target_role_title=target_role_title,
        generate_zh=False,
        generate_quality_report=False,
        generate_jd_annotated_pdf=False,
        min_jd_match_pct=min_jd_match_pct,
        write_review_bundle=write_review_bundle,
    )
    return en_path


def _build_jd_text_and_keywords(
    jd_url: Optional[str],
    jd_file: Optional[str],
    jd_keywords_manual: Optional[List[str]],
    max_kw: int,
) -> Tuple[str, List[str]]:
    jd_text = ""
    if jd_file:
        jd_text = load_jd_text_from_file(jd_file) or ""
    if not jd_text.strip() and jd_url:
        jd_text = fetch_jd_text_from_url(jd_url, cookies=_get_linkedin_cookies()) or ""

    kws: List[str] = list(jd_keywords_manual or [])
    if not kws and jd_text.strip():
        kws = extract_keywords_from_text(jd_text, max_keywords=max_kw)
    if not jd_text.strip() and kws:
        jd_text = "Job keywords (no full JD text provided):\n" + ", ".join(kws)
    return jd_text, kws


async def run_cv_iterate(args: argparse.Namespace) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")

    jd_text, jd_keywords = _build_jd_text_and_keywords(
        getattr(args, "jd_url", None),
        getattr(args, "jd_file", None),
        getattr(args, "jd_keywords", None),
        max_kw=int(getattr(args, "max_keywords", 24)),
    )
    if not jd_text.strip():
        raise SystemExit("Provide --jd-file, --jd-url, or --jd-keywords for review context.")

    role = str(getattr(args, "role", "fullstack"))
    cli_model = getattr(args, "model", None)
    model = (
        (cli_model or "").strip()
        or os.environ.get("OPENAI_MODEL", "").strip()
        or "gpt-4o-mini"
    )

    out = await iterate_cv_from_pdf_jd(
        repo_root=repo_root,
        pdf_path=pdf_path,
        jd_text=jd_text,
        jd_keywords=jd_keywords,
        role_type=role,
        company_name=getattr(args, "company", None),
        target_role_title=getattr(args, "title", None),
        max_projects=int(getattr(args, "max_projects", 6)),
        model=model,
        dry_run=bool(getattr(args, "dry_run", False)),
        output_pdf=getattr(args, "output", None),
        min_jd_match_pct=float(getattr(args, "min_jd_match_pct", 85.0)),
        write_review_bundle=not bool(getattr(args, "no_review_bundle", False)),
    )

    if not getattr(args, "dry_run", False):
        print(f"\nDone.\n  PDF (after auto edit): {out}")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="LLM review PDF+JD, patch KB, regenerate CV PDF")
    p.add_argument("--pdf", required=True, help="Path to existing CV PDF")
    p.add_argument(
        "--role",
        default="fullstack",
        choices=["android", "ai", "backend", "fullstack"],
        help="Resume role / summary variant",
    )
    p.add_argument("--company", default=None, help="Company tag for output naming")
    p.add_argument("--title", default=None, help="Target role title")
    p.add_argument("--jd-url", default=None)
    p.add_argument("--jd-file", default=None)
    p.add_argument(
        "--jd-keywords",
        nargs="*",
        dest="jd_keywords",
        metavar="KW",
        help="Optional JD keywords (used if URL/file missing or to supplement)",
    )
    p.add_argument("--max-keywords", type=int, default=24)
    p.add_argument("--max-projects", type=int, default=6)
    p.add_argument(
        "--output",
        default=None,
        help="Output PDF path (default: <input_stem>_AUTO_<timestamp>.pdf next to input)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show LLM analysis/edits; do not write KB or PDF",
    )
    p.add_argument(
        "--min-jd-match-pct",
        type=float,
        default=85.0,
        help="Same as generate.py cv (default 85)",
    )
    p.add_argument(
        "--no-review-bundle",
        action="store_true",
        help="Skip writing *_AI_REVIEW_BUNDLE.md after regeneration",
    )
    p.add_argument(
        "--model",
        default=None,
        help="Chat model id (default: env OPENAI_MODEL or gpt-4o-mini)",
    )
    return p


def main() -> None:
    args = build_arg_parser().parse_args()
    asyncio.run(run_cv_iterate(args))


if __name__ == "__main__":
    main()
