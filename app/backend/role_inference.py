"""Shared role inference heuristics for CLI and JD matcher."""

from __future__ import annotations

import re

try:
    from generation_config import load_generation_config
except ModuleNotFoundError:
    from app.backend.generation_config import load_generation_config


_CFG = load_generation_config()
_ROLE_KEYWORDS = _CFG.get("role_inference", {}).get("keywords", {})

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


_ANDROID_PATTERNS = _compile_patterns(_ROLE_KEYWORDS.get("android", []))
_AI_PATTERNS      = _compile_patterns(_ROLE_KEYWORDS.get("ai", []))
_BACKEND_PATTERNS = _compile_patterns(_ROLE_KEYWORDS.get("backend", []))


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

    a = _count(_ANDROID_PATTERNS)
    i = _count(_AI_PATTERNS)
    b = _count(_BACKEND_PATTERNS)

    if a >= max(i, b) and a > 0:
        return "android"
    if i >= max(a, b) and i > 0:
        return "ai"
    if b >= max(a, i) and b > 0:
        return "backend"
    return "fullstack"

