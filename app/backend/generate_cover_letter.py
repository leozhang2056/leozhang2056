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
import html

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
    'fintech': 'default',
    'photon': 'default',
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
        'fintech': {
            'en': 'Senior Software Engineer with 10+ years of experience delivering high-performance FinTech and industrial systems',
            'zh': '拥有 10 年以上高性能金融与工业系统开发经验的高级软件工程师',
        },
        'westpac': {
            'en': 'Senior Android Developer with 10+ years of experience building secure, high-scale mobile banking solutions',
            'zh': '拥有 10 年以上大规模安全移动银行应用开发经验的资深 Android 工程师',
        },
        'photon': {
        'en': 'Lead Android Developer with 10+ years of experience building high-scale mobile applications',
        'zh': '拥有 10 年以上大规模移动应用开发经验的资深 Android 负责人',
    },
}

# 公司共鸣叙事钩子（不写硬事实，避免与 JD/官网信息冲突）
_COMPANY_FIT_HOOKS = {
    'westpac': {
        'en': (
            "What resonates with me about Westpac is your commitment to 'helping Kiwis succeed' and your leadership in digital banking transformation. "
            "I value Westpac's focus on building secure, accessible, and high-quality mobile experiences that provide real financial value to customers. "
            "My own background in architecting reliability-focused Android systems and delivering secure mobile solutions for over 10 years aligns perfectly with Westpac's standards for safety and trust in financial technology."
        ),
    },
    'photon': {
        'en': (
            "What resonates with me about Photon is your commitment to high-standard mobile delivery and your 'customer-first' approach to engineering. "
            "I value the way Photon combines deep technical specialization with agile execution to ship mobile experiences that actually scale. "
            "My own background in building complex, reliability-focused Android systems for over 10 years aligns perfectly with the standards of excellence I see in Photon's projects."
        ),
    },
    'younity': {
        'en': (
            "What resonates with me about Younity is your focus on 'Real People, Real Outcomes.' "
            "As a Senior Software Engineer, I believe technical excellence only matters when it translates into meaningful impact for businesses and their users. "
            "I also value your commitment to community impact and sustainability, which reflects a professional culture of responsibility that I strive to uphold in my own work."
        ),
    },
    'halter': {
        'en': (
            "What resonates with me about Halter is your mission to improve how farmers operate day to day, with software that changes real behavior in the field rather than staying as a prototype. "
            "That reflects the kind of engineering values I care about: meaningful impact, high standards, and execution under real constraints. "
            "I also strongly identify with your culture of tackling hard problems with a high-performing team and shipping systems that are built to last."
        ),
        'zh': (
            "我与 Halter 的共鸣点在于：你们的产品不是停留在原型，而是持续改变农场一线的真实作业方式。"
            "这和我认同的工程价值观一致——做有意义的事、保持高标准、并在真实约束下稳定交付。"
            "我也非常认同你们“高绩效团队 + 挑战硬问题 + 长期可持续产品”的文化方向。"
        ),
    },
    'windcave': {
        'en': (
            'What resonates with me about Windcave is the combination of product depth and operational seriousness. '
            'Payments software sits close to real business risk, so mobile quality, integration discipline, and reliability '
            'matter in a very concrete way. I am motivated by engineering environments where stable releases, careful testing, '
            'and dependable user journeys are part of the product value, not just delivery hygiene.'
        ),
        'zh': (
            '鎴戜笌 Windcave 鐨勫叡楦ｇ偣鍦ㄤ簬锛屽畠鎶婁骇鍝佹繁搴﹀拰涓氬姟绋冲畾鎬х粨鍚堝湪浜嗕竴璧枫€?'
            '鏀粯绯荤粺闈㈠悜鐪熷疄浜ゆ槗鍦烘櫙锛屽洜姝ょЩ鍔ㄧ璐ㄩ噺銆侀泦鎴愮邯寰嬪拰鍙潬鎬ч兘鏄潪甯稿叧閿殑浠峰€笺€?'
            '鎴戝緢璁ゅ悓杩欑被宸ョ▼鐜锛氱ǔ瀹氬彂甯冦€佷弗璋ㄦ祴璇曞拰鍙俊鐢ㄦ埛浣撻獙锛屾湰韬氨鏄骇鍝佺珵浜夊姏鐨勪竴閮ㄥ垎銆?'
        ),
    },
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
    'atom': {
        'en': (
            "What resonates with me about ATOM Intelligence is your focus on vertical AI and data platforms "
            "that ship to real enterprise clients — not sandbox demos."
        ),
        'zh': (
            "我与 ATOM Intelligence 的共鸣在于：你们做的是面向真实企业客户的垂直 AI 与数据平台，而不是沙盒演示。"
        ),
    },
}

