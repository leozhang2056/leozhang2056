from app.backend.cv_post_generation_check import (
    PostGenerationCheck,
    analyze_keyword_distribution,
    analyze_layout,
    build_post_check_markdown,
    evaluate_thresholds,
)


def _sample_html() -> str:
    return """
    <div class="cv-summary">
      Senior Android developer building Kotlin and Compose user experiences for payments apps.
      Delivered stable releases and improved app quality through testing and monitoring.
    </div>
    <div class="cv-skills">
      Kotlin, Jetpack Compose, MVVM, Retrofit, Android
    </div>
    <ul>
      <li>Built Android flows with Kotlin and Compose.</li>
      <li>Integrated Retrofit APIs and improved release stability.</li>
      <li>Worked closely with product and QA on production issues.</li>
    </ul>
    """


def test_analyze_keyword_distribution_counts_hits_by_section():
    summary_hits, skills_hits, bullet_hits = analyze_keyword_distribution(
        _sample_html(),
        ["Kotlin", "Compose", "Retrofit", "Android"],
    )

    assert summary_hits >= 3
    assert skills_hits == 4
    assert bullet_hits >= 3


def test_analyze_layout_flags_missing_core_blocks():
    score, notes = analyze_layout("<div><ul><li>Only bullets</li></ul></div>")

    assert score < 100
    assert any("cv-summary" in note for note in notes)
    assert any("cv-skills" in note for note in notes)


def test_evaluate_thresholds_passes_for_strong_report():
    report = PostGenerationCheck(
        fluency_score=90,
        fluency_notes=[],
        layout_score=91,
        layout_notes=[],
        jd_coverage_pct=100.0,
        jd_hit_count=4,
        jd_total=4,
        jd_misses=[],
        summary_kw_hits=3,
        skills_kw_hits=4,
        bullets_kw_hits=3,
    )

    result = evaluate_thresholds(report, min_target_pct=85.0)

    assert result.overall_pass is True
    assert all(ok for _, ok, _ in result.checks)


def test_build_post_check_markdown_includes_gate_and_sections():
    report = PostGenerationCheck(
        fluency_score=75,
        fluency_notes=["Repeated phrase"],
        layout_score=80,
        layout_notes=["Summary looks short"],
        jd_coverage_pct=50.0,
        jd_hit_count=2,
        jd_total=4,
        jd_misses=["Compose", "Retrofit"],
        summary_kw_hits=1,
        skills_kw_hits=2,
        bullets_kw_hits=1,
    )

    markdown = build_post_check_markdown(report, min_target_pct=85.0)

    assert "# CV Post-Generation Check" in markdown
    assert "Gate status" in markdown
    assert "Recruiter Review" in markdown
    assert "Interviewer Review" in markdown
    assert "Compose, Retrofit" in markdown
