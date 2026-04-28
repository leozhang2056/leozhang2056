"""Shared role inference heuristics for CLI and JD matcher."""

from __future__ import annotations

import re

try:
    from generation_config import load_generation_config
except ModuleNotFoundError:
    from app.backend.generation_config import load_generation_config

# Pre-compile word-boundary patterns for each keyword set.
# Using \b ensures "cv" in "my_cv.pdf" or "/cv/" won't fire;
# only standalone occurrences like "cv engineer" will match.
def _compile_patterns(keywords: list[str]) -> list[re.Pattern]:
    patterns = []
    for kw in keywords:
        # Multi-word phrases: require surrounding whitespace / start-of-string / end
        if " " in kw:
            # e.g. "computer vision", "spring boot"
            pat = re.compile(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", re.IGNORECASE)
        else:
            pat = re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE)
        patterns.append(pat)
    return patterns


def _get_role_patterns() -> tuple[list[re.Pattern], list[re.Pattern], list[re.Pattern]]:
    cfg = load_generation_config()
    role_keywords = cfg.get("role_inference", {}).get("keywords", {})
    return (
        _compile_patterns(role_keywords.get("android", [])),
        _compile_patterns(role_keywords.get("ai", [])),
        _compile_patterns(role_keywords.get("backend", [])),
    )


def infer_role_from_text(text: str) -> str:
    """Infer one of android|ai|backend|fullstack from free text.

    Uses word-boundary regex matching so that short tokens like 'cv' in a
    URL path or filename do not accidentally trigger an 'ai' classification.
    """
    t = (text or "")
    if not t.strip():
        return "fullstack"

    def _count(patterns: list[re.Pattern]) -> int:
        return sum(1 for p in patterns if p.search(t))

    android_patterns, ai_patterns, backend_patterns = _get_role_patterns()

    a = _count(android_patterns)
    i = _count(ai_patterns)
    b = _count(backend_patterns)

    if a >= max(i, b) and a > 0:
        return "android"
    if i >= max(a, b) and i > 0:
        return "ai"
    if b >= max(a, i) and b > 0:
        return "backend"
    return "fullstack"