_WHY_ME_HOOKS = {
    'westpac': {
        'en': (
            "I believe I am a strong fit for this Senior Android Developer role because I combine deep technical expertise in Kotlin and Java with a disciplined approach to mobile security and reliability. "
            "My experience includes architecting robust Android apps using Jetpack Compose and MVVM, while ensuring high standards for accessibility and performance. "
            "I am particularly motivated by the opportunity to apply my 10+ years of delivery experience to help Westpac build trusted, innovative banking solutions in a high-performing Agile environment."
        ),
    },
    'photon': {
        'en': (
            "I believe I am a strong fit for this Lead Android Developer role because I combine deep technical expertise in Kotlin and Java with a proven track record of delivering end-to-end mobile solutions. "
            "My experience includes architecting robust Android apps using Jetpack Compose, RxJava, and MVVM, while ensuring high performance and screen-agnostic UI consistency. "
            "I am particularly motivated by the opportunity to apply my 10+ years of delivery experience to lead technical excellence and mentor teams in Photon's fast-paced, customer-focused environment."
        ),
    },
    'younity': {
        'en': (
            "I believe I am a strong fit for this FinTech opportunity because I combine deep technical expertise in .NET and Java with a focus on delivering scalable, greenfield platforms. "
            "My experience building high-scale messaging systems and industrial IoT solutions has taught me how to balance architectural purity with pragmatic delivery—ensuring that the technology serves the business's real-world needs. "
            "I am particularly motivated by the opportunity to contribute to scalable systems that require the high standards of reliability and performance essential for the FinTech sector."
        ),
    },
    'halter': {
        'en': (
            "I believe I am a particularly strong fit because I combine three capabilities that this role depends on: "
            "full-stack execution across mobile, backend, and AI integration; production-first delivery habits built through long-cycle systems; "
            "and comfort turning ambiguous requirements into reliable tools teams actually use every day. "
            "I am based in Auckland and value in-person collaboration, which aligns with Halter's office-first culture and the pace needed to ship high-quality internal AI tooling. "
            "I can contribute quickly by owning meaningful slices end-to-end while collaborating closely with product and cross-functional stakeholders."
        ),
        'zh': (
            "我之所以非常匹配这个岗位，是因为我同时具备三项关键能力："
            "跨移动端/后端/AI 集成的全栈交付能力；面向生产环境的长期稳定交付习惯；"
            "以及把模糊需求快速收敛为可用、可维护工具的能力。"
            "我目前在奥克兰，也认同并习惯高强度线下协作方式，这与 Halter 的 office-first 文化非常一致。"
            "我能在与产品及跨职能团队紧密协作的同时，端到端负责有价值的模块并快速产出结果。"
        ),
    },
    'windcave': {
        'en': (
            'I believe I can contribute well in this context because my Android experience has consistently involved more than UI delivery alone: '
            'I have worked across app architecture, backend integration, device-adjacent workflows, release pipelines, and production troubleshooting. '
            'That combination fits environments where mobile software must be maintainable, integration-friendly, and reliable under real usage.'
        ),
        'zh': (
            '鎴戣涓鸿嚜宸遍€傚悎杩欑被鍦烘櫙锛屽洜涓烘垜鐨?Android 缁忛獙涓嶅彧鏄仛鐣岄潰鍔熻兘锛?'
            '鑰屾槸闀挎湡鍚屾椂瑕嗙洊搴旂敤鏋舵瀯銆佸悗绔泦鎴愩€佽澶囩浉鍏虫祦绋嬨€佸彂甯冩祦姘村拰鐢熶骇闂闂幆銆?'
            '杩欑缁勫悎姝ｅソ閫傚悎瀵圭淮鎶ゆ€с€侀泦鎴愯兘鍔涘拰鍙潬鎬ф湁楂樿姹傜殑浜т笟绾у洟闃熴€?'
        ),
    },
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
}


