"""Project ranking helpers extracted from generate_cv_from_kb for reuse and testing."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from generation_config import load_generation_config
except ModuleNotFoundError:
    from app.backend.generation_config import load_generation_config


_CFG = load_generation_config().get("project_ranking", {})

BASE_PRIORITY: Dict[str, int] = dict(_CFG.get("base_priority", {}))

DEFAULT_PRIORITY = int(_CFG.get("default_priority", 9999))
PRIORITY_OFFSET = int(_CFG.get("priority_offset", 200))

ROLE_PROJECT_ORDER: Dict[str, List[str]] = dict(_CFG.get("role_project_order", {}))


def score_project_by_jd(project: Dict[str, Any], jd_keywords: Optional[List[str]]) -> float:
    """Score a project by JD keywords using weighted evidence fields."""
    jd_keywords_list = [k for k in (jd_keywords or []) if isinstance(k, str) and k.strip()]
    if not jd_keywords_list:
        return 0.0

    score = 0.0
    kws_lower = [k.lower() for k in jd_keywords_list]

    proj_kws = [k.lower() for k in project.get("keywords", [])]
    for kw in kws_lower:
        if kw in proj_kws:
            score += 1.5

    roles = [r.lower() for r in project.get("related_to_roles", [])]
    for kw in kws_lower:
        if any(kw in r for r in roles):
            score += 0.8

    tech_stack = project.get("tech_stack", {})
    all_techs: List[str] = []
    tech_count = 0
    for tech_list in tech_stack.values():
        if isinstance(tech_list, list):
            all_techs.extend([t.lower() for t in tech_list if isinstance(t, str)])
            tech_count += len(tech_list)

    for kw in kws_lower:
        if any(kw in t for t in all_techs):
            score += 1.2

    score += min(tech_count / 10.0, 0.5)

    raw_highlights = project.get("highlights", [])
    parts: List[str] = []
    for h in raw_highlights:
        if isinstance(h, str):
            parts.append(h)
        elif isinstance(h, dict):
            parts.append(h.get("en") or h.get("zh") or h.get("text") or "")

    highlights_text = " ".join(parts).lower()
    for kw in kws_lower:
        if kw in highlights_text:
            score += 0.4

    timeline = project.get("timeline", {})
    if isinstance(timeline, dict):
        end_date = timeline.get("end", "")
        if end_date and len(end_date) >= 4:
            try:
                end_year = int(end_date[:4])
                years_old = datetime.now().year - end_year
                score += max(0.0, 0.3 - years_old * 0.05)
            except ValueError:
                pass

    return score


def sort_projects(
    projects: List[Dict[str, Any]],
    role_type: str = "fullstack",
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = 6,
) -> List[Dict[str, Any]]:
    """Sort projects by JD relevance first, then role/static priority."""
    fallback_order = ROLE_PROJECT_ORDER.get("fullstack", [])
    role_order = ROLE_PROJECT_ORDER.get(role_type, fallback_order)

    def get_base_priority(project: Dict[str, Any]) -> int:
        pid = str(project.get("_project_dir", "")).lower()
        for idx, role_pid in enumerate(role_order):
            if role_pid in pid:
                return idx
        for key, val in BASE_PRIORITY.items():
            if key in pid:
                return PRIORITY_OFFSET + val
        return DEFAULT_PRIORITY

    if jd_keywords:
        for p in projects:
            p["_jd_score"] = score_project_by_jd(p, jd_keywords)
        sorted_projects = sorted(projects, key=lambda p: (-p.get("_jd_score", 0), get_base_priority(p)))
    else:
        sorted_projects = sorted(projects, key=get_base_priority)

    return sorted_projects[:max_projects]

