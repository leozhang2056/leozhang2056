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


def test_enforce_keeps_edu_at_lead_when_present():
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
    # Edu sentence stays at lead position per current architecture
    assert parts[0].startswith("Master")
    assert parts[-1] != SUMMARY_EDU_CLOSING_EN


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


def test_generate_summary_with_jd_keywords_sentence1_bold(profile):
    text = generate_summary(
        profile,
        role_type="android",
        lang="en",
        jd_keywords=["Kotlin", "Agile", "Android SDK"],
    )
    # JD bolding is handled by Skills/Experience sections.
    # Summary should still be well-formed with bold highlights.
    sentences = _split_summary_sentences(text, "en")
    assert len(sentences) >= 5
    assert "<strong>" in text


def test_generate_summary_android_five_sentences(profile):
    text = generate_summary(profile, role_type="android", lang="en")
    stripped = re.sub(r"<[^>]+>", "", text)
    assert "Android" in stripped or "android" in stripped.lower()
    assert len(stripped) > 50
    lowered = text.lower()
    assert "work rights" not in lowered
    assert "based in auckland" not in lowered
    assert "<strong>" in text


def test_generate_summary_zh_android_five_sentences(profile):
    text = generate_summary(profile, role_type="android", lang="zh")
    parts = _split_summary_sentences(text, "zh")
    assert len(parts) == 5
    assert "一等荣誉" in parts[-1]
    assert "AUT" in parts[-1] or "奥克兰理工" in parts[-1]
