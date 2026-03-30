from app.backend.project_ranking import score_project_by_jd, sort_projects


def _project(pid: str, *, keywords=None, roles=None, tech=None, highlights=None, end="2024"):
    return {
        "_project_dir": pid,
        "keywords": keywords or [],
        "related_to_roles": roles or [],
        "tech_stack": {"backend": tech or []},
        "highlights": highlights or [],
        "timeline": {"start": "2020", "end": end},
    }


def test_score_project_by_jd_prefers_keyword_and_tech_hits():
    p1 = _project(
        "enterprise-messaging",
        keywords=["spring", "kafka"],
        roles=["backend"],
        tech=["Spring Boot", "Redis"],
        highlights=["Built Kafka messaging pipeline"],
    )
    p2 = _project("chatclothes", keywords=["pytorch"], tech=["PyTorch"], highlights=["AI model training"])

    assert score_project_by_jd(p1, ["spring", "kafka"]) > score_project_by_jd(p2, ["spring", "kafka"])


def test_sort_projects_without_jd_uses_role_priority():
    projects = [
        _project("chatclothes"),
        _project("enterprise-messaging"),
        _project("smart-factory"),
    ]

    ranked = sort_projects(projects, role_type="android", jd_keywords=None, max_projects=3)
    assert ranked[0]["_project_dir"] == "enterprise-messaging"


def test_sort_projects_with_jd_uses_score_first():
    projects = [
        _project("smart-factory", keywords=["iot"], tech=["RFID"]),
        _project("enterprise-messaging", keywords=["spring", "java"], tech=["Spring Boot"]),
    ]

    ranked = sort_projects(projects, role_type="fullstack", jd_keywords=["spring"], max_projects=2)
    assert ranked[0]["_project_dir"] == "enterprise-messaging"

