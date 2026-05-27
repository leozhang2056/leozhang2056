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
- **Chunxiao career progression title rule**: The second stage "Senior Android Developer" must **never** be remapped to fullstack/backend equivalents (e.g. "Senior Full-Stack Developer", "Senior Backend Developer"). This stage was genuinely an Android development role and stays as "Senior Android Developer" in **all** role types. Identity mapping lives in `_PROGRESSION_TITLE_ROLE_MAP` in `generate_cv_from_kb.py`. The first stage "Team Lead & Full-stack Engineer" and third stage ".NET Software Engineer" keep their original titles as well.

## Integrations and Cross-Component Behavior
- JD ingestion: `app/backend/jd_fetch.py` uses `requests` + `beautifulsoup4`; URL fetch failures should degrade to manual `--jd-keywords`.
- PDF rendering: Playwright Chromium is required by `html_to_pdf`; failures here are environment/dependency issues, not KB logic. **CV font is Inter only** (Google Fonts in HTML head + `document.fonts.ready` before PDF); see `.cursor/rules/resume-generation-standards.mdc` § PDF / print layout.
- **Summary is always five sentences**; highlights only; **JD keywords** (if provided) woven into **sentence 1** and bolded when KB-supported; then strategic bold on differentiators (~6 total). See rules file § Summary rules.
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
- **Core philosophy**: answer 4 questions — who you are, why this role, why you fit, why interview you. NOT a resume rehash, NOT "I'm hardworking", NOT vague.
- **Key insight**: "I understand what problem you're solving, and I'm exactly the person who can do it."
- **Structure**: `app/backend/generate_cover_letter.py`
  - Company-specific hand-crafted versions (best quality) live in `build_cover_letter_content()` as an early-return for known company+role combos.
  - Generic generator follows the 4-paragraph GPT-derived structure: opening (apply + background + culture) → evidence (project/thesis + differentiator) → experience (role attraction + years + mindset) → closing (motivation + team + thank you).
- **9 Rules** (from GPT version analysis):
  1. First sentence directly states position: `"I am applying for the {title} at {company}."`
  2. Each paragraph has a clear topic sentence
  3. Background summarized in one sentence (use tagline from profile.yaml)
  4. Use specific project names (ChatClothes) and concrete tech terms (diffusion models, CI/CD), not vague abstractions
  5. Every piece of evidence links back to role requirements — not just "I did X" but "X maps to what this role needs"
  6. Soft skills embedded in hard facts: `"10 years... helped me develop a practical engineering mindset focused on reliability, collaboration, and continuous improvement"` — never standalone "I'm hardworking"
  7. No cross-paragraph repetition — each paragraph covers a different dimension
  8. Closing names the specific team (`_COMPANY_TEAMS` dict), not generic "your team"
  9. Natural length: 4 paragraphs, 2-4 sentences each, fits one A4 page
- **Company data dictionaries**:
  - `_COMPANY_CULTURE_HOOKS`: lowercase phrases appendable after "because" (e.g. `"it focuses on building practical AI solutions..."`)
  - `_COMPANY_TEAMS`: specific team names for closing (e.g. `"The Warehouse Group's Data and AI team"`)
- **Anti-patterns to avoid**:
  - AI-blog phrasing: "runnable, measurable, iteratively improved" → instead "I build AI systems that actually ship"
  - Keyword dumping: "I noticed this role emphasizes solutions, APIs, Graduate..." → instead connect naturally
  - Identity crisis: telling vs showing credentials; let facts speak through linking sentences

## GitHub profile README (`README.md`)
- In the `username/username` repo layout, root **`README.md`** is rendered on the GitHub **profile** page.
- **Contribution grid:** GitHub does not provide an embeddable copy of the official profile calendar for arbitrary READMEs; use **ghchart.rshah.org** SVG (`/HEXCOLOR/username`, or `/username` fallback). Do **not** re-add `github-readme-stats` or `github-readme-streak-stats` image widgets — they often time out and show broken images.
- **Publications:** Keep the README list aligned with **`kb/achievements.yaml`** → `publications` and **`projects/chatclothes/facts.yaml`** → `evidence` where `type: publication`. Typical order: IVCNZ (published) → IGI chapter (**under review** if applicable) → thesis.
