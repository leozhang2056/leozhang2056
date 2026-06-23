# Resume & Cover Letter Output Rules

> **Single source of truth for ALL resume/cover-letter output behavior.**
> This file replaces: `kb/resume_generation_rules.md`, `.cursor/rules/resume-generation-standards.mdc`, `kb/ai_prompts/resume_generation.md`, `kb/ai_input_spec.md`.
> Must be read before any CV/CL generation. Architected for both human and AI consumption.

---

## 1. Core Principles

- Use only facts from KB YAML files (`kb/*.yaml`) and project `facts.yaml` (`projects/*/facts.yaml`).
- Do not invent projects, titles, metrics, dates, team size, or scope.
- If a required fact is missing, return `MISSING_INFO` — do not guess.
- If two factual sources disagree, return `FACT_CONFLICT` — do not pick one silently.
- Optimize for relevance to the target role, not for completeness.
- Treat each JD sentence as meaningful input: map responsibilities, must-haves, and preferred items at sentence level, not keyword-only matching.

---

## 2. Source Priority & Context Assembly

### Input source order (what to feed the generator)
1. `kb/profile.yaml`
2. `kb/skills.yaml`
3. `kb/project_relations.yaml`
4. `projects/*/facts.yaml`
5. `kb/bullets/*.yaml`

### What NOT to send by default
- Full project `README.md` files (optional supporting material only)
- Generated files in `outputs/` and resume samples in `templates/` (reference, not truth source)
- Historical variant intents (presentation material, not factual data)

### Anti-redundancy checklist
- One fact appears once in the payload.
- Is this fact already present elsewhere in the payload? → Remove duplicate.
- Is this file factual source or just presentation material? → Skip presentation material.
- Does this section help selection or generation? → If not, remove.
- Can this be replaced by a shorter structured field? → Prefer shorter.

### Failure mode markers
- `MISSING_INFO`: required fact not found
- `FACT_CONFLICT`: two factual sources disagree
- `LOW_CONFIDENCE_MATCH`: project relevance is weak

---

## 3. Summary Rules

### Five-sentence structure (hard constraint)
Every EN/ZH Summary must be **exactly five sentences** (one paragraph). Sentence order:

1. **Identity + tenure + core stack** — aligned to role/JD. When JD is provided, KB-supported JD terms (languages, frameworks, Agile/Scrum if in JD) must appear in sentence 1 and be **bolded** (max ~3 terms).
2. **Positioning** — what type of engineer you are, what problem domains you specialise in (2–3 domains). Capabilities, not tool dumps.
3. **Proven delivery** — one flagship outcome narrative (scenario + role). No numeric metrics for Android role; other roles may use KB-backed metrics when concise.
4. **Additional expertise** — for Android: AI-assisted tools + hard Android strengths (Kotlin/Java, SDK, NDK, OEM fragmentation) in one sentence. Cursor/Copilot/Claude enumeration goes in Key Skills, not here.
5. **Education close** — `Master's in Computer and Information Sciences from AUT, First Class Honours.` No graduation month/year in Summary. Full school name in Education section.

**Do not:** prepend a sixth hook sentence, place AUT/honours in sentence 1. Education always closes, never opens.

### Highlights & bold
- Summary is for **competitive differentiators**, not baseline facts every candidate shares.
- **Do not put in Summary:** location / city (`Auckland`), work rights / visa, generic filler (`Agile`, `code review`, `team player`, `communication skills`) — unless tied to a specific evidenced outcome.
- **JD sentence-1 bold:** KB-supported JD keywords woven into sentence 1, bolded there first (max ~3).
- **Strategic bold:** max ~6 bold spans total per Summary. Do NOT bold location, work rights, or filler.
- Integrate highlights naturally into prose — no explicit `Highlights:` label.
- Do not append mechanical keyword tails (`Additional role alignment: ...`).

