---
description: Run full test suite
---

Run all tests to verify nothing is broken after changes.

```bash
python -m pytest tests/ -v
```

With coverage:
```bash
python -m pytest tests/ --cov=app/backend -v
```
