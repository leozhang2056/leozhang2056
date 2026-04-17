# AGENTS.md

## Purpose
- This repo is a KB-driven "resume compiler": structured YAML facts in `kb/` + `projects/*/facts.yaml` are transformed into CV/cover-letter/email outputs (not handwritten each time).
- Treat generated artifacts in `outputs/` and templates in `templates/` as outputs/reference, not truth sources.

## Layered Memory Startup (Important)
- To reduce cold-start scanning, read in this fixed order:
  1. `memory/L0_BOOTSTRAP.md`
  2. `memory/L1_SESSION_STATE.md`
  3. `memory/L2_DEEP_INDEX.md` (then jump to only necessary deep files)
- Do not load large documents by default if L0/L1 already provide enough execution context.
- Keep memory layers clean:
  - L0 = stable minimal facts + startup protocol
  - L1 = current session continuity (goal/progress/next action)
  - L2 = deep-document index only (no duplicated long content)

## Big Picture Architecture
- Single entrypoint: `generate.py` dispatches subcommands (`cv`, `cl`, `email`, `interview`, `match`, `cv-iterate`) and injects `app/backend` into import path.
- Core pipeline lives in `app/backend/generate_cv_from_kb.py`:
  - load YAML (`load_yaml`, `load_projects`)
  - rank projects by role + JD keywords (`sort_projects`, `score_project_by_jd`)
  - generate HTML, then PDF via `app/backend/generate_cv_html_to_pdf.py::html_to_pdf`.
- Data contracts are YAML-first: `kb/profile.yaml`, `kb/skills.yaml`, `kb/achievements.yaml`, `kb/project_relations.yaml`, and per-project `projects/<id>/facts.yaml`.
- Validation boundary:
  - unified validation helpers: `app/backend/kb_validation.py`
  - CLI validator: `app/backend/validate.py`
  - typed loader/validators: `app/backend/kb_loader.py` + `app/backend/data_models.py` (Pydantic).

## Critical Workflows (Commands)
- Install deps:
```bash
pip install -r requirements.txt
```
- Validate KB after any `facts.yaml` edits:
```bash
python app/backend/validate.py
```
- Main generation flows:
```bash
python generate.py cv --role android
python generate.py cl --role backend --company "Acme"
python generate.py email --role fullstack --company "Acme"
python generate.py match --role auto --jd-file jd.txt
python generate.py interview --category technical
```
- After each `cv` run, the generator prints a **post-generation check** (fluency heuristics, HTML layout signals, JD keyword coverage) and writes `*_POST_CHECK.md` next to the PDF. Use `python generate.py cv ... --no-post-check` to skip.
- Run tests:
```bash
pytest
```

## Project-Specific Conventions
- Non-negotiable anti-hallucination rule: only use facts from `kb/*.yaml` and `projects/*/facts.yaml` (see `kb/resume_generation_rules.md`, `kb/ai_input_spec.md`, `.cursorrules`).
- If required facts are missing/conflicting, prefer explicit markers (`MISSING_INFO`, `FACT_CONFLICT`) over guessing.
- Source priority for AI context assembly: `kb/profile.yaml` -> `kb/skills.yaml` -> `kb/project_relations.yaml` -> `projects/*/facts.yaml` -> `kb/bullets/*.yaml`.
- Role vocabulary is fixed: `auto|android|ai|backend|fullstack` (CLI and ranking heuristics depend on this).
- Keep generated CV scope tight (default 6 projects; cap in code) for ~2 A4 pages.
- Tune role inference and ranking via `kb/generation_config.yaml` (instead of hardcoding keywords/priority maps).

## Integrations and Cross-Component Behavior
- JD ingestion: `app/backend/jd_fetch.py` uses `requests` + `beautifulsoup4`; URL fetch failures should degrade to manual `--jd-keywords`.
- PDF rendering: Playwright Chromium is required by `html_to_pdf`; failures here are environment/dependency issues, not KB logic.
- Iterative AI patch loop: `python generate.py cv-iterate ...` in `app/backend/cv_auto_review_iterate.py`:
  - extracts PDF text via `pypdf`
  - calls OpenAI-compatible `/chat/completions` (`OPENAI_API_KEY`, optional `OPENAI_BASE_URL`, `OPENAI_MODEL`)
  - backs up touched YAML to `outputs/<date>/kb_backup_auto_*` before patching.
  - prints a KB change summary and file-level rollback copy hints after patching.
- Interview QA loader prefers `interview_qa/` at repo root, then falls back to `kb/interview_qa/` (`app/backend/interview_qa_cli.py`).

## Practical Debugging Notes
- If a generated PDF looks unchanged, check dated output folder selection in `outputs/YYYY-MM-DD/` or force `--output` (called out in `generate.py` docstring).
- For schema-sensitive additions, mirror required fields from `kb/schema/project_facts_schema.yaml` and re-run `validate.py`.

## GitHub profile README (`README.md`)
- In the `username/username` repo layout, root **`README.md`** is rendered on the GitHub **profile** page.
- **Contribution grid:** GitHub does not provide an embeddable copy of the official profile calendar for arbitrary READMEs; use **ghchart.rshah.org** SVG (`/HEXCOLOR/username`, or `/username` fallback). Do **not** re-add `github-readme-stats` or `github-readme-streak-stats` image widgets — they often time out and show broken images.
- **Publications:** Keep the README list aligned with **`kb/achievements.yaml`** → `publications` and **`projects/chatclothes/facts.yaml`** → `evidence` where `type: publication`. Typical order: IVCNZ (published) → IGI chapter (**under review** if applicable) → thesis.
