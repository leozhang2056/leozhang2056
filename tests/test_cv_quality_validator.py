from app.backend.cv_quality_validator import check_bullet_quality, estimate_ai_flavor, check_ai_authenticity


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


def test_estimate_ai_flavor_basic():
    text = "Led a team to deliver a feature with 15% performance improvement using Python and Docker."
    res = estimate_ai_flavor(text)
    assert isinstance(res, dict)
    assert 'ai_score' in res and 'notes' in res


def test_check_ai_authenticity_no_evidence():
    html = "<html><body>Sample CV content with no links.</body></html>"
    score, issues = check_ai_authenticity(html)
    assert isinstance(score, (int, float))
    assert isinstance(issues, list)


def test_check_ai_authenticity_with_evidence():
    html = "<html><body>See <a href=\"https://example.com\">demo</a></body></html>"
    score, issues = check_ai_authenticity(html)
    assert isinstance(score, (int, float))
    assert isinstance(issues, list)