# ---------------------------------------------------------------------------
# 核心逻辑
# ---------------------------------------------------------------------------

def _adapt_progression_title(title: str, role_type: str) -> str:
    """根据目标角色对职级标题进行微调。"""
    if role_type in ['android', 'westpac'] and 'Technical Lead' in title:
        return 'Technical Lead (Android Focus)'
    if role_type == 'ai' and 'Full-stack' in title:
        return 'AI/Full-stack Lead'
    return title

def _best_metrics(project: Dict) -> List[str]:
    """提取项目中的量化指标。"""
    metrics = []
    # 尝试从 highlights 中提取带数字的行
    for h in project.get('highlights', []) or []:
        if isinstance(h, str) and any(char.isdigit() for char in h):
            metrics.append(h)
    return metrics[:2]

def _build_jd_fit_hook(role_type: str, lang: str, jd_keywords: Optional[List[str]]) -> str:
    """基于 JD 关键词构建“为什么我适合”的钩子。"""
    if not jd_keywords:
        return ""
    
    kws = ", ".join(jd_keywords[:4])
    if lang == 'zh':
        return f"我注意到该职位对 {kws} 等方面有明确要求，这正是我长期深耕并具备成功交付经验的领域。"
    return f"I noticed that this role emphasizes {kws}, which are areas where I have consistently delivered high-quality production results."

