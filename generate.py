#!/usr/bin/env python3
"""
Unified CV / Cover Letter generator.

Usage examples:

  # Generate Android CV (English only by default):
  python generate.py cv --role android

  # Generate Android CV with Chinese version:
  python generate.py cv --role android --with-zh

  # Generate AI CV with JD keywords:
  python generate.py cv --role ai --jd-keywords Python PyTorch ONNX "model optimization"

  # Generate Cover Letter:
  python generate.py cl --role auto --jd-url "<job-url>" --company "Entelect" --title "Senior Android Engineer"

  # Generate application email text:
  python generate.py email --role backend --company "Datacom" --title "Senior Backend Engineer"

  # Generate CV with custom output path:
  python generate.py cv --role backend --output outputs/my_resume.pdf

  # Generate Cover Letter in Chinese:
  python generate.py cl --role android --company "字节跳动" --lang zh

  # List interview Q&A (by category / role / keyword):
  python generate.py interview --category technical
  python generate.py interview --role android --search "NDK"

  # Compare CV match scores across multiple JDs:
  python generate.py match --role auto --jd-file jd_a.txt --jd-file jd_b.txt
  python generate.py match --role backend --jd-url "<job-url-1>" --jd-url "<job-url-2>"

  # LLM loop: extract text from PDF + JD → OpenAI JSON edits → patch KB → new PDF:
  # Requires OPENAI_API_KEY (optional OPENAI_BASE_URL, OPENAI_MODEL); install pypdf.
  python generate.py cv-iterate --pdf outputs/.../CV_....pdf --jd-file jd.txt --role android --company "Acme"
Available roles: auto | android | ai | backend | fullstack

Output naming convention (auto, when --output is not specified):
  outputs/<YYYY-MM-DD>/CV_Leo_Zhang_<YYYYMMDD>_<role>[_<company>].pdf
    (default --max-projects 6, capped for about two A4 pages)
  outputs/<YYYY-MM-DD>/CV_Leo_Zhang_<YYYYMMDD>_<role>[_<company>]_CN.pdf (optional, with --with-zh)
  outputs/<YYYY-MM-DD>/CV_Leo_Zhang_<YYYYMMDD>_<role>[_<company>]_JD_Annotated.pdf (optional, --with-jd-annotated)
  outputs/<YYYY-MM-DD>/CoverLetter_<company>_<YYYYMMDD>.pdf
  outputs/<YYYY-MM-DD>/ApplicationEmail_<company>_<YYYYMMDD>.txt
  outputs/<YYYY-MM-DD>/JD_Match_Report_<YYYYMMDD>.md
  outputs/<YYYY-MM-DD>/CV_*_AI_REVIEW_BUNDLE.md (optional, with --with-review-bundle)
  The dated subfolder is created automatically if it does not exist.
  If your PDF preview looks unchanged, you may be opening an older dated file; use
  `--output outputs/my_cv.pdf` to overwrite one path, or `--keep-html` to inspect the HTML.
"""

import sys
import argparse
import asyncio
from pathlib import Path
from urllib.parse import urlparse

