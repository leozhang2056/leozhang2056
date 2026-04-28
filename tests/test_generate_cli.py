import argparse
import asyncio
import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import generate


def test_auto_company_from_workday_url():
    args = argparse.Namespace(company=None, jd_url="https://eroadgroup.wd3.myworkdayjobs.com/Careers/job/Auckland/123")

    assert generate._auto_company(args) == "Eroadgroup"


def test_auto_company_returns_explicit_company():
    args = argparse.Namespace(company="OrbitRemit", jd_url="https://example.com/jobs/1")

    assert generate._auto_company(args) == "OrbitRemit"


def test_auto_role_prefers_jd_file_content(monkeypatch):
    fake_jd_fetch = types.SimpleNamespace(load_jd_text_from_file=lambda _: "Need Android Kotlin and Jetpack Compose")
    monkeypatch.setitem(sys.modules, "app.backend.jd_fetch", fake_jd_fetch)

    args = argparse.Namespace(role="auto", title="Engineer", jd_url=None, jd_file="jd.txt")

    assert generate._auto_role(args) == "android"


def test_strict_kb_pre_check_uses_strict_loader(monkeypatch, tmp_path):
    load_all = MagicMock()

    class FakeLoader:
        def __init__(self, base_path):
            self.base_path = base_path

        def load_all(self, strict=False):
            load_all(strict=strict, base_path=self.base_path)

    monkeypatch.setitem(sys.modules, "app.backend.kb_loader", types.SimpleNamespace(KBLoader=FakeLoader))

    generate._strict_kb_pre_check(tmp_path)

    load_all.assert_called_once_with(strict=True, base_path=tmp_path)


def test_run_cv_passes_inferred_arguments(monkeypatch):
    fake_generate_cv = AsyncMock(return_value=("out.pdf", None, None))
    monkeypatch.setitem(
        sys.modules,
        "generate_cv_from_kb",
        types.SimpleNamespace(generate_cv_from_kb=fake_generate_cv),
    )
    monkeypatch.setattr(generate, "_HAS_MEMORY", False)
    monkeypatch.setattr(generate, "_auto_keywords_from_jd", lambda args: ["Kotlin", "Compose"])
    monkeypatch.setattr(generate, "_auto_role", lambda args: "android")
    monkeypatch.setattr(generate, "_auto_company", lambda args: "OrbitRemit")
    monkeypatch.setattr(generate, "_normalize_cv_output_path", lambda output, role, company: "normalized.pdf")

    args = argparse.Namespace(
        command="cv",
        output="ignored.pdf",
        max_projects=4,
        with_zh=False,
        with_quality_report=False,
        with_jd_annotated=False,
        min_jd_match_pct=85.0,
        review_bundle=False,
        keep_html=False,
        no_strict_kb=False,
        no_post_check=False,
        title="Senior Android Developer",
    )

    asyncio.run(generate.run(args))

    fake_generate_cv.assert_awaited_once_with(
        output_path="normalized.pdf",
        role_type="android",
        jd_keywords=["Kotlin", "Compose"],
        max_projects=4,
        company_name="OrbitRemit",
        target_role_title="Senior Android Developer",
        generate_zh=False,
        generate_quality_report=False,
        generate_jd_annotated_pdf=False,
        min_jd_match_pct=85.0,
        write_review_bundle=False,
        keep_html=False,
        strict_kb=True,
        run_post_check=True,
    )


def test_run_email_calls_strict_check_and_generator(monkeypatch, tmp_path):
    fake_email = MagicMock(return_value="email.txt")
    monkeypatch.setitem(
        sys.modules,
        "generate_application_email",
        types.SimpleNamespace(generate_application_email=fake_email),
    )
    strict_precheck = MagicMock()
    monkeypatch.setattr(generate, "_strict_kb_pre_check", strict_precheck)
    monkeypatch.setattr(generate, "_auto_keywords_from_jd", lambda args: ["Java"])
    monkeypatch.setattr(generate, "_auto_role", lambda args: "backend")
    monkeypatch.setattr(generate, "_auto_company", lambda args: "Infosys")

    args = argparse.Namespace(
        command="email",
        output=None,
        role="auto",
        lang="en",
        company=None,
        title="Senior Java Developer",
        jd_keywords=None,
        jd_url=None,
        jd_file=None,
        no_strict_kb=False,
    )

    asyncio.run(generate.run(args))

    expected_root = Path(generate.__file__).parent
    strict_precheck.assert_called_once_with(expected_root)
    fake_email.assert_called_once_with(
        output_path=None,
        role_type="backend",
        lang="en",
        company_name="Infosys",
        target_role_title="Senior Java Developer",
        jd_keywords=["Java"],
    )
