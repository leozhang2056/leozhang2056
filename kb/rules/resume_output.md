# Resume & Cover Letter Output Rules

> **Single source of truth for ALL resume/cover-letter output behavior.**
> All output formatting rules live here. Pre-generation JD analysis → `kb/rules/jd_analysis_standard.md`.
> Must be read before any CV/CL generation. Architected for both human and AI consumption.

---

## 1. Core Principles

- Use only facts from KB YAML files (`kb/*.yaml`) and project `facts.yaml` (`projects/*/facts.yaml`).
- Do not invent projects, titles, metrics, dates, team size, or scope.
- **Missing facts:** Caught by `validate.py` pre-generation; generation aborts unless `--no-strict-kb`.
- **Conflicting facts:** Must be resolved in KB YAML before generation. No runtime conflict resolution.
- Optimize for relevance to the target role, not for completeness.
- Treat each JD sentence as meaningful input: map responsibilities, must-haves, and preferred items at sentence level, not keyword-only matching.
- **JD coverage target:** `MIN_JD_MATCH_PCT = 85.0` (configurable via `--min-jd-match-pct`). Soft alert, not a hard gate — generation proceeds regardless. Use for gap awareness, not blocking.

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

---

## 3. Summary Rules

### Structure (code-aligned, role-dependent)

**Code constant:** `SUMMARY_REQUIRED_SENTENCES = 6`. Template policy: `locked_six_sentences`.
Template entries have 5 base sentences. When JD is present, code injects a target-role sentence, making 6 total.
When no JD: 5 base sentences.

**Sentence-1 content is ROLE-DEPENDENT** — per `kb/cv_base_template.yaml` `roles.<role>.summary_sentences.en[0]`:

| Role | Sentence 1 | Notes |
|------|-----------|-------|
| `backend` | **Degree:** `Master's in Computer and Information Sciences from AUT, First Class Honours.` | Education opens; role positioning follows |
| `ai` | **Degree:** `Master of Computer and Information Sciences (First Class Honours) from AUT.` | Education opens; narrative follows |
| `fullstack` | **Degree:** `Master of Computer and Information Sciences (First Class Honours) from AUT.` | Education opens; role positioning follows |
| `embedded` | **Degree:** `Master's in Computer and Information Sciences from AUT, First Class Honours.` | Education opens; domain expertise follows |
| `android` | **Identity:** `Senior Android Architect with 10+ years building large-scale Android platforms...` | Identity opens; Education closes (sentence 5) |

**Rule:** For backend/ai/fullstack/embedded, degree opens sentence 1. For android, identity opens and degree closes.
Do not override the template sentence order. Do not place AUT/honours in sentence 1 for android.

### Summary semantics (when JD is present)
1. **Sentence 1**: Role-dependent per table above.
2. **JD injection**: Target-role positioning injected when JD provided. Maps to JD title/domain.
3. **Proven delivery**: One flagship outcome narrative (scenario + role). No numeric metrics for Android.
4. **Additional expertise**: Skills/methods that differentiate.
5. **Role-dependent close**: Education for android; narrative/persona for other roles.
6. **JD sentence (when present)**: May shift education or add positioning.

### Highlights & bold
- Summary is for **competitive differentiators**, not baseline facts every candidate shares.
- **Do not put in Summary:** location / city (`Auckland`), work rights / visa, generic filler (`Agile`, `code review`, `team player`, `communication skills`) — unless tied to a specific evidenced outcome.
- **JD sentence-1 bold (DISABLED):** `_apply_jd_sentence1_alignment()` returns text unchanged. JD keyword injection into sentence 1 is disabled by architectural decision. JD alignment happens via Skills section ordering and Experience bullet selection, not sentence-1 injection.
- **Strategic bold:** `_apply_summary_highlight_bold()` applies role-specific term bolding, max ~6 bold spans per Summary. Do NOT bold location, work rights, or filler.
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
- Target 5–6 printed lines. Code enforces `SUMMARY_MAX_CHARS_EN = 780` / `SUMMARY_MAX_CHARS_ZH = 520`.
- Must end with complete sentence — no truncation. One paragraph only.

---

## 4. Key Skills Rules

