# AGENTS.md

## Purpose
- KB-driven "resume compiler": structured YAML facts in `kb/` + `projects/*/facts.yaml` are transformed into CV/cover-letter/email outputs.
- Generated artifacts in `outputs/` and templates in `templates/` are outputs/reference, not truth sources.

## Constraint File Map
| File | Role | When to Read |
|------|------|-------------|
| `.cursorrules` | Immutable facts + absolute prohibitions | Every session, before any generation |
| `kb/rules/resume_output.md` | **ALL** resume + cover letter output rules | Before any CV/CL generation |
| `kb/rules/jd_analysis_standard.md` | **JD analysis + recruiter-perspective targeting** | Every new JD, before writing CV |
| `AGENTS.md` (this file) | Architecture, workflows, integrations | When navigating repo structure |

## Big Picture Architecture
- Single entrypoint: `generate.py` dispatches subcommands (`cv`, `cl`, `email`, `interview`, `match`, `cv-iterate`, `cv-best`, `batch-cv`, `li-jd`) and injects `app/backend` into import path.
- Core pipeline: `app/backend/generate_cv_from_kb.py` — load YAML → rank projects by role + JD keywords → generate HTML → PDF via `app/backend/generate_cv_html_to_pdf.py::html_to_pdf`.
- Data contracts are YAML-first: `kb/profile.yaml`, `kb/skills.yaml`, `kb/achievements.yaml`, `kb/project_relations.yaml`, and per-project `projects/<id>/facts.yaml`.
- Validation: `app/backend/validate.py` (CLI), `app/backend/kb_validation.py` (helpers), `app/backend/kb_loader.py` + `app/backend/data_models.py` (Pydantic typed loaders).

### Key Directories
```
generate.py                  # Unified CLI entrypoint
app/backend/                 # Core engine (35+ modules)
kb/                          # Career knowledge base (YAML ground truth)
  rules/resume_output.md       # All output formatting rules
  rules/jd_analysis_standard.md # JD analysis workflow
  generation_config.yaml       # Role inference + project ranking tunables
  cv_base_template.yaml        # Per-role CV templates
  schema/project_facts_schema.yaml  # Schema for new projects
projects/                    # 19 real projects (each: facts.yaml + README.md)
Interview/                   # Interview Q&A, job descriptions, behavioral scripts
outputs/                     # Generated PDFs (gitignored)
jd_archive/                  # Archived JD text files
tests/                       # pytest test suite
```

## Critical Commands

### Setup
```bash
pip install -r requirements.txt
```

### Validate KB (run after ANY facts.yaml edit)
```bash
python app/backend/validate.py
```

### Generate CV
```bash
python generate.py cv --role android
python generate.py cv --role auto --jd-file jd.txt --company "Acme"
python generate.py cv --role backend --output outputs/my_cv.pdf
python generate.py cv --role android --with-zh          # + Chinese version
python generate.py cv --role android --gen-md outputs/CV.md  # editable MD
python generate.py cv --from-md outputs/CV.md --output outputs/CV.pdf  # MD → PDF
```

### Generate Cover Letter
```bash
python generate.py cl --role backend --company "Acme" --jd-file jd.txt
```

### Batch / LinkedIn
```bash
python generate.py batch-cv                              # all JDs in Interview/NewJobs/
python generate.py batch-cv --input jd_archive           # custom dir
python generate.py li-jd                                 # LinkedIn saved jobs → CV
python generate.py li-jd --auto 0 --no-generate          # fetch only
```

### Multi-Agent Pipeline
```bash
python generate.py cv-best --role android --jd-file jd.txt --company "Acme" --auto-refine
```

### LLM Iteration
```bash
python generate.py cv-iterate --pdf outputs/CV.pdf --jd-file jd.txt --role android
# Requires OPENAI_API_KEY (optional OPENAI_BASE_URL, OPENAI_MODEL)
```

### Tests
```bash
pytest                    # all tests (mocks HTML→PDF automatically)
pytest -k kb              # KB validation tests only
pytest -v                 # verbose
```

## Project-Specific Conventions

### Anti-Hallucination (NON-NEGOTIABLE)
- Only use facts from `kb/*.yaml` and `projects/*/facts.yaml`.
- If required facts are missing or conflicting, ask the user — do not guess.
- Missing facts caught by `validate.py` pre-generation; generation aborts unless `--no-strict-kb`.

### Role Vocabulary (fixed)
`auto` | `android` | `ai` | `backend` | `fullstack` | `embedded`
- CLI and ranking heuristics depend on these exact strings.
- Other role names have been removed (2026-06 cleanup).

