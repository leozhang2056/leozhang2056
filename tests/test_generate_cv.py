import os
import tempfile

import yaml


class TestLoadYaml:
    def test_load_yaml_success(self):
        from app.backend.generate_cv_from_kb import load_yaml

        data = {"key": "value", "number": 42}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(data, f)
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == data
        finally:
            os.unlink(temp_path)

    def test_load_yaml_file_not_found(self):
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml("non_existent_file.yaml")
        assert result == {}

    def test_load_yaml_empty_file(self):
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_yaml_invalid_yaml(self):
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [\n")
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_yaml_invalid_file_path_type(self):
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml(123)
        assert result == {}


class TestGenerationQuality:
    def test_generate_summary_does_not_append_mechanical_jd_tail(self):
        from app.backend.generate_cv_from_kb import generate_summary

        profile = {
            "career_identity": {
                "summary_variants": {
                    "default": (
                        "Software engineer with 10+ years across Java backend, Android delivery, "
                        "and IoT systems. Delivered enterprise systems with measurable production outcomes."
                    )
                }
            }
        }

        summary = generate_summary(
            profile,
            role_type="backend",
            lang="en",
            jd_keywords=["Kafka", "Redis", "Kubernetes", "Observability"],
        )

        assert "Hands-on with" not in summary
        assert "stable release discipline" not in summary

    def test_select_bullets_prefers_stronger_evidence_backed_variant(self):
        from app.backend.generate_cv_from_kb import _select_bullets_for_project

        project = {
            "project_id": "enterprise-messaging",
            "keywords": ["messaging", "java"],
            "related_to_roles": ["backend"],
            "tech_stack": {"backend": ["Java", "Redis"]},
        }
        bullets = [
            {
                "evidence": ["enterprise-messaging"],
                "tags": ["backend", "java", "redis"],
                "variants": [
                    "Helped with backend messaging features.",
                    "Built Java messaging services handling 5000 DAU with Redis-backed session routing.",
                ],
            }
        ]

        selected = _select_bullets_for_project(
            project,
            bullets,
            role_type="backend",
            jd_keywords=["Java", "Redis"],
            max_bullets=1,
        )

        assert selected == [
            "Built Java messaging services handling 5000 DAU with Redis-backed session routing."
        ]
