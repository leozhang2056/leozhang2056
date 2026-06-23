---
description: Run multi-agent CV generation pipeline
---

Multi-agent orchestration: pre-discussion + post-review + arbiter (highest quality).

`python generate.py cv-best --role backend --jd-file <path> --company "<name>" --auto-refine`

For multiple jobs at once (parallel batch):
`python generate.py batch-cv --parallel 3`
