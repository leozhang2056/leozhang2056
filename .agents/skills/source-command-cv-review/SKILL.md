---
name: "source-command-cv-review"
description: "Review CV quality against best practices and KB alignment"
---

# source-command-cv-review

Use this skill when the user asks to run the migrated source command `cv-review`.

## Command Template

Analyze a generated CV PDF against the resume writing best practices guide (`kb/resume_writing_best_practices.md`) and KB data.

1. Check JD coverage: verify keyword coverage ≥ 85%
2. Check CARL structure: each bullet should show constraint → decision → result
3. Check anti-patterns: no AI腔, no keyword stuffing, no empty superlatives
4. Check data traceability: all metrics traceable to KB YAML files
5. Check consistency: Summary, Skills, Experience tell the same story

```bash
# After generating a CV, review its post-check report
cat outputs/*/CV_*_POST_CHECK.md
```

For JD annotated PDF review:
```bash
python generate.py cv --role <role> --jd-file <jd.txt> --company "<company>" --with-jd-annotated
```
