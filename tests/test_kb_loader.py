from pathlib import Path

import yaml
import pytest

from app.backend.kb_loader import KBLoader


def _write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _valid_project(project_id: str = "demo-project") -> dict:
    return {
        "project_id": project_id,
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


def _build_repo(tmp_path: Path, *, with_project: bool = True) -> Path:
    repo = tmp_path / "repo"
    _write_yaml(
        repo / "kb" / "profile.yaml",
        {
            "personal_info": {"name": "Leo Zhang"},
            "career_identity": {"summary_variants": {"default": "Backend engineer"}},
            "education": [],
        },
    )
    _write_yaml(repo / "kb" / "skills.yaml", {"backend": ["Java", "Python"]})
    _write_yaml(repo / "kb" / "achievements.yaml", {"certifications": [], "awards": [], "publications": []})
    _write_yaml(repo / "kb" / "project_relations.yaml", {"timelines": []})
    _write_yaml(
        repo / "kb" / "bullets" / "backend.yaml",
        {
            "bullets": [
                {
                    "variants": ["Built backend services."],
                    "tags": ["backend"],
                    "evidence": ["demo-project"],
                }
            ]
        },
    )
    if with_project:
        _write_yaml(repo / "projects" / "demo-project" / "facts.yaml", _valid_project())
    else:
        (repo / "projects").mkdir(parents=True, exist_ok=True)
    return repo


def test_kb_loader_load_all_strict_success(tmp_path):
    repo = _build_repo(tmp_path)

    data = KBLoader(repo).load_all(strict=True)

    assert data.profile.personal_info["name"] == "Leo Zhang"
    assert len(data.projects) == 1
    assert data.projects[0].project_id == "demo-project"
    assert len(data.bullets) == 1


def test_kb_loader_non_strict_skips_invalid_project(tmp_path):
    repo = _build_repo(tmp_path)
    _write_yaml(repo / "projects" / "demo-project" / "facts.yaml", {"project_id": "demo-project"})

    data = KBLoader(repo).load_all(strict=False)

    assert data.projects == []


def test_kb_loader_strict_raises_for_invalid_project(tmp_path):
    repo = _build_repo(tmp_path)
    _write_yaml(repo / "projects" / "demo-project" / "facts.yaml", {"project_id": "demo-project"})

    with pytest.raises(ValueError, match="KB projects validation failed"):
        KBLoader(repo).load_all(strict=True)


def test_kb_loader_strict_raises_for_missing_achievements_file(tmp_path):
    repo = _build_repo(tmp_path)
    (repo / "kb" / "achievements.yaml").unlink()

    with pytest.raises(FileNotFoundError, match="Achievements file not found"):
        KBLoader(repo).load_all(strict=True)


def test_kb_loader_cache_and_invalidate(tmp_path):
    repo = _build_repo(tmp_path)
    loader = KBLoader(repo)

    first = loader.load_all(strict=True)
    _write_yaml(repo / "projects" / "demo-project" / "facts.yaml", _valid_project(project_id="updated-project"))

    cached = loader.load_all(strict=True)
    assert cached is first
    assert cached.projects[0].project_id == "demo-project"

    loader.invalidate_cache()
    reloaded = loader.load_all(strict=True)
    assert reloaded is not first
    assert reloaded.projects[0].project_id == "updated-project"
