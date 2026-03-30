"""Shared role inference heuristics for CLI and JD matcher."""

from __future__ import annotations

try:
    from generation_config import load_generation_config
except ModuleNotFoundError:
    from app.backend.generation_config import load_generation_config


_CFG = load_generation_config()
_ROLE_KEYWORDS = _CFG.get("role_inference", {}).get("keywords", {})


def infer_role_from_text(text: str) -> str:
    """Infer one of android|ai|backend|fullstack from free text."""
    t = (text or "").lower()
    if not t:
        return "fullstack"

    android_hits = tuple(_ROLE_KEYWORDS.get("android", []))
    ai_hits = tuple(_ROLE_KEYWORDS.get("ai", []))
    backend_hits = tuple(_ROLE_KEYWORDS.get("backend", []))

    def _count(hits: tuple[str, ...]) -> int:
        return sum(1 for h in hits if h in t)

    a = _count(android_hits)
    i = _count(ai_hits)
    b = _count(backend_hits)

    if a >= max(i, b) and a > 0:
        return "android"
    if i >= max(a, b) and i > 0:
        return "ai"
    if b >= max(a, i) and b > 0:
        return "backend"
    return "fullstack"