### Anti-"AI resume" tone
- No keyword comma-lists in Summary: "Highly skilled in Java, Kotlin, Python..." — banned.
- No empty buzzwords: "passionate", "world-class", "robust", "leverage" — banned.
- At most one short sentence with a few concrete tools/terms. Put most JD fit in bullets and Key Skills.

### Edge / 边缘 terms
- Remove `edge AI`, `edge deployment`, `边缘部署`, `边缘计算`, `端侧` unless JD explicitly requires them.
- Describe same work with: `on-device`, `Raspberry Pi`, `offline-capable`, `local deployment`, `ARM-class hardware`.

### Summary length
- 5–6 printed lines (five sentences). Must end with complete sentence — no truncation.
- One paragraph only.

---

## 4. Key Skills Rules

### Labels & formatting
- Do not show implementation labels like `JD Match`.
- Use `Android` label (not `Android Development`) for Android row.
- Prefer visually balanced one-line skill rows; avoid excessive line wrap.

### AI-Assisted Development tools (fixed list)
```
Cursor, GitHub Copilot, Claude Code, Antigravity, OpenCode
```

### Role-specific skill configuration
- **Fullstack:** Filter out `IIS`, `Windows Server`, `*Administration*` phrasing. Keep `Databases` comprehensive (`MySQL, Redis, MongoDB, SQL Server, SQLite`). Split `AI / ML` + `AI-Assisted Development` as two separate rows. Apply minimal text shortening to prevent wraps (`CI/CD Pipeline Design` → `CI/CD`, `LLM Fine-tuning` → `LLM FT`).
- **All roles:** Allow `Reverse Engineering` and `.NET` when layout permits. 5–8 lines or categories. Order by JD relevance. Keep practical hard-skill focus.

---

## 5. Experience / Project Rules

### Always-keep projects
- `chatclothes` — non-negotiable for all roles.
- `smart-factory` — non-negotiable for all roles.
- Android target: also prioritize `forest-patrol-inspection` (offline map/GIS relevance).

### Ordering
- **Recency first:** Newest entries first. AUT ChatClothes before older Chunxiao employer group.
- **Android role:** Pin `chatclothes` first, then `forest-patrol-inspection`, `enterprise-messaging`, `iot-solutions`, `smart-factory`.
- **Chunxiao sub-projects:** Internal sort by timeline end date descending.

### Chunxiao two-stage rule (HARD CONSTRAINT)
- Chunxiao experience **must always** render as **two distinct career stages** within one employer block:
  - Stage 1: Full-stack Engineer
  - Stage 2: Senior Android Engineer
- Each stage: own title, period, bullet points, and tech stack from `kb/experience/work.yaml`.
- Never merge the 10-year span into a single undifferentiated role.
- Merged single-block rendering path is **deprecated for all target roles**.

### JD title adaptation rule (HARD CONSTRAINT)
- When JD file is provided, CV titles must adapt to JD:
  - **Experience section:** Employer role title reflects JD's actual job title.
  - **Professional Summary:** Positioning sentence incorporates target role and domain keywords.
- Hardcoded generic titles (`Senior Backend Engineer`, `Senior Full-Stack Engineer`) must NOT appear when JD specifies a different title.

### Bullet writing rules
- 2–4 bullets per project. Select at least 5 projects or roles.
- **Decision narrative:** Each bullet answers: constraint → decision → result. Not just execution output.
- Start with strong action verbs. Good: `Built`, `Led`, `Developed`, `Architected`, `Optimized`, `Integrated`, `Engineered`, `Orchestrated`, `Migrated`. Weak (avoid): `Helped`, `Participated`, `Was responsible for`.
- Include metrics when available. Include impact + technology + scope.
- Each bullet focuses on one core contribution. Avoid repetitive patterns across projects.
- Bold key tech terms and metrics using `<strong>` tags.
- Soft skills conveyed through actions, not standalone buzzwords.
- Bullet length: 2–3 lines max. Order by impact.