# Ensure app/backend is importable regardless of cwd
_BACKEND = Path(__file__).parent / 'app' / 'backend'
sys.path.insert(0, str(_BACKEND))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='generate',
        description='Leo Zhang CV / Cover Letter generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest='command', required=True)

    # ── cv ──────────────────────────────────────────────────────────────────
    cv_parser = sub.add_parser('cv', help='Generate CV (English PDF; JD annotated PDF optional)')
    cv_parser.add_argument(
        '--role', default='auto',
        choices=['auto', 'android', 'ai', 'backend', 'fullstack'],
        help='Target role type (default: auto; inferred from JD/title)',
    )
    cv_parser.add_argument(
        '--title',
        help='Target job title (e.g. "Senior Android Developer"). '
             'If omitted, a sensible default will be used based on --role.',
    )
    cv_parser.add_argument(
        '--jd-keywords', nargs='*', dest='jd_keywords',
        metavar='KEYWORD',
        help='JD keywords that drive project/skill ranking',
    )
    cv_parser.add_argument(
        '--jd-url',
        help='Public job posting URL; if provided and --jd-keywords is empty, '
             'keywords will be auto-derived from the page content.',
    )
    cv_parser.add_argument(
        '--jd-file',
        help='Path to a local JD text file; if provided and --jd-keywords is empty, '
             'keywords will be auto-derived from the file content.',
    )
    cv_parser.add_argument(
        '--company',
        help='Target company name; if provided and --output is not set, '
             'the generated CV filenames will include this company tag.',
    )
    cv_parser.add_argument(
        '--max-projects', type=int, default=6, dest='max_projects',
        help='Maximum number of projects to include (default: 6; capped for ~2 A4 pages)',
    )
    cv_parser.add_argument(
        '--output', default=None,
        help='English PDF output path',
    )
    cv_parser.add_argument(
        '--with-zh',
        action='store_true',
        help='Also generate Chinese CV PDF (_CN). Default: off',
    )
    cv_parser.add_argument(
        '--with-quality-report',
        action='store_true',
        help='Also generate CV quality report. Default: off',
    )
    cv_parser.add_argument(
        '--with-jd-annotated',
        action='store_true',
        help='Also generate JD keyword annotated PDF (_JD_Annotated). Default: off',
    )
    cv_parser.add_argument(
        '--min-jd-match-pct',
        type=float,
        default=85.0,
        metavar='PCT',
        help='Target minimum coverage %% for KB-supported JD keywords (default: 85; use 0 to disable auto tail)',
    )
    cv_parser.add_argument(
        '--with-review-bundle',
        dest='review_bundle',
        action='store_true',
        help='Also write *_AI_REVIEW_BUNDLE.md for external AI review. Default: off',
    )
    cv_parser.set_defaults(review_bundle=False)
    cv_parser.add_argument(
        '--keep-html',
        action='store_true',
        help='Keep intermediate .html next to the PDF (default: delete after PDF for cleanliness)',
    )

    # ── cl (cover letter) ────────────────────────────────────────────────────
    cl_parser = sub.add_parser('cl', help='Generate Cover Letter PDF')
    cl_parser.add_argument(
        '--role', default='auto',
        choices=['auto', 'android', 'ai', 'backend', 'fullstack'],
        help='Target role type (default: auto; inferred from JD/title)',
    )
    cl_parser.add_argument(
        '--lang', default='en',
        choices=['en', 'zh'],
        help='Output language (default: en)',
    )
    cl_parser.add_argument(
        '--company', default='the company',
        help='Company name',
    )
    cl_parser.add_argument(
        '--title', default='Software Engineer',
        help='Target job title (e.g. "Senior Android Engineer")',
    )
    cl_parser.add_argument(
        '--jd-keywords', nargs='*', dest='jd_keywords',
        metavar='KEYWORD',
        help='JD keywords that drive project selection',
    )
    cl_parser.add_argument(
        '--jd-url',
        help='Public job posting URL; if provided and --jd-keywords is empty, '
             'keywords will be auto-derived from the page content.',
    )
    cl_parser.add_argument(
        '--jd-file',
        help='Path to a local JD text file; if provided and --jd-keywords is empty, '
             'keywords will be auto-derived from the file content.',
    )
    cl_parser.add_argument(
        '--output', default=None,
        help='PDF output path',
    )

    # ── email (application email) ───────────────────────────────────────────
    email_parser = sub.add_parser('email', help='Generate application email TXT')
    email_parser.add_argument(
        '--role', default='auto',
        choices=['auto', 'android', 'ai', 'backend', 'fullstack'],
        help='Target role type (default: auto; inferred from JD/title)',
    )
    email_parser.add_argument(
        '--lang', default='en',
        choices=['en', 'zh'],
        help='Output language (default: en)',
    )
    email_parser.add_argument(
        '--company', default='the company',
        help='Company name',
    )
    email_parser.add_argument(
        '--title', default='Software Engineer',
        help='Target job title (e.g. "Senior Android Engineer")',
    )
    email_parser.add_argument(
        '--jd-keywords', nargs='*', dest='jd_keywords',
        metavar='KEYWORD',
        help='JD keywords that drive project selection',
    )
    email_parser.add_argument(
        '--jd-url',
        help='Public job posting URL; if provided and --jd-keywords is empty, '
             'keywords will be auto-derived from the page content.',
    )
    email_parser.add_argument(
        '--jd-file',
        help='Path to a local JD text file; if provided and --jd-keywords is empty, '
             'keywords will be auto-derived from the file content.',
    )
    email_parser.add_argument(
        '--output', default=None,
        help='TXT output path',
    )

    # ── interview (Q&A 库) ────────────────────────────────────────────────────
    qa_parser = sub.add_parser('interview', help='List interview Q&A by category/role/search')
    qa_parser.add_argument(
        '--category',
        choices=['technical', 'behavioral', 'role_specific'],
        help='Limit to one question category',
    )
    qa_parser.add_argument(
        '--role',
        choices=['android', 'backend', 'ai', 'iot', 'leadership', 'company'],
        help='Limit to role-specific questions',
    )
    qa_parser.add_argument(
        '--search',
        help='Keyword to filter questions and answer points',
    )
    qa_parser.add_argument(
        '--short',
        action='store_true',
        help='Only print question text (no points/tips)',
    )

    # ── match (multi-JD match scoring) ────────────────────────────────────────
    match_parser = sub.add_parser('match', help='Compare CV match scores across multiple JDs')
    match_parser.add_argument(
        '--role', default='auto',
        choices=['auto', 'android', 'ai', 'backend', 'fullstack'],
        help='Role mode (auto infers role for each JD)',
    )
    match_parser.add_argument(
        '--jd-url', action='append', dest='jd_urls',
        help='JD URL (can be used multiple times)',
    )
    match_parser.add_argument(
        '--jd-file', action='append', dest='jd_files',
        help='JD file path (can be used multiple times)',
    )
    match_parser.add_argument(
        '--jd-keywords', nargs='*', dest='jd_keywords',
        metavar='KEYWORD',
        help='Manual JD keywords (used when no URL/file is provided)',
    )
    match_parser.add_argument(
        '--max-projects', type=int, default=6, dest='max_projects',
        help='Max projects used for CV generation during scoring (default: 6)',
    )
    match_parser.add_argument(
        '--max-keywords', type=int, default=24, dest='max_keywords',
        help='Max extracted keywords per JD (default: 24)',
    )
    match_parser.add_argument(
        '--output', default=None,
        help='Output report path (Markdown)',
    )

    # ── cv-iterate (LLM: PDF + JD → KB patches → regenerate CV PDF) ──────────
    cit_parser = sub.add_parser(
        'cv-iterate',
        help='OpenAI-compatible API: review CV PDF + JD, apply KB edits, regenerate PDF',
    )
    cit_parser.add_argument('--pdf', required=True, help='Path to existing CV PDF')
    cit_parser.add_argument(
        '--role', default='fullstack',
        choices=['android', 'ai', 'backend', 'fullstack'],
        help='Resume role / summary variant',
    )
    cit_parser.add_argument('--company', default=None, help='Company tag for output naming')
    cit_parser.add_argument('--title', default=None, help='Target job title')
    cit_parser.add_argument('--jd-url', default=None, help='JD page URL')
    cit_parser.add_argument('--jd-file', default=None, help='Local JD text file')
    cit_parser.add_argument(
        '--jd-keywords', nargs='*', dest='jd_keywords', metavar='KW',
        help='JD keywords if no full JD text',
    )
    cit_parser.add_argument('--max-keywords', type=int, default=24)
    cit_parser.add_argument('--max-projects', type=int, default=6)
    cit_parser.add_argument('--output', default=None, help='Output PDF path')
    cit_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Call model and print edits only; do not write KB or PDF',
    )
    cit_parser.add_argument('--min-jd-match-pct', type=float, default=85.0)
    cit_parser.add_argument(
        '--no-review-bundle',
        action='store_true',
        help='Skip *_AI_REVIEW_BUNDLE.md after regeneration',
    )
    cit_parser.add_argument(
        '--model', default=None,
        help='Chat model (default: env OPENAI_MODEL or gpt-4o-mini)',
    )

    return parser


