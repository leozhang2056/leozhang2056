"""
Low-level KB I/O helpers.

This module owns the *only* functions that read YAML files from disk and
return raw dicts/lists.  By keeping IO here (and not in generate_cv_from_kb),
kb_loader can import from kb_io without creating a circular dependency:

    kb_io  ←  kb_loader  ←  generate_cv_from_kb
    (no circular edge)
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# YAML file loading
# ---------------------------------------------------------------------------

def load_yaml(file_path: Union[str, Path, "os.PathLike[str]"]) -> Dict[str, Any]:
    """
    Load a YAML file and return a dict.

    Accepts str or Path; silently returns {} on any error so callers can
    always do safe dict-access without extra guards.
    """
    try:
        raw_path = Path(file_path)
    except TypeError:
        logger.error("Invalid file_path type: %s", type(file_path))
        return {}

    if "\x00" in str(file_path):
        logger.error("Invalid file_path: null byte")
        return {}

    try:
        safe_path = raw_path.expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as e:
        logger.error("Could not resolve path %r: %s", file_path, e)
        return {}

    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            logger.warning("YAML file is empty: %s", safe_path)
            return {}
        return data
    except FileNotFoundError:
        logger.error("YAML file not found: %s", safe_path)
        return {}
    except yaml.YAMLError as e:
        logger.error("YAML parsing error in %s: %s", safe_path, e)
        return {}
    except PermissionError:
        logger.error("Permission denied reading %s", safe_path)
        return {}
    except Exception as e:  # pragma: no cover
        logger.error("Unexpected error loading YAML %s: %s", safe_path, e)
        return {}


# ---------------------------------------------------------------------------
# Project loading
# ---------------------------------------------------------------------------

def load_projects(projects_dir: Union[str, Path]) -> List[Dict[str, Any]]:
    """Load all projects/*/facts.yaml files, returning a list of raw dicts."""
    projects: List[Dict[str, Any]] = []
    projects_path = Path(projects_dir)

    if not projects_path.exists():
        logger.error("Projects directory does not exist: %s", projects_dir)
        return projects

    if not projects_path.is_dir():
        logger.error("Projects path is not a directory: %s", projects_dir)
        return projects

    for project_dir in projects_path.iterdir():
        if not project_dir.is_dir():
            continue

        facts_file = project_dir / "facts.yaml"
        if not facts_file.exists():
            logger.debug("No facts.yaml found in %s, skipping", project_dir.name)
            continue

        try:
            facts = load_yaml(str(facts_file))
            if facts:
                facts["_project_dir"] = project_dir.name
                projects.append(facts)
                logger.debug("Loaded project: %s", project_dir.name)
            else:
                logger.warning("Empty facts.yaml in %s", project_dir.name)
        except Exception as e:
            logger.error("Failed to load project %s: %s", project_dir.name, e)

    logger.info("Loaded %d projects from %s", len(projects), projects_dir)
    return projects


# ---------------------------------------------------------------------------
# Bullets loading
# ---------------------------------------------------------------------------

def load_all_bullets(base: Path) -> List[Dict[str, Any]]:
    """Load all bullet entries from kb/bullets/*.yaml."""
    kb_dir = base / "kb"
    bullets_dir = kb_dir / "bullets"
    results: List[Dict[str, Any]] = []

    if not bullets_dir.exists():
        logger.warning("Bullets directory not found")
        return results

    if not bullets_dir.is_dir():
        logger.error("Bullets path is not a directory")
        return results

    for bullet_file in bullets_dir.glob("*.yaml"):
        try:
            with open(bullet_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data is None:
                    logger.warning("Empty bullets file: %s", bullet_file.name)
                    continue

            bullets_list = data.get("bullets", [])
            if not isinstance(bullets_list, list):
                logger.warning("Invalid bullets structure in %s", bullet_file.name)
                continue

            for b in bullets_list:
                if isinstance(b, dict):
                    results.append(b)
                else:
                    logger.warning(
                        "Invalid bullet entry in %s: %s", bullet_file.name, type(b)
                    )

            logger.debug(
                "Loaded %d bullets from %s", len(bullets_list), bullet_file.name
            )

        except yaml.YAMLError as e:
            logger.error("YAML parsing error in %s: %s", bullet_file.name, e)
        except Exception as e:
            logger.error("Unexpected error loading %s: %s", bullet_file.name, e)

    logger.info("Loaded %d total bullet entries", len(results))
    return results


# ---------------------------------------------------------------------------
# Project relations loading
# ---------------------------------------------------------------------------

def load_project_relations(base: Path) -> Dict[str, Any]:
    """Load kb/project_relations.yaml; returns {} on missing/error."""
    kb_dir = base / "kb"
    rel_file = kb_dir / "project_relations.yaml"
    if not rel_file.exists():
        logger.debug("project_relations.yaml not found, using empty relations")
        return {}

    try:
        with open(rel_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                logger.warning("project_relations.yaml is empty")
                return {}
            logger.debug("Loaded project relations successfully")
            return data
    except yaml.YAMLError as e:
        logger.error("YAML parsing error in project_relations.yaml: %s", e)
        return {}
    except Exception as e:
        logger.error("Unexpected error loading project_relations.yaml: %s", e)
        return {}
