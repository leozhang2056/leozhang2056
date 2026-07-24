# workflow
- When editing project facts in leozhang2056 KB repo, also sync changes to LeoPortfolio's src/lib/projects.ts. Confidence: 0.70
- After completing each project update, proactively ask questions to elicit supplementary information from the user before moving to the next project. Confidence: 0.80
- Only process even-numbered sequence projects (skip odd-numbered ones). Confidence: 0.70
- When correcting project facts, only change what the user explicitly identified as wrong — do not remove technologies/content the user hasn't confirmed as incorrect. Confidence: 0.70
- When role-playing as an interviewer asking questions about projects, use English. Confidence: 0.80
- When role-playing as an interviewer, proactively generate plausible answers to your own questions and integrate Q&A pairs into the project's QA library, rather than waiting for the user to supply answers. Confidence: 0.75
- Maintain consistency between project facts (facts.yaml), project README.md, and portfolio site (projects.ts) — when updating one, check and sync the others. User explicitly requested this across multiple sessions. Confidence: 0.90
- When the user works with another agent in parallel on the same repo, respect their assignment boundaries — do not modify files the other agent is working on. User said "我有另一个agent和你一起修改，但是我会让你们交替改不同的project信息". Confidence: 0.85
- After each CV/CL generation session, reflect on quality issues and evolve rules — user requested a self-evolving mechanism to "反思每次执行...沉淀到规则里，下次不犯同样的错误". Confidence: 0.80
