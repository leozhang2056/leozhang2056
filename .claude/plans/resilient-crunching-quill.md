# Plan: Generate CV for Halter — Software Engineering Manager

## Context

Leo is applying for a **Software Engineering Manager** role at **Halter** (Auckland, on-site). The JD emphasizes a hands-on engineering manager who leads both frontend and backend engineers, shapes technical direction, stays close to code, and works across a system combining hardware, software, and AI for real-world farming operations.

The CV generator's available roles (`auto`, `android`, `ai`, `backend`, `embedded`, `fullstack`) don't include a dedicated "management" template, so we need the best approximation. After analysis, `fullstack` is the best choice — it covers the breadth (frontend + backend + cloud + AI) that Halter's engineering managers need to navigate.

## Role Decision: `fullstack`

| Factor | Why `fullstack` wins |
|---|---|
| JD mentions **both frontend and backend** engineers to lead | Fullstack template covers both |
| **IoT/hardware systems** | Fullstack includes `iot-solutions`, `smart-factory` in pinned projects |
| **AI tools** (Claude Code, Copilot, LLM) | Fullstack has an "AI & Tools" skills section |
| **No management-specific template** exists | Fullstack is the most flexible fallback |
| Leo's actual background spans backend, frontend, Android, cloud | Fullstack best represents this breadth |

**Not** `backend` because: Halter's JD explicitly mentions leading frontend AND backend teams, and `backend` template excludes frontend tech skills and frontend-heavy projects entirely.

## Steps

### 1. Save JD to file
Write the user's Halter SEM JD to a new file (e.g. `jd_halter_sem.txt` or place in `Interview/` if that's the convention).

### 2. Generate CV via `/cv-best` (multi-agent pipeline)
Run:
```
python generate.py cv-best --role fullstack --jd-file jd_halter_sem.txt --company Halter --title "Software Engineering Manager" --auto-refine
```

The multi-agent pipeline provides the highest quality — it generates, reviews, and refines automatically.

### 3. Verify output
- Check the generated PDF in `outputs/`
- Confirm the 2-page limit
- Review that the summary is adapted for an engineering leadership role (the CV generator's JD adaptation mechanism handles this)

## Considerations

- **Summary sentence 1**: Currently "Staff Software Engineer with 10+ years..." — the JD adaptation rule will adapt this per the `jd_adjustment` policy. The JD title is "Software Engineering Manager" so the output should reflect that.
- **Leadership framing**: The CV system will leverage Leo's existing experience leading technical teams and mentoring at Chunxiao Technology. No facts need to be fabricated — the existing project descriptions include leadership aspects.
- **No Halter SEM JD exists yet**: The existing Halter files are for Intern (2026) and Senior Engineer (2026) roles — this is a new one.

## Files to Create / Modify

- `E:\Coding\leozhang2056\jd_halter_sem.txt` — New JD file (write from user-provided text)
- Output will land in `E:\Coding\leozhang2056\outputs\CV_Leo_Zhang_YYYYMMDD_fullstack_Halter.pdf`

## Verification

1. Confirm `outputs/` contains `CV_Leo_Zhang_*_Halter.*` files
2. Open the PDF and verify layout is clean
3. Run `python -m pytest tests/ -v -k kb` if any KB changes were made (none expected for this simple generation)
