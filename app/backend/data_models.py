"""
Data validation models using Pydantic for type safety and validation.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class ProjectFacts(BaseModel):
    """Validation model for project facts.yaml"""

    model_config = ConfigDict(extra="allow")

    project_id: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    name_cn: Optional[str] = None
    summary: Optional[str] = None
    summary_cn: Optional[str] = None
    overview: Optional[str] = None
    overview_cn: Optional[str] = None
    role: Optional[str] = None
    role_cn: Optional[str] = None
    company: Optional[Dict[str, Any]] = None
    institution: Optional[Dict[str, Any]] = None
    timeline: Optional[Dict[str, Any]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    related_to_roles: List[str] = Field(default_factory=list)
    tech_stack: Dict[str, List[str]] = Field(default_factory=dict)
    highlights: List[Any] = Field(default_factory=list)
    highlights_cn: List[Any] = Field(default_factory=list)
    impact: List[str] = Field(default_factory=list)
    achievements: List[Union[Dict[str, Any], str]] = Field(default_factory=list)
    skills_demonstrated: Optional[Union[Dict[str, Any], List[Any], str]] = None
    last_updated: Optional[str] = None

    @field_validator('keywords', 'related_to_roles', mode='before')
    @classmethod
    def validate_non_empty_strings(cls, v):
        if isinstance(v, list):
            out = []
            for item in v:
                if isinstance(item, str):
                    s = item.strip()
                    if s:
                        out.append(s)
                else:
                    out.append(item)
            return out
        return v

    @model_validator(mode='after')
    def validate_required_minimum(self):
        required = [
            'project_id', 'name', 'type', 'timeline', 'role',
            'summary', 'highlights', 'tech_stack', 'keywords',
            'last_updated', 'skills_demonstrated', 'related_to_roles',
        ]

        missing = []
        for field_name in required:
            value = getattr(self, field_name, None)
            if value is None:
                missing.append(field_name)
            elif isinstance(value, str) and not value.strip():
                missing.append(field_name)
            elif isinstance(value, (list, dict)) and not value:
                missing.append(field_name)

        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")

        if not isinstance(self.timeline, dict):
            raise ValueError("timeline must be an object")
        if not self.timeline.get('start'):
            raise ValueError("timeline.start is required")
        if not self.timeline.get('end'):
            raise ValueError("timeline.end is required")

        return self

class SkillsData(BaseModel):
    """Validation model for skills.yaml"""

    model_config = ConfigDict(extra="allow")

    android: Optional[List[str]] = None
    programming_languages: Optional[List[str]] = None
    ai_coding_tools: Optional[List[str]] = None
    backend: Optional[List[str]] = None
    devops: Optional[List[str]] = None
    databases: Optional[List[str]] = None
    ai_ml: Optional[List[str]] = None
    iot_hardware: Optional[List[str]] = None

class ProfileData(BaseModel):
    """Validation model for profile.yaml"""

    model_config = ConfigDict(extra="allow")

    personal_info: Dict[str, Any] = Field(default_factory=dict)
    career_identity: Dict[str, Any] = Field(default_factory=dict)
    education: List[Dict[str, Any]] = Field(default_factory=list)

class BulletEntry(BaseModel):
    """Validation model for bullet entries"""

    model_config = ConfigDict(extra="allow")

    original: Optional[str] = None
    variants: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)

    @field_validator('variants', 'tags', 'evidence', mode='before')
    @classmethod
    def validate_non_empty_strings(cls, v):
        if isinstance(v, list):
            out = []
            for item in v:
                if isinstance(item, str):
                    s = item.strip()
                    if s:
                        out.append(s)
                else:
                    out.append(item)
            return out
        return v


class AchievementsData(BaseModel):
    """Validation model for achievements.yaml"""

    model_config = ConfigDict(extra="allow")

    certifications: List[Dict[str, Any]] = Field(default_factory=list)
    awards: List[Dict[str, Any]] = Field(default_factory=list)
    publications: List[Dict[str, Any]] = Field(default_factory=list)

def validate_project_facts(data: Dict[str, Any]) -> ProjectFacts:
    """Validate project facts data"""
    return ProjectFacts(**data)


def validate_skills_data(data: Dict[str, Any]) -> SkillsData:
    """Validate skills data"""
    return SkillsData(**data)


def validate_profile_data(data: Dict[str, Any]) -> ProfileData:
    """Validate profile data"""
    return ProfileData(**data)


def validate_bullet_entry(data: Dict[str, Any]) -> BulletEntry:
    """Validate bullet entry"""
    return BulletEntry(**data)


def validate_achievements_data(data: Dict[str, Any]) -> AchievementsData:
    """Validate achievements data"""
    return AchievementsData(**data)
