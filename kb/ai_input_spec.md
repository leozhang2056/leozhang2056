# AI Input Specification
# AI 输入规范

> Purpose: keep AI context small, factual, and deterministic.
> 目的：让 AI 输入保持精简、可追溯、低冲突。

---

## 1. Source Priority

Use sources in this order:

1. `kb/profile.yaml`
2. `kb/skills.yaml`
3. `kb/project_relations.yaml`
4. `projects/*/facts.yaml`
5. `kb/bullets/*.yaml`

Default rule:
- `facts.yaml` and `kb/*.yaml` are the only factual sources.
- Project `README.md` files are optional supporting material, not default input.
- Generated files in `outputs/` and resume samples in `templates/` are references only, not source of truth.

---

## 2. What To Send To AI

For a normal resume-generation run, send only:

1. Job description or extracted JD keywords
2. One selected summary variant from `kb/profile.yaml`
3. Targeted skills from `kb/skills.yaml`
4. Top 3-5 matched project `facts.yaml`
5. Optional reusable bullets from `kb/bullets/*.yaml`
6. Resume generation rules

Do not send by default:
- Full project `README.md`
- Image lists
- Presentation text
- Historical resume files
- Repeated copies of the same metrics or timeline

---

## 3. Recommended AI Payload Shape

Use a compact structured payload like:

```yaml
task:
  type: resume_generation
  target_role: Android Developer
  language: English

constraints:
  no_fabrication: true
  max_projects: 5
  bullet_count_per_project: 2-4
  summary_sentences: 3-4

jd:
  raw_text: |
    ...
  keywords:
    - Kotlin
    - Android SDK
    - MVVM

candidate:
  profile:
    preferred_name: Leo Zhang
    summary_variant: android_focus
  skills:
    selected:
      - Java
      - Kotlin
      - Android SDK
      - Spring Boot
  projects:
    - project_id: enterprise-messaging
      source: projects/enterprise-messaging/facts.yaml
    - project_id: smart-factory
      source: projects/smart-factory/facts.yaml
  bullets:
    - id: android_perf_01
      source: kb/bullets/android.yaml
```

---

## 4. Rules For Context Assembly

- One fact appears once in the payload.
- If two sources disagree, keep the YAML source and flag `FACT_CONFLICT`.
- If a required fact is missing, output `MISSING_INFO` instead of guessing.
- Keep each selected project focused on role, impact, metrics, tech stack, and evidence.
- Use project relations only to improve narrative ordering, not to invent missing experience.

---

## 5. Minimal Project Slice

When passing a project to AI, prefer this slice only:

```yaml
project_id:
name:
timeline:
role:
summary:
highlights:
metrics:
tech_stack:
skills_demonstrated:
related_to_roles:
keywords:
evidence:
```

Avoid passing large descriptive sections unless needed:
- `applications`
- long `research_contributions`
- exhaustive image inventories
- duplicated achievement lists

---

## 6. Separation Of Responsibilities

- `kb/ai_input_spec.md`: what data to send
- `kb/resume_generation_rules.md`: how the output should behave
- `kb/ai_prompts/resume_generation.md`: execution prompt template
- `templates/resume_generation_guide.md`: human-facing style guide and historical reference

---

## 7. Anti-Redundancy Checklist

Before sending context to AI, check:

- [ ] Is this fact already present elsewhere in the payload?
- [ ] Is this file factual source or just presentation material?
- [ ] Does this section help selection or generation?
- [ ] Can this be replaced by a shorter structured field?
- [ ] Is there any date, metric, or title conflict?

---

## 8. Preferred Failure Modes

Prefer explicit markers over hallucination:

- `MISSING_INFO`: required fact not found
- `FACT_CONFLICT`: two factual sources disagree
- `LOW_CONFIDENCE_MATCH`: project relevance is weak

These markers are better than silent guessing.

---

*Version: 2026-03-09*
