#!/usr/bin/env python3
"""
Lightweight company profile utilities.
Provides: loading profiles, extracting company name from text, rendering a tiny alignment snippet.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any
import yaml


def load_company_profiles(path: str = "kb/company_profiles.yaml") -> Dict[str, Any]:
    """Load company profiles from a YAML file. Returns a dict keyed by company name."""
    p = Path(path)
    if not p.exists():
        return {}
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    if isinstance(data, dict):
        return data
    return {}


def load_company_profile(name: str, path: str = "kb/company_profiles.yaml") -> Optional[Dict[str, Any]]:
    """Load a single company profile by exact name (case-insensitive match)."""
    profiles = load_company_profiles(path)
    if not isinstance(profiles, dict):
        return None
    if name in profiles:
        return profiles[name]
    lname = name.lower()
    for k, v in profiles.items():
        if isinstance(k, str) and k.lower() == lname:
            return v
    return None


def render_alignment_snippet(profile: Optional[Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> str:
    """Render a short alignment snippet for the given company profile.
    This is intended for human readers to quickly see how the candidate aligns with the company.
    """
    if not profile:
        return ""
    name = profile.get("name") or "Company"
    mission = profile.get("mission") or ""
    values = profile.get("values") or []
    parts: list[str] = []
    if mission:
        parts.append(f"Alignment with {name} mission: {mission}")
    if isinstance(values, list) and values:
        first = ", ".join(str(v) for v in values[:3])
        parts.append(f"Values alignment: {first}")
    # Architecture hint if present
    arch = profile.get("architecture_notes")
    if arch:
        if isinstance(arch, list):
            arch_text = ", ".join(str(a) for a in arch[:3])
        else:
            arch_text = str(arch)
        parts.append(f"Architecture focus: {arch_text}")
    return "; ".join(parts)


def extract_company_name_from_text(text: Optional[str]) -> Optional[str]:
    """Heuristic extraction of a company name from free text (e.g., a JD).
    Returns None if no plausible name found.
    Notes:
      - Very lightweight heuristic intended for quick wins; not a robust NER.
    """
    if not text:
        return None
    import re
    candidates = []
    patterns = [
        r"Company\s*[:\-]\s*([A-Z][A-Za-z0-9&\-\s]+)",
        r"Employer\s*[:\-]\s*([A-Z][A-Za-z0-9&\-\s]+)",
        r"at\s+([A-Z][A-Za-z0-9&\-\s]+)$",
        r"at\s+([A-Z][A-Za-z0-9&\-\s]+)\s*\n",
        r"Position\s+at\s+([A-Z][A-Za-z0-9&\-\s]+)",
        r"Company name\s*[:]\s*([A-Z][A-Za-z0-9&\-\s]+)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            name = m.group(1).strip().strip(". ")
            if name:
                candidates.append(name)
    if candidates:
        # 去重并返回首个候选
        seen = set()
        for c in candidates:
            if c.lower() not in seen:
                seen.add(c.lower())
                return c
    return None
