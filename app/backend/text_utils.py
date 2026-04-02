"""
Text processing utilities for CV generation.

This module contains reusable text manipulation functions extracted from
generate_cv_from_kb.py to improve modularity and testability.
"""

from __future__ import annotations

import re
from typing import List, Dict, Any


def strip_parenthetical_notes(text: str) -> str:
    """
    Remove parenthetical notes from tech names.
    
    Example:
        ``Dify (Workflow Orchestration)`` -> ``Dify``
    
    Args:
        text: Input string that may contain parenthetical notes
        
    Returns:
        Cleaned string with parenthetical notes removed
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    t = text.strip()
    # Remove Chinese parentheses
    t = re.sub(r"\s*（[^）]*）\s*", " ", t)
    # Remove English parentheses
    t = re.sub(r"\s*\([^)]*\)\s*", " ", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def join_items_within_budget(items: List[str], max_chars: int, separator: str = ", ") -> str:
    """
    Join items within character budget, keeping whole items only.
    
    Avoids truncating in the middle of words (e.g., ``YOLO1...``).
    If budget is exceeded, only fully fitting items are included.
    
    Args:
        items: List of strings to join
        max_chars: Maximum total character length
        separator: String to use between items (default: ", ")
        
    Returns:
        Joined string within budget
    """
    if not items:
        return ""
    parts: List[str] = []
    total = 0
    for it in items:
        sep = separator if parts else ""
        chunk = sep + it
        if total + len(chunk) > max_chars:
            break
        parts.append(it)
        total += len(chunk)
    return separator.join(parts)


def compact_tech_stack(
    tech_stack: Dict[str, Any],
    *,
    max_items: int = 8,
    max_chars: int = 140,
) -> str:
    """
    Compress tech_stack from facts into a single-line text.
    
    Items have parenthetical notes removed and are truncated at word boundaries.
    
    Args:
        tech_stack: Dictionary of technology categories and lists
        max_items: Maximum number of tech items to include
        max_chars: Maximum total character length
        
    Returns:
        Comma-separated tech stack string
    """
    if not isinstance(tech_stack, dict) or not tech_stack:
        return ""
    seen: set[str] = set()
    ordered: List[str] = []
    for _cat, techs in tech_stack.items():
        if not isinstance(techs, list):
            continue
        for t in techs:
            if not isinstance(t, str):
                continue
            x = strip_parenthetical_notes(t)
            if not x:
                continue
            key = x.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(x)
            if len(ordered) >= max_items:
                break
        if len(ordered) >= max_items:
            break
    return join_items_within_budget(ordered, max_chars)


def strip_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: HTML string
        
    Returns:
        Plain text with HTML tags removed
    """
    return re.sub(r"<[^>]+>", "", text)


def normalize_text_for_match(text: str) -> str:
    """
    Normalize text for keyword matching.
    
    Converts to lowercase and removes special characters for fuzzy matching.
    
    Args:
        text: Input text
        
    Returns:
        Normalized lowercase text
    """
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def keyword_variant_candidates(keyword: str) -> List[str]:
    """
    Generate variant forms of a keyword for matching.
    
    Handles common variations like:
    - C++ -> cpp
    - C# -> csharp
    - Spring Boot -> springboot
    
    Args:
        keyword: Original keyword
        
    Returns:
        List of variant forms to check
    """
    kw = keyword.lower().strip()
    variants = [kw]
    
    # Handle special characters
    if "++" in kw:
        variants.append(kw.replace("++", "pp"))
    if "#" in kw:
        variants.append(kw.replace("#", "sharp"))
    
    # Handle compound terms (with spaces or hyphens)
    if " " in kw:
        variants.append(kw.replace(" ", ""))
        variants.append(kw.replace(" ", "-"))
    if "-" in kw:
        variants.append(kw.replace("-", ""))
        variants.append(kw.replace("-", " "))
    
    return variants
