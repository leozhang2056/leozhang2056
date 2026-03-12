#!/usr/bin/env python3
"""
面试问答库 CLI
List / search interview Q&A by category or role.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional


def _qa_dir(base: Path) -> Path:
    # 优先使用仓库根目录的 interview_qa（常见面试题专用文件夹）
    root_qa = base / "interview_qa"
    if root_qa.exists():
        return root_qa
    return base / "kb" / "interview_qa"


def load_index(base: Path) -> Dict:
    p = _qa_dir(base) / "index.yaml"
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_technical(base: Path) -> List[Dict]:
    p = _qa_dir(base) / "technical.yaml"
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("questions", [])


def load_behavioral(base: Path) -> List[Dict]:
    p = _qa_dir(base) / "behavioral.yaml"
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("questions", [])


def load_role_specific(base: Path) -> Dict[str, List[Dict]]:
    p = _qa_dir(base) / "role_specific.yaml"
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    out: Dict[str, List[Dict]] = {}
    for key, val in data.items():
        if isinstance(val, list):
            out[key] = val
    return out


# 角色到 role_specific 里 section 的映射
_ROLE_SECTIONS = {
    "android": ["android_questions"],
    "backend": ["backend_questions"],
    "ai": ["ai_ml_questions"],
    "iot": ["iot_questions"],
    "leadership": ["leadership_questions"],
    "company": ["company_research_questions"],
}


def _normalize(q: Dict, source: str, section: Optional[str] = None) -> Dict:
    q = dict(q)
    q["_source"] = source
    if section:
        q["_section"] = section
    return q


def list_questions(
    base: Path,
    category: Optional[str] = None,
    role: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Dict]:
    """
    category: technical | behavioral | role_specific
    role: android | backend | ai | iot | leadership | company
    search: 关键词过滤（匹配 question / answer_points 文本）
    """
    base = Path(base)
    results: List[Dict] = []

    def matches(q: Dict, kw: str) -> bool:
        if not kw:
            return True
        k = kw.lower()
        if k in (q.get("question") or "").lower():
            return True
        for pt in q.get("answer_points") or []:
            if k in str(pt).lower():
                return True
        return False

    if category is None or category == "technical":
        for q in load_technical(base):
            q = _normalize(q, "technical")
            if search and not matches(q, search):
                continue
            results.append(q)

    if category is None or category == "behavioral":
        for q in load_behavioral(base):
            q = _normalize(q, "behavioral")
            if search and not matches(q, search):
                continue
            results.append(q)

    if category is None or category == "role_specific" or role:
        role_data = load_role_specific(base)
        sections = _ROLE_SECTIONS.get(role, list(role_data.keys())) if role else list(role_data.keys())
        for sec in sections:
            for q in role_data.get(sec, []):
                q = _normalize(q, "role_specific", sec)
                if search and not matches(q, search):
                    continue
                if role and sec not in _ROLE_SECTIONS.get(role, []):
                    continue
                results.append(q)

    return results


def format_question(q: Dict, verbose: bool = True) -> str:
    lines = [
        f"Q: {q.get('question', '')}",
        f"  [id: {q.get('id', '')}] [{q.get('_source', '')}]",
    ]
    points = q.get("answer_points") or []
    if points:
        lines.append("  Points:")
        for p in points:
            lines.append(f"    - {p}")
    if verbose:
        ev = q.get("evidence") or []
        if ev:
            lines.append("  Evidence:")
            for e in ev:
                if isinstance(e, dict):
                    proj = e.get("project", "")
                    h = e.get("highlight") or e.get("highlights") or ""
                    lines.append(f"    - {proj}: {h}")
    tips = q.get("tips") or []
    if tips:
        lines.append("  Tips:")
        for t in tips:
            lines.append(f"    - {t}")
    return "\n".join(lines)


def run_list(
    base: Path,
    category: Optional[str] = None,
    role: Optional[str] = None,
    search: Optional[str] = None,
    verbose: bool = True,
) -> None:
    base = Path(base)
    qa_base = _qa_dir(base)
    if not qa_base.exists():
        print("Interview Q&A directory not found:", qa_base)
        return

    questions = list_questions(base, category=category, role=role, search=search)
    if not questions:
        print("No questions found.")
        return

    print(f"Found {len(questions)} question(s).\n")
    for i, q in enumerate(questions, 1):
        print(format_question(q, verbose=verbose))
        print()


def main() -> None:
    import argparse
    repo_root = Path(__file__).parent.parent.parent
    parser = argparse.ArgumentParser(description="List interview Q&A by category/role/search")
    parser.add_argument("--category", choices=["technical", "behavioral", "role_specific"],
                        help="Limit to one category")
    parser.add_argument("--role", choices=list(_ROLE_SECTIONS),
                        help="Limit to one role (uses role_specific only)")
    parser.add_argument("--search", help="Keyword to filter questions/answers")
    parser.add_argument("--short", action="store_true", help="Only question text, no points/tips")
    parser.add_argument("--base", default=str(repo_root), help="Repo root path")
    args = parser.parse_args()
    run_list(
        Path(args.base),
        category=args.category,
        role=args.role,
        search=args.search,
        verbose=not args.short,
    )


if __name__ == "__main__":
    main()
