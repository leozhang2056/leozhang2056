from app.backend.kb_validation import validate_project_data


def _valid_project():
    return {
        "project_id": "demo-project",
        "name": "Demo Project",
        "type": "Enterprise System",
        "timeline": {"start": "2024-01", "end": "2024-12"},
        "role": "Developer",
        "summary": "A" * 60,
        "highlights": ["Implemented core feature"],
        "tech_stack": {"languages": ["Python"]},
        "keywords": ["python"],
        "last_updated": "2026-03-30",
        "skills_demonstrated": {"technical": ["Python"]},
        "related_to_roles": ["backend"],
    }


def test_validate_project_data_success():
    model, errors = validate_project_data(_valid_project())
    assert errors == []
    assert model is not None
    assert model.project_id == "demo-project"


def test_validate_project_data_missing_required_field():
    data = _valid_project()
    data.pop("project_id")

    model, errors = validate_project_data(data)
    assert model is None
    assert any("project_id" in e for e in errors)


def test_validate_project_data_invalid_timeline_object():
    data = _valid_project()
    data["timeline"] = "2024"

    model, errors = validate_project_data(data)
    assert model is None
    assert any("timeline" in e for e in errors)

