#!/usr/bin/env python3
"""
Generate application email text from Career KB facts.

Usage examples:
  python app/backend/generate_application_email.py --role android --company "Datacom" --title "Senior Android Developer"
  python app/backend/generate_application_email.py --role backend --company "Air New Zealand" --lang zh
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from generate_cover_letter import build_cover_letter_content
from generate_cv_from_kb import load_yaml, load_projects


def _build_email_subject(company_name: str, target_role_title: str, lang: str) -> str:
    company = (company_name or "the company").strip()
    title = (target_role_title or "Software Engineer").strip()
    if lang == "zh":
        return f"应聘 {company} - {title} | Leo Zhang"
    return f"Application for {title} at {company} - Leo Zhang"


def _trim_sentence(text: str, max_chars: int) -> str:
    s = re.sub(r"\s+", " ", text or "").strip()
    if len(s) <= max_chars:
        return s
    cut = s.rfind(".", 0, max_chars)
    if cut > 40:
        return s[:cut + 1]
    return s[:max_chars].rstrip(" ,;") + "..."


def generate_application_email_text(
    role_type: str = "fullstack",
    lang: str = "en",
    company_name: str = "the company",
    target_role_title: str = "Software Engineer",
    jd_keywords: Optional[List[str]] = None,
) -> str:
    base = Path(__file__).parent.parent.parent
    kb_dir = base / "kb"
    profile = load_yaml(kb_dir / "profile.yaml")
    achievements = load_yaml(kb_dir / "achievements.yaml")
    all_projects = load_projects(base / "projects")

    content = build_cover_letter_content(
        profile=profile,
        achievements=achievements,
        all_projects=all_projects,
        role_type=role_type,
        company_name=company_name,
        target_role_title=target_role_title,
        jd_keywords=jd_keywords or [],
        lang=lang,
    )

    subject = _build_email_subject(company_name, target_role_title, lang)
    opening = _trim_sentence(content.get("opening", ""), 240)
    body1 = _trim_sentence(content.get("body1", ""), 280)
    body2 = _trim_sentence(content.get("body2", ""), 240)
    closing = _trim_sentence(content.get("closing", ""), 180)
    name = content.get("name", "Leo Zhang")
    email = content.get("email", "")
    phone = content.get("phone", "")

    if lang == "zh":
        greeting = "尊敬的招聘团队，"
        signoff = "此致"
    else:
        greeting = "Dear Hiring Team,"
        signoff = "Best regards,"

    return (
        f"Subject: {subject}\n\n"
        f"{greeting}\n\n"
        f"{opening}\n\n"
        f"{body1}\n\n"
        f"{body2}\n\n"
        f"{closing}\n\n"
        f"{signoff}\n"
        f"{name}\n"
        f"{email}\n"
        f"{phone}\n"
    )


def generate_application_email(
    output_path: Optional[str] = None,
    role_type: str = "fullstack",
    lang: str = "en",
    company_name: str = "the company",
    target_role_title: str = "Software Engineer",
    jd_keywords: Optional[List[str]] = None,
) -> str:
    today = datetime.now().strftime("%Y%m%d")
    today_dir = datetime.now().strftime("%Y-%m-%d")
    repo_root = Path(__file__).parent.parent.parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    dated_outputs_dir = outputs_dir / today_dir
    dated_outputs_dir.mkdir(exist_ok=True)

    if not output_path:
        safe_company = re.sub(r"[^a-zA-Z0-9_-]", "_", company_name)[:24]
        output_path = str(dated_outputs_dir / f"ApplicationEmail_{safe_company}_{today}.txt")

    text = generate_application_email_text(
        role_type=role_type,
        lang=lang,
        company_name=company_name,
        target_role_title=target_role_title,
        jd_keywords=jd_keywords,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate application email from Career KB")
    parser.add_argument(
        "--role",
        default="fullstack",
        choices=["android", "ai", "backend", "fullstack"],
        help="Target role type",
    )
    parser.add_argument("--lang", default="en", choices=["en", "zh"], help="Output language")
    parser.add_argument("--company", default="the company", help="Company name")
    parser.add_argument("--title", default="Software Engineer", help="Target role title")
    parser.add_argument("--jd-keywords", nargs="*", dest="jd_keywords", help="JD keywords for relevance")
    parser.add_argument("--output", default=None, help="Output TXT path")
    args = parser.parse_args()

    out = generate_application_email(
        output_path=args.output,
        role_type=args.role,
        lang=args.lang,
        company_name=args.company,
        target_role_title=args.title,
        jd_keywords=args.jd_keywords,
    )
    print(f"Email text generated: {out}")


if __name__ == "__main__":
    main()