<!-- EVOLVE: 2026-07-01 | source: session | issue: Skills section had 8 categories with 40+ items, user asked to trim -->
### Category count (HARD CONSTRAINT)
- **Maximum 6 categories.** Too many categories dilute focus and look like keyword stuffing.
- Each category: 3–5 items max. If a category exceeds 5, split or trim.
- **No buzzword categories.** Do not create categories for vague concepts ("Architecture & Practices", "CMS & Content"). Every category must map to a concrete technology group.

### Labels & formatting
- Do not show implementation labels like `JD Match`.
- Use `Android` label (not `Android Development`) for Android row.
- Prefer visually balanced one-line skill rows; avoid excessive line wrap.

### JD-driven ordering (from jd_analysis_standard)
- **JD's most emphasized technology goes in the first category, first position.**
- Technologies not mentioned in JD go to the end of their category or are removed.
- Each category: 3–5 items max. If a category exceeds 5, split or trim.
- Code enforces via `_ROLE_SKILL_CONFIG` and JD keyword prioritization.

### AI-Assisted Development tools (fixed list)
```
Cursor, GitHub Copilot, Claude Code, Antigravity, OpenCode
```

### Role-specific skill configuration
- **Fullstack:** Filter out `IIS`, `Windows Server`, `*Administration*` phrasing. Keep `Databases` comprehensive (`MySQL, Redis, MongoDB, SQL Server, SQLite`). Split `AI / ML` + `AI-Assisted Development` as two separate rows. Apply minimal text shortening to prevent wraps.
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
- Chunxiao experience **must always** render as **two distinct career stages** within one employer block.
  Implemented via `_render_career_progression_html()` reading `kb/experience/work.yaml` `career_progression`.
- Each stage: own title, period, bullet points, and tech stack.
- Never merge the 10-year span into a single undifferentiated role.

### JD title adaptation
- Employer role titles in Chunxiao stages adapt via `_adapt_progression_title()`:
  - **Android role:** Maps to mobile-focused titles (e.g., "Full-stack Engineer" → "Senior Mobile Engineer")
  - **Other roles + JD:** Two-stage title gradient enforced (HARD CONSTRAINT — see below)
  - AUT "AI Research Engineer" title is invariant across all roles
- **CV header/target-role line:** Shows the full JD-extracted target role title.
- **Professional Summary:** Positioning incorporates target role domain keywords, not literal JD title.

### Chunxiao title gradient (HARD CONSTRAINT)
Chunxiao's two career stages MUST show plausible career progression — never the same title for both.

- **Later stage (2018-2024):** JD core title (via `_extract_core_jd_title()`). Represents the target role.
- **Earlier stage (2013-2018):** KB original title retained — shows growth from specialist (e.g., "Senior Android Engineer") to the JD's role (e.g., "Senior Software Engineer"). Only downgrades to a derived title if KB original has zero overlap with JD domain (e.g., KB says "Accountant" but JD is "Software Engineer").
- **Level-blocking:** JD titles containing `junior|graduate|intern|associate|intermediate|trainee` are NOT applied to Chunxiao stages — the KB original titles show genuine career progression, not a mismatched junior label on 10-year experience.

`_extract_core_jd_title()` splits at `&` only for known standalone role fragments (Technical Lead, Manager, Architect, Director, Principal). Domain descriptors (Operations, Integration, Automation) are preserved — "Infrastructure & Operations Engineer" stays as-is.

### JD-driven bullet selection (from jd_analysis_standard)
- **First bullet must hit JD's core requirement** (recruiter only reads the first one)
- Prioritize bullets with metrics (numbers sell)
- Prioritize end-to-end scenarios (需求 → 交付)
- Include AI-related content when relevant (ChatClothes, LLM, diffusion models)

### JD-driven bullet selection (from jd_analysis_standard)
- **First bullet must hit JD's core requirement** (recruiter only reads the first one)
- Prioritize bullets with metrics (numbers sell)
- Prioritize end-to-end scenarios (需求 → 交付)
- Include AI-related content when relevant (ChatClothes, LLM, diffusion models)
- Soft skills conveyed through actions, not standalone labels ("Good communicator")

### Bullet writing rules
- 2–4 bullets per project. Select at least 5 projects or roles.
- **Decision narrative (advisory):** Each bullet should ideally answer: constraint → decision → result.
  Not just execution output. This is a writing quality target — no automated enforcement exists.
