---
description: Generate CV for AI/ML roles
---

Generate a CV for AI/ML roles.

Usage: `/cv-ai --jd-file <path> --company "<name>" --title "<title>"`

```bash
python generate.py cv --role ai --jd-file <path> --company "<company>" --title "<title>" --with-quality-report --with-jd-annotated
```

##同步生成 Cover Letter (MANDATORY)

```bash
python generate.py cl --role ai --jd-file <path> --company "<company>" --title "<title>"
```

## Post-generation review (MANDATORY)

After the CV is generated, you MUST:

1. **Read** the generated HTML file from `outputs/`
2. **Read** `kb/rules/resume_output.md` for all rules
3. **Read** the quality report (`*_QUALITY.md`) if it exists
4. **Spawn a review sub-agent** to analyze the HTML against rules
5. **Apply fixes** for all HIGH and MED findings
6. **Regenerate PDF** with fixes applied
7. **Clean up** intermediate files (HTML, POST_CHECK.md, QUALITY.md)

Do NOT present the raw first draft to the user. Present the reviewed, fixed version.
