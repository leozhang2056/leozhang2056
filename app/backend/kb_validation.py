"""Unified KB validation helpers used by CLI and loaders."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

try:
    from data_models import validate_project_facts  # type: ignore
except ModuleNotFoundError:
    from app.backend.data_models import validate_project_facts

REQUIRED_PROJECT_FIELDS = [
    "project_id",
    "name",
    "type",
    "timeline",
    "role",
    "summary",
    "highlights",
    "tech_stack",
    "keywords",
    "last_updated",
    "skills_demonstrated",
    "related_to_roles",
]


def validate_project_data(data: Dict[str, Any]) -> Tuple[Optional[Any], List[str]]:
    """Validate one project dict with required-field + model checks."""
    errors: List[str] = []

    if not data:
        return None, ["文件为空"]

    for field in REQUIRED_PROJECT_FIELDS:
        if field not in data:
            errors.append(f"缺少必需字段: {field}")

    timeline = data.get("timeline")
    if "timeline" in data:
        if isinstance(timeline, dict):
            if not timeline.get("start"):
                errors.append("timeline.start 为空")
            if not timeline.get("end"):
                errors.append("timeline.end 为空")
        else:
            errors.append("timeline 必须是对象")

    metrics = data.get("metrics")
    if isinstance(metrics, list):
        for i, m in enumerate(metrics):
            if isinstance(m, dict):
                if "value" not in m:
                    errors.append(f"metrics[{i}] 缺少 value")
                if "label" not in m:
                    errors.append(f"metrics[{i}] 缺少 label")

    try:
        model = validate_project_facts(data)
    except Exception as e:
        errors.append(f"模型校验失败: {e}")
        model = None

    return model, errors


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

