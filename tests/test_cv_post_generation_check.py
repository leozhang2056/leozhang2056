from app.backend.cv_post_generation_check import analyze_fluency


def _html(summary: str, body: str) -> str:
    return f"""
    <html>
      <body>
        <div class="cv-summary">{summary}</div>
        <div class="cv-skills">Java, Spring Boot, AWS</div>
        <ul>{body}</ul>
      </body>
    </html>
    """


def test_fluency_flags_repeated_tech_terms():
    html = _html(
        "Backend engineer with production systems experience.",
        """
        <li>Built Spring Boot services with Spring Boot APIs.</li>
        <li>Maintained Spring Boot modules and Spring Boot integrations.</li>
        <li>Used AWS coursework exposure alongside AWS database labs.</li>
        <li>Mapped AWS fundamentals to AWS-style cloud operations.</li>
        """,
    )

    score, notes = analyze_fluency(html)

    assert score < 100
    assert any('Repeated tech term "spring boot"' in note for note in notes)
    assert any('Repeated tech term "aws"' in note for note in notes)


def test_fluency_flags_conversational_summary_tone():
    html = _html(
        "I build backend systems. I ship features. My work is reliable. I've led teams, and I like production work.",
        "<li>Delivered backend services with clear release checks.</li>",
    )

    score, notes = analyze_fluency(html)

    assert score < 100
    assert any("First-person wording in Summary" in note for note in notes)
