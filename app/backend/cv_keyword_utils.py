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


STOP_WORDS = frozenset({
    # Generic verbs / adjectives that appear in every JD
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'can', 'shall', 'must',
    'not', 'no', 'nor', 'if', 'then', 'else', 'when', 'where', 'how',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
    'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
    # Common JD filler words
    'experience', 'ability', 'skills', 'knowledge', 'understanding',
    'strong', 'good', 'excellent', 'great', 'proven', 'solid',
    'including', 'such', 'like', 'well', 'also', 'able',
    'working', 'work', 'role', 'position', 'job', 'team',
    'new', 'existing', 'various', 'different', 'multiple',
    'develop', 'development', 'developing', 'technical',
    'preferred', 'desired', 'desirable', 'required', 'nice',
    'must', 'should', 'need', 'looking', 'seeking',
    'opportunity', 'environment', 'culture', 'company',
    'benefits', 'offer', 'offers', 'providing', 'provide',
    'join', 'joining', 'candidates', 'applicant',
    'communication', 'communication skills', 'interpersonal',
    'time', 'full', 'part', 'contract', 'permanent',
    'degree', 'qualification', 'bachelor', 'master', 'diploma',
    'years', 'year', 'plus', 'least', 'minimum',
    'excellent', 'outstanding', 'exceptional', 'superior',
    'highly', 'very', 'extremely', 'incredibly',
    'day', 'days', 'per', 'week', 'month', 'year',
    'location', 'office', 'remote', 'hybrid', 'onsite',
    'salary', 'compensation', 'pay', 'rate', 'bonus',
    'health', 'insurance', 'leave', 'kiwisaver',
    'monday', 'friday', 'tuesday', 'wednesday', 'thursday',
    'please', 'note', 'apply', 'apply now', 'submit',
    'love', 'excited', 'passionate', 'enthusiastic',
    'fast', 'paced', 'dynamic', 'agile', 'lean',
    'about', 'us', 'our', 'them', 'their',
    'click', 'clicks', 'people', 'posted', 'ago',
    'promoted', 'hirer', 'responses', 'managed',
    'matches', 'preferences', 'workplace', 'type',
    'show', 'match', 'details', 'help', 'stand',
    'create', 'cover', 'letter', 'beta', 'information',
    'beneficial', 'advantageous', 'plus', 'bonus',
    'relevant', 'related', 'similar', 'equivalent',
    'ability', 'capable', 'comfortable', 'confident',
    'familiar', 'familiarity', 'exposure', 'awareness',
    'practical', 'hands', 'on', 'real', 'world',
    'level', 'senior', 'junior', 'mid', 'intermediate',
    'lead', 'principal', 'staff', 'architect', 'manager',
    'director', 'head', 'vp', 'c-level', 'cto', 'ceo',
    'engineer', 'developer', 'designer', 'analyst',
    'design', 'develop', 'build', 'test', 'deploy',
    'support', 'maintain', 'improve', 'optimize',
    'create', 'implement', 'deliver', 'ship',
    'collaborate', 'partner', 'work', 'contribute',
    'drive', 'lead', 'manage', 'coordinate',
    'ensure', 'confirm', 'verify', 'validate',
    'understand', 'identify', 'evaluate', 'assess',
    'analyze', 'review', 'research', 'investigate',
    'document', 'communicate', 'present', 'report',
    'follow', 'adhere', 'comply', 'conform',
    'commitment', 'dedication', 'motivation',
    'initiative', 'proactive', 'self', 'directed',
    'deadline', 'pressure', 'fast', 'paced',
    'changing', 'shifting', 'evolving', 'growing',
    'results', 'driven', 'focused', 'oriented',
    'mindset', 'approach', 'philosophy', 'principle',
    'values', 'mission', 'vision', 'purpose',
    'diversity', 'inclusion', 'equal', 'opportunity',
    'gender', 'age', 'ethnicity', 'identity',
    'disability', 'orientation', 'religion', 'belief',
    'veteran', 'military', 'protected', 'characteristic',
    'eligible', 'entitled', 'visa', 'sponsorship',
    'citizenship', 'residency', 'permit', 'status',
    'legal', 'lawful', 'authorized', 'work',
    'closing', 'date', 'deadline', 'closing date',
    'apply', 'submit', 'send', 'email',
    'contact', 'phone', 'call', 'text',
    'website', 'link', 'url', 'page',
    'reference', 'referral', 'recommend',
    'assessment', 'test', 'interview', 'screening',
    'background', 'check', 'reference check',
    'probation', 'trial', 'period',
    'termination', 'resignation', 'notice',
    'overtime', 'shift', 'rotation',
    'travel', 'relocate', 'relocation',
    'driver', 'licence', 'license', 'vehicle',
    'security', 'clearance', 'check',
    'confidential', 'nda', 'agreement',
    'intellectual', 'property', 'ip',
    'non', 'compete', 'non', 'disclosure',
})


def normalize_keywords(jd_keywords: Optional[List[str]]) -> List[str]:
    """Normalize JD keywords by lowercasing, trimming, de-duplicating, and filtering stop words."""
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
        # Skip stop words and empty terms
        if not normalized or normalized in STOP_WORDS:
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
    """Return the subset of keywords that appear in the text (with word boundary awareness)."""
    if not text or not keywords:
        return []
    normalized_text = normalize_text_for_match(text)
    hits: List[str] = []
    for keyword in keywords:
        matched = False
        for variant in keyword_variant_candidates(keyword):
            normalized_variant = normalize_text_for_match(variant)
            if not normalized_variant:
                continue
            # Use word boundary matching to avoid false positives
            # e.g., "api" should not match "capital", "rapid"
            if re.search(r'\b' + re.escape(normalized_variant) + r'\b', normalized_text):
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
    """Keep only JD keywords that are supported by KB evidence (with word boundary matching)."""
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
            if not normalized_variant:
                continue
            # Use word boundary matching to avoid false positives
            if re.search(r'\b' + re.escape(normalized_variant) + r'\b', corpus):
                hit = True
                break
        if hit:
            supported.append(keyword)
        else:
            filtered.append(keyword)
    return supported, filtered
