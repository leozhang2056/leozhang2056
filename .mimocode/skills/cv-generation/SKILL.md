---
name: cv-generation
description: "Standard workflow for generating a CV and cover letter — JD saving, generation, review, cleanup"
---

# CV Generation Workflow

This skill codifies the repeated manual workflow for generating tailored CVs and cover letters from the knowledge base.

## Steps

1. **Save JD** to `jd_archive/` with naming convention: `{company_slug}_{role_slug}.txt`
   - Company slug: lowercase, hyphens for spaces (e.g., `heartland_bank`, `nateva`)
   - Role slug: lowercase, hyphens (e.g., `senior_software_developer_gis`)
   - Include: company name, location, role title, salary (if listed), key requirements
   - **This file is the source of truth for what you applied to** — always save before generating

2. **Generate CV**:
   ```bash
   python generate.py cv --role <role> --jd-file <path> --company "<name>" --title "<title>" --with-quality-report --with-jd-annotated
   ```
   - Role must be one of: `auto | android | ai | backend | fullstack | embedded`
   - Use `--with-quality-report` to get quality metrics
   - Use `--with-jd-annotated` to see JD keyword coverage

3. **Generate Cover Letter** (synchronously):
   ```bash
   python generate.py cl --role <role> --jd-file <path> --company "<name>" --title "<title>"
   ```

4. **Sub-agent review** (MANDATORY):
   - Read generated HTML + rules + quality report
   - Spawn review sub-agent → returns structured findings
   - Apply HIGH + MED fixes → regenerate PDF
   - If HIGH findings remained → re-review (max 2 iterations)

5. **Clean up intermediate files** (HTML, POST_CHECK.md, QUALITY.md):
   ```bash
   # Remove HTML and check files from today's output folder
   find outputs/$(date +%Y-%m-%d)/ -name "*.html" -delete
   find outputs/$(date +%Y-%m-%d)/ -name "*_POST_CHECK.md" -delete
   find outputs/$(date +%Y-%m-%d)/ -name "*_QUALITY.md" -delete
   ```

6. **Present final PDF** to user with summary of review changes

## Output Location
- PDFs are saved in `outputs/YYYY-MM-DD/` with auto-generated filenames
- Delete intermediate `.html` and `*_POST_CHECK.md` after generation — keep only PDFs

## Notes
- The `validate.py` pre-check runs automatically unless `--no-strict-kb` is used
- For Chinese version, add `--with-zh` to the CV generation command
- For editable Markdown, use `--gen-md`; to convert back to PDF, use `--from-md`