### Output Format Rules
- **All formatting rules live in `kb/rules/resume_output.md`** — Summary, Skills, Experience, Education, Publications, Cover Letter, PDF Layout, Validation Checklist. Read before any CV/CL generation.
- **Summary**: 5–6 sentences (6 when JD present, 5 when no JD). Role-dependent sentence-1 structure. Label: "Professional Summary". Max ~780 chars EN.
- **Education**: Always placed **after Experience**. Full name "Auckland University of Technology" (not "AUT").
- **Publications**: After Licenses & Certifications. IVCNZ 2025 first, IGI Global second.
- **Key Skills**: Max 6 categories, 3–5 items each. JD's most emphasized technology goes first.
- **CV font**: Inter only (Google Fonts in HTML head + `document.fonts.ready` before PDF).
- **Page limit**: 2 pages or fewer. Hard constraint.
- **Output location**: `outputs/YYYY-MM-DD/` with auto-generated filenames.
- Delete intermediate `.html` and `*_POST_CHECK.md` after generation — keep only PDFs.

### Chunxiao Two-Stage Rule (HARD CONSTRAINT)
- Chunxiao experience **must always** render as **two distinct career stages** within one employer block.
- Each stage: own title, period, bullet points, tech stack.
- Later stage (2018–2024) = JD core title. Earlier stage (2013–2018) = KB original title (shows career progression).
- Level-blocking: JD titles with `junior|graduate|intern|associate|intermediate|trainee` are NOT applied to Chunxiao stages.

### Non-Negotiable Projects
- `chatclothes` — always included for all roles.
- `smart-factory` — always included for all roles.
- `exhibition-robot` — always excluded (configurable in `kb/generation_config.yaml`).

### JD Coverage
- Target: 85% KB-supported JD keyword coverage (`--min-jd-match-pct`).
- **Soft alert, not a hard gate** — generation proceeds regardless.
- Generic words (`team`, `quickly`, `features`, `codebase`) are filtered out.

### Cover Letter Rules
- 4 paragraphs, 250–400 words total. No metrics in body. Max 1 project name referenced.
- Answer: who you are, why this role, why you fit, why interview you. NOT a resume rehash.
- Implementation: `app/backend/generate_cover_letter.py`.

## Integrations
- **JD ingestion**: `app/backend/jd_fetch.py` uses `requests` + `beautifulsoup4`. URL failures degrade to manual `--jd-keywords`.
- **PDF rendering**: Playwright Chromium required. Failures are environment/dependency issues, not KB logic.
- **LinkedIn fetch**: `app/backend/linkedin_jd_fetcher.py` uses Playwright with Chrome profile. Auto-starts managed Chrome.
- **Iterative AI loop**: `app/backend/cv_auto_review_iterate.py` — extracts PDF text via `pypdf`, calls OpenAI API, patches KB, regenerates.
- **Interview QA**: `app/backend/interview_qa_cli.py` — loads from `interview_qa/` at repo root, then `Interview/`, falls back to `kb/interview_qa/`.
- **GitHub profile README**: Root `README.md` renders on GitHub profile page. Use `ghchart.rshah.org` for contribution grid (not `github-readme-stats` widgets).

## Practical Debugging
- If generated PDF looks unchanged, check dated output folder in `outputs/YYYY-MM-DD/` or force `--output`.
- For schema-sensitive additions, mirror required fields from `kb/schema/project_facts_schema.yaml` and re-run `validate.py`.
- Tests mock `html_to_pdf` automatically via `conftest.py` — no Playwright needed for test runs.
- CI (`validate-kb.yml`) runs `validate.py` on push/PR touching `projects/**/facts.yaml` or `kb/**/*.yaml`.

## Agent Skills
- Skills are in `.opencode/skills/<skill-name>/SKILL.md`.
- If a task matches a skill, invoke it via the `skill` tool — **never implement directly** if a skill applies.
- Follow the skill instructions exactly; do not partially apply them.

### Intent → Skill Mapping
- Feature / new functionality → `spec-driven-development`, then `incremental-implementation`, `test-driven-development`
- Planning / breakdown → `planning-and-task-breakdown`
- Bug / failure / unexpected behavior → `debugging-and-error-recovery`
- Code review → `code-review-and-quality`
- Refactoring / simplification → `code-simplification`
- API or interface design → `api-and-interface-design`
- UI work → `frontend-ui-engineering`
