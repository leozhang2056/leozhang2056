"""
Knowledge Base Loader with improved architecture and validation.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    # Package import (when called as `app.backend.kb_loader`)
    from .kb_io import (
        load_yaml,
        load_projects,
        load_all_bullets,
        load_project_relations,
    )
    from .data_models import (
        validate_skills_data,
        validate_profile_data,
        validate_bullet_entry,
        validate_achievements_data,
        ProjectFacts,
        SkillsData,
        ProfileData,
        BulletEntry,
        AchievementsData,
    )
    from .kb_validation import validate_project_data
except ImportError:  # pragma: no cover
    # Top-level module import (when `app/backend` is on sys.path)
    from kb_io import (  # type: ignore
        load_yaml,
        load_projects,
        load_all_bullets,
        load_project_relations,
    )
    from data_models import (  # type: ignore
        validate_skills_data,
        validate_profile_data,
        validate_bullet_entry,
        validate_achievements_data,
        ProjectFacts,
        SkillsData,
        ProfileData,
        BulletEntry,
        AchievementsData,
    )
    from kb_validation import validate_project_data  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class KBData:
    """Container for all KB data"""
    profile: ProfileData
    skills: SkillsData
    projects: List[ProjectFacts]
    bullets: List[BulletEntry]
    achievements: AchievementsData
    relations: Dict[str, Any]


class KBLoader:
    """
    Knowledge Base Loader with validation and caching.

    Provides a clean interface for loading and validating all KB data.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.kb_path = base_path / 'kb'
        self.projects_path = base_path / 'projects'
        self._cache: Optional[KBData] = None

    def load_all(self, force_reload: bool = False, strict: bool = False) -> KBData:
        """
        Load all KB data with validation.

        Args:
            force_reload: If True, reload from disk even if cached
            strict: If True, fail-fast on any validation/load error instead of silently
                    skipping invalid entries or falling back to empty data.

        Returns:
            KBData: Validated KB data container
        """
        if self._cache is not None and not force_reload:
            return self._cache

        logger.info("Loading KB data...")

        # Load and validate each component
        profile = self._load_profile(strict=strict)
        skills = self._load_skills(strict=strict)
        projects = self._load_projects(strict=strict)
        bullets = self._load_bullets(strict=strict)
        achievements = self._load_achievements(strict=strict)
        relations = self._load_relations()

        self._cache = KBData(
            profile=profile,
            skills=skills,
            projects=projects,
            bullets=bullets,
            achievements=achievements,
            relations=relations,
        )

        logger.info(f"Loaded KB data: {len(projects)} projects, {len(bullets)} bullets")
        return self._cache

    def _load_profile(self, strict: bool = False) -> ProfileData:
        """Load and validate profile data"""
        profile_file = self.kb_path / 'profile.yaml'
        if not profile_file.exists():
            raise FileNotFoundError(f"Profile file not found: {profile_file}")

        data = load_yaml(str(profile_file))
        if not data:
            raise ValueError("Empty profile data")

        return validate_profile_data(data)

    def _load_skills(self, strict: bool = False) -> SkillsData:
        """Load and validate skills data"""
        skills_file = self.kb_path / 'skills.yaml'
        if not skills_file.exists():
            if strict:
                raise FileNotFoundError(f"Skills file not found: {skills_file}")
            logger.warning(f"Skills file not found: {skills_file}, using empty skills")
            return validate_skills_data({})

        data = load_yaml(str(skills_file))
        return validate_skills_data(data or {})

    def _load_projects(self, strict: bool = False) -> List[ProjectFacts]:
        """Load and validate all projects"""
        if not self.projects_path.exists():
            if strict:
                raise FileNotFoundError(f"Projects directory not found: {self.projects_path}")
            logger.warning(f"Projects directory not found: {self.projects_path}")
            return []

        # Use strict-friendly loader:
        # - In strict mode we must not skip empty/invalid `facts.yaml` files, otherwise fail-fast loses signal.
        if strict:
            raw_projects: List[Dict[str, Any]] = []
            for project_dir in self.projects_path.iterdir():
                if not project_dir.is_dir():
                    continue
                facts_file = project_dir / "facts.yaml"
                if not facts_file.exists():
                    continue
                facts = load_yaml(str(facts_file)) or {}
                facts["_project_dir"] = project_dir.name
                raw_projects.append(facts)
        else:
            raw_projects = load_projects(str(self.projects_path))

        validated_projects = []
        project_errors: List[str] = []
        for project in raw_projects:
            try:
                validated, field_errors = validate_project_data(project)
                if field_errors:
                    logger.error(
                        "Failed to validate project %s: %s",
                        project.get('_project_dir', 'unknown'),
                        "; ".join(field_errors),
                    )
                    if strict:
                        project_errors.append(
                            f"{project.get('_project_dir', 'unknown')}: " + "; ".join(field_errors)
                        )
                    continue
                if validated is not None:
                    validated_projects.append(validated)
            except Exception as e:
                project_dir = project.get('_project_dir', 'unknown')
                logger.error(f"Failed to validate project {project_dir}: {e}")
                if strict:
                    project_errors.append(f"{project_dir}: exception {e}")

        if strict and project_errors:
            head = "\n".join(project_errors[:5])
            more = "" if len(project_errors) <= 5 else f"\n... and {len(project_errors) - 5} more"
            raise ValueError(f"KB projects validation failed:\n{head}{more}")

        return validated_projects

    def _load_bullets(self, strict: bool = False) -> List[BulletEntry]:
        """Load and validate bullet entries"""
        raw_bullets = load_all_bullets(self.base_path)

        validated_bullets = []
        bullet_errors: List[str] = []
        for bullet in raw_bullets:
            try:
                validated = validate_bullet_entry(bullet)
                validated_bullets.append(validated)
            except Exception as e:
                logger.error(f"Failed to validate bullet: {e}")
                if strict:
                    bullet_errors.append(f"{e}")

        if strict and bullet_errors:
            # Keep message short: show first few errors.
            head = "\n".join(bullet_errors[:5])
            more = "" if len(bullet_errors) <= 5 else f"\n... and {len(bullet_errors) - 5} more"
            raise ValueError(f"KB bullets validation failed:\n{head}{more}")

        return validated_bullets

    def _load_achievements(self, strict: bool = False) -> AchievementsData:
        """Load and validate achievements data"""
        achievements_file = self.kb_path / 'achievements.yaml'
        if not achievements_file.exists():
            if strict:
                raise FileNotFoundError(f"Achievements file not found: {achievements_file}")
            logger.warning(f"Achievements file not found: {achievements_file}, using empty achievements")
            return validate_achievements_data({})

        data = load_yaml(str(achievements_file))
        return validate_achievements_data(data or {})

    def _load_relations(self) -> Dict[str, Any]:
        """Load project relations data"""
        return load_project_relations(self.base_path)

    def get_project_by_id(self, project_id: str) -> Optional[ProjectFacts]:
        """Get a project by ID"""
        data = self.load_all()
        for project in data.projects:
            if project.project_id == project_id:
                return project
        return None

    def get_projects_by_role(self, role: str) -> List[ProjectFacts]:
        """Get projects related to a specific role"""
        data = self.load_all()
        return [
            p for p in data.projects
            if role.lower() in [r.lower() for r in p.related_to_roles]
        ]

    def invalidate_cache(self):
        """Clear the cache to force reload on next access"""
        self._cache = None
        logger.info("KB cache invalidated")