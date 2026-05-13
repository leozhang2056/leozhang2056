---
inclusion: always
---

# Karpathy-Inspired Execution Guardrails (Repo Adapted)

This rule adapts the practical guidance from `forrestchang/andrej-karpathy-skills` to this KB-driven resume compiler.

## 1) Think Before Coding
- Start by stating assumptions when a request is ambiguous.
- Ask for clarification before changing data or generator logic if key intent is unclear.
- Surface tradeoffs briefly when multiple valid options exist (for example: quick wording tweak vs reusable rule change).
- If inputs conflict with verified facts in `kb/` or `projects/*/facts.yaml`, stop and call out the conflict explicitly.

## 2) Simplicity First
- Prefer the smallest change that satisfies the request.
- Avoid speculative abstractions, feature creep, and broad refactors.
- Do not add knobs/configs unless they are needed now or repeatedly requested.
- Keep generated content concise and evidence-backed; avoid keyword stuffing.

## 3) Surgical Changes
- Touch only files directly needed for the task.
- Do not "clean up nearby code" unless it is a direct side effect of your change.
- Preserve existing style and structure in touched files.
- Remove only artifacts made obsolete by your own edits (unused imports/variables caused by this task).

## 4) Goal-Driven Execution
- Convert user intent into explicit success criteria before implementation.
- For bug fixes or regressions, prefer reproduce -> fix -> verify loops.
- For generator/KB edits, verify with the relevant command, typically:
  - `python app/backend/validate.py`
  - `python generate.py cv --role <role>`
- Report verification results and any residual risk clearly.

## Repo-Specific Safety Additions
- Facts are source-of-truth only from `kb/*.yaml` and `projects/*/facts.yaml`; never invent missing details.
- If required facts are missing, emit `MISSING_INFO` rather than guessing.
- Preserve canonical CV section order and established output conventions unless user explicitly requests a change.
- When repeated user preferences appear, prefer codifying them in rules/config over one-off edits.
