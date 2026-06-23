# Leo CV Generator

Knowledge-base-driven resume compiler for Leo Zhang (Yuchao Zhang), Senior Software Engineer in Auckland, NZ.

## Quick Start

```bash
# Generate CV for a job
python generate.py cv --role backend --jd-file jd.txt --company "Company" --title "Senior Engineer"

# HTML-only draft (fast, no PDF)
python generate.py cv --role backend --jd-file jd.txt --company "Company" --html-only

# Generate cover letter
python generate.py cl --role backend --jd-file jd.txt --company "Company" --title "Senior Engineer"

# Multi-agent pipeline (highest quality)
python generate.py cv-best --role backend --jd-file jd.txt --company "Company" --auto-refine

# Batch: all JDs in Interview/NewJobs/ sequentially
python generate.py batch-cv

# Batch: parallel with shared browser (3x faster for many JDs)
python generate.py batch-cv --parallel 3

# Validate knowledge base
python -m pytest tests/ -v -k kb
```

## Available Roles
`auto` | `android` | `ai` | `backend` | `fullstack`

## Architecture

```
generate.py              ← CLI entrypoint (subcommands: cv, cl, email, interview, match)
app/backend/             ← Core engine
  generate_cv_from_kb.py   ← Main CV generation pipeline
  generate_cv_html_to_pdf.py ← HTML → PDF via Playwright
  kb_loader.py / kb_validation.py ← Knowledge base I/O
  project_ranking.py       ← JD-driven project scoring
  role_inference.py        ← Auto-role from JD text
kb/                      ← Career knowledge base (YAML ground truth)
  profile.yaml             ← Personal info, summaries, education
  skills.yaml              ← Categorized skills with proof points
  cv_base_template.yaml    ← Per-role CV templates (summary, skills, tech stack)
  generation_config.yaml   ← Role inference keywords, project ranking
projects/                ← 19 real projects, each with facts.yaml + README.md
```

## Data Philosophy
Manage career experience as data; compile resumes as software.
- `kb/` + `projects/*/facts.yaml` = single source of truth
- Generated PDFs in `outputs/` are artifacts, not truth
- Never fabricate facts — if it's not in YAML, it doesn't go on the CV

## Key Files
- `AGENTS.md` — Full architecture docs for AI agents
- `kb/cv_base_template.yaml` — CV layout templates per role
- `kb/rules/resume_output.md` — Wording/layout constraints (all in one file)
- `kb/generation_config.yaml` — Tunable ranking/inference parameters

## Custom Slash Commands
- `/cv-backend`, `/cv-android`, `/cv-fullstack`, `/cv-ai` — Role-specific CV generation
- `/cv-best` — Multi-agent pipeline for highest quality
- `/cover-letter` — Generate cover letter
- `/kb-validate` — Validate knowledge base YAML
- `/run-tests` — Run test suite