def build_cover_letter_content(
    profile: Dict,
    achievements: Dict,
    all_projects: List[Dict],
    role_type: str,
    company_name: str,
    target_role_title: str,
    jd_keywords: Optional[List[str]],
    lang: str = 'en',
) -> Dict[str, str]:
    """组装 Cover Letter 的文本内容块。"""
    hint_text = _ROLE_NARRATIVE_HINT.get(role_type, _ROLE_NARRATIVE_HINT['fullstack'])[lang]
    top_projects = sort_projects(all_projects, role_type, jd_keywords, max_projects=2)
    
    # 收集核心论据
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

    def _opening_hook_text(_role_type: str, _lang: str) -> str:
        """开场钩子：首句先抓注意力，再进入岗位匹配。"""
        if _lang == 'zh':
            hook_map_zh = {
                'android': '我擅长把复杂业务需求快速落成稳定、可维护、可持续迭代的 Android 生产系统。',
                'backend': '我擅长把复杂业务规则落成高可用、可扩展、可长期演进的后端系统。',
                'ai': '我擅长把 AI 方案从原型推进到可运行、可评估、可持续迭代的工程形态。',
                'fullstack': '我擅长把模糊需求收敛为可上线、可运维的端到端系统交付。',
            }
            return hook_map_zh.get(_role_type, hook_map_zh['fullstack'])
        hook_map_en = {
            'android': 'I turn complex product requirements into stable Android systems that hold up in production.',
            'backend': 'I turn complex business requirements into reliable backend systems that scale and remain maintainable.',
            'ai': 'I turn AI ideas into production-ready workflows that are runnable, measurable, and iteratively improved.',
            'fullstack': 'I turn ambiguous requirements into production-ready end-to-end systems teams can rely on.',
        }
        return hook_map_en.get(_role_type, hook_map_en['fullstack'])

    # Thesis / publication highlight
    pubs = achievements.get('publications', [])
    pub_note = ''
    if pubs:
        first_pub = pubs[0]
        pub_note_en = (f'My Master\'s thesis "{first_pub.get("title", "")}" '
                       f'({first_pub.get("venue", "")}, {first_pub.get("year", "")}) '
                       f'demonstrates my ability to independently design, build, and evaluate AI systems.')
        pub_note = pub_note_en if lang == 'en' else ""

    if lang == 'en':
        opening_hook = _opening_hook_text(role_type, 'en')
        jd_fit_hook = _build_jd_fit_hook(role_type, 'en', jd_keywords)
        if "years" in hint_text.lower():
            opening = (
                f'{opening_hook} '
                f'I am excited to apply for the {target_role_title} position at {company_name}. '
                f'This role is a strong fit for my background as a {hint_text}. '
                f'I am especially drawn to teams where product quality, integration discipline, and long-term maintainability matter in production. '
                f'{jd_fit_hook}'.strip()
            )
        else:
            opening = (
                f'{opening_hook} '
                f'I am excited to apply for the {target_role_title} position at {company_name}. '
                f'This role is a strong fit for my background as a {hint_text} with {years_str} years of delivery experience. '
                f'I am especially drawn to teams where product quality, integration discipline, and long-term maintainability matter in production. '
                f'{jd_fit_hook}'.strip()
            )

        proj1 = top_projects[0] if top_projects else {}
        proj2 = top_projects[1] if len(top_projects) > 1 else {}
        proj1_name = proj1.get('name', '')
        proj2_name = proj2.get('name', '')
        proj1_evidence = evidence_lines[0] if evidence_lines else ''
        proj2_evidence = evidence_lines[1] if len(evidence_lines) > 1 else ''

        company_lower = (company_name or '').lower()
        if role_type == 'android':
            body1 = (
                'I have built and maintained Android applications in complex production environments using '
                'Kotlin/Java, Android SDK, Jetpack components, MVVM architecture, and REST API integration. '
                + (f'In {proj1_name}, {proj1.get("highlights", ["I delivered end-to-end Android implementation and release workflows"])[0].lower()}. '
                   if proj1_name else '')
                + (f'In {proj2_name}, {proj2.get("highlights", ["I improved mobile reliability and maintainability through iterative engineering practices"])[0].lower()}.'
                   if proj2_name else '')
            )
        elif company_lower == 'younity':
            body1 = (
                f"Throughout my career, I have prioritized the delivery of stable, high-performance systems that meet demanding business requirements. "
                "In my recent role, I architected and deployed a microservices-based industrial platform that improved operational efficiency by over 30% across multiple sites. "
                "I also have extensive experience in high-scale messaging systems, where I engineered backends supporting 500K+ daily messages with sub-200ms latency, "
                "ensuring that the technology remains robust and reliable under heavy production load."
            )
        elif company_lower == 'westpac':
            body1 = (
                f"With over 10 years of experience in mobile engineering, I have developed a disciplined approach to building secure and stable Android applications. "
                "In my recent work, I have delivered robust solutions using Kotlin, Java, and Jetpack Compose, ensuring high standards for performance and reliability. "
                "My experience includes architecting mobile platforms that support large user bases, optimizing app performance to achieve significant crash reductions, "
                "and implementing secure communication protocols (SSL/TLS, certificate management) essential for high-stakes financial environments."
            )
        elif company_lower == 'photon':
            body1 = (
                f"With over 10 years of experience in mobile development, I have a deep understanding of building and leading high-scale Android applications. "
                "Throughout my recent projects, I have successfully delivered robust mobile solutions using Kotlin, Java, and Jetpack Compose, focusing on scalable architecture and UI excellence. "
                "My experience leading the migration of legacy components to modern MVVM patterns, optimizing memory usage to reduce crash rates, "
                "and implementing automated CI/CD pipelines with Jenkins and Bitbucket demonstrates my commitment to high-standard engineering and sustainable delivery."
            )
        else:
            body1 = (
                f'In my most recent work, {proj1_name}, I served as {proj1.get("role", "sole developer")} '
                f'and delivered a complete solution from design through deployment. '
                + (f'{proj1_evidence}. ' if proj1_evidence else '')
                + (f'Additionally, through {proj2_name}, I {proj2.get("highlights", ["built and maintained a production system"])[0].lower() if proj2 else ""}.'
                   if proj2_name else '')
            )
        
        if company_lower.strip() == 'aut' or 'auckland university of technology' in company_lower:
            body1 = (
                "At AUT, I completed my Master's in Computer and Information Sciences with First Class Honours, "
                "where I strengthened my practical knowledge across software architecture, AI applications, "
                "integration workflows, and production-oriented delivery. "
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
        
        if 'theta' in company_lower:
            body2 = (
                f'{body2} '
                'What especially motivates me about Theta is your pragmatic consulting culture and focus on secure, mission-critical systems. '
                'I enjoy working closely with stakeholders, translating technical trade-offs clearly for non-technical audiences, '
                'and continuously improving engineering practices in fast-moving environments.'
            )
        if 'eroad' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["eroad"]["en"]} {_WHY_ME_HOOKS["eroad"]["en"]}'
        if 'windcave' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["windcave"]["en"]} {_WHY_ME_HOOKS["windcave"]["en"]}'
        if 'halter' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["halter"]["en"]} {_WHY_ME_HOOKS["halter"]["en"]}'
        if 'l3harris' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["l3harris"]["en"]} {_WHY_ME_HOOKS["l3harris"]["en"]}'
        if company_lower.strip() == 'aut' or 'auckland university of technology' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["aut"]["en"]} {_WHY_ME_HOOKS["aut"]["en"]}'
        if 'atom' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["atom"]["en"]} {_WHY_ME_HOOKS["atom"]["en"]}'
        if 'photon' in company_lower:
            body2 = f'{body2} {_COMPANY_FIT_HOOKS["photon"]["en"]} {_WHY_ME_HOOKS["photon"]["en"]}'

        closing_map = {
            'android': (
                f'I would welcome the opportunity to discuss how my Android delivery background, integration experience, and reliability-focused habits can contribute to {company_name}. '
                'Thank you for your time and consideration.'
            ),
            'backend': (
                f'I would welcome the opportunity to discuss how my backend engineering depth, API design experience, and reliability-focused delivery habits can contribute to {company_name}. '
                'Thank you for your time and consideration.'
            ),
            'ai': (
                f'I would welcome the opportunity to discuss how my AI engineering practice, full-stack implementation experience, and production-focused delivery habits can contribute to {company_name}. '
                'Thank you for your time and consideration.'
            ),
            'fullstack': (
                f'I would welcome the opportunity to discuss how my full-stack delivery experience, integration discipline, and reliability-focused execution can contribute to {company_name}. '
                'Thank you for your time and consideration.'
            ),
            'photon': (
                f'I would welcome the opportunity to discuss how my Lead Android delivery background, Jetpack Compose experience, and commitment to high-quality mobile architecture can contribute to Photon. '
                'Thank you for your time and consideration.'
            ),
            'westpac': (
                f'I would welcome the opportunity to discuss how my Senior Android delivery background, security focus, and commitment to reliable banking architecture can contribute to Westpac. '
                'Thank you for your time and consideration.'
            ),
        }
        closing = closing_map.get(role_type, closing_map['fullstack'])

    else:  # zh fallback
        opening = "申请自荐信内容（中文）"
        body1 = "核心项目与经验描述"
        body2 = "岗位匹配度描述"
        closing = "期待面试回复"

    return {
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
    kb_data: Optional[Dict] = None,
) -> str:
    """生成 Cover Letter 的 HTML 字符串。"""
    if kb_data is None:
        from kb_loader import KBLoader
        loader = KBLoader(Path(os.getcwd()))
        kb_data_obj = loader.load_all()
        # Convert dataclass to dict if necessary for the rest of the function
        # But wait, build_cover_letter_content might expect the old structure.
        kb_data = {
            'profile': kb_data_obj.profile.__dict__,
            'achievements': kb_data_obj.achievements.__dict__,
            'projects': [p.__dict__ for p in kb_data_obj.projects],
            'relations': kb_data_obj.relations,
        }
    
    profile = kb_data.get('profile', {})
    achievements = kb_data.get('achievements', {})
    all_projects = kb_data.get('projects', [])
    
    content = build_cover_letter_content(
        profile, achievements, all_projects,
        role_type, company_name, target_role_title, jd_keywords, lang,
    )
    
    name = profile.get('name', 'Leo Zhang')
    email = profile.get('contact', {}).get('email', '')
    phone = profile.get('contact', {}).get('phone', '')
    date_str = datetime.now().strftime("%d %B %Y")
    
    html_template = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>Cover Letter - {name}</title>
    <style>{_CL_CSS}</style>
