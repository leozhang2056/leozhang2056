# AGENTS.md

## Purpose
- This repo is a KB-driven "resume compiler": structured YAML facts in `kb/` + `projects/*/facts.yaml` are transformed into CV/cover-letter/email outputs (not handwritten each time).
- Treat generated artifacts in `outputs/` and templates in `templates/` as outputs/reference, not truth sources.

## Constraint File Map
| File | Role | When to Read |
|------|------|-------------|
| `.cursorrules` | Immutable facts + absolute prohibitions | Every session, before any generation |
| `memory/L0_BOOTSTRAP.md` | Startup protocol + minimal facts | Session start |
| `memory/L1_SESSION_STATE.md` | Current goal / next-action / improvements | After L0 |
| `kb/rules/resume_output.md` | **ALL** resume + cover letter output rules | Before any CV/CL generation |
| `kb/rules/jd_analysis_standard.md` | **JD analysis + recruiter-perspective targeting** | Every new JD, before writing CV |
| `AGENTS.md` (this file) | Architecture, workflows, integrations | When navigating repo structure |
| `memory/L2_DEEP_INDEX.md` | Deep-doc navigation index | When needing specific deep docs |

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

### Repository Directory Structure
```
.
├── generate.py                  # Unified CLI Entrypoint
├── AGENTS.md                    # Core workflow rules & architecture (this file)
├── README.md                    # GitHub profile README
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Build/tool configuration
│
├── projects/                    # 19 real projects portfolio
│   └── <project_id>/
│       ├── README.md            # Humans/AI readable details
│       └── facts.yaml           # Ground-truth structured facts (anti-hallucination source)
│
├── kb/                          # Core Career Knowledge Base
│   ├── profile.yaml             # Personal profile & target roles
│   ├── skills.yaml              # Categorized skills & proof points
│   ├── achievements.yaml        # Publications, awards, certs
│   ├── project_relations.yaml   # Narration threads & project links
│   ├── resume_generation_rules.md  # Detailed layout/wording constraints (archived → see kb/rules/resume_output.md)
│   ├── career/                  # Career strategy & NZ job market guides
│   ├── experience/              # Work & research history
│   ├── bullets/                 # Reusable bullet point templates by role
│   ├── schema/                  # Validation schemas
│   └── interview_qa/            # Scripted/YAML interview Q&As + methodology guides
│
├── app/backend/                 # Resume compiler backend logic
├── templates/                   # Real layout templates (TeX, Markdown base)
├── outputs/                     # Generated outputs (Gitignored)
├── jd_archive/                  # Historically fetched JD text files
├── memory/                      # Layered state tracking memory
└── tests/                       # Automated test suite
```

