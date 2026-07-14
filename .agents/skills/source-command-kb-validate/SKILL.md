---
name: "source-command-kb-validate"
description: "Validate knowledge base YAML files"
---

# source-command-kb-validate

Use this skill when the user asks to run the migrated source command `kb-validate`.

## Command Template

Run KB validation to check profile.yaml, skills.yaml, and all projects/facts.yaml are consistent and error-free.

```bash
python -m pytest tests/ -v -k kb
```

Or run the CLI validator:
```bash
python app/backend/validate.py
```