</head>
<body>
    <div class="cl-header">
        <div class="cl-name">{html.escape(name)}</div>
        <div class="cl-contact">{html.escape(email)} | {html.escape(phone)}</div>
    </div>

    <div class="cl-date">{date_str}</div>

    <div class="cl-recipient">
        Hiring Manager<br>
        {html.escape(company_name)}
    </div>

    <div class="cl-salutation">Dear Hiring Manager,</div>

    <div class="cl-body">
        <p>{html.escape(content['opening'])}</p>
        <p>{html.escape(content['body1'])}</p>
        <p>{html.escape(content['body2'])}</p>
        <p>{html.escape(content['closing'])}</p>
    </div>

    <div class="cl-sign">
        <div class="cl-sign-label">Sincerely,</div>
        <div class="cl-sign-name">{html.escape(name)}</div>
    </div>
</body>
</html>"""
    return html_template


async def generate_cover_letter(
    role_type: str = 'fullstack',
    lang: str = 'en',
    company_name: str = 'the company',
    target_role_title: str = 'Software Engineer',
    jd_keywords: Optional[List[str]] = None,
    output_path: Optional[str] = None,
) -> str:
    """主入口：生成 PDF 文件。"""
    html_content = generate_cover_letter_html(
        role_type, lang, company_name, target_role_title, jd_keywords
    )
    
    if not output_path:
        today = datetime.now().strftime("%Y-%m-%d")
        safe_company = re.sub(r'[^a-zA-Z0-9]+', '_', company_name).strip('_')
        filename = f"CoverLetter_{safe_company}_{datetime.now().strftime('%Y%m%d')}.pdf"
        output_path = os.path.join("outputs", today, filename)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 也保存一个 HTML 副本方便调试
    html_path = output_path.replace(".pdf", ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  HTML → {html_path}")
    
    await html_to_pdf(html_content, output_path)
    print(f"  PDF  → {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--role', default='fullstack', choices=['android', 'ai', 'backend', 'fullstack', 'fintech', 'idexx', 'nateva', 'photon', 'westpac'])
    parser.add_argument('--lang', default='en', choices=['en', 'zh'])
    parser.add_argument('--company', default='the company')
    parser.add_argument('--title', default='Software Engineer')
    parser.add_argument('--jd-keywords', nargs='*')
    parser.add_argument('--output', default=None)
    args = parser.parse_args()

    asyncio.run(generate_cover_letter(
        args.role, args.lang, args.company, args.title, args.jd_keywords, args.output
    ))
