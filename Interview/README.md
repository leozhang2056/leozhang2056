# Interview Knowledge Base

This folder is the entry point for all interview preparation materials.

> **Source of truth**: `kb/*.yaml` and `projects/*/facts.yaml`  
> **Purpose here**: spoken practice, response frameworks, scenario dialogues, technical supplements, external references

## Directory

```
core/        Full interview workflow + job search strategy
technology/  Technical knowledge points
resource/    AUT original PDFs (kept for reference)
NewJobs/     JD archive + batch-cv pipeline working directory
```

---

## core/ — Full Interview Workflow + Job Search Strategy

### Core Files

| File | Purpose |
|---|---|
| `interview_guide.md` | **One-stop interview guide** — 48-question quick reference / STAR methodology / response templates / interview day / reverse questions |
| `career_playbook.md` | **Career & job search playbook** — job search strategy / LinkedIn / networking / elevator pitch / personal brand / NZ workplace culture / volunteering / hiring cycles / CV & cover letter guide |
| `behavioral_common_qa.md` | Full STAR oral scripts (Q1–Q45 / follow-ups / material inbox) — behavioral interview source of truth |
| `Behavioral Book.pdf` | Classic behavioral interview reference |

### Language Support
| File | Purpose |
|---|---|
| `small_talk_topics.md` | Small talk scenarios for overseas workplace & social settings |
| `IT_English.md` | IT scenario Chinese-English reference |

### Personal Fact Sheet
| File | Purpose |
|---|---|
| `personal_facts.md` | Leo Zhang's core facts — profile, education, skills, projects, achievements, certifications |

---

## resource/ — AUT Original PDFs

13 AUT official PDFs (kept for reference). Content fully integrated into `core/interview_guide.md` + `core/career_playbook.md`.

---

## kb Integration

- `kb/career/` — Career workflow methodology (9 articles)
- `kb/interview_qa/` — Structured YAML + methodology + personal oral scripts
- CLI: `python generate.py interview --category technical` or `--role android`

---

## Workflow

### When You Receive a JD
- `python generate.py match --jd-file jd.txt`
- `python generate.py cv --role auto --jd-file jd.txt`
- `python generate.py cl --role auto --company "CompanyName"`

### Interview Preparation
- `core/interview_guide.md` → Full workflow quick reference
- `core/career_playbook.md` → Job search strategy + NZ culture
- `core/behavioral_common_qa.md` → Rehearse STAR stories
- `core/small_talk_topics.md` → Warm up conversation skills
