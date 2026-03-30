# Career KB Resume Generation Rules
# 简历生成规则

> This file defines output behavior only.
> AI input assembly is defined in `kb/ai_input_spec.md`.

---

## 1. Core Principles

- Use only facts from KB YAML files and project `facts.yaml`.
- Do not invent projects, titles, metrics, dates, team size, or scope.
- If a required fact is missing, return `MISSING_INFO`.
- If two factual sources disagree, return `FACT_CONFLICT`.
- Optimize for relevance to the target role, not for completeness.
- Treat each JD sentence as meaningful input: map responsibilities, must-haves, and preferred items at sentence level, not keyword-only matching.

---

## 2. Output Scope

Recommended structure:

1. Header  
2. Professional Summary  
3. Core Skills (= **Key Skills** in `generate_cv_from_kb` HTML)  
4. Professional Experience  
5. **Education** — in the KB HTML renderer, this block is **after Experience and before Licenses** (not at top after Summary).  
6. Licenses & Certifications  

> Canonical order in code: `generate_html_from_kb()` → Summary → Key Skills → Experience → Education → Licenses & Certifications. See also `.cursor/rules/resume-generation-standards.mdc` § CV HTML section order.

Default length:
- ~2 pages preferred for this profile
- 1 page acceptable only when explicitly requested

---

## 3. Section Rules

### Summary

- 5-6 lines preferred (concise but high-impact)
- One paragraph
- Focus on role fit, core strengths, and domain relevance
- Include at least one concrete, evidence-backed achievement when possible (prefer quantified impact)
- Avoid JD **关键词整段罗列**（易被判定为模板/AI 腔）；用 1 句自然话融入少量具体技术词即可，更多匹配放在 Experience bullet
- 少用空泛套话（如 endless “leverage / robust / passionate / world-class”）；有数据写数据，无数据写可验证的工程行为（测试、评审、发布、监控）
- 参考：`kb/resume_writing_best_practices.md`
- Do not include visa status by default
- Include dates or years only when the target output explicitly wants them
- Must end with a complete sentence (no truncation artifacts)
- Integrate matching highlights naturally into prose (do not add `Highlights:` label)
- Do not append mechanical keyword tails such as `Additional role alignment: ...` in final candidate-facing PDF.
- For developer roles, emphasize:
  - fast execution / quick iteration
  - strong self-management / ownership
- Remove edge-related wording unless explicitly required by target JD:
  - `edge AI`, `edge deployment`, `边缘部署`, `边缘计算`, `端侧`

### Skills

- 5-8 lines or categories
- Order by JD relevance
- Prefer grouped skills over long raw lists
- Remove weakly relevant or distracting skills
- Keep a practical hard-skill focus; optionally keep one compact soft-skill line only when role requires collaboration/mentoring
- Do not show implementation labels like `JD Match`
- For Android CV, use label `Android` (not `Android Development`)
- AI-assisted development tools should default to:
  - Cursor, GitHub Copilot, Claude Code, Antigravity, OpenCode
- Keep rows visually balanced; avoid excessive wrap when possible
- Include relevant practical skills such as `Reverse Engineering` and `.NET` when role-fit allows

### Experience

- Select at least 5 projects or roles
- Use 2-4 bullets per item
- Start bullets with strong action verbs
- Include metrics when available
- Prefer impact + technology + scope in each bullet
- Avoid repetitive bullets across projects; each project should highlight a distinct challenge/outcome
- Prefer concise bullet lines over long paragraph blocks for ATS readability
- No truncated sentences in project overview or bullets (e.g., `Designed and de.`); fix before output.
- Prefer role-relevant project evidence over broad technology listing; for finance/payment roles, prioritize reliability, testing, security, production support, and change safety language.
- Always keep key projects:
  - `chatclothes`
  - `smart-factory`
- For Android-targeted resumes, prioritize:
  - `forest-patrol-inspection` (offline map/GIS relevance)
- For developer roles, de-emphasize people-management wording

### Education

- Keep concise
- Include thesis or honors only if helpful for the target role
- Use full name `Auckland University of Technology` (do not abbreviate to `AUT`)
- Reduce awkward line breaks in institution rendering where possible
- **Narrative lockstep**: if `profile.yaml` marks the degree **Completed** with a concrete `end_date`, Summary and `experience/work.yaml` must not still describe “Master’s student”, “graduating Feb 2026”, or Chinese “硕士在读 / 2026年2月毕业”. Treat conflicting YAML as a KB fix before shipping a CV. (Full guardrails: `kb/ai_prompts/resume_generation.md` Section 8.)

---

