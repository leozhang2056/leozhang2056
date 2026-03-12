#!/usr/bin/env python3
"""
从 Career KB YAML 文件生成 Cover Letter PDF
Generate Cover Letter PDF from Career KB YAML files

根据 kb/ai_prompts/cover_letter_generation.md 定义的规则实现。

用法:
  python generate_cover_letter.py --role android --company "Acme Corp" --jd-keywords Android Kotlin MVVM
  python generate_cover_letter.py --role ai --company "OpenAI" --output outputs/cover_letter.pdf
"""

import yaml
import os
import re
import argparse
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from generate_cv_html_to_pdf import html_to_pdf
from generate_cv_from_kb import (
    load_yaml,
    load_projects,
    sort_projects,
    score_project_by_jd,
)


# ---------------------------------------------------------------------------
# 角色预设内容（Cover Letter 使用，从 KB 读取后填充占位）
# ---------------------------------------------------------------------------

# 角色 → summary variant key（对应 profile.yaml）
_ROLE_SUMMARY_KEY = {
    'android':  'android_focus',
    'ai':       'ai_focus',
    'backend':  'java_focus',
    'fullstack': 'default',
}

# 各角色的主要叙事角度提示（用于生成开头和结尾）
_ROLE_NARRATIVE_HINT = {
    'android': {
        'en': 'Senior Android engineer with 10+ years of enterprise mobile development',
        'zh': '拥有 10 年以上企业级移动开发经验的高级 Android 工程师',
    },
    'ai': {
        'en': 'AI/ML engineer with published research and hands-on edge deployment experience',
        'zh': '具有学术发表经历和边缘 AI 部署经验的 AI/ML 工程师',
    },
    'backend': {
        'en': 'Backend engineer with 10+ years building high-scale Java microservices',
        'zh': '拥有 10 年以上高并发 Java 微服务开发经验的后端工程师',
    },
    'fullstack': {
        'en': 'Full-stack engineer with 10+ years of end-to-end delivery across mobile, backend, and AI',
        'zh': '拥有 10 年以上移动端、后端和 AI 全栈交付经验的全栈工程师',
    },
}


# ---------------------------------------------------------------------------
# Content builder
# ---------------------------------------------------------------------------

def _pick_top_projects(
    all_projects: List[Dict],
    role_type: str,
    jd_keywords: Optional[List[str]],
    n: int = 2,
) -> List[Dict]:
    """选出最相关的 n 个项目用于 Cover Letter 叙述"""
    return sort_projects(all_projects, role_type, jd_keywords, max_projects=n)


def _best_metrics(project: Dict) -> List[str]:
    """从项目中提取最有力的量化指标"""
    metrics = project.get('metrics', [])
    results = []
    for m in metrics:
        if isinstance(m, dict):
            value = str(m.get('value', ''))
            label = str(m.get('label', ''))
            desc  = str(m.get('description', ''))
            if value and label:
                results.append(f'{value}{label} {desc}'.strip())
    # fallback: highlights 里包含数字的句子
    if not results:
        for h in project.get('highlights', []):
            if isinstance(h, str) and re.search(r'\d', h):
                results.append(h[:100])
                if len(results) >= 2:
                    break
    return results[:2]


