#!/usr/bin/env python3
"""Persistent planning files for CV generation runs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class GenerationPlanContext:
    plan_dir: Path
    task_plan_path: Path
    findings_path: Path
    progress_path: Path


def _slugify(value: str, fallback: str = "target") -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value or "").strip("-").lower()
    return (slug or fallback)[:48]


def _format_keywords(keywords: Optional[Iterable[str]]) -> str:
    items = [str(k).strip() for k in (keywords or []) if str(k).strip()]
    return ", ".join(items) if items else "none"


def start_generation_plan(
    *,
    repo_root: Path,
    command: str,
    role_type: str,
    company_name: Optional[str],
    target_role_title: Optional[str],
    jd_keywords: Optional[Iterable[str]],
    max_projects: int,
    min_jd_match_pct: float,
) -> GenerationPlanContext:
    """Create Manus-style planning files for one CV generation run."""
    now = datetime.now()
    slug_parts = [now.strftime("%Y-%m-%d"), command, role_type]
    if company_name:
        slug_parts.append(_slugify(company_name))
    plan_id = "-".join(slug_parts)
    plan_dir = repo_root / ".planning" / plan_id
    plan_dir.mkdir(parents=True, exist_ok=True)
    (repo_root / ".planning" / ".active_plan").write_text(plan_id, encoding="utf-8")

    task_plan_path = plan_dir / "task_plan.md"
    findings_path = plan_dir / "findings.md"
    progress_path = plan_dir / "progress.md"

    title = target_role_title or "not provided"
    company = company_name or "not provided"
    task_plan_path.write_text(
        "\n".join(
            [
                "# CV Generation Plan",
                "",
                "## Goal",
                f"Generate a targeted CV for `{company}` / `{title}` without inventing facts.",
                "",
                "## Constraints",
                "- Use only `kb/*.yaml` and `projects/*/facts.yaml` as factual sources.",
                "- Keep output within the existing CV/CL rules in `kb/rules/resume_output.md`.",
                "- Treat unsupported JD keywords as anti-hallucination filtered items, not writing targets.",
                "",
                "## Run Context",
                f"- Command: `{command}`",
                f"- Role: `{role_type}`",
                f"- Company: `{company}`",
                f"- Target title: `{title}`",
                f"- Max projects: `{max_projects}`",
                f"- JD match target: `{min_jd_match_pct:.1f}%`",
                f"- JD keywords: `{_format_keywords(jd_keywords)}`",
                "",
                "## Phases",
                "- [x] Resolve role, company, title, and JD keywords.",
                "- [ ] Generate CV from KB.",
                "- [ ] Run post-generation quality gate.",
                "- [ ] Record improvement actions for next iteration.",
                "",
                "## Errors Encountered",
                "| Error | Attempt | Resolution |",
                "|---|---|---|",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    findings_path.write_text(
        "\n".join(
            [
                "# CV Generation Findings",
                "",
                "## JD Signals",
                f"- Supported/initial keywords: `{_format_keywords(jd_keywords)}`",
                "",
                "## Quality Findings",
                "- Pending post-generation check.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    progress_path.write_text(
        "\n".join(
            [
                "# CV Generation Progress",
                "",
                f"- {now.isoformat(timespec='seconds')} Started planning run `{plan_id}`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return GenerationPlanContext(
        plan_dir=plan_dir,
        task_plan_path=task_plan_path,
        findings_path=findings_path,
        progress_path=progress_path,
    )


def finish_generation_plan(
    *,
    context: GenerationPlanContext,
    pdf_path: str,
    post_check_path: Optional[str],
    post_check_report: object = None,
    supported_keywords: Optional[Iterable[str]] = None,
    filtered_keywords: Optional[Iterable[str]] = None,
    min_jd_match_pct: float = 85.0,
) -> None:
    """Update planning files with generated artifacts and quality findings."""
    now = datetime.now().isoformat(timespec="seconds")
    report = post_check_report
    gate = "UNKNOWN"
    fluency = layout = coverage = "n/a"
    misses = "none"
    if report is not None:
        fluency_score = float(getattr(report, 'fluency_score', 0.0))
        layout_score = float(getattr(report, 'layout_score', 0.0))
        coverage_pct = float(getattr(report, 'jd_coverage_pct', 0.0))
        jd_total = int(getattr(report, 'jd_total', 0) or 0)
        fluency = f"{fluency_score:.0f}/100"
        layout = f"{layout_score:.0f}/100"
        coverage = f"{coverage_pct:.1f}%"
        miss_items = getattr(report, "jd_misses", []) or []
        misses = _format_keywords(miss_items)
        coverage_ok = jd_total == 0 or min_jd_match_pct <= 0 or coverage_pct >= min_jd_match_pct
        gate = "PASS" if fluency_score >= 78.0 and layout_score >= 82.0 and coverage_ok else "CHECK"

    task_plan = context.task_plan_path.read_text(encoding="utf-8")
    task_plan = task_plan.replace("- [ ] Generate CV from KB.", "- [x] Generate CV from KB.")
    if post_check_path or report is not None:
        task_plan = task_plan.replace(
            "- [ ] Run post-generation quality gate.",
            "- [x] Run post-generation quality gate.",
        )
    task_plan = task_plan.replace(
        "- [ ] Record improvement actions for next iteration.",
        "- [x] Record improvement actions for next iteration.",
    )
    if "## Output" not in task_plan:
        task_plan += (
            "\n## Output\n"
            f"- PDF: `{pdf_path}`\n"
            f"- Post-check: `{post_check_path or 'not generated'}`\n"
            f"- Gate: `{gate}`\n"
        )
    context.task_plan_path.write_text(task_plan, encoding="utf-8")

    context.findings_path.write_text(
        "\n".join(
            [
                "# CV Generation Findings",
                "",
                "## JD Signals",
                f"- KB-supported keywords: `{_format_keywords(supported_keywords)}`",
                f"- Filtered unsupported keywords: `{_format_keywords(filtered_keywords)}`",
                "",
                "## Quality Findings",
                f"- Gate: `{gate}`",
                f"- Fluency: `{fluency}`",
                f"- Layout: `{layout}`",
                f"- JD coverage: `{coverage}`",
                f"- JD misses: `{misses}`",
                "",
                "## Next Improvement Focus",
                "- If gate is not PASS, improve only KB-supported wording or project selection.",
                "- Do not add unsupported metrics, titles, or technologies to chase coverage.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with context.progress_path.open("a", encoding="utf-8") as f:
        f.write(f"- {now} Generated PDF `{pdf_path}`.\n")
        f.write(f"- {now} Post-check `{post_check_path or 'not generated'}`; gate `{gate}`.\n")