- Start with strong action verbs. Good: `Built`, `Led`, `Developed`, `Architected`, `Optimized`, `Integrated`, `Engineered`, `Orchestrated`, `Migrated`. Weak (avoid): `Helped`, `Participated`, `Was responsible for`.
- Include metrics when available. Include impact + technology + scope.
- Each bullet focuses on one core contribution. **No duplicate bullets across projects (HARD CONSTRAINT).** <!-- EVOLVE: 2026-07-01 -->
- Bold key tech terms and metrics using `<strong>` tags.
- Bullet length: 2–3 lines max. Order by impact.

### Professional terminology (advisory — no automated scanner)
Replace beginner/amateur phrasing with senior-engineer vocabulary. These are writing guidelines:

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

- Use full name `Auckland University of Technology` (do not abbreviate to `AUT` in Education section).
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
- Single centered line: `✉ email | ☎ phone | Portfolio | LinkedIn | GitHub`.
- **No location/address in header** — user explicitly does not want it shown. <!-- EVOLVE: 2026-07-01 -->
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

### 9 Rules

<!-- EVOLVE: 2026-07-01 | source: session | issue: Rule §9.1 conflicted with code — "I am applying for..." replaced by fit hook -->
1. **Opening paragraph:** Lead with a fit hook — `{tagline}, I am drawn to {company} because {culture_reason}`. Do NOT start with "I am applying for..." or "Master of Computer...". The goal is to show you chose THIS company, not that you're mass-applying.
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

### CL-CV separation (HARD CONSTRAINT)
- **CL must NOT repeat CV content.** CV has data; CL makes them WANT to read the CV.
- **No metrics in CL body.** No "5,000 DAU", no "10+ factories", no "sub-100ms".
- **No project enumeration.** Mention at most 1 project name total, as a brief reference.
- CL focuses on: motivation, values, soft skills, culture fit, career philosophy.

<!-- EVOLVE: 2026-07-01 | source: session | issue: CL quality check had no word count rule; added validator with 200-400 range -->
### CL length (HARD CONSTRAINT)
- **250–400 words total.** Under 250 = too thin to make an impression. Over 400 = they won't read it.
- **4 paragraphs, 2–4 sentences each.** Each paragraph has a distinct purpose.
- Code enforces via `cl_quality_validator.py` (`CL_WORD_COUNT_MIN=200`, `CL_WORD_COUNT_MAX=400`).

### Soft skills emphasis (HARD CONSTRAINT)
- **Each paragraph must embed at least one soft skill** through storytelling, not listing.
- Soft skills to highlight (rotate across paragraphs):
  - Mentoring / helping junior engineers grow
  - Cross-functional communication (PM, QA, product)
  - Pragmatic decision-making (quality vs delivery tradeoffs)
  - Continuous learning / growth mindset
  - Collaborative engineering philosophy
- **Never standalone:** ❌ "I am a good communicator" → ✅ "I've learned that the best systems come from teams that communicate well before writing code."

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
| Fake skill | Claiming Angular, Firebase, or any skill not in KB (use adjacent KB skills to show transferability) |
| Default title | Hardcoding "Senior Backend Engineer" when JD says otherwise (use role-type mapping; header via `--title`) |
| Skill bloat | Filling skill rows beyond 3-5 items, causing line wrap (trim to most relevant) |
| No metrics | Bullets with zero numbers or impact data |
| Generic close | Ending with "team player" or "great communicator" (embed soft skills in hard facts) |
| 100% coverage pursuit | Chasing every JD keyword including noise words (focus on hard-skill matches) |

---

## 11. Validation Checklist

### Pre-generation (before running `generate.py cv`)
- [ ] Read the full JD — not just the keyword list (from jd_analysis_standard)
- [ ] Hard skills → KB evidence mapping table completed (from jd_analysis_standard)
- [ ] Missing items handled: no fabrication, use adjacent skills as bridge (from jd_analysis_standard)
- [ ] Company domain / culture / team size researched (company-fit analysis)
- [ ] Correct role template selected (`android`/`backend`/`fullstack`/`ai`/`embedded`)
- [ ] `python app/backend/validate.py` passes

