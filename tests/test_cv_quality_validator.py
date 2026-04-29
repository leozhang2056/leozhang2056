from app.backend.cv_quality_validator import check_bullet_quality


def test_check_bullet_quality_detects_strong_leading_verb_with_marker():
    score = check_bullet_quality(
        "• Built Android payment module handling 120k monthly users with Kotlin and Spring APIs"
    )

    assert score.verb_strength == 1.0


def test_check_bullet_quality_detects_weak_leading_phrase():
    score = check_bullet_quality(
        "Worked on backend migration and improved p95 latency by 37% using Python and Redis"
    )

    assert score.verb_strength == 0.3
    assert any('Weak verb detected: "worked on"' == issue for issue in score.issues)


def test_check_bullet_quality_does_not_flag_weak_phrase_in_middle():
    score = check_bullet_quality(
        "Built an observability pipeline and worked with SRE to reduce incidents by 42% in production"
    )

    assert score.verb_strength == 1.0
    assert all("Weak verb detected" not in issue for issue in score.issues)