def _infer_role_from_text(text: str) -> str:
    """
    Very small heuristic classifier: infer role from JD/title/keywords.
    Returns one of: android | ai | backend | fullstack
    """
    t = (text or "").lower()
    if not t:
        return "fullstack"

    # Android signals
    android_hits = (
        "android", "kotlin", "jetpack", "compose", "gradle", "adb", "ndk", "jni",
        "mvvm", "room", "coroutines", "retrofit", "okhttp",
    )
    # AI signals
    ai_hits = (
        "pytorch", "tensorflow", "llm", "diffusion", "computer vision", "cv",
        "onnx", "cuda", "transformer", "fine-tuning", "finetuning", "rag",
        "embedding", "prompt", "ml", "machine learning",
    )
    # Backend/Java signals
    backend_hits = (
        "spring", "spring boot", "spring cloud", "java", "microservice",
        "rest", "api", "mybatis", "hibernate", "jpa", "redis", "kafka",
    )

    def _count(hits: tuple[str, ...]) -> int:
        return sum(1 for h in hits if h in t)

    a = _count(android_hits)
    i = _count(ai_hits)
    b = _count(backend_hits)

    if a >= max(i, b) and a > 0:
        return "android"
    if i >= max(a, b) and i > 0:
        return "ai"
    if b >= max(a, i) and b > 0:
        return "backend"
    return "fullstack"