## 4. Writing Rules

- Use concise, direct, active voice
- Prefer `Built`, `Led`, `Developed`, `Architected`, `Optimized`, `Integrated`
- Avoid `Helped`, `Participated`, `Was responsible for`
- Naturally embed technologies in achievements
- Keep each bullet focused on one core contribution
- Prefer concrete impact over generic responsibility
- Keep formatting ATS-friendly: simple section labels, no decorative symbols in content blocks, no dense text walls

Good:
- `Built Spring Boot microservices supporting 5+ factory sites with 99.9% uptime.`

Weak:
- `Responsible for backend development and system maintenance.`

---

## 5. Role Focus

Adjust emphasis by target role:

- Android: Android SDK, Kotlin/Java, architecture, performance, hardware integration
- Backend: Spring Boot, microservices, APIs, databases, scalability, DevOps
- AI/ML: model training, CV/NLP, deployment, evaluation, research contributions
- Full-stack: delivery across client, backend, deployment, and integration

Do not force unrelated strengths into every version.

Company-fit emphasis:
- Before final generation, gather company context (domain, product type, values/culture, team model, risk profile).
- For banking/financial/payment roles, prefer wording around:
  - reliability and operational stability
  - testing discipline and secure engineering
  - cloud/infra ownership and production change support
  - cross-functional Agile delivery
- Keep tone practical and evidence-led; avoid generic motivational wording.

Role auto-selection guidance:
- Infer role from JD/title when role is not explicitly forced:
  - `android` / `backend` / `ai` / `fullstack`
- If JD page content is noisy (login pages, browser labels, share forms), avoid over-trusting extracted keywords and prefer title/manual keywords.

---

## 6. Validation Checklist

- [ ] All content is traceable to KB or `facts.yaml`
- [ ] JD requirements are mapped at sentence level where possible (not only keyword matching)
- [ ] Selected skills match the JD
- [ ] Selected projects support the target role
- [ ] No unsupported metrics or titles were added
- [ ] Summary is targeted, 5-6 lines, and ends as a complete sentence
- [ ] Summary includes at least one concrete achievement when evidence exists
- [ ] Bullets use strong verbs
- [ ] Bullets are not repetitive across projects
- [ ] Timeline is internally consistent (`profile.yaml` education, `experience/work.yaml`, `projects/*/facts.yaml`)
- [ ] Degree status matches employment rows (e.g. no AUT/thesis row `current: true` past completed `end_date`)
- [ ] Android-target Summary has no generic “Seeking … roles” closer unless explicitly requested
- [ ] Facts come from the resume KB payload, not stale copy in `kb/interview_qa/*` when those conflict
- [ ] No edge-related terms remain unless explicitly requested
- [ ] No internal label artifacts (e.g., `JD Match`) are shown

---

## 7. Notes

- **Header contact (HTML/PDF):** single centered row — email, phone, map-pin icon + location (`Auckland,NZ`-style from `profile.yaml`), then LinkedIn and GitHub as icon + label links without visible URLs; implementation and CSS live in `app/backend/generate_cv_from_kb.py`.
- Presentation style, colors, fonts, and layout belong to rendering templates, not to generation rules.
- Human-oriented historical guidance lives in `templates/resume_generation_guide.md`.
- Output behavior preference:
  - Resume generation should save outputs in `outputs/YYYY-MM-DD/`.
  - Resume generation should keep PDF outputs and remove intermediate HTML files.
  - Default outputs should include:
    - Main English CV PDF
  - Optional output (explicit flag): JD annotated PDF (highlighted hit keywords + match score + hit/miss list).
  - Do not generate or retain `.md` sidecar files by default.
  - Optional companion file for second-AI review: `*_AI_REVIEW_BUNDLE.md` only when explicitly enabled via `--with-review-bundle`.
  - **Automated second-AI loop** (OpenAI-compatible API): `python generate.py cv-iterate --pdf ... --jd-file ...` extracts PDF text + JD, calls the model for strict JSON edits, backs up YAML under `outputs/.../kb_backup_auto_*`, patches `kb/profile.yaml` / `projects/*/facts.yaml`, then regenerates a new CV PDF. Requires `OPENAI_API_KEY` and `pypdf`. Scanned/image-only PDFs may yield empty text.
  - JD keyword coverage control (default): aim for **≥85%** coverage on **KB-supported** JD keywords; the generator may append a short Summary tail listing any still-missing supported terms (no unsupported JD terms).
  - Generation should apply anti-hallucination gating:
    - Filter out JD keywords unsupported by KB evidence before final rendering.

---

*Version: 2026-03-30*
