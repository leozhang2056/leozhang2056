"""Unified KB validation helpers used by CLI and loaders."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

try:
    from data_models import validate_project_facts  # type: ignore
except ModuleNotFoundError:
    from app.backend.data_models import validate_project_facts


def validate_project_data(data: Dict[str, Any]) -> Tuple[Optional[Any], List[str]]:
    """Validate one project dict.

    Delegates entirely to the Pydantic model (``ProjectFacts``) which is the
    single source of truth for required fields and type constraints.  All error
    messages are derived from Pydantic's ``ValidationError`` so that required-
    field lists never need to be maintained in two places.
    """
    if not data:
        return None, ["文件为空"]

    try:
        model = validate_project_facts(data)
    except Exception as exc:
        # Pydantic v2 raises ValidationError; convert to list of strings
        errors: List[str] = []
        if hasattr(exc, "errors"):
            for e in exc.errors():
                loc = " -> ".join(str(l) for l in e.get("loc", []))
                msg = e.get("msg", str(e))
                errors.append(f"{loc}: {msg}" if loc else msg)
        else:
            errors = [str(exc)]
        return None, errors

    # Additional structural checks not covered by Pydantic field types
    extra_errors: List[str] = []
    metrics = data.get("metrics")
    if isinstance(metrics, list):
        for i, m in enumerate(metrics):
            if isinstance(m, dict):
                if "value" not in m:
                    extra_errors.append(f"metrics[{i}] 缺少 value")
                if "label" not in m:
                    extra_errors.append(f"metrics[{i}] 缺少 label")

    if extra_errors:
        return model, extra_errors

    return model, []



def validate_project_file(file_path: Path) -> List[str]:
    """Validate one facts.yaml file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"YAML 解析错误: {e}"]

    _, errors = validate_project_data(data or {})
    return errors


def validate_all_projects(projects_dir: Path) -> Dict[str, List[str]]:
    """Validate all projects under projects directory."""
    results: Dict[str, List[str]] = {}

    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue

        facts_file = project_dir / "facts.yaml"
        if not facts_file.exists():
            results[project_dir.name] = ["缺少 facts.yaml"]
            continue

        results[project_dir.name] = validate_project_file(facts_file)

    return results

