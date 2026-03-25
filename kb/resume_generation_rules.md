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

---

## 2. Output Scope

Recommended structure:

1. Header
2. Professional Summary
3. Core Skills
4. Professional Experience
5. Education
6. Certifications or Selected Projects if needed

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
- [ ] Timeline is internally consistent
- [ ] No edge-related terms remain unless explicitly requested
- [ ] No internal label artifacts (e.g., `JD Match`) are shown

---

## 7. Notes

- Presentation style, colors, fonts, and layout belong to rendering templates, not to generation rules.
- Human-oriented historical guidance lives in `templates/resume_generation_guide.md`.
- Output behavior preference:
  - Resume generation should save outputs in `outputs/YYYY-MM-DD/`.
  - Resume generation should keep PDF outputs and remove intermediate HTML files.
  - Default outputs should include:
    - Main English CV PDF
    - JD annotated PDF (highlighted hit keywords + match score + hit/miss list)
  - Generation should apply anti-hallucination gating:
    - Filter out JD keywords unsupported by KB evidence before final rendering.

---

*Version: 2026-03-12*
