---
name: "source-command-run-tests"
description: "Run full test suite"
---

# source-command-run-tests

Use this skill when the user asks to run the migrated source command `run-tests`.

## Command Template

Run all tests to verify nothing is broken after changes.

```bash
python -m pytest tests/ -v
```

With coverage:
```bash
python -m pytest tests/ --cov=app/backend -v
```
