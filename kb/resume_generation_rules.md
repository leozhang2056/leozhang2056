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
- 1 page preferred
- 2 pages acceptable for senior or highly targeted roles

---

## 3. Section Rules

### Summary

- 3-4 sentences
- One paragraph
- Focus on role fit, core strengths, and domain relevance
- Do not include visa status by default
- Include dates or years only when the target output explicitly wants them

### Skills

- 5-8 lines or categories
- Order by JD relevance
- Prefer grouped skills over long raw lists
- Remove weakly relevant or distracting skills

### Experience

- Select 3-5 projects or roles
- Use 2-4 bullets per item
- Start bullets with strong action verbs
- Include metrics when available
- Prefer impact + technology + scope in each bullet

### Education

- Keep concise
- Include thesis or honors only if helpful for the target role

---

## 4. Writing Rules

- Use concise, direct, active voice
- Prefer `Built`, `Led`, `Developed`, `Architected`, `Optimized`, `Integrated`
- Avoid `Helped`, `Participated`, `Was responsible for`
- Naturally embed technologies in achievements
- Keep each bullet focused on one core contribution
- Prefer concrete impact over generic responsibility

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

---

## 6. Validation Checklist

- [ ] All content is traceable to KB or `facts.yaml`
- [ ] Selected skills match the JD
- [ ] Selected projects support the target role
- [ ] No unsupported metrics or titles were added
- [ ] Summary is short and targeted
- [ ] Bullets use strong verbs
- [ ] Timeline is internally consistent

---

## 7. Notes

- Presentation style, colors, fonts, and layout belong to rendering templates, not to generation rules.
- Human-oriented historical guidance lives in `templates/resume_generation_guide.md`.

---

*Version: 2026-03-09*