### Professional terminology (hard constraint)
Replace beginner/amateur phrasing with senior-engineer vocabulary. The following are **banned** in output:

| Forbidden | Required Replacement |
|---|---|
| `cleaned up` | `optimized` / `refactored` |
| `built ... with automatic upload` | `engineered ... with automated reporting` |
| `backup channel` | `failover channel` / `redundant path` |
| `keep-alive` | `connection persistence` / `session maintenance` |
| `implemented` (distribution/deployment) | `orchestrated` / `managed` |

### Anti-repetition
- Vary verbs naturally (avoid repeated `Built` chains).
- Each project highlights a distinct challenge/outcome.
- Do not repeat the same headline metrics across multiple bullets.

---

## 6. Education Rules

- Use full name `Auckland University of Technology` (do not abbreviate to `AUT`).
- **Placement:** After Experience, before Licenses & Certifications.
- Reduce awkward line breaks in institution rendering.
- **Timeline lockstep:** If `profile.yaml` marks degree **Completed** with concrete `end_date`, Summary and `work.yaml` must not describe "Master's student" or "graduating Feb 2026". Treat conflicting YAML as a KB fix before shipping.
- Include thesis or honours only if helpful for target role.

---

## 7. Publications Rules

- Always render Publications section when `kb/achievements.yaml` has entries.
- **Placement:** After Licenses & Certifications (final substantive section).
- **Default order:** IVCNZ 2025 first (`ChatClothes: Conversational Virtual Try-On with Diffusion Models`), IGI Global second (`Clothes Recognition Based on Lightweight Deep Learning Models`, under review).
- Render title as clickable when DOI/URL exists. Show explicit `Link:` text when available.
- Sync both: `kb/achievements.yaml` (`publications`) AND `projects/chatclothes/facts.yaml` (`evidence` with `type: publication`).
- **GitHub profile README:** Mirror publication changes to root `README.md` `## 📄 Publications`.

---

## 8. Header & PDF Layout Rules

### Typography (hard constraint)
- CV font is **Inter only**. Do not switch to Times New Roman, Aptos, Georgia, or others.
- Load via Google Fonts in HTML `<head>`. Apply `font-family: Inter, 'Segoe UI', system-ui, -apple-system, sans-serif` on body, `.cv-name`, `.section-title`.
- PDF render must wait for webfonts: `document.fonts.ready`.

### Contact row
- Single centered line: `✉ email | ☎ phone | 📍 location | LinkedIn | GitHub`.
- Location text from `kb/profile.yaml` → `personal_info.contact.location` (EN: `Auckland,NZ`).
- LinkedIn / GitHub: brand SVG + visible labels `LinkedIn` / `GitHub`. No full URLs — `href` only.

### Page layout
- **Hard limit:** 2 pages or fewer. Do not generate/ship beyond 2 pages.
- **Page breaks:** Use `page-break-inside: auto` / `break-inside: auto` on `.job-employer` and `.sub-project` blocks so multi-project blocks may continue mid-section across pages. Standalone single `.job` cards may keep `page-break-inside: avoid`.
- **Target:** End on full page count (2 pages) with minimal trailing whitespace.

### Canonical section order (do not reorder)
1. Header (name + contact row)
2. Summary
3. Key Skills
4. Experience
5. Education (between Experience and Licenses)
6. Licenses & Certifications
7. Publications (when present in achievements.yaml)
8. Interests (optional; last; only if `include_interests_in_cv` is true and interests non-empty)

### Output artifacts
- Save under `outputs/YYYY-MM-DD/`.
- Generate PDF only. Delete intermediate `.html` after successful generation (keep with `--keep-html` flag).
- Delete `*_POST_CHECK.md` after generation. Keep only PDFs.
- Include company tag in output filename when provided.

### Post-generation check
- After every CV PDF generation, run post-check and output `*_POST_CHECK.md`.
- Must include two qualitative sections: **Recruiter Review (Screening Lens)** and **Interviewer Review (Technical Lens)**.

