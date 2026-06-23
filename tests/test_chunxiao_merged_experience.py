import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app" / "backend"))

from generate_cv_from_kb import _render_career_progression_html


def _load_chunxiao_entry():
    with open("kb/experience/work.yaml", encoding="utf-8") as f:
        work = yaml.safe_load(f)
    return next(exp for exp in work["experiences"] if "Chunxiao" in exp["company"])


def test_chunxiao_two_stages_for_backend():
    html = _render_career_progression_html(_load_chunxiao_entry(), "en", "backend")

    assert "Full-stack Engineer" in html
    assert "Senior Android Engineer" in html
    assert html.count('class="career-stage"') == 2


def test_chunxiao_two_stages_for_android():
    entry = _load_chunxiao_entry()
    html = _render_career_progression_html(entry, "en", "android")

    assert "Senior Mobile Engineer" in html
    assert "Senior Android Engineer" in html
    assert html.count('class="career-stage"') == 2


def test_chunxiao_two_stages_for_fullstack():
    html = _render_career_progression_html(_load_chunxiao_entry(), "en", "fullstack")

    assert "Full-stack Engineer" in html
    assert "Senior Android Engineer" in html
    assert html.count('class="career-stage"') == 2


def test_chunxiao_two_stages_for_ai():
    html = _render_career_progression_html(_load_chunxiao_entry(), "en", "ai")

    assert "Full-stack Engineer" in html
    assert "Senior Android Engineer" in html
    assert html.count('class="career-stage"') == 2