def _auto_keywords_from_jd(args) -> list[str]:
    """
    如果用户没有显式提供 jd_keywords，但提供了 jd_url 或 jd_file，
    尝试自动从 JD 文本中提取一组关键词。
    """
    if getattr(args, "jd_keywords", None):
        return list(args.jd_keywords)

    jd_url  = getattr(args, "jd_url", None)
    jd_file = getattr(args, "jd_file", None)
    if not jd_url and not jd_file:
        return []

    # 延迟导入，避免在未使用时增加依赖负担
    try:
        from app.backend.jd_fetch import (  # type: ignore
            derive_keywords_from_url,
            load_jd_text_from_file,
            extract_keywords_from_text,
        )
    except Exception:
        # 在路径不一致时再尝试相对导入
        try:
            from jd_fetch import (  # type: ignore
                derive_keywords_from_url,
                load_jd_text_from_file,
                extract_keywords_from_text,
            )
        except Exception:
            print("Warning: failed to import jd_fetch helpers; please install dependencies "
                  "or provide --jd-keywords manually.")
            return []

    if jd_url:
        print(f"Fetching JD from URL: {jd_url}")
        _, kws = derive_keywords_from_url(jd_url)
        if kws:
            print(f"  Auto-extracted JD keywords: {kws}")
        return kws

    if jd_file:
        print(f"Loading JD from file: {jd_file}")
        text = load_jd_text_from_file(jd_file)
        kws = extract_keywords_from_text(text) if text else []
        if kws:
            print(f"  Auto-extracted JD keywords: {kws}")
        return kws

    return []


def _auto_role(args) -> str:
    """
    If user chose --role auto, infer from JD (file/url) and/or title.
    """
    role = getattr(args, "role", "auto")
    if role and role != "auto":
        return role

    title = (getattr(args, "title", None) or "").strip()
    jd_url = getattr(args, "jd_url", None)
    jd_file = getattr(args, "jd_file", None)

    # Prefer local JD file content (most reliable)
    if jd_file:
        try:
            from app.backend.jd_fetch import load_jd_text_from_file  # type: ignore
        except Exception:
            try:
                from jd_fetch import load_jd_text_from_file  # type: ignore
            except Exception:
                load_jd_text_from_file = None  # type: ignore
        if load_jd_text_from_file:
            text = load_jd_text_from_file(jd_file) or ""
            inferred = _infer_role_from_text(text + "\n" + title)
            print(f"Auto-inferred role: {inferred}")
            return inferred

    # Next: infer from title + URL (weak)
    inferred = _infer_role_from_text((jd_url or "") + "\n" + title)
    print(f"Auto-inferred role: {inferred}")
    return inferred


