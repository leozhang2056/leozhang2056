"""Summary five-sentence structure enforcement."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from generate_cv_from_kb import (  # noqa: E402
    SUMMARY_EDU_CLOSING_EN,
    SUMMARY_REQUIRED_SENTENCES,
    _apply_jd_sentence1_alignment,
    _enforce_summary_five_sentences,
    _split_summary_sentences,
    _strip_summary_low_signal,
    generate_summary,
)


@pytest.fixture
def profile():
    path = ROOT / "kb" / "profile.yaml"
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def test_enforce_moves_edu_from_lead_to_closing():
    raw = (
        "Master's in Computer and Information Sciences from AUT, First Class Honours. "
        "Backend engineer with 10+ years on Java. "
        "Specialized in enterprise APIs. "
        "Proven delivery on production services. "
        "Additional expertise includes CI/CD and observability."
    )
    out = _enforce_summary_five_sentences(raw, "en")
    parts = _split_summary_sentences(out, "en")
    assert len(parts) == 5
    assert parts[-1] == SUMMARY_EDU_CLOSING_EN
    assert not _split_summary_sentences(parts[0], "en")[0].startswith("Master")


def test_strip_work_rights_and_location():
    raw = (
        "Android engineer with 10+ years. "
        "Specialized in mobile delivery. "
        "Proven delivery at scale. "
        "Additional expertise includes AI tools, and open full-time work rights in Auckland, New Zealand. "
        "Master's in Computer and Information Sciences from AUT, First Class Honours."
    )
    out = _strip_summary_low_signal(raw, "en")
    lowered = out.lower()
    assert "work rights" not in lowered
    assert "auckland" not in lowered


def test_jd_terms_bolded_in_sentence1(profile):
    skills_path = ROOT / "kb" / "skills.yaml"
    with skills_path.open(encoding="utf-8") as f:
        skills_data = yaml.safe_load(f)
    career = profile["career_identity"]
    raw = career["summary_variants"]["android_focus"]
    raw = " ".join(raw.split())
    input_text = _enforce_summary_five_sentences(raw, "en")
    aligned = _apply_jd_sentence1_alignment(
        input_text,
        ["Kotlin", "Agile", "Android", "JunkToolXYZ"],
        skills_data,
        "en",
    )
    # The automatic JD injection/bolding in summary is disabled per architecture decisions
    # (Summary is controlled by cv_base_template.yaml, JD matching by Skills/Experience).
    # Thus, _apply_jd_sentence1_alignment should return the input unchanged.
    assert aligned == input_text


def test_generate_summary_with_jd_keywords_sentence1_bold(profile):
    text = generate_summary(
        profile,
        role_type="android",
        lang="en",
        jd_keywords=["Kotlin", "Agile", "Android SDK"],
    )
    first = _split_summary_sentences(text, "en")[0]
    assert "<strong>" in first
    assert re.search(r"<strong>\s*Kotlin", first, re.I) or re.search(
        r"<strong>\s*Android", first, re.I
    )


def test_generate_summary_android_five_sentences(profile):
    text = generate_summary(profile, role_type="android", lang="en")
    parts = _split_summary_sentences(text, "en")
    assert len(parts) == SUMMARY_REQUIRED_SENTENCES
    assert "First Class Honours" in parts[-1]
    assert "AUT" in parts[-1]
    assert "10+ years" in parts[0] or "10+ years" in text
    lowered = text.lower()
    assert "work rights" not in lowered
    assert "based in auckland" not in lowered
    assert "<strong>" in text
    assert re.search(r"<strong>\s*First Class Honours\s*</strong>", text, re.I)


def test_generate_summary_zh_android_five_sentences(profile):
    text = generate_summary(profile, role_type="android", lang="zh")
    parts = _split_summary_sentences(text, "zh")
    assert len(parts) == 5
    assert "一等荣誉" in parts[-1]
    assert "AUT" in parts[-1] or "奥克兰理工" in parts[-1]
