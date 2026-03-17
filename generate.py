#!/usr/bin/env python3
"""
Unified CV / Cover Letter generator.

Usage examples:

  # Generate Android CV (default role):
  python generate.py cv --role android

  # Generate AI CV with JD keywords:
  python generate.py cv --role ai --jd-keywords Python PyTorch ONNX "model optimization"

  # Generate Cover Letter:
  python generate.py cl --role auto --jd-url "<job-url>" --company "Entelect" --title "Senior Android Engineer"

  # Generate CV with custom output path:
  python generate.py cv --role backend --output outputs/my_resume.pdf

  # Generate Cover Letter in Chinese:
  python generate.py cl --role android --company "字节跳动" --lang zh

  # List interview Q&A (by category / role / keyword):
  python generate.py interview --category technical
  python generate.py interview --role android --search "NDK"
Available roles: auto | android | ai | backend | fullstack

Output naming convention (auto, when --output is not specified):
  outputs/<YYYY-MM-DD>/CV_Leo_Zhang_<YYYYMMDD>_<role>[_<company>].pdf
  outputs/<YYYY-MM-DD>/CV_Leo_Zhang_<YYYYMMDD>_<role>[_<company>]_CN.pdf
  outputs/<YYYY-MM-DD>/CoverLetter_<company>_<YYYYMMDD>.pdf
  The dated subfolder is created automatically if it does not exist.
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
    cv_parser = sub.add_parser('cv', help='Generate CV (English + Chinese PDF)')
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
        '--max-projects', type=int, default=5, dest='max_projects',
        help='Maximum number of projects to include (default: 5)',
    )
    cv_parser.add_argument(
        '--output', default=None,
        help='English PDF output path (CN version is auto-derived)',
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
        return company or "the company"

    try:
        parsed = urlparse(jd_url)
        host = (parsed.netloc or "").lower()
        path = (parsed.path or "").strip("/")
    except Exception:
        return company or "the company"

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

    return company or "the company"


async def run(args) -> None:
    if args.command == 'cv':
        from generate_cv_from_kb import generate_cv_from_kb
        jd_keywords = _auto_keywords_from_jd(args)
        role = _auto_role(args)
        company = _auto_company(args)
        en_path, zh_path = await generate_cv_from_kb(
            output_path=args.output,
            role_type=role,
            jd_keywords=jd_keywords or [],
            max_projects=args.max_projects,
            company_name=company,
            target_role_title=getattr(args, 'title', None),
        )
        print(f"\nDone.")
        print(f"  EN: {en_path}")
        print(f"  ZH: {zh_path}")

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


def main():
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == '__main__':
    main()
