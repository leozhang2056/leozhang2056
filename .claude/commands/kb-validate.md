---
description: Validate knowledge base YAML files
---

Run KB validation to check profile.yaml, skills.yaml, and all projects/facts.yaml are consistent and error-free.

```bash
python -m pytest tests/ -v -k kb
```

Or run the CLI validator:
```bash
python app/backend/validate.py
```