def build_cover_letter_content(
    profile: Dict,
    achievements: Dict,
    all_projects: List[Dict],
    role_type: str,
    company_name: str,
    target_role_title: str,
    jd_keywords: Optional[List[str]],
    lang: str,
) -> Dict[str, str]:
    """
    组装 Cover Letter 各段落内容（纯文本，不含 HTML 标签）。
    返回 dict: opening, body1, body2, closing
    """
    personal = profile.get('personal_info', {})
    name     = personal.get('preferred_name') or personal.get('name', 'Leo Zhang')
    contact  = personal.get('contact', {})
    email    = contact.get('email', '')
    phone    = contact.get('phone', '')

    career = profile.get('career_identity', {})
    summaries = career.get('summary_variants', {})
    variant_key = _ROLE_SUMMARY_KEY.get(role_type, 'default')
    summary_text = summaries.get(variant_key) or summaries.get('default', '')
    summary_text = re.sub(r'\s+', ' ', summary_text).strip()

    narrative_hint = _ROLE_NARRATIVE_HINT.get(role_type, _ROLE_NARRATIVE_HINT['fullstack'])
    hint_text = narrative_hint[lang]

    # 选出最相关的两个项目
    top_projects = _pick_top_projects(all_projects, role_type, jd_keywords, n=2)

    # 收集量化证据
    evidence_lines = []
    for proj in top_projects:
        proj_name = proj.get('name', proj.get('project_id', ''))
        metrics = _best_metrics(proj)
        if metrics:
            for m in metrics:
                evidence_lines.append(f'{proj_name}: {m}')
        else:
            highlights = [h for h in proj.get('highlights', []) if isinstance(h, str)]
            if highlights:
                evidence_lines.append(f'{proj_name}: {highlights[0][:100]}')

    # 总年限
    work_exp = profile.get('career_identity', {}).get('tagline', '')
    years_match = re.search(r'(\d+)\+?\s*years?', work_exp, re.IGNORECASE)
    years_str = f'{years_match.group(1)}+' if years_match else '10+'

    # Thesis / publication highlight
    pubs = achievements.get('publications', [])
    pub_note = ''
    if pubs:
        first_pub = pubs[0]
        pub_note_en = (f'My Master\'s thesis "{first_pub.get("title", "")}" '
                       f'({first_pub.get("venue", "")}, {first_pub.get("year", "")}) '
                       f'demonstrates my ability to independently design, build, and evaluate AI systems.')
        pub_note_zh = (f'我的硕士论文《{first_pub.get("title", "")}》'
                       f'（{first_pub.get("venue", "")}，{first_pub.get("year", "")}）'
                       f'体现了我独立设计、构建和评估 AI 系统的能力。')
        pub_note = pub_note_en if lang == 'en' else pub_note_zh

    if lang == 'en':
        opening = (
            f'I am writing to express my strong interest in the {target_role_title} position at {company_name}. '
            f'As a {hint_text} with {years_str} years of professional experience, '
            f'I am confident that my background aligns well with the requirements of this role.'
        )

        proj1 = top_projects[0] if top_projects else {}
        proj2 = top_projects[1] if len(top_projects) > 1 else {}
        proj1_name = proj1.get('name', '')
        proj2_name = proj2.get('name', '')
        proj1_evidence = evidence_lines[0] if evidence_lines else ''
        proj2_evidence = evidence_lines[1] if len(evidence_lines) > 1 else ''

        body1 = (
            f'In my most recent work, {proj1_name}, I served as {proj1.get("role", "sole developer")} '
            f'and delivered a complete solution from design through deployment. '
            + (f'{proj1_evidence}. ' if proj1_evidence else '')
            + (f'Additionally, through {proj2_name}, I {proj2.get("highlights", ["built and maintained a production system"])[0].lower() if proj2 else ""}.'
               if proj2_name else '')
        )

        body2_parts = [summary_text[:300] + '...'] if len(summary_text) > 300 else [summary_text]
        if pub_note:
            body2_parts.append(pub_note)
        body2 = ' '.join(body2_parts)

        closing = (
            f'I would welcome the opportunity to discuss how my experience can contribute to {company_name}. '
            f'I am available for an interview at your convenience and can be reached at {email} or {phone}.'
        )

    else:  # zh
        opening = (
            f'我诚挚地申请贵公司 {company_name} 的{target_role_title}职位。'
            f'作为一名{hint_text}，拥有 {years_str} 年专业经验，'
            f'我相信我的背景与该职位要求高度匹配。'
        )

        proj1 = top_projects[0] if top_projects else {}
        proj2 = top_projects[1] if len(top_projects) > 1 else {}
        proj1_name = proj1.get('name_cn') or proj1.get('name', '')
        proj2_name = proj2.get('name_cn') or proj2.get('name', '')
        proj1_evidence = evidence_lines[0] if evidence_lines else ''

        body1 = (
            f'在最近的项目 {proj1_name} 中，我担任{proj1.get("role_cn") or proj1.get("role", "独立开发者")}，'
            f'独立完成了从设计到部署的完整方案。'
            + (f'{proj1_evidence}。' if proj1_evidence else '')
            + (f'此外，在 {proj2_name} 项目中，我积累了丰富的相关技术经验。' if proj2_name else '')
        )

        body2_parts = [summary_text[:300] + '……'] if len(summary_text) > 300 else [summary_text]
        if pub_note:
            body2_parts.append(pub_note)
        body2 = ''.join(body2_parts)

        closing = (
            f'我期待有机会进一步探讨如何为 {company_name} 做出贡献。'
            f'如有面试意向，欢迎随时通过 {email} 或 {phone} 与我联系。'
        )

    return {
        'name':    name,
        'email':   email,
        'phone':   phone,
        'opening': opening,
        'body1':   body1,
        'body2':   body2,
        'closing': closing,
    }


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CL_CSS = """
    @page {
      size: A4;
      margin: 20mm 20mm 20mm 20mm;
    }

    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.65;
      color: #111;
      max-width: 170mm;
      margin: 0 auto;
      padding: 0;
      background: #fff;
    }

    a { color: #1a4a8a; text-decoration: none; }

    .cl-header {
      margin-bottom: 20px;
    }

    .cl-name {
      font-size: 18pt;
      font-weight: 700;
      color: #1a3a6a;
      margin-bottom: 4px;
    }

    .cl-contact {
      font-size: 10pt;
      color: #444;
    }

    .cl-date {
      margin-top: 24px;
      margin-bottom: 16px;
      font-size: 10.5pt;
      color: #333;
    }

    .cl-recipient {
      margin-bottom: 16px;
      font-size: 10.5pt;
    }

    .cl-salutation {
      margin-bottom: 12px;
      font-size: 10.5pt;
    }

    .cl-body p {
      margin-bottom: 14px;
      text-align: justify;
      font-size: 10.5pt;
    }

    .cl-sign {
      margin-top: 24px;
    }

    .cl-sign-label {
      font-size: 10.5pt;
      margin-bottom: 32px;
    }

    .cl-sign-name {
      font-size: 11pt;
      font-weight: 700;
      color: #1a3a6a;
    }

    @media print {
      body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    }
"""


# ---------------------------------------------------------------------------
# HTML 组装
# ---------------------------------------------------------------------------

def generate_cover_letter_html(
    role_type: str = 'fullstack',
    lang: str = 'en',
    company_name: str = 'the company',
    target_role_title: str = 'Software Engineer',
    jd_keywords: Optional[List[str]] = None,
) -> str:
    """生成 Cover Letter 完整 HTML"""

    base = Path(__file__).parent.parent.parent
    kb_dir = base / 'kb'
    profile      = load_yaml(kb_dir / 'profile.yaml')
    achievements = load_yaml(kb_dir / 'achievements.yaml')
    all_projects = load_projects(base / 'projects')

    content = build_cover_letter_content(
        profile, achievements, all_projects,
        role_type, company_name, target_role_title, jd_keywords, lang,
    )

    today_fmt = datetime.now().strftime('%B %d, %Y') if lang == 'en' else \
                datetime.now().strftime('%Y 年 %m 月 %d 日')
    salutation = 'Dear Hiring Manager,' if lang == 'en' else '尊敬的招聘负责人：'
    sign_off   = 'Sincerely,' if lang == 'en' else '此致'

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>{content["name"]} — Cover Letter</title>
  <style>{_CL_CSS}</style>
</head>
<body>

  <div class="cl-header">
    <div class="cl-name">{content["name"]}</div>
    <div class="cl-contact">
      <a href="mailto:{content["email"]}">{content["email"]}</a>
      &nbsp;|&nbsp; {content["phone"]}
    </div>
  </div>

  <div class="cl-date">{today_fmt}</div>

  <div class="cl-recipient">
    <strong>{company_name}</strong><br>
    Hiring Team
  </div>

  <div class="cl-salutation">{salutation}</div>

  <div class="cl-body">
    <p>{content["opening"]}</p>
    <p>{content["body1"]}</p>
    <p>{content["body2"]}</p>
    <p>{content["closing"]}</p>
  </div>

  <div class="cl-sign">
    <div class="cl-sign-label">{sign_off}</div>
    <div class="cl-sign-name">{content["name"]}</div>
  </div>

</body>
</html>'''

    return html


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

async def generate_cover_letter(
    output_path: Optional[str] = None,
    role_type: str = 'fullstack',
    lang: str = 'en',
    company_name: str = 'the company',
    target_role_title: str = 'Software Engineer',
    jd_keywords: Optional[List[str]] = None,
):
    """生成 Cover Letter PDF"""
    today = datetime.now().strftime('%Y%m%d')
    repo_root   = Path(__file__).parent.parent.parent
    outputs_dir = repo_root / 'outputs'
    outputs_dir.mkdir(exist_ok=True)

    if not output_path:
        safe_company = re.sub(r'[^a-zA-Z0-9_-]', '_', company_name)[:20]
        output_path = str(outputs_dir / f'CoverLetter_{safe_company}_{today}.pdf')

    lang_suffix = '' if lang == 'en' else '_CN'
    pdf_path  = output_path.replace('.pdf', f'{lang_suffix}.pdf')
    html_path = pdf_path.replace('.pdf', '.html')

    role_tag = role_type.upper()
    print(f"\nGenerating Cover Letter [{role_tag}] for {company_name} ({lang.upper()})...")
    if jd_keywords:
        print(f"  JD keywords: {jd_keywords}")

    html = generate_cover_letter_html(
        role_type, lang, company_name, target_role_title, jd_keywords
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  HTML → {html_path}")

    await html_to_pdf(html, pdf_path)
    print(f"  PDF  → {pdf_path}  ({os.path.getsize(pdf_path)/1024:.1f} KB)")

    return pdf_path


def main():
    parser = argparse.ArgumentParser(description='Generate Cover Letter from Career KB')
    parser.add_argument('--role',       default='fullstack',
                        choices=['android', 'ai', 'backend', 'fullstack'],
                        help='Target role type')
    parser.add_argument('--lang',       default='en',
                        choices=['en', 'zh'],
                        help='Output language')
    parser.add_argument('--company',    default='the company',
                        help='Company name')
    parser.add_argument('--title',      default='Software Engineer',
                        help='Target role title (e.g. "Senior Android Developer")')
    parser.add_argument('--jd-keywords', nargs='*', dest='jd_keywords',
                        help='JD keywords for relevance ranking')
    parser.add_argument('--output',     default=None,
                        help='Output PDF path')
    args = parser.parse_args()

    asyncio.run(generate_cover_letter(
        output_path=args.output,
        role_type=args.role,
        lang=args.lang,
        company_name=args.company,
        target_role_title=args.title,
        jd_keywords=args.jd_keywords,
    ))


if __name__ == '__main__':
    main()