def _auto_company(args) -> str:
    """
    If --company is not explicitly set, try infer company name from --jd-url.
    """
    company = (getattr(args, "company", None) or "").strip()
    if company and company.lower() not in {"the company", "target company"}:
        return company

    jd_url = (getattr(args, "jd_url", None) or "").strip()
    if not jd_url:
        # No JD URL: omit company slug in default CV filenames (generic resume).
        return company or ""

    try:
        parsed = urlparse(jd_url)
        host = (parsed.netloc or "").lower()
        path = (parsed.path or "").strip("/")
    except Exception:
        return company or ""

    # Workday hosts like eroadgroup.wd3.myworkdayjobs.com -> eroadgroup
    if ".myworkdayjobs.com" in host:
        org = host.split(".")[0]
        if org:
            inferred = org.replace("-", " ").replace("_", " ").title()
            print(f"Auto-inferred company from JD URL: {inferred}")
            return inferred

    # Greenhouse format: /<company>/jobs/<id>
    if "greenhouse.io" in host and path:
        first = path.split("/")[0]
        if first and first not in {"job-boards", "boards"}:
            inferred = first.replace("-", " ").replace("_", " ").title()
            print(f"Auto-inferred company from JD URL: {inferred}")
            return inferred

    # SmartRecruiters: jobs.smartrecruiters.com/<Company>/...
    if "smartrecruiters.com" in host and path:
        first = path.split("/")[0]
        if first:
            inferred = first.replace("-", " ").replace("_", " ").title()
            print(f"Auto-inferred company from JD URL: {inferred}")
            return inferred

    # Generic fallback: first host label
    root = host.split(".")[0] if host else ""
    if root and root not in {"www", "jobs", "careers", "apply"}:
        inferred = root.replace("-", " ").replace("_", " ").title()
        print(f"Auto-inferred company from JD URL: {inferred}")
        return inferred

    return company or ""


async def run(args) -> None:
    if args.command == 'cv':
        from generate_cv_from_kb import generate_cv_from_kb
        jd_keywords = _auto_keywords_from_jd(args)
        role = _auto_role(args)
        company = _auto_company(args)
        en_path, zh_path, annotated_path = await generate_cv_from_kb(
            output_path=args.output,
            role_type=role,
            jd_keywords=jd_keywords or [],
            max_projects=args.max_projects,
            company_name=company,
            target_role_title=getattr(args, 'title', None),
            generate_zh=bool(getattr(args, 'with_zh', False)),
            generate_quality_report=bool(getattr(args, 'with_quality_report', False)),
            generate_jd_annotated_pdf=bool(getattr(args, 'with_jd_annotated', False)),
            min_jd_match_pct=float(getattr(args, 'min_jd_match_pct', 85.0)),
            write_review_bundle=bool(getattr(args, 'review_bundle', False)),
            keep_html=bool(getattr(args, 'keep_html', False)),
        )
        print(f"\nDone.")
        print(f"  EN: {Path(en_path).resolve()}")
        if annotated_path:
            print(f"  EN (JD Annotated): {annotated_path}")
        if zh_path:
            print(f"  ZH: {zh_path}")
        else:
            print("  ZH: skipped (use --with-zh to generate)")

    elif args.command == 'cl':
        from generate_cover_letter import generate_cover_letter
        jd_keywords = _auto_keywords_from_jd(args)
        role = _auto_role(args)
        company = _auto_company(args)
        pdf_path = await generate_cover_letter(
            output_path=args.output,
            role_type=role,
            lang=args.lang,
            company_name=company,
            target_role_title=args.title,
            jd_keywords=jd_keywords or [],
        )
        print(f"\nDone.")
        print(f"  PDF: {pdf_path}")

    elif args.command == 'interview':
        from interview_qa_cli import run_list
        repo_root = Path(__file__).parent
        run_list(
            repo_root,
            category=getattr(args, 'category', None),
            role=getattr(args, 'role', None),
            search=getattr(args, 'search', None),
            verbose=not getattr(args, 'short', False),
        )

    elif args.command == 'email':
        from generate_application_email import generate_application_email
        jd_keywords = _auto_keywords_from_jd(args)
        role = _auto_role(args)
        company = _auto_company(args)
        txt_path = generate_application_email(
            output_path=args.output,
            role_type=role,
            lang=args.lang,
            company_name=company,
            target_role_title=args.title,
            jd_keywords=jd_keywords or [],
        )
        print(f"\nDone.")
        print(f"  EMAIL TXT: {txt_path}")

    elif args.command == 'match':
        from match_cv_to_jds import generate_match_report_file
        report_path = generate_match_report_file(
            role_type=args.role,
            jd_urls=getattr(args, 'jd_urls', None),
            jd_files=getattr(args, 'jd_files', None),
            jd_keywords=getattr(args, 'jd_keywords', None),
            max_projects=getattr(args, 'max_projects', 6),
            max_keywords=getattr(args, 'max_keywords', 24),
            output_path=args.output,
        )
        print(f"\nDone.")
        print(f"  MATCH REPORT: {report_path}")

    elif args.command == 'cv-iterate':
        from cv_auto_review_iterate import run_cv_iterate
        await run_cv_iterate(args)


def main():
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == '__main__':
    main()