---

## 9. Cover Letter Rules

### 9 Rules (from GPT version analysis, adopted as permanent convention)

1. **First sentence:** `"I am applying for the {title} at {company}."` — no hooks, no filler.
2. **Topic sentences:** Each paragraph starts with a clear topic sentence.
3. **One-sentence background:** Use profile tagline from `profile.yaml`.
4. **Specific names + tech:** Use specific project names (ChatClothes) and concrete terms (diffusion models, CI/CD), not vague abstractions.
5. **Evidence → role:** Every piece of evidence links back to role requirements — not just "I did X" but "X maps to what this role needs".
6. **Soft skills embedded:** In hard facts: `"10 years... developed a practical engineering mindset focused on reliability..."`. Never standalone "I'm hardworking".
7. **No repetition across paragraphs:** Each paragraph covers a distinct dimension.
8. **Specific team:** Closing names the specific team (use `_COMPANY_TEAMS` dict).
9. **Length:** 4 paragraphs, 2–4 sentences each. Fits one A4 page.

### Structure
- Para 1: Opening — "I am applying for..." + background + culture connection.
- Para 2: Evidence — project/thesis + differentiator.
- Para 3: Experience — what attracted me to the role + years + mindset.
- Para 4: Closing — motivation + specific team + thank you.

### Company data
- `_COMPANY_CULTURE_HOOKS`: lowercase phrases for "because" clauses.
- `_COMPANY_TEAMS`: specific team names for closing.
- Company-specific hand-crafted versions take priority (early-return pattern in `build_cover_letter_content()`).

### Anti-patterns
- AI-blog phrasing: "runnable, measurable, iteratively improved" → instead: "I build AI systems that actually ship".
- Keyword dumping: "I noticed this role emphasizes solutions, APIs..." → instead: connect naturally.
- Identity crisis: telling vs showing credentials.

---

## 10. Narrative Writing Principles

> You are not selling skills. You are selling future value. In the age of AI resumes, differentiation comes from clear thinking, structured personal narrative, and verifiable decision-making ability.

### Summary narrative
- Sentence 1: Degree (invariant).
- Sentence 2: **Positioning** — what type of engineer you are, what problems you naturally solve.
- Sentence 3: **Narrative** — what you learned, why that matters more than tools.
- Sentence 4: **Method** — what you care about, your engineering philosophy.
- Avoid: tool lists, keyword dumps, AI腔 (leverage/robust/passionate/world-class).

### Experience narrative
- Each bullet answers: **constraint → decision → result**.
- Avoid: tool-only lists, responsibility-only descriptions.

### Persona by role
- Backend: "builds systems that work under real constraints".
- Android: "builds mobile systems that work at scale".
- Fullstack: "works across the entire delivery chain".
- AI: "builds systems that actually ship".

### Anti-pattern catalog
| Pattern | Example (forbidden) |
|---|---|
| Keyword dump | `"Highly skilled in Java, Kotlin, Python, C++, Go, Rust..."` |
| Empty buzzwords | `"Passionate about building world-class products"` |
| Tool list as content | `"Tech stack: React, Node.js, PostgreSQL, Redis, Docker..."` |
| AI腔 | `"Leveraged cutting-edge technologies to drive innovation"` |
| Beginner vocabulary | `cleaned up`, `automatic upload`, `backup channel`, `keep-alive` |

---

## 11. Validation Checklist

Before shipping any CV/CL, verify:

