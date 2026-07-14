---
name: "source-command-cv-fullstack"
description: "Generate CV for fullstack roles"
---

# source-command-cv-fullstack

Use this skill when the user asks to run the migrated source command `cv-fullstack`.

## Command Template

Generate a CV for fullstack roles.

Usage: `/cv-fullstack --jd-file <path> --company "<name>" --title "<title>"`

```bash
python generate.py cv --role fullstack --jd-file <path> --company "<company>" --title "<title>" --with-quality-report --with-jd-annotated
```

##同步生成 Cover Letter (MANDATORY)

每次生成 CV 时，必须同步生成 CL：

```bash
python generate.py cl --role fullstack --jd-file <path> --company "<company>" --title "<title>"
```

CL 生成后按 `cover-letter.md` 技能的审阅流程执行。

## Post-generation review (MANDATORY)

After the CV is generated, you MUST:

1. **Read** the generated HTML file from `outputs/`
2. **Read** `kb/rules/resume_output.md` for all rules
3. **Read** the quality report (`*_QUALITY.md`) if it exists
4. **Spawn a review sub-agent** to analyze the HTML against rules
5. **Apply fixes** for all HIGH and MED findings
6. **Regenerate PDF** with fixes applied
7. **Clean up** intermediate files (HTML, POST_CHECK.md, QUALITY.md)

The review sub-agent should check:
- Summary: exactly 5 sentences, ≤ 100 words, correct structure
- Skills: max 6 categories, JD-driven ordering
- Bullets: constraint → decision → result, no duplicates, strong verbs
- Fluency: no phrase repeated > 3 times
- Anti-AI tone: no keyword dumps, no empty buzzwords

Do NOT present the raw first draft to the user. Present the reviewed, fixed version.
