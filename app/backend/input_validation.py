"""
Input validation utilities for security.
"""

import re
from typing import List, Optional


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and injection attacks.

    Args:
        filename: Input filename

    Returns:
        Sanitized filename safe for filesystem operations
    """
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")

    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)

    # Prevent path traversal
    if '..' in sanitized or sanitized.startswith('/'):
        raise ValueError("Invalid filename: potential path traversal")

    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]

    return sanitized.strip()


def validate_role(role: str) -> str:
    """
    Validate role parameter.

    Args:
        role: Role string

    Returns:
        Validated role

    Raises:
        ValueError: If role is invalid
    """
    valid_roles = {'auto', 'android', 'ai', 'backend', 'fullstack'}
    if role not in valid_roles:
        raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")
    return role


def validate_language(lang: str) -> str:
    """
    Validate language parameter.

    Args:
        lang: Language code

    Returns:
        Validated language

    Raises:
        ValueError: If language is invalid
    """
    valid_langs = {'en', 'zh'}
    if lang not in valid_langs:
        raise ValueError(f"Invalid language: {lang}. Must be one of {valid_langs}")
    return lang


def validate_jd_keywords(keywords: Optional[List[str]]) -> List[str]:
    """
    Validate and sanitize JD keywords.

    Args:
        keywords: List of keywords

    Returns:
        Sanitized keywords list
    """
    if keywords is None:
        return []

    sanitized = []
    for kw in keywords:
        if isinstance(kw, str) and kw.strip():
            # Remove potentially dangerous characters
            clean_kw = re.sub(r'[<>"\'\x00-\x1f]', '', kw.strip())
            if clean_kw and len(clean_kw) <= 100:  # Reasonable length limit
                sanitized.append(clean_kw)

    return sanitized[:50]  # Limit total keywords


def validate_company_name(company: str) -> str:
    """
    Validate and sanitize company name.

    Args:
        company: Company name

    Returns:
        Sanitized company name
    """
    if not isinstance(company, str):
        raise ValueError("Company name must be a string")

    # Remove dangerous characters but allow basic punctuation
    sanitized = re.sub(r'[<>|?*\x00-\x1f]', '', company.strip())

    if len(sanitized) > 100:
        sanitized = sanitized[:100]

    return sanitized or "Company"


def validate_url(url: str) -> str:
    """
    Basic URL validation.

    Args:
        url: URL string

    Returns:
        Validated URL

    Raises:
        ValueError: If URL is invalid
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Basic URL pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # path

    if not url_pattern.match(url):
        raise ValueError(f"Invalid URL format: {url}")

    return url