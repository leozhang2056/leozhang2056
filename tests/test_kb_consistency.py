"""Cross-file KB consistency checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# Must match input_validation.py:validate_role()
VALID_ROLES = {'auto', 'android', 'ai', 'backend', 'fullstack'}


class TestKBConsistency:
    def test_template_roles_match_valid_roles(self):
        """Every role in cv_base_template.yaml must be in valid_roles."""
        tpl = _load("kb/cv_base_template.yaml")
        template_roles = set(tpl.get("roles", {}).keys())
        missing = template_roles - VALID_ROLES
        assert not missing, f"Roles in template but not in valid_roles: {missing}"

    def test_profile_summary_variants_have_template(self):
        """Every summary_variant key (except default) should map to a template role."""
        profile = _load("kb/profile.yaml")
        variants = set(profile.get("career_identity", {}).get("summary_variants", {}).keys())
        variants.discard("default")
        tpl = _load("kb/cv_base_template.yaml")
        template_roles = set(tpl.get("roles", {}).keys())
        allowed_no_template = {"android_focus", "ai_focus", "java_focus"}
        extra = variants - template_roles - allowed_no_template
        assert not extra, f"summary_variant keys with no template role: {extra}"

    def test_education_dates_match_work(self):
        """Education end_date and work end_date should not conflict."""
        profile = _load("kb/profile.yaml")
        work = _load("kb/experience/work.yaml")
        edu = profile.get("education", [])
        experiences = work.get("experiences", [])
        aut_edu = [e for e in edu if "AUT" in e.get("institution", "").upper() or "Auckland" in e.get("institution", "")]
        aut_work = [e for e in experiences if "AUT" in e.get("company", "").upper() or "Auckland" in e.get("company", "")]
        if aut_edu and aut_work:
            edu_end = max(e.get("end_date", "") for e in aut_edu if e.get("end_date"))
            work_end = max(e.get("end_date", "") for e in aut_work if e.get("end_date"))
            assert edu_end[:4] == work_end[:4], f"AUT edu end {edu_end} vs work end {work_end} mismatch"

    def test_all_projects_have_facts(self):
        """Every project directory should have a valid facts.yaml."""
        projects_dir = ROOT / "projects"
        if not projects_dir.is_dir():
            pytest.skip("No projects directory")
        for pdir in sorted(projects_dir.iterdir()):
            if pdir.is_dir():
                facts = pdir / "facts.yaml"
                assert facts.is_file(), f"Missing facts.yaml in {pdir.name}"
                data = yaml.safe_load(facts.read_text(encoding="utf-8"))
                assert data.get("project_id") == pdir.name, f"project_id mismatch in {pdir.name}"
                assert data.get("name"), f"Missing 'name' in {pdir.name}/facts.yaml"

    def test_cv_template_has_five_sentences(self):
        """Each role summary in cv_base_template must have exactly 5 sentences."""
        tpl = _load("kb/cv_base_template.yaml")
        for role_name, role_data in tpl.get("roles", {}).items():
            sentences = role_data.get("summary_sentences", {}).get("en", [])
            assert len(sentences) == 5, f"{role_name} has {len(sentences)} sentences (expected 5)"