### Component Responsibility
- `projects/<id>/facts.yaml` is the SINGLE source of truth for project details.
- `kb/` represents cross-project aggregated profile facts.
- Generated PDFs and cover letters compile these facts dynamically; do not handwrite target CVs.

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
python generate.py cv --role auto --jd-file jd.txt
python generate.py cl --role backend --company "Acme"
python generate.py email --role fullstack --company "Acme"
python generate.py match --role auto --jd-file jd.txt
python generate.py interview --category technical
```
- **LinkedIn saved jobs → CV** (Chrome automation via Playwright):
  ```bash
  # Interactive: choose from saved jobs, then auto-generate CV
  python generate.py li-jd

  # Auto-select first saved job, skip CV generation (fetch only)
  python generate.py li-jd --auto 0 --no-generate

  # Custom CDP port (if Chrome already running with --remote-debugging-port=9223)
  python generate.py li-jd --port 9223
  ```
  The script automatically starts a Playwright-managed Chrome with your profile,
  so your LinkedIn session is preserved. No need to start Chrome manually first.
-   After each `cv` run, the generator prints a **post-generation check** (fluency heuristics, HTML layout signals, JD keyword coverage) and writes `*_POST_CHECK.md` next to the PDF. Use `python generate.py cv ... --no-post-check` to skip. Delete `*_POST_CHECK.md` and `.html` files after generation (keep only PDFs).
- **Batch CV generation** (from saved JD files):
  ```bash
  # Generate CVs for ALL JD files in Interview/NewJobs/ (auto-detects role)
  python generate.py batch-cv

  # Dry run (list files without generating)
  python generate.py batch-cv --dry-run

  # Custom input directory
  python generate.py batch-cv --input jd_archive
  ```
  Place `.txt` or `.md` JD files in `Interview/NewJobs/`, then run. Each file gets processed and moved to `_processed/` when done.
  - **LinkedIn markdown files**: `app/backend/jd_extractor.py` automatically strips YAML frontmatter, premium upsells, tracking URLs, and navigation noise to extract the real JD. Coverage improved from ~20% to ~46-92% after this fix.
## Workflow Preference
- For each JD, generate **both CV and CL** (cover letter), always with `--company` flag.
- After generating, delete intermediate `.html` and `*_POST_CHECK.md` files — keep only PDFs.
- **Editable CV workflow** (added 2026-06):
  ```bash
  python generate.py cv --role android --gen-md outputs/CV.md  # generate editable MD
  python generate.py cv --from-md outputs/CV.md --output outputs/CV.pdf  # MD → PDF
  ```
- DOCX generation removed (2026-06): quality too low, HTML→PDF is the canonical output.
- Run tests:
```bash
pytest
```

## Project-Specific Conventions
- Non-negotiable anti-hallucination rule: only use facts from `kb/*.yaml` and `projects/*/facts.yaml` (see `.cursorrules`).
- If required facts are missing or conflicting, ask the user whether they have relevant experience or details to add before proceeding; do not guess.
- Role vocabulary is fixed: `auto|android|ai|backend|fullstack` (CLI and ranking heuristics depend on this).
  Other roles (`nateva|idexx|fintech|photon|westpac|hnry`) have been removed (2026-06 cleanup).
- Keep generated CV scope tight (default 6 projects; cap in code) for ~2 A4 pages.
- Tune role inference and ranking via `kb/generation_config.yaml` (instead of hardcoding keywords/priority maps).
- **Output format rules → `kb/rules/resume_output.md`** — Summary, Skills, Experience, Education, Publications, Cover Letter rules, validation checklist, anti-patterns, CLI commands. All in one file. Read before any CV/CL generation.
- AI usage habits:
  - Read every diff the AI writes.
  - Ask the AI to explain its choices.
  - Treat the AI as a mentor that can be wrong.

## Integrations and Cross-Component Behavior
- JD ingestion: `app/backend/jd_fetch.py` uses `requests` + `beautifulsoup4`; URL fetch failures should degrade to manual `--jd-keywords`.
- PDF rendering: Playwright Chromium is required by `html_to_pdf`; failures here are environment/dependency issues, not KB logic. **CV font is Inter only** (Google Fonts in HTML head + `document.fonts.ready` before PDF); see `kb/rules/resume_output.md` § Header & PDF Layout.
- **Summary is always up to five sentences**; highlights only; **JD keywords** (if provided) woven into **sentence 1** and bolded when KB-supported; then strategic bold on differentiators (~6 total). See `kb/rules/resume_output.md` § Summary Rules.
- Summary label: **"Professional Summary"** (not "Career Objective").
- Android summary: education sentence (Master + First Class Honours) as sentence 1, then experience, skills, delivery, AI/data-driven products.
- Education always placed **after Experience** in CV output.
- Iterative AI patch loop: `python generate.py cv-iterate ...` in `app/backend/cv_auto_review_iterate.py`:
  - extracts PDF text via `pypdf`
  - calls OpenAI-compatible `/chat/completions` (`OPENAI_API_KEY`, optional `OPENAI_BASE_URL`, `OPENAI_MODEL`)
  - backs up touched YAML to `outputs/<date>/kb_backup_auto_*` before patching.
  - prints a KB change summary and file-level rollback copy hints after patching.
- Interview QA loader prefers `interview_qa/` at repo root, then `Interview/`, then falls back to `kb/interview_qa/` (`app/backend/interview_qa_cli.py`).
- Behavioral interview **full script** (STAR, Q1–Q45, appendix): `Interview/behavioral_common_qa.md` (see `Interview/README.md` for navigation). Treat `Interview/qa_backup.md` as a historical snapshot, not a second truth source.

## Practical Debugging Notes
- If a generated PDF looks unchanged, check dated output folder selection in `outputs/YYYY-MM-DD/` or force `--output` (called out in `generate.py` docstring).
- For schema-sensitive additions, mirror required fields from `kb/schema/project_facts_schema.yaml` and re-run `validate.py`.

## Cover Letter Generation (NZ IT Market)
- **See `kb/rules/resume_output.md` § Cover Letter Rules** for all formatting, 9 rules, company data, and anti-patterns.
- Core philosophy: answer 4 questions — who you are, why this role, why you fit, why interview you. NOT a resume rehash.
- Implementation: `app/backend/generate_cover_letter.py` with company-specific early-return + generic 4-paragraph generator.

## GitHub profile README (`README.md`)
- In the `username/username` repo layout, root **`README.md`** is rendered on the GitHub **profile** page.
- **Contribution grid:** GitHub does not provide an embeddable copy of the official profile calendar for arbitrary READMEs; use **ghchart.rshah.org** SVG (`/HEXCOLOR/username`, or `/username` fallback). Do **not** re-add `github-readme-stats` or `github-readme-streak-stats` image widgets — they often time out and show broken images.
- **Publications:** Keep the README list aligned with **`kb/achievements.yaml`** → `publications` and **`projects/chatclothes/facts.yaml`** → `evidence` where `type: publication`. Typical order: IVCNZ (published) → IGI chapter (**under review** if applicable) → thesis.
