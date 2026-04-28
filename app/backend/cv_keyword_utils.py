"""Shared JD keyword matching helpers for CV generation and JD matching."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

try:
    from kb_io import load_projects, load_yaml  # type: ignore
except ModuleNotFoundError:
    from app.backend.kb_io import load_projects, load_yaml


def strip_html_tags(text: str) -> str:
    """Remove HTML tags and return plain text."""
    if not isinstance(text, str):
        return ""
    return re.sub(r"<[^>]+>", " ", text)


def normalize_keywords(jd_keywords: Optional[List[str]]) -> List[str]:
    """Normalize JD keywords by lowercasing, trimming and de-duplicating."""
    if not jd_keywords:
        return []
    out: List[str] = []
    seen = set()
    for kw in jd_keywords:
        if not kw:
            continue
        normalized = str(kw).strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def normalize_text_for_match(text: str) -> str:
    """Normalize free text to improve keyword matching robustness."""
    normalized = (text or "").lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return re.sub(r"\s{2,}", " ", normalized).strip()


def keyword_variant_candidates(keyword: str) -> List[str]:
    """Generate a few common textual variants for a JD keyword."""
    raw = (keyword or "").strip().lower()
    if not raw:
        return []
    variants = {raw}
    variants.add(raw.replace("apis", "api"))
    variants.add(raw.replace("restful", "rest"))
    variants.add(raw.replace("&", "and"))
    variants.add(raw.replace("/", " "))
    return [variant for variant in variants if variant]


def keyword_hits_in_text(text: str, keywords: List[str]) -> List[str]:
    """Return the subset of keywords that appear in the text."""
    if not text or not keywords:
        return []
    normalized_text = normalize_text_for_match(text)
    hits: List[str] = []
    for keyword in keywords:
        matched = False
        for variant in keyword_variant_candidates(keyword):
            normalized_variant = normalize_text_for_match(variant)
            if normalized_variant and normalized_variant in normalized_text:
                matched = True
                break
        if matched:
            hits.append(keyword)
    return hits


def build_kb_evidence_corpus(base: Path) -> str:
    """Build a lightweight evidence corpus from KB skills and project facts."""
    texts: List[str] = []
    try:
        texts.append(str(load_yaml(base / "kb" / "skills.yaml")))
    except Exception:
        pass

    try:
        for project in load_projects(base / "projects"):
            texts.extend([str(x) for x in project.get("keywords", []) if x])
            texts.extend([str(x) for x in project.get("related_to_roles", []) if x])
            for highlight in project.get("highlights", []) or []:
                if isinstance(highlight, str):
                    texts.append(highlight)
            tech_stack = project.get("tech_stack", {}) or {}
            for values in tech_stack.values():
                if isinstance(values, list):
                    texts.extend([str(value) for value in values if value])
    except Exception:
        pass

    return normalize_text_for_match(" ".join(texts))


def filter_jd_keywords_by_kb_evidence(
    jd_keywords: Optional[List[str]],
    base: Path,
) -> tuple[List[str], List[str]]:
    """Keep only JD keywords that are supported by KB evidence."""
    normalized_keywords = normalize_keywords(jd_keywords)
    if not normalized_keywords:
        return [], []

    corpus = build_kb_evidence_corpus(base)
    supported: List[str] = []
    filtered: List[str] = []
    for keyword in normalized_keywords:
        hit = False
        for variant in keyword_variant_candidates(keyword):
            normalized_variant = normalize_text_for_match(variant)
            if normalized_variant and normalized_variant in corpus:
                hit = True
                break
        if hit:
            supported.append(keyword)
        else:
            filtered.append(keyword)
    return supported, filtered
