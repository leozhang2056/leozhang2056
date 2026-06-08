"""CV Markdown generation and parsing for editable workflow."""

from __future__ import annotations

import html as html_mod
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "app" / "backend"))

from generate_cv_from_kb import (
    _CSS,
    _CV_FONT_HEAD,
    generate_education_section,
    generate_interests_section,
    generate_licenses_section,
    generate_skills_section,
)
from kb_io import load_projects, load_project_relations, load_all_bullets


def _load_yaml(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_md(
    role_type: str = "android",
    lang: str = "en",
    output_path: Optional[str] = None,
) -> str:
    """Generate an editable Markdown CV from KB data."""
    kb_dir = ROOT / "kb"
    profile = _load_yaml(str(kb_dir / "profile.yaml"))
    skills_data = _load_yaml(str(kb_dir / "skills.yaml"))
    achievements = _load_yaml(str(kb_dir / "achievements.yaml"))
    work_exp = _load_yaml(str(kb_dir / "experience" / "work.yaml"))
    projects = load_projects(ROOT / "projects")
    bullets = load_all_bullets(ROOT / "kb")
    relations = load_project_relations(ROOT / "kb")
    tpl = _load_yaml(str(kb_dir / "cv_base_template.yaml"))

    personal = profile.get("personal_info", {})
    name = personal.get("preferred_name") or personal.get("name", "Leo Zhang")
    contact = personal.get("contact", {})
    email = contact.get("email", "")
    phone = contact.get("phone", "")
    loc = contact.get("location", {})
    city = loc.get("city", "")
    country = loc.get("country", "")
    linkedin = contact.get("linkedin", "")
    github = contact.get("github", "https://github.com/leozhang2056")

    # Summary
    role_tpl = tpl.get("roles", {}).get(role_type, {})
    summary_sents = role_tpl.get("summary_sentences", {}).get(lang, [])
    summary = "\n\n".join(summary_sents) if summary_sents else ""

    # Core Competencies
    skills_html = generate_skills_section(skills_data, role_type, lang)
    # Convert HTML skills table back to markdown-like format
    skills_lines = re.findall(r"<strong>([^<]+)</strong>\s*([^<]+)</div>", skills_html)
    skills_md_lines = []
    for label, skill_text in skills_lines:
        skills_md_lines.append(f"- **{label}**: {skill_text.strip()}")

    # Education
    edu_html = generate_education_section(profile, lang)
    edu_text = re.sub(r"<[^>]+>", "", edu_html)
    edu_text = edu_text.replace("&amp;", "&").replace("&nbsp;", " ")

    # Experience - from work.yaml
    exp_lines = []
    experiences = work_exp.get("experiences", []) if isinstance(work_exp, dict) else []
    for exp in experiences:
        company = exp.get("company", "")
        location = exp.get("location", "")
        role = exp.get("role", "")
        period = exp.get("start_date", "")[:4]
        if exp.get("end_date"):
            period += f" – {exp['end_date'][:4]}"
        exp_lines.append(f"\n### {company} — {location}  \n{role} | {period}")
        exp_achievements = exp.get("achievements", [])
        if isinstance(exp_achievements, list):
            for a in exp_achievements:
                clean = re.sub(r"<[^>]+>", "", str(a))
                exp_lines.append(f"- {clean}")
        # Career progression
        progression = exp.get("career_progression", [])
        if isinstance(progression, list):
            for stage in progression:
                title = stage.get("title", "")
                st_period = stage.get("period", "")
                exp_lines.append(f"\n**{title}** | {st_period}")
                for a in stage.get("achievements", []):
                    clean = re.sub(r"<[^>]+>", "", str(a))
                    exp_lines.append(f"- {clean}")
        # Tech stack
        tech_stack = exp.get("tech_stack", [])
        if tech_stack:
            exp_lines.append(f"  \n*Tech: {', '.join(str(t) for t in tech_stack)}*")

    # Licenses
    lic_html = generate_licenses_section(achievements, lang)
    lic_text = re.sub(r"<[^>]+>", "", lic_html)
    lic_text = lic_text.replace("&amp;", "&").replace("&nbsp;", " ")

    # Interests
    interests_html = generate_interests_section(profile, lang)
    interests_text = re.sub(r"<[^>]+>", "", interests_html)
    interests_text = interests_text.replace("&amp;", "&").replace("&nbsp;", " ")

    # Referees
    referees_text = "References available upon request."

    # Build contact line
    contact_line = f"{email} | {phone} | {city}, {country}"
    social_line = f"LinkedIn: {linkedin} | GitHub: {github}"

    md = f"""# {name}

{contact_line}
{social_line}

---

## Summary

{summary}

---

## Core Competencies

{chr(10).join(skills_md_lines)}

---

## Experience

{chr(10).join(exp_lines)}

---

## Education

{edu_text.strip()}

---

## Licenses & Certifications

{lic_text.strip()}

---

## Interests

{interests_text.strip()}

---

## Referees

{referees_text}
"""
    if output_path:
        Path(output_path).write_text(md, encoding="utf-8")
        print(f"  MD  → {output_path}")
    return md


def md_to_html(md_path: str, lang: str = "en") -> str:
    """Parse an edited Markdown CV back into HTML for PDF generation."""
    md_text = Path(md_path).read_text(encoding="utf-8")

    def _get_section(title: str) -> str:
        m = re.search(
            rf"^## {re.escape(title)}\s*\n(.*?)(?=\n## |\Z)",
            md_text,
            re.DOTALL | re.MULTILINE,
        )
        return m.group(1).strip() if m else ""

    summary = _get_section("Summary")
    competencies_raw = _get_section("Core Competencies")
    education_raw = _get_section("Education")
    experience_raw = _get_section("Experience")
    licenses_raw = _get_section("Licenses & Certifications")
    interests_raw = _get_section("Interests")
    referees_raw = _get_section("Referees")

    # Parse header
    first_line = md_text.split("\n")[0].lstrip("# ")
    name = first_line.strip()

    # Extract contact info from lines after name
    lines = md_text.split("\n")
    contact_info = ""
    social_info = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if "@" in line and ("|" in line or "linkedin" in line.lower()):
            contact_info = line
        if "LinkedIn:" in line:
            social_info = line

    # Build labels
    labels = {
        "summary": "Summary",
        "skills": "Core Competencies",
        "edu": "Education",
        "exp": "Experience",
        "licenses": "Licenses & Certifications",
        "interests": "Interests",
        "referees": "REFEREES",
    }

    def _md_to_html_paragraph(text: str) -> str:
        """Convert simple md paragraphs to HTML."""
        if not text:
            return ""
        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # Italic
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        # Bullet lists
        text = re.sub(r"(?m)^- (.+)$", r"<li>\1</li>", text)
        text = re.sub(r"(?:<li>.*?</li>\s*)+", lambda m: f"<ul class=\"stage-list\">{m.group()}</ul>", text)
        # Line breaks
        text = text.replace("\n", "<br>\n")
        # Escape HTML
        return text

    skills_html = _md_to_html_paragraph(competencies_raw)
    edu_html = _md_to_html_paragraph(education_raw)
    exp_html = _md_to_html_paragraph(experience_raw)
    lic_html = _md_to_html_paragraph(licenses_raw)
    interests_html = _md_to_html_paragraph(interests_raw)
    summary_html = "<p>" + _md_to_html_paragraph(summary) + "</p>" if summary else ""

    # Contact header bits
    contact_primary = f'<a href="mailto:{html_mod.escape(contact_info)}">&#9993;&nbsp;{html_mod.escape(contact_info)}</a>'
    if social_info:
        parts = social_info.split("|")
        for p in parts:
            p = p.strip()
            if "linkedin" in p.lower():
                url = p.split(":")[-1].strip() if ":" in p else p
                contact_primary += f' | <a href="{html_mod.escape(url)}">LinkedIn</a>'
            elif "github" in p.lower():
                url = p.split(":")[-1].strip() if ":" in p else p
                contact_primary += f' | <a href="{html_mod.escape(url)}">GitHub</a>'

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>{html_mod.escape(name)} — CV</title>
  {_CV_FONT_HEAD}
  <style>{_CSS}</style>
</head>
<body>
  <div class="cv-header">
    <div class="cv-name">{html_mod.escape(name)}</div>
    <div class="cv-contact">{contact_primary}</div>
  </div>

  <div class="section-title">{labels['summary']}</div>
  <div class="cv-summary">{summary_html}</div>

  <div class="section-title">{labels['skills']}</div>
  <div class="cv-skills">{skills_html}</div>

  <div class="section-title">{labels['edu']}</div>
  {edu_html}

  <div class="section-title">{labels['exp']}</div>
  {exp_html}

  <div class="section-title">{labels['licenses']}</div>
  <ul class="stage-list">{lic_html}</ul>

  <div class="section-title">{labels['interests']}</div>
  <div class="cv-summary">{interests_html}</div>

  <div class="section-title">{labels['referees']}</div>
  <p class="cv-references">References available upon request.</p>
</body>
</html>"""

    return html
