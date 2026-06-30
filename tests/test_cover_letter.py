#!/usr/bin/env python3
"""Tests for cover letter generation and quality validation."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from generate_cover_letter import build_cover_letter_content
from cl_quality_validator import run_cl_quality_check, build_cl_check_markdown, CLQualityReport


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def kb_data():
    """Load minimal KB data needed for CL generation."""
    import yaml
    kb_root = ROOT / "kb"
    with (kb_root / "profile.yaml").open(encoding="utf-8") as f:
        profile = yaml.safe_load(f)
    with (kb_root / "achievements.yaml").open(encoding="utf-8") as f:
        achievements = yaml.safe_load(f)
    # Load all project facts
    projects = []
    projects_dir = ROOT / "projects"
    for d in projects_dir.iterdir():
        facts_path = d / "facts.yaml"
        if facts_path.is_file():
            with facts_path.open(encoding="utf-8") as f:
                projects.append(yaml.safe_load(f))
    return profile, achievements, projects


# ---------------------------------------------------------------------------
# Content generation tests
# ---------------------------------------------------------------------------
class TestCLContent:
    def test_generic_template_produces_four_sections(self, kb_data):
        profile, achievements, projects = kb_data
        content = build_cover_letter_content(
            profile, achievements, projects,
            role_type="fullstack",
            company_name="Test Company Ltd",
            target_role_title="Software Developer",
            jd_keywords=["React", "Node.js", "TypeScript"],
            lang="en",
        )
        assert "opening" in content
        assert "body1" in content
        assert "body2" in content
        assert "closing" in content
        assert len(content["opening"]) > 20
        assert len(content["body1"]) > 20
        assert len(content["body2"]) > 20
        assert len(content["closing"]) > 10

    def test_all_role_types_produce_valid_content(self, kb_data):
        profile, achievements, projects = kb_data
        for role in ["android", "backend", "ai", "fullstack"]:
            content = build_cover_letter_content(
                profile, achievements, projects,
                role_type=role,
                company_name="Acme Corp",
                target_role_title="Software Engineer",
                jd_keywords=["Java", "Python"],
                lang="en",
            )
            assert content["opening"], f"Empty opening for role={role}"
            assert content["body1"], f"Empty body1 for role={role}"
            assert content["body2"], f"Empty body2 for role={role}"

    def test_company_specific_hooks_used_when_available(self, kb_data):
        """When company matches _WHY_ME_HOOKS, body1 should use that content."""
        profile, achievements, projects = kb_data
        content = build_cover_letter_content(
            profile, achievements, projects,
            role_type="fullstack",
            company_name="Halter",
            target_role_title="Senior Software Engineer",
            jd_keywords=["React", "Java"],
            lang="en",
        )
        # Halter has a _WHY_ME_HOOKS entry — body1 should reference it
        assert "Halter" in content["body1"] or "farmer" in content["body1"].lower()

    def test_jd_keywords_appear_in_body2(self, kb_data):
        profile, achievements, projects = kb_data
        content = build_cover_letter_content(
            profile, achievements, projects,
            role_type="backend",
            company_name="Random Corp",
            target_role_title="Backend Engineer",
            jd_keywords=["Java", "Spring Boot", "REST API"],
            lang="en",
        )
        # Body2 should reference JD themes
        body2_lower = content["body2"].lower()
        assert "java" in body2_lower or "spring" in body2_lower or "rest" in body2_lower


# ---------------------------------------------------------------------------
# Quality validation tests
# ---------------------------------------------------------------------------
class TestCLQuality:
    def test_quality_check_basic(self):
        html = """
        <p>Dear Hiring Manager,</p>
        <p>I am applying for the Software Developer position at Acme Corp.
        With 10+ years of experience in full-stack development, I bring strong
        Java and React skills to your team.</p>
        <p>In my recent work on enterprise platforms, I built microservices
        handling 500K+ daily messages and designed REST APIs consumed by
        mobile and web teams. This experience aligns well with your need
        for scalable backend systems.</p>
        <p>My background includes mentoring junior developers, leading
        technical discussions, and writing documentation that non-technical
        stakeholders can use. I communicate clearly across teams.</p>
        <p>Kind regards,<br>Leo Zhang</p>
        """
        report = run_cl_quality_check(html, jd_keywords=["Java", "React"])
        assert report.word_count > 50
        assert report.paragraph_count >= 3
        assert report.has_salutation
        assert report.has_closing

    def test_quality_check_flags_too_short(self):
        html = "<p>Dear Manager,</p><p>I am interested.</p><p>Thanks.</p>"
        report = run_cl_quality_check(html)
        assert not report.word_count_ok

    def test_quality_check_detects_ai_tone(self):
        html = """
        <p>Dear Hiring Manager,</p>
        <p>I am passionate about building world-class, cutting-edge solutions
        that seamlessly integrate with your robust and scalable platform.</p>
        <p>I am writing to express my strong interest in this role.</p>
        <p>I would like to apply my proven track record to your team.</p>
        <p>Kind regards, Leo</p>
        """
        report = run_cl_quality_check(html)
        assert len(report.tone_flags) >= 3

    def test_markdown_report_generation(self):
        html = """
        <p>Dear Hiring Manager,</p>
        <p>I am applying for the role. With 10 years experience in Java backend
        development and microservices architecture, I can contribute to your team.
        My recent work includes building REST APIs and Spring Boot services.</p>
        <p>I have mentored engineers and led technical discussions across teams.
        I communicate clearly and write documentation for non-technical stakeholders.</p>
        <p>Kind regards, Leo</p>
        """
        report = run_cl_quality_check(html, jd_keywords=["Java", "Spring Boot"])
        md = build_cl_check_markdown(report)
        assert "Cover Letter Quality Check" in md
        assert "Word count" in md