- [ ] All content traceable to `kb/` or `projects/*/facts.yaml`
- [ ] JD requirements mapped at sentence level (not only keyword matching)
- [ ] Selected skills match the JD
- [ ] Selected projects support the target role
- [ ] No unsupported metrics or titles
- [ ] Summary is targeted, 5 sentences, ends as complete sentence
- [ ] Summary includes at least one concrete achievement when evidence exists
- [ ] Bullets use strong action verbs
- [ ] Bullets are not repetitive across projects
- [ ] Timeline internally consistent (`profile.yaml` education, `work.yaml`, `facts.yaml`)
- [ ] Degree status matches employment rows
- [ ] Chunxiao is two distinct stages (never merged)
- [ ] JD title adaptation applied (when JD provided)
- [ ] No edge-related terms unless JD requires them
- [ ] No internal label artifacts (`JD Match`)
- [ ] No truncated phrases or broken clauses
- [ ] After KB data edits: `python app/backend/validate.py` passes

---

## 12. CLI Command Reference

### Resume generation
```bash
python generate.py cv --role android
python generate.py cv --role backend
python generate.py cv --role ai
python generate.py cv --role fullstack
python generate.py cv --role auto --jd-file jd.txt
python generate.py cv --role android --output outputs/CV_Leo_Zhang_android_latest.pdf
python generate.py cv --role android --with-zh --with-review-bundle
```

### Cover letter
```bash
python generate.py cl --role backend --company "Acme"
```

### Email
```bash
python generate.py email --role fullstack --company "Acme"
```

### Batch CV + JD matching
```bash
python generate.py batch-cv
python generate.py match --role auto --jd-file jd.txt
```

### LinkedIn saved jobs
```bash
python generate.py li-jd
python generate.py li-jd --auto 0 --no-generate
```

### Interview QA
```bash
python generate.py interview --category technical
```

### Validation & testing
```bash
python app/backend/validate.py
pytest
```

### Editable CV workflow
```bash
python generate.py cv --role android --gen-md outputs/CV.md    # Generate editable MD
python generate.py cv --from-md outputs/CV.md --output outputs/CV.pdf  # MD → PDF
```

### Automated second-AI iteration
```bash
python generate.py cv-iterate --pdf outputs/CV.pdf --jd-file jd.txt
```

### Post-generation
```bash
python generate.py cv --role <role> --no-post-check    # Skip post-check
python generate.py cv --role <role> --keep-html        # Keep intermediate HTML
```

---

## 13. Company-Fit & Role Targeting

### Before generating, gather
- Company business domain and product type
- Tech stack signals
- Culture / values
- Team model and risk profile

### Banking / financial / payment roles
Prefer wording around:
- Reliability and operational stability
- Testing discipline and secure engineering
- Cloud/infra ownership and production change support
- Cross-functional Agile delivery

### Developer roles (general)
- Emphasize: fast execution / quick iteration, strong self-management / ownership.
- De-emphasize people-management wording.
- Avoid squad-leadership framing in Summary unless JD requires it.

### Role focus by type
- **Android:** Android SDK, Kotlin/Java, architecture, performance, hardware integration.
- **Backend:** Spring Cloud, microservices, APIs, databases, scalability, DevOps.
- **AI/ML:** Model training, CV/NLP, deployment, evaluation, research contributions.
- **Full-stack:** Cross-layer delivery, client + backend + deployment + integration.

### Role auto-selection
- Infer role from JD/title: `android` / `backend` / `ai` / `fullstack`.
- If JD page is noisy (login pages, browser labels, share forms), prefer title/manual keywords over extracted content.

---

## 14. KB Edit Protocol

1. Before editing: understand which YAML keys control which generated output fields.
2. After any edit to `kb/*.yaml` or `projects/*/facts.yaml`: run `python app/backend/validate.py`.
3. If validation fails: fix errors before generation. Do not skip validation.
4. New projects: must follow `kb/schema/project_facts_schema.yaml`.
5. New bullets: must include `id, category, tags, variants, evidence`.
6. If missing facts: output `MISSING_INFO`, prompt user to supplement, do not guess.

---

*Version: 2026-06-17 — consolidated from kb/resume_generation_rules.md, .cursor/rules/resume-generation-standards.mdc, kb/ai_prompts/resume_generation.md, kb/ai_input_spec.md, AGENTS.md*