### Post-generation (before shipping CV/CL)
- [ ] All content traceable to `kb/` or `projects/*/facts.yaml`
- [ ] JD requirements mapped at sentence level (not only keyword matching)
- [ ] Selected skills match JD; first skill row hits JD's top priority
- [ ] Selected projects support target role; first two bullets hit JD core needs
- [ ] No unsupported metrics or titles
- [ ] Summary sentence count: 6 when JD present, 5 when no JD (template + JD injection)
- [ ] Summary sentence-1 content matches role-dependent behavior: degree opens for backend/ai/fullstack/embedded; identity opens for android
- [ ] Summary ends as complete sentence; within `SUMMARY_MAX_CHARS` budget
- [ ] Summary includes at least one concrete achievement when evidence exists
- [ ] Bullets use strong action verbs; not repetitive across projects
- [ ] Timeline internally consistent (profile.yaml education, work.yaml, facts.yaml)
- [ ] Degree status matches employment rows
- [ ] Chunxiao is two distinct stages (never merged)
- [ ] JD title adaptation applied: Chunxiao employer stages show JD core title with gradient (later stage = JD title, earlier stage = KB original or downgraded — never identical)
- [ ] No edge-related terms unless JD requires them
- [ ] No internal label artifacts (`JD Match`, `Additional:`, keyword tails)
- [ ] No truncated phrases or broken clauses
- [ ] JD coverage ≥85%: if below, confirm it's a soft alert (not a gate)
- [ ] Recruiter 30-second scan: title matches + skills hit + depth stories + not template-looking

---

## 12. CLI Command Reference

### Resume generation
```bash
python generate.py cv --role android
python generate.py cv --role backend
python generate.py cv --role ai
python generate.py cv --role fullstack
python generate.py cv --role auto --jd-file jd.txt
python generate.py cv --role auto --jd-file jd.txt --company "Acme"
python generate.py cv --role android --output outputs/CV.pdf
python generate.py cv --role android --with-zh --with-review-bundle
```

### Cover letter
```bash
python generate.py cl --role backend --company "Acme" --jd-file jd.txt
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
python generate.py cv --role android --gen-md outputs/CV.md
python generate.py cv --from-md outputs/CV.md --output outputs/CV.pdf
```

### Automated second-AI iteration
```bash
python generate.py cv-iterate --pdf outputs/CV.pdf --jd-file jd.txt
```

### Post-generation
```bash
python generate.py cv --role <role> --no-post-check    # Skip post-check
python generate.py cv --role <role> --keep-html        # Keep intermediate HTML
python generate.py cv --role <role> --min-jd-match-pct 70  # Lower JD coverage threshold
```

---

## 13. Role Selection Reference

### Role inference (how `--role auto` works)
| JD characteristic | Role |
|---|---|
| Pure backend / Java-dominant | `backend` |
| Frontend + backend + AI mix | `fullstack` |
| Pure AI/ML | `ai` |
| Pure Android | `android` |
| IoT / embedded / C/C++ dominant | `embedded` |

### Role focus by type
- **Android:** Android SDK, Kotlin/Java, architecture, performance, hardware integration.
- **Backend:** Spring Cloud, microservices, APIs, databases, scalability, DevOps.
- **AI/ML:** Model training, CV/NLP, deployment, evaluation, research contributions.
- **Full-stack:** Cross-layer delivery, client + backend + deployment + integration.
- **Embedded:** IoT platforms, C/Linux, firmware, protocol implementation, device integration.

---

## 14. KB Edit Protocol

1. Before editing: understand which YAML keys control which generated output fields.
2. After any edit to `kb/*.yaml` or `projects/*/facts.yaml`: run `python app/backend/validate.py`.
3. If validation fails: fix errors before generation. Do not skip validation.
4. New projects: must follow `kb/schema/project_facts_schema.yaml`.
5. New bullets: must include `id, category, tags, variants, evidence`.
6. If missing facts: supplement KB YAML, do not guess. Generation aborts when KB validation is strict.

---

*Version: 2026-07-11 — resolved contradictions with code behavior: role-dependent sentence-1, 6 sentences (JD-injected), disabled JD sentence-1 bold, corrected JD title adaptation via _extract_core_jd_title(), merged checklists/anti-patterns from jd_analysis_standard, moved company-fit to jd_analysis_standard, documented 85% coverage as soft alert, killed MISSING_INFO/FACT_CONFLICT dead rules, marked decision-narrative and terminology bans as advisory, added role selection reference. 2026-07-11 update: added Chunxiao title gradient rules (HARD CONSTRAINT), level-blocking list (junior/graduate/intern/associate/intermediate/trainee), _extract_core_jd_title() &-split logic documented. Bugs fixed: CV font Roboto→Inter, CL --title default None for auto-JD-extract, Summary skill-strip regex cleanup, html param shadowing, & split for domain descriptors.*
