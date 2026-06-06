import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app" / "backend"))

from generate_cv_from_kb import _render_career_progression_html


def _load_chunxiao_entry():
    with open("kb/experience/work.yaml", encoding="utf-8") as f:
        work = yaml.safe_load(f)
    return next(exp for exp in work["experiences"] if "Chunxiao" in exp["company"])


def test_chunxiao_experience_is_merged_for_target_role():
    html = _render_career_progression_html(_load_chunxiao_entry(), "en", "backend")

    assert "Senior Backend Engineer" in html
    assert html.count('class="job-role"') == 1



def test_chunxiao_merged_title_changes_by_role():
    entry = _load_chunxiao_entry()

    assert "Senior Android Developer" in _render_career_progression_html(entry, "en", "android")
    assert "Senior Full-Stack Engineer" in _render_career_progression_html(entry, "en", "fullstack")
    assert "AI Software Engineer" in _render_career_progression_html(entry, "en", "ai")
