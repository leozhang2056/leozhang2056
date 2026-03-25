"""
Knowledge Base Loader with improved architecture and validation.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .data_models import (
    validate_project_facts,
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

    def load_all(self, force_reload: bool = False) -> KBData:
        """
        Load all KB data with validation.

        Args:
            force_reload: If True, reload from disk even if cached

        Returns:
            KBData: Validated KB data container
        """
        if self._cache is not None and not force_reload:
            return self._cache

        logger.info("Loading KB data...")

        # Load and validate each component
        profile = self._load_profile()
        skills = self._load_skills()
        projects = self._load_projects()
        bullets = self._load_bullets()
        achievements = self._load_achievements()
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

    def _load_profile(self) -> ProfileData:
        """Load and validate profile data"""
        profile_file = self.kb_path / 'profile.yaml'
        if not profile_file.exists():
            raise FileNotFoundError(f"Profile file not found: {profile_file}")

        from .generate_cv_from_kb import load_yaml  # Import here to avoid circular imports
        data = load_yaml(str(profile_file))
        if not data:
            raise ValueError("Empty profile data")

        return validate_profile_data(data)

    def _load_skills(self) -> SkillsData:
        """Load and validate skills data"""
        skills_file = self.kb_path / 'skills.yaml'
        if not skills_file.exists():
            logger.warning(f"Skills file not found: {skills_file}, using empty skills")
            return validate_skills_data({})

        from .generate_cv_from_kb import load_yaml
        data = load_yaml(str(skills_file))
        return validate_skills_data(data or {})

    def _load_projects(self) -> List[ProjectFacts]:
        """Load and validate all projects"""
        if not self.projects_path.exists():
            logger.warning(f"Projects directory not found: {self.projects_path}")
            return []

        from .generate_cv_from_kb import load_projects
        # Use existing load_projects but add validation
        raw_projects = load_projects(str(self.projects_path))

        validated_projects = []
        for project in raw_projects:
            try:
                validated = validate_project_facts(project)
                validated_projects.append(validated)
            except Exception as e:
                logger.error(f"Failed to validate project {project.get('_project_dir', 'unknown')}: {e}")
                # Continue with other projects rather than failing completely

        return validated_projects

    def _load_bullets(self) -> List[BulletEntry]:
        """Load and validate bullet entries"""
        from .generate_cv_from_kb import _load_all_bullets
        raw_bullets = _load_all_bullets(self.base_path)

        validated_bullets = []
        for bullet in raw_bullets:
            try:
                validated = validate_bullet_entry(bullet)
                validated_bullets.append(validated)
            except Exception as e:
                logger.error(f"Failed to validate bullet: {e}")

        return validated_bullets

    def _load_achievements(self) -> AchievementsData:
        """Load and validate achievements data"""
        achievements_file = self.kb_path / 'achievements.yaml'
        if not achievements_file.exists():
            logger.warning(f"Achievements file not found: {achievements_file}, using empty achievements")
            return validate_achievements_data({})

        from .generate_cv_from_kb import load_yaml
        data = load_yaml(str(achievements_file))
        return validate_achievements_data(data or {})

    def _load_relations(self) -> Dict[str, Any]:
        """Load project relations data"""
        from .generate_cv_from_kb import _load_project_relations
        return _load_project_relations(self.base_path)

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