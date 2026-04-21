#!/usr/bin/env python3
"""
从 Career KB YAML 文件生成 Cover Letter PDF
Generate Cover Letter PDF from Career KB YAML files

根据 kb/ai_prompts/cover_letter_generation.md 定义的规则实现。

用法:
  python generate_cover_letter.py --role android --company "Acme Corp" --jd-keywords Android Kotlin MVVM
  python generate_cover_letter.py --role ai --company "OpenAI" --output outputs/cover_letter.pdf
"""

# Ensure sibling imports work regardless of invocation method
from _path_setup import setup_backend_path
setup_backend_path()

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
        'en': 'Senior Android engineer focused on production mobile delivery',
        'zh': '拥有 10 年以上企业级移动开发经验的高级 Android 工程师',
    },
    'ai': {
        'en': 'AI/ML engineer with published research and strong production implementation experience',
        'zh': '具有学术发表经历和扎实生产级落地经验的 AI/ML 工程师',
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

# 公司共鸣叙事钩子（不写硬事实，避免与 JD/官网信息冲突）
_COMPANY_FIT_HOOKS = {
    'eroad': {
        'en': (
            'What resonates with me about EROAD is the practical impact of software on real-world operations. '
            'My experience building IoT-connected systems, production APIs, and reliability-focused delivery fits this '
            'mission style: turning complex data and workflows into stable tools teams can trust every day.'
        ),
        'zh': (
            '我与 EROAD 的共鸣点在于：用软件直接改善一线真实业务。'
            '我长期做 IoT 连接系统、生产级 API 与稳定性交付，擅长把复杂数据与流程落成团队每天可依赖的工具。'
        ),
    },
    'l3harris': {
        'en': (
            "What resonates with me about L3Harris is your values-led engineering culture: dedication to mission, "
            "commitment to excellence, and building trusted technology for high-stakes environments. "
            "I am motivated by teams that pair technical depth with accountability, where secure and reliable delivery "
            "matters as much as feature speed."
        ),
        'zh': (
            "我与 L3Harris 的共鸣点在于其以价值观驱动的工程文化：强调使命感、追求卓越，"
            "并在高要求场景中交付可信技术。"
            "我认同“技术深度 + 交付责任”并重的团队方式，在这里系统安全与稳定和功能迭代同样重要。"
        ),
    },
    'aut': {
        'en': (
            "What resonates with me most about AUT is its values-led culture and practical mission: "
            "Pono, Tika, and Aroha, together with \"Knowledge that Works,\" reflect the kind of environment "
            "where I do my best work. As a recent AUT graduate, I have experienced this culture directly and "
            "genuinely value how AUT supports students, staff, and diverse communities through real-world impact."
        ),
        'zh': (
            "我与 AUT 最深的共鸣来自其价值观导向的文化与务实使命："
            "Pono、Tika、Aroha，以及“Knowledge that Works”。"
            "作为刚毕业的 AUT 学生，我亲身感受过这种文化，也真心认同 AUT 通过实际成果服务学生、教职员工与多元社区。"
        ),
    },
}

_WHY_ME_HOOKS = {
    'eroad': {
        'en': (
            'I believe I am a strong fit because I combine three qualities that are hard to find together: '
            'cross-layer execution (mobile, backend, and hardware integration), proven production outcomes '
            '(500K+ messages/day, sub-200ms latency, and multi-site rollout impact), and disciplined delivery '
            'habits (CI/CD, code review, and pragmatic troubleshooting under real deadlines). '
            'This means I can contribute quickly with minimal ramp-up and deliver reliable results from early iterations.'
        ),
        'zh': (
            '我认为自己适合这个岗位，关键在于三点同时具备：跨层交付能力（移动端、后端与硬件集成）、'
            '可验证的生产结果（50 万+消息/天、亚 200ms 延迟、多站点上线效果），以及稳定的工程交付习惯'
            '（CI/CD、代码评审、在真实截止期下的问题闭环）。这让我可以低磨合快速上手，并持续交付可落地结果。'
        ),
    }
    ,
    'l3harris': {
        'en': (
            "I believe I can add value quickly because I bring cross-stack delivery habits aligned with this role: "
            "building maintainable backend services and APIs, shipping production web/mobile features, and closing issues "
            "through testing, CI/CD, and pragmatic troubleshooting. "
            "I also work comfortably in distributed Agile teams and communicate technical trade-offs clearly."
        ),
        'zh': (
            "我能较快产生价值，是因为我具备与该岗位一致的跨栈交付习惯："
            "能构建可维护的后端服务与 API，也能稳定交付前端/移动端功能，并通过测试、CI/CD 和问题闭环保障质量。"
            "同时我适应分布式敏捷协作，能够清晰沟通技术取舍。"
        ),
    },
    'aut': {
        'en': (
            "I would be proud to continue my journey at AUT and contribute as an engineer in the same community that shaped me. "
            "I have been waiting for an opportunity like this. "
            "More than anything, I hope to work alongside my AUT teachers and mentors as colleagues, and keep building meaningful outcomes together. "
            "This role is deeply personal to me, and I am genuinely excited and strongly committed to growing my career at AUT."
        ),
        'zh': (
            "能够以工程师身份继续留在 AUT 这个培养我的社区，我会感到非常自豪。"
            "我非常愿意并且有强烈动力投入 AUT 的 AI 与数字体验平台建设，"
            "以稳定交付、务实集成和协作方式持续贡献。这个岗位对我有很强的个人意义，"
            "我也真心期待并坚定希望在 AUT 长期发展。"
        ),
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
    ranked = sort_projects(all_projects, role_type, jd_keywords, max_projects=max(n + 3, 5))
    by_id = {str(p.get("project_id") or p.get("_project_dir") or ""): p for p in all_projects}

    # 会话偏好：
    # - fullstack 叙事优先 smart-factory / iot-solutions，弱化 chatclothes
    # - 其他角色维持 chatclothes + smart-factory
    preferred = []
    if role_type == "fullstack":
        preferred_order = ("smart-factory", "iot-solutions", "chatclothes")
    else:
        preferred_order = ("chatclothes", "smart-factory")

    for pid in preferred_order:
        p = by_id.get(pid)
        if p:
            preferred.append(p)

    seen = set()
    out: List[Dict] = []
    for p in preferred + ranked:
        pid = str(p.get("project_id") or p.get("_project_dir") or "")
        if not pid or pid in seen:
            continue
        # cover letter 中默认不使用 enterprise-messaging 作为主叙事项目
        if pid == "enterprise-messaging":
            continue
        seen.add(pid)
        out.append(p)
        if len(out) >= n:
            break

    return out[:n]


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
            f'I am genuinely excited to apply for the {target_role_title} position at {company_name}. '
            f'I have been waiting for an opportunity like this for a long time, and this role feels like a very strong fit. '
            f'As a recent AUT graduate and a {hint_text}, this opportunity feels especially meaningful to me. '
            f'I care deeply about AUT and the people here, and I would be honoured to contribute back to this community.'
        )

        proj1 = top_projects[0] if top_projects else {}
        proj2 = top_projects[1] if len(top_projects) > 1 else {}
        proj1_name = proj1.get('name', '')
        proj2_name = proj2.get('name', '')
        proj1_evidence = evidence_lines[0] if evidence_lines else ''
        proj2_evidence = evidence_lines[1] if len(evidence_lines) > 1 else ''

        if role_type == 'android':
            body1 = (
                'I have built and maintained Android applications in complex production environments using '
                'Kotlin/Java, Android SDK, Jetpack components, MVVM architecture, and REST API integration. '
                + (f'In {proj1_name}, {proj1.get("highlights", ["I delivered end-to-end Android implementation and release workflows"])[0].lower()}. '
                   if proj1_name else '')
                + (f'In {proj2_name}, {proj2.get("highlights", ["I improved mobile reliability and maintainability through iterative engineering practices"])[0].lower()}.'
                   if proj2_name else '')
            )
        else:
            body1 = (
                f'In my most recent work, {proj1_name}, I served as {proj1.get("role", "sole developer")} '
                f'and delivered a complete solution from design through deployment. '
                + (f'{proj1_evidence}. ' if proj1_evidence else '')
                + (f'Additionally, through {proj2_name}, I {proj2.get("highlights", ["built and maintained a production system"])[0].lower() if proj2 else ""}.'
                   if proj2_name else '')
            )
        company_lower = (company_name or '').lower()
        if company_lower.strip() == 'aut' or 'auckland university of technology' in company_lower:
            body1 = (
                "At AUT, I completed my Master's in Computer and Information Sciences with First Class Honours, "
                "where I strengthened my practical knowledge across software architecture, AI applications, "
                "integration workflows, and production-oriented delivery. "
                "My core AUT project was ChatClothes, where I independently designed and implemented an end-to-end system, "
                "from model workflow orchestration to a usable application experience and evaluation outputs. "
                "I also contributed through applied research and publication work, including my thesis and peer-reviewed output, "
                "which reflects my commitment to turning learning into real, useful outcomes."
            )

        # 第三段专注“岗位匹配能力”，避免与项目段重复
        role_match_map = {
            'android': (
                f'For this role at {company_name}, I can contribute to customer-facing mobile journeys by building '
                'clean, maintainable Android code, improving app performance and reliability, and resolving complex production issues. '
                'I work effectively in Agile product squads and collaborate closely with Product Managers, UI/UX Designers, and backend engineers '
                'to deliver high-quality releases at pace.'
            ),
            'backend': (
                'For this role, I bring strong backend engineering depth in Java/Spring APIs, data-layer reliability, '
                'and pragmatic delivery with code reviews, testing, and CI/CD.'
            ),
            'ai': (
                'For this role, I bring practical AI engineering experience with end-to-end implementation, '
                'evaluation, and production-focused delivery with clear technical communication.'
            ),
            'fullstack': (
                'For this role, I bring hands-on full-stack delivery across frontend, backend APIs, and cloud workflows. '
                'I write maintainable code, value test automation and code reviews, and collaborate effectively in Agile teams. '
                'I am fast in execution, strong in self-management, and comfortable driving work from ambiguity to reliable outcomes.'
            ),
        }
        body2 = role_match_map.get(role_type, role_match_map['fullstack'])
        # Company-fit highlights: add non-resume narrative hooks without inventing hard facts
        if 'theta' in company_lower:
            body2 = (
                f'{body2} '
                'What especially motivates me about Theta is your pragmatic consulting culture and focus on secure, mission-critical systems. '
                'I enjoy working closely with stakeholders, translating technical trade-offs clearly for non-technical audiences, '
                'and continuously improving engineering practices in fast-moving environments.'
            )
        if 'eroad' in company_lower:
            body2 = (
                f'{body2} '
                f'{_COMPANY_FIT_HOOKS["eroad"]["en"]} '
                f'{_WHY_ME_HOOKS["eroad"]["en"]}'
            )
        if 'l3harris' in company_lower:
            body2 = (
                f'{body2} '
                f'{_COMPANY_FIT_HOOKS["l3harris"]["en"]} '
                f'{_WHY_ME_HOOKS["l3harris"]["en"]}'
            )
        if company_lower.strip() == 'aut' or 'auckland university of technology' in company_lower:
            body2 = (
                f'{body2} '
                f'{_COMPANY_FIT_HOOKS["aut"]["en"]} '
                f'{_WHY_ME_HOOKS["aut"]["en"]}'
            )
        if pub_note and role_type == 'ai':
            body2 = f'{body2} {pub_note}'

        closing = (
            f'I am deeply grateful for the education and support I received at {company_name}, '
            f'and I sincerely hope to earn this opportunity to contribute in return. '
            f'I would welcome the opportunity to discuss how my experience can contribute to {company_name}.'
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

        # 第三段专注“岗位匹配能力”，避免与项目段重复
        role_match_map_zh = {
            'android': (
                '针对该岗位，我具备面向生产环境的 Android 交付经验，熟悉 API 集成、测试质量控制与 CI/CD 发布流程，'
                '并能与产品、设计和测试团队高效协作。'
            ),
            'backend': (
                '针对该岗位，我具备扎实的后端工程能力（Java/Spring/API/数据层），'
                '注重可维护性、稳定性与可持续交付。'
            ),
            'ai': (
                '针对该岗位，我具备 AI 工程端到端落地能力，能够在工程约束下平衡效果、性能与交付节奏。'
            ),
            'fullstack': (
                '针对该岗位，我具备前后端一体化交付能力，注重代码可维护性、自动化测试、代码评审与敏捷协作。'
                '我执行效率高、自我管理能力强，能在不确定需求下持续推进并稳定交付。'
            ),
        }
        body2 = role_match_map_zh.get(role_type, role_match_map_zh['fullstack'])
        company_lower = (company_name or '').lower()
        if 'theta' in company_lower:
            body2 = (
                f'{body2}'
                '我也非常认同 Theta 务实、以结果为导向的咨询文化，以及对关键系统安全性的重视。'
                '我擅长与业务和非技术干系人沟通技术取舍，并在快节奏环境中持续优化工程实践。'
            )
        if 'eroad' in company_lower:
            body2 = f'{body2}{_COMPANY_FIT_HOOKS["eroad"]["zh"]}{_WHY_ME_HOOKS["eroad"]["zh"]}'
        if 'l3harris' in company_lower:
            body2 = f'{body2}{_COMPANY_FIT_HOOKS["l3harris"]["zh"]}{_WHY_ME_HOOKS["l3harris"]["zh"]}'
        if company_lower.strip() == 'aut' or 'auckland university of technology' in company_lower:
            body2 = f'{body2}{_COMPANY_FIT_HOOKS["aut"]["zh"]}{_WHY_ME_HOOKS["aut"]["zh"]}'
        if pub_note and role_type == 'ai':
            body2 = f'{body2}{pub_note}'

        closing = (
            f'我期待有机会进一步探讨如何为 {company_name} 做出贡献。'
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
    today_dir = datetime.now().strftime('%Y-%m-%d')
    repo_root   = Path(__file__).parent.parent.parent
    outputs_dir = repo_root / 'outputs'
    outputs_dir.mkdir(exist_ok=True)
    dated_outputs_dir = outputs_dir / today_dir
    dated_outputs_dir.mkdir(exist_ok=True)

    if not output_path:
        safe_company = re.sub(r'[^a-zA-Z0-9_-]', '_', company_name)[:20]
        output_path = str(dated_outputs_dir / f'CoverLetter_{safe_company}_{today}.pdf')

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
    # 清理中间产物：HTML
    try:
        os.remove(html_path)
    except Exception:
        pass

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
