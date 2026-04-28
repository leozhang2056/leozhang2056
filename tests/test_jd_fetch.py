"""
Tests for jd_fetch.py - JD text fetching and keyword extraction.
"""

import sys
import types
from pathlib import Path
from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup

# Add app/backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "backend"))

import pytest
from jd_fetch import (
    _parse_cookie_string,
    fetch_jd_text_from_url,
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


class TestFetchJdTextFromUrl:
    """Tests for fetch_jd_text_from_url function."""

    def test_fetches_and_strips_html_noise(self):
        response = MagicMock()
        response.text = """
        <html>
          <head>
            <style>.x { color: red; }</style>
            <script>console.log("ignore")</script>
          </head>
          <body>
            <h1>Senior Android Developer</h1>
            <p>Need Kotlin and Jetpack Compose.</p>
          </body>
        </html>
        """
        response.raise_for_status.return_value = None
        fake_requests = types.SimpleNamespace(get=MagicMock(return_value=response))
        fake_bs4 = types.SimpleNamespace(BeautifulSoup=BeautifulSoup)

        with patch.dict(sys.modules, {"requests": fake_requests, "bs4": fake_bs4}):
            text = fetch_jd_text_from_url("https://example.com/job")

        assert "Senior Android Developer" in text
        assert "Need Kotlin and Jetpack Compose." in text
        assert "console.log" not in text
        assert "color: red" not in text

    def test_returns_empty_string_on_network_failure(self):
        fake_requests = types.SimpleNamespace(get=MagicMock(side_effect=Exception("timeout")))
        fake_bs4 = types.SimpleNamespace(BeautifulSoup=MagicMock())

        with patch.dict(sys.modules, {"requests": fake_requests, "bs4": fake_bs4}):
            assert fetch_jd_text_from_url("https://example.com/job") == ""

    def test_returns_empty_string_when_dependencies_missing(self):
        real_requests = sys.modules.pop("requests", None)
        real_bs4 = sys.modules.pop("bs4", None)
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name in {"requests", "bs4"}:
                raise ImportError("missing dependency")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            assert fetch_jd_text_from_url("https://example.com/job") == ""

        if real_requests is not None:
            sys.modules["requests"] = real_requests
        if real_bs4 is not None:
            sys.modules["bs4"] = real_bs4
