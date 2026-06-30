---
description: Generate cover letter PDF
---

`python generate.py cl --role <role> --jd-file <path> --company "<name>" --title "<title>"`

## Post-generation review (MANDATORY)

After the CL is generated, you MUST:

1. **Read** the generated HTML file from `outputs/`
2. **Read** `kb/rules/resume_output.md` §9 (CL rules) for all rules
3. **Spawn a review sub-agent** to analyze the HTML against CL rules
4. **Apply fixes** for all HIGH and MED findings
5. **Regenerate PDF** with fixes applied
6. **Clean up** intermediate files (HTML)

CL-specific review checks:
- No CV content repeated (no metrics, no project enumeration)
- Each paragraph embeds ≥ 1 soft skill through storytelling
- Personal values/philosophy present
- Company culture referenced
- Max 1 project name total
- 4 paragraphs, 2–4 sentences each

Do NOT present the raw first draft to the user. Present the reviewed, fixed version.
