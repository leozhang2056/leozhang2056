"""
Tests for jd_fetch.py - JD text fetching and keyword extraction.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add app/backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "backend"))

import pytest
from jd_fetch import (
    _parse_cookie_string,
    extract_keywords_from_text,
    load_jd_text_from_file,
)


class TestParseCookieString:
    """Tests for _parse_cookie_string function."""

    def test_single_cookie(self):
        result = _parse_cookie_string("session=abc123")
        assert result == {"session": "abc123"}

    def test_multiple_cookies(self):
        result = _parse_cookie_string("session=abc123; user=john; token=xyz")
        assert result == {"session": "abc123", "user": "john", "token": "xyz"}

    def test_strips_whitespace(self):
        result = _parse_cookie_string("  session = abc123 ;  user = john  ")
        assert result == {"session": "abc123", "user": "john"}

    def test_handles_quoted_values(self):
        result = _parse_cookie_string('name="value with spaces"')
        assert result == {"name": "value with spaces"}

    def test_empty_string(self):
        result = _parse_cookie_string("")
        assert result == {}


class TestExtractKeywordsFromText:
    """Tests for extract_keywords_from_text function."""

    def test_empty_text(self):
        assert extract_keywords_from_text("") == []
        assert extract_keywords_from_text(None) == []

    def test_extracts_tech_keywords(self):
        text = "We need Python, Java, and Kubernetes experience."
        result = extract_keywords_from_text(text)
        assert "Python" in result
        assert "Java" in result
        assert "Kubernetes" in result

    def test_filters_stopwords(self):
        text = "The engineer will work with the team on software development."
        result = extract_keywords_from_text(text)
        # Common words should be filtered
        assert "the" not in [kw.lower() for kw in result]
        assert "with" not in [kw.lower() for kw in result]
        assert "engineer" not in [kw.lower() for kw in result]

    def test_filters_short_tokens(self):
        text = "We use AI ML and NLP for data processing"
        result = extract_keywords_from_text(text)
        # Short tokens (< 3 chars) should be filtered
        assert "AI" not in result
        assert "ML" not in result

    def test_preserves_special_chars(self):
        text = "Experience with C++ and C# is required."
        result = extract_keywords_from_text(text)
        # C++ and C# should be captured (with special chars)
        keywords_lower = [kw.lower() for kw in result]
        assert any("c++" in kw for kw in keywords_lower) or "C++" in result

    def test_respects_max_keywords(self):
        # Create text with many keywords
        text = " ".join([f"Keyword{i}" for i in range(100)])
        result = extract_keywords_from_text(text, max_keywords=10)
        assert len(result) <= 10

    def test_deduplicates_keywords(self):
        text = "Python Python Python Java Java"
        result = extract_keywords_from_text(text)
        # Should deduplicate
        assert result.count("Python") == 1
        assert result.count("Java") == 1

    def test_filters_singleton_noise_but_keeps_tech_terms(self):
        text = (
            "Career advice and salary insights for members. "
            "Need Node.js experience. "
            "Career growth in a collaborative team."
        )
        result = extract_keywords_from_text(text)
        lowered = [kw.lower() for kw in result]
        assert "career" in lowered
        assert "node.js" in lowered
        # singleton non-tech noise should be filtered by frequency floor
        assert "salary" not in lowered

    def test_real_jd_sample(self):
        jd_text = """
        Senior Android Developer

        Requirements:
        - 5+ years of Android development experience
        - Strong proficiency in Kotlin and Java
        - Experience with Jetpack Compose, MVVM architecture
        - Knowledge of RESTful APIs and Retrofit
        - Familiarity with Git and CI/CD pipelines
        """
        result = extract_keywords_from_text(jd_text)
        keywords_lower = [kw.lower() for kw in result]
        
        assert "android" in keywords_lower
        assert "kotlin" in keywords_lower


class TestLoadJdTextFromFile:
    """Tests for load_jd_text_from_file function."""

    def test_nonexistent_file(self):
        result = load_jd_text_from_file("/nonexistent/path/jd.txt")
        assert result == ""

    def test_reads_existing_file(self, tmp_path):
        # Create a temporary JD file
        jd_file = tmp_path / "test_jd.txt"
        jd_content = "Senior Python Developer\nExperience with Django required."
        jd_file.write_text(jd_content, encoding="utf-8")

        result = load_jd_text_from_file(jd_file)
        assert result == jd_content

    def test_handles_path_object(self, tmp_path):
        jd_file = tmp_path / "test_jd.txt"
        jd_file.write_text("Test content", encoding="utf-8")

        result = load_jd_text_from_file(Path(jd_file))
        assert result == "Test content"
