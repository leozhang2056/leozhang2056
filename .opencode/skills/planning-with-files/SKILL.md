---
name: planning-with-files
description: "Persistent file-based planning for multi-step CV, cover-letter, and KB generation tasks in this repository. Use when work needs research, generation, validation, or multiple iterations."
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep"
---

# Planning With Files

Use persistent markdown files as working memory on disk. For complex tasks, keep planning state in the project, not only in chat.

## Project Pattern

Create or use `.planning/<date-task-slug>/` with:

- `task_plan.md` — goal, constraints, phases, acceptance checks, errors.
- `findings.md` — research findings, JD signals, KB constraints, quality observations.
- `progress.md` — timestamped actions, generated artifacts, validation results.

Set `.planning/.active_plan` to the active plan directory name.

## Repository Rules

- Read `.cursorrules`, `memory/L0_BOOTSTRAP.md`, and `memory/L1_SESSION_STATE.md` before generation work.
- Read `kb/rules/resume_output.md` before any CV or cover-letter generation.
- Use only `kb/*.yaml` and `projects/*/facts.yaml` as factual sources.
- Log missing facts as `MISSING_INFO`; do not invent projects, metrics, titles, or technologies.
- After editing KB YAML or project facts, run `python app/backend/validate.py`.

## CV Generation Use

Prefer the built-in persistent planning mode:

```powershell
python generate.py cv --role auto --jd-file jd.txt --company "Acme" --with-planning
```

This writes `.planning/cv-.../task_plan.md`, `findings.md`, and `progress.md` with the resolved targeting context and post-generation quality findings.

## Manual Rules

- Re-read `task_plan.md` before major decisions.
- Update `findings.md` after research or post-generation checks.
- Update `progress.md` after generation, validation, or failed attempts.
- If the same action fails twice, change approach and log the reason.
