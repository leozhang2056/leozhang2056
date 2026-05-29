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


_DIFFERENTIATOR_HOOKS = {
    'ai': {
        'en': (
            "I also do the engineering side properly — clean code, testing, CI/CD, API design. "
            "I don't just understand models; I can build the pipeline around them."
        ),
    },
    'android': {
        'en': (
            "What sets me apart is breadth: I've shipped Android apps that talk to hardware, "
            "microservices, and cloud backends — not just standalone UIs. I understand the full stack "
            "my mobile code lives in, which means fewer integration surprises and faster delivery."
        ),
    },
    'backend': {
        'en': (
            "What sets me apart is that I bring full-stack awareness to backend delivery — I've built "
            "APIs that mobile and frontend teams actually enjoy consuming, and I design data contracts "
            "before writing implementation code. That comes from 10+ years working across layers."
        ),
    },
    'fullstack': {
        'en': (
            "What sets me apart is that I've delivered across Android, Java backends, Vue.js frontends, "
            "and AI/ML integrations — which means I can own a feature from database to UI without handovers. "
            "In fast-moving teams, that reduces dependencies and speeds up iteration."
        ),
    },
    'westpac': {
        'en': (
            "What sets me apart is my combination of Android depth and full-stack awareness: "
            "I've architected secure mobile platforms, optimized performance at scale, and implemented "
            "SSL/TLS communication protocols essential for financial environments — all while delivering "
            "clean, maintainable code that teams can build on."
        ),
    },
    'photon': {
        'en': (
            "What sets me apart is my track record leading Android migrations and modernisation: "
            "I've taken legacy architectures to MVVM, reduced crash rates through memory optimisation, "
            "and automated CI/CD pipelines — delivering measurable quality improvements while maintaining "
            "release velocity."
        ),
    },
}


def _differentiator_hook(role_type: str) -> str:
    """返回"为什么面试你"差异段落。"""
    return _DIFFERENTIATOR_HOOKS.get(role_type, {}).get("en", "")


# ---------------------------------------------------------------------------
# 公司信息映射（用于 generic 生成器）
# ---------------------------------------------------------------------------

_COMPANY_CULTURE_HOOKS = {
    'the warehouse group': "it focuses on building practical AI solutions that deliver measurable business impact.",
    'westpac': "it builds financial tools that millions of New Zealanders rely on with confidence.",
    'halter': "it builds AI and software that changes how farmers actually operate — real tools used in the field.",
    'eroad': "it turns complex telematics data into reliable tools that fleets depend on daily.",
    'windcave': "payments infrastructure sits at the intersection of reliability, security, and scale.",
    'l3harris': "engineering is defined by mission-critical delivery, not feature velocity.",
    'aut': "'knowledge that works' defines both research and teaching.",
    'atom': "it ships AI to real enterprise clients — not sandbox demos.",
    'photon': "it ships quality mobile experiences at scale for global clients.",
    'younity': "it focuses on 'Real People, Real Outcomes' in financial technology.",
    'theta': "it combines technical depth with pragmatic delivery in consulting.",
    'catch design': "it creates meaningful, inclusive, and impactful digital experiences for New Zealand's most recognised brands.",
    'catch': "it creates meaningful, inclusive, and impactful digital experiences for New Zealand's most recognised brands.",
    'henry schein one': "it is redefining dental care through intelligent practice management and AI-driven treatment.",
    'henry schein': "it is redefining dental care through intelligent practice management and AI-driven treatment.",
    'dexibit': "it helps visitor attractions make sense of their data through AI — from museums to zoos to theme parks.",
    'accesso': "it serves over 1,000 venues across 30+ countries with technology that enhances the guest experience.",
    'visa': "it operates the world's most sophisticated payment processing network, handling 65k+ secure transactions per second across 200+ countries.",
    'whip around': "it is a Kiwi SaaS company helping fleets work smarter, safer, and more efficiently, now entering an exciting growth chapter with Accel-KKR investment.",
    'vista group': "it powers the moviegoer experience with innovative cinema software solutions used globally.",
    'kami': "it is an award-winning EdTech startup helping over 30 million teachers and students worldwide create more interactive learning experiences.",
    'engflow': "it helps developers save time by accelerating software builds and tests through distributed remote execution and caching.",
    'digital generationz': "it is an agile digital venture building cutting-edge web infrastructure, automated media pipelines, and next-gen platform concepts.",
    'enable': "it simplifies pricing and rebate management with an intelligent, AI-powered platform used by companies globally.",
    'vector': "it is powering a smarter, cleaner energy future through cloud-native data platforms and AWS serverless technology.",
    'vts': "it is building the Diverge platform — a cloud-native energy data platform co-developed with AWS.",
}

_COMPANY_TEAMS = {
    'the warehouse group': "The Warehouse Group's Data and AI team",
    'westpac': "Westpac's mobile engineering team",
    'halter': "Halter's engineering team",
    'eroad': "EROAD's platform team",
    'windcave': "Windcave's engineering team",
    'l3harris': "L3Harris's software team",
    'aut': "AUT's technology team",
    'atom': "ATOM Intelligence's AI team",
    'photon': "Photon's Android team",
    'younity': "Younity's engineering team",
    'theta': "Theta's consulting team",
    'catch design': "Catch Design's development team",
    'catch': "Catch Design's development team",
    'henry schein one': "Henry Schein One's development team",
    'henry schein': "Henry Schein One's development team",
    'dexibit': "Dexibit's engineering team",
    'accesso': "accesso's engineering team",
    'visa': "Visa Spend Clarity's engineering team",
    'whip around': "Whip Around's engineering team",
    'vista group': "Vista Group's engineering team",
    'kami': "Kami's engineering team",
    'engflow': "EngFlow's engineering team",
    'digital generationz': "Digital Generationz's engineering team",
    'vector nz': "Vector Technology Services (VTS) engineering team",
    'vector': "Vector Technology Services (VTS) engineering team",
    'vts': "Vector Technology Services (VTS) engineering team",
    'enable': "Enable's engineering team",
}

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
    """组装 Cover Letter 的文本内容块。

    结构（2026-05）：
      opening = 寒暄问候 + 认同公司文化
      body1   = 竞争力亮点（证据 + 差异化合并）
      body2   = 在贵公司的展望作用
      closing = Thank you.
    """
    # Role-based default title fallback
    if not target_role_title or target_role_title == 'Software Engineer':
        role_title_defaults = {
            'ai': 'AI Engineer',
            'android': 'Senior Android Developer',
            'backend': 'Senior Backend Engineer',
            'fullstack': 'Full-stack Engineer',
            'westpac': 'Senior Android Developer',
            'photon': 'Lead Android Developer',
        }
        target_role_title = role_title_defaults.get(role_type, target_role_title or 'Software Engineer')

    top_projects = sort_projects(all_projects, role_type, jd_keywords, max_projects=1)
    proj = top_projects[0] if top_projects else {}
    proj_name = proj.get('name', proj.get('project_id', ''))
    proj_role = proj.get('role', 'developer')
    proj_highlights = [h for h in (proj.get('highlights', []) or []) if isinstance(h, str)]

    # 总年限
    tagline = profile.get('career_identity', {}).get('tagline', '')
    years_match = re.search(r'(\d+)\+?\s*years?', tagline, re.IGNORECASE)
    years_raw = f"{years_match.group(1)}+" if years_match else "10+"
    years_str = years_raw.rstrip("+") if years_raw.endswith("+") else years_raw

    # Thesis / publication
    pubs = achievements.get('publications', [])
    thesis_project = proj if any(kw in (proj.get('project_id', '') or '').lower()
                                  for kw in ['thesis', 'publication']) else {}

    if lang == 'en':
        # Company-specific hand-crafted version (best quality)
        company_lower = (company_name or '').strip().lower()
        is_twg = 'the warehouse' in company_lower or 'warehouse group' in company_lower
        is_twg = is_twg or ('twg' in company_lower)

        if role_type == 'ai' and is_twg:
            opening = (
                "I am applying for the AI Engineer (Graduate) position at The Warehouse Group. "
                "With a background spanning AI research, full-stack development, Android systems, "
                "and industrial IoT platforms, I am particularly interested in this opportunity "
                "because it focuses on building practical AI solutions that deliver measurable business impact."
            )
            body1 = (
                "I recently completed my Master of Computer and Information Sciences at Auckland University "
                "of Technology with First Class Honours. My thesis project, ChatClothes, involved designing "
                "and building a multimodal AI system that combined diffusion models, garment classification, "
                "local LLM integration, and workflow orchestration into a working end-to-end prototype. "
                "The project was accepted by IVCNZ 2025 and gave me hands-on experience developing AI systems "
                "that balance research innovation with usability, maintainability, and deployment considerations."
            )
            body2 = (
                "What particularly attracted me to this role is The Warehouse Group's emphasis on moving AI "
                "solutions from prototype to production. In addition to my academic AI work, I bring more than "
                "10 years of software engineering experience across Android, backend, and real-time IoT systems. "
                "I have worked with APIs, cloud-connected services, CI/CD workflows, Docker-based deployments, "
                "and scalable production systems supporting real users and operational environments. This background "
                "has helped me develop a practical engineering mindset focused on reliability, collaboration, "
                "and continuous improvement."
            )
            closing = (
                "I am also highly motivated by the opportunity to work within a collaborative AI capability "
                "where learning, experimentation, and rapid delivery are encouraged. I enjoy working across "
                "technical and business contexts, translating ideas into working solutions, and continuously "
                "learning new tools and frameworks as AI technologies evolve. "
                "I would welcome the opportunity to contribute my technical background, problem-solving ability, "
                "and hands-on development experience to The Warehouse Group's Data and AI team. "
                "Thank you for your time and consideration."
            )
        elif 'catch' in company_lower or 'catch design' in company_lower:
            opening = (
                "I am applying for the Senior Full-Stack Developer position at Catch Design. "
                "I am a full-stack software engineer with 10+ years of experience delivering "
                "end-to-end solutions across backend services, mobile applications, and web frontends, "
                "and I recently completed my Master of Computer and Information Sciences at AUT "
                "with First Class Honours. "
                "I am particularly interested in Catch Design because it creates meaningful, inclusive, "
                "and impactful digital experiences for New Zealand's most recognised brands."
            )
            body1 = (
                "What I enjoy most about full-stack development is owning a feature from database "
                "to UI — designing the data model, building the API, wiring the business logic, "
                "and shaping the user interface into something people actually use. "
                "My recent work on an Enterprise Messaging Platform is a good example: "
                "I engineered the NDK TCP/UDP transport layer handling sub-200ms latency for 5,000 DAU, "
                "while also building the Android client, coordinating with backend teams on API contracts, "
                "and delivering the full feature set across the stack. "
                "Earlier in my career I also built and maintained WordPress-based websites (2013–2015), "
                "which gave me early exposure to CMS workflows, theme customisation, and the iterative "
                "nature of web delivery."
            )
            body2 = (
                "What particularly attracts me to Catch Design is the emphasis on cross-functional "
                "collaboration with designers, strategists, and project managers — that reflects how "
                "I naturally work. I have contributed to technical scoping, estimation, and solution "
                "architecture across multiple client-facing projects, and I enjoy translating business "
                "requirements into maintainable, scalable applications. "
                "With a background spanning Java, .NET, Python, Node.js, React, Vue.js, and Android, "
                "I bring the breadth to contribute across Catch's full technology stack while also "
                "deepening expertise in areas like cloud infrastructure, CI/CD, and automated testing."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056) and my "
                "portfolio (github.com/leozhang2056#-featured-projects), including my Master's thesis "
                "project ChatClothes — an AI virtual try-on system — which was accepted at IVCNZ 2025. "
                "I would welcome the opportunity to contribute my technical background, full-stack "
                "experience, and collaborative mindset to Catch Design's development team. "
                "Thank you for your time and consideration."
            )
        elif 'henry schein' in company_lower:
            opening = (
                "I am applying for the Senior Developer position at Henry Schein One. "
                "I am a backend software engineer with 10+ years of experience designing, building, "
                "and maintaining production systems in C#/.NET and Java, and I recently completed "
                "my Master of Computer and Information Sciences at AUT with First Class Honours. "
                "I am particularly interested in Henry Schein One because it is redefining dental care "
                "through intelligent practice management and AI-driven treatment."
            )
            body1 = (
                "What draws me to this role is the emphasis on solving real problems rather than "
                "simply taking tickets — that is how I have always worked. Across my career I have "
                "delivered full-stack solutions in .NET, Spring Cloud, and Android environments, "
                "from low-level NDK transport layers handling sub-200ms latency for 5,000 DAU to "
                "microservice backends supporting smart factory operations across 10+ sites. "
                "I have worked extensively with SQL Server, MySQL, and PostgreSQL, and I bring "
                "deep experience with CI/CD pipelines, code review, and mentoring less experienced "
                "engineers through technical guidance and architectural decisions."
            )
            body2 = (
                "Henry Schein One's blend of modern tools (.NET, C#, Azure) with legacy system "
                "modernisation particularly appeals to me — I have spent years working across both "
                "new platforms and established codebases, and I understand the discipline required "
                "to improve a product incrementally without breaking what customers depend on. "
                "I also share the company's value that 'Each Person is as Important as the Next', "
                "and I have consistently fostered open communication and collaboration in every team "
                "I have been part of."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my technical background, .NET experience, "
                "and collaborative mindset to Henry Schein One's development team. "
                "Thank you for your time and consideration."
            )
        elif 'dexibit' in company_lower or 'accesso' in company_lower:
            opening = (
                "I am applying for the Senior Software Engineer position at accesso (Dexibit). "
                "I am a full-stack software engineer with 10+ years of experience across Java, Python, "
                "TypeScript, and React, and I recently completed my Master of Computer and Information "
                "Sciences at AUT with First Class Honours — where my thesis focused on AI-driven "
                "virtual try-on using diffusion models and LLM integration. "
                "I am particularly interested in Dexibit because it helps visitor attractions make "
                "sense of their data through AI, and I love the combination of deep data engineering "
                "with agentic interfaces that real users interact with."
            )
            body1 = (
                "What excites me about this role is the depth of the technical problems — from "
                "streaming and context window management to tool orchestration and sandboxed execution. "
                "In my Master's project ChatClothes I built exactly this kind of system: an AI agent "
                "that orchestrated ComfyUI workflows, managed local LLM context, and exposed "
                "a FastAPI interface for real-time inference. Before that, I engineered production "
                "systems handling 5,000 DAU with sub-200ms messaging latency, and smart factory "
                "platforms across 10+ sites using Java microservices, PostgreSQL, and cloud-native "
                "infrastructure on AWS and Docker."
            )
            body2 = (
                "I am particularly drawn to Dexibit's product-minded culture — the emphasis on "
                "understanding the 'why', breaking complex problems into simple solutions, and "
                "mentoring naturally through design decisions and code review. "
                "That reflects exactly how I work. I also value the team's use of modern AI tooling "
                "(Claude Code, Codex) in daily development, which aligns with my own workflow."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056), "
                "including the ChatClothes project which demonstrates full-stack AI system delivery "
                "from model orchestration to web interface. "
                "I would welcome the opportunity to contribute my technical depth, product-minded approach, "
                "and collaborative mindset to Dexibit's engineering team. "
                "Thank you for your time and consideration."
            )
        elif 'visa' in company_lower:
            opening = (
                "I am applying for the Full Stack Senior Developer position at Visa Spend Clarity. "
                "I am a full-stack software engineer with 10+ years of experience building production "
                "systems in .NET, C#, Java, and React, and I recently completed my Master of Computer "
                "and Information Sciences at AUT with First Class Honours. "
                "I am particularly interested in Visa because it operates the world's most sophisticated "
                "payment processing network, and I want to contribute to building scalable, reliable "
                "financial technology that impacts billions of people."
            )
            body1 = (
                "This role's focus on .NET, C#, React, and AWS cloud-native development maps directly "
                "to my experience. I have delivered enterprise .NET systems including a SaaS platform "
                "serving 10+ manufacturing sites with SQL Server backend and REST APIs, and I have "
                "contributed to React and TypeScript frontends with CI/CD pipelines on AWS. "
                "I practise TDD, code review, and SOLID principles as part of my daily workflow, "
                "and I have mentored engineers through technical guidance and architectural decisions "
                "across multiple teams."
            )
            body2 = (
                "What particularly attracts me to this role is Visa's emphasis on technical excellence "
                "combined with product-minded delivery. I thrive in cross-functional scrum teams where "
                "I can own features end-to-end — from technical design and API contracts through to "
                "testing, deployment, and production support. "
                "I also bring experience working in regulated enterprise environments and balancing "
                "commercial considerations with robust engineering practices."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my .NET full-stack expertise, "
                "cloud development experience, and collaborative mindset to Visa Spend Clarity's "
                "engineering team. "
                "Thank you for your time and consideration."
            )
        elif 'whip' in company_lower:
            opening = (
                "I am applying for the Full Stack Engineer position at Whip Around. "
                "I am a full-stack software engineer with 10+ years of experience building "
                "production web applications using React, TypeScript, Java, Python, and .NET, "
                "and I recently completed my Master of Computer and Information Sciences at AUT "
                "with First Class Honours. "
                "I am particularly interested in Whip Around because it is a Kiwi SaaS company "
                "entering an exciting growth chapter, and I want to help shape what's next — from "
                "new product experiences to scalable systems and AI-driven improvements."
            )
            body1 = (
                "What draws me to this role is the emphasis on product impact and developer empowerment "
                "rather than just sprint delivery. Throughout my career I have shipped full-stack features "
                "that real users depend on daily — from an enterprise messaging platform handling 5,000 DAU "
                "with sub-200ms latency, to IoT dashboards serving factory operators across 10+ sites. "
                "I bring strong React and TypeScript experience on the front end, and while I have not "
                "worked professionally with PHP/Laravel, I have deep backend experience in Java, Python, "
                "C#/.NET, and Node.js, and I am confident picking up new languages and frameworks quickly."
            )
            body2 = (
                "I am particularly excited about Whip Around's investment in AI (generative + agentic) "
                "to improve both product and developer experience — my Master's thesis involved building "
                "an AI agent that orchestrated diffusion models and LLMs, and I use AI coding tools "
                "(Claude Code, Copilot) daily in my development workflow. "
                "I also share the team's values of growth, ownership, and manaakitanga, and I thrive "
                "in environments where engineers are encouraged to experiment, improve systems, and "
                "solve real customer problems."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056), "
                "including full-stack projects and my AI thesis work. "
                "I would welcome the opportunity to contribute my full-stack experience, "
                "product-minded approach, and builder mentality to Whip Around's engineering team. "
                "Thank you for your time and consideration."
            )
        elif 'vista' in company_lower:
            opening = (
                "I am applying for the Graduate Software Engineer position at Vista Group. "
                "I recently completed my Master of Computer and Information Sciences at Auckland "
                "University of Technology with First Class Honours, where my thesis focused on "
                "building an AI-driven virtual try-on system accepted at IVCNZ 2025. "
                "I am particularly interested in Vista Group because it powers the moviegoer "
                "experience with innovative cinema software used globally, and I want to apply "
                "my technical skills in a collaborative, product-focused team."
            )
            body1 = (
                "During my Master's I designed and built ChatClothes, a full-stack AI system "
                "combining diffusion models, LLM integration, and a FastAPI backend with React "
                "frontend — giving me hands-on experience with Python, TypeScript, REST APIs, "
                "and cloud deployment on AWS. I also bring prior industry experience across "
                "C#/.NET, SQL Server, Java, and React from 10+ years of software engineering, "
                "which means I can contribute meaningfully from day one while continuing to "
                "learn and grow within Vista's tech stack."
            )
            body2 = (
                "What attracts me to Vista Group is the culture of 'good things with good people' "
                "and the shared standards of One Crew, Make it Happen, and Chase Great. "
                "I value strong mentoring and career development, and I am genuinely excited "
                "about the opportunity to work with C#, .NET, React, and cloud technologies "
                "in a domain as creative and impactful as cinema technology."
            )
            closing = (
                "Examples of my work, including ChatClothes, are available on GitHub "
                "(github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my technical skills, fresh "
                "perspective, and collaborative mindset to Vista Group's engineering team. "
                "Thank you for your time and consideration."
            )
        elif 'kami' in company_lower:
            opening = (
                "I am applying for the Senior Full-Stack Developer position at Kami. "
                "I am a full-stack software engineer with 10+ years of experience building "
                "web applications using JavaScript, TypeScript, React, Vue.js, Java, and Python, "
                "and I recently completed my Master of Computer and Information Sciences at AUT "
                "with First Class Honours. "
                "I am particularly interested in Kami because it is an award-winning EdTech startup "
                "that helps over 30 million teachers and students worldwide, and I want to contribute "
                "to a product that makes a real difference in education."
            )
            body1 = (
                "This role's emphasis on front-end engineering with product sense aligns closely "
                "with my strengths. I have built large single-page applications using React and Vue.js, "
                "worked extensively with JavaScript, TypeScript, HTML, and CSS, and profiled and "
                "optimised front-end performance using Chrome Developer Tools. "
                "On the backend side, I bring Java, Python, Node.js, PostgreSQL, and REST API design "
                "experience — so I can contribute across the full stack while leaning into the "
                "front-end depth this role requires."
            )
            body2 = (
                "What particularly attracts me to Kami is the culture of talking directly to customers "
                "and designing solutions based on real user needs — not just implementing spec sheets. "
                "Throughout my career I have worked closely with product teams and end users to shape "
                "features, and I thrive in environments where engineers are trusted to make product "
                "decisions. "
                "Kami's mission of helping educators create better learning outcomes resonates with me, "
                "and I would be proud to work on technology that reaches millions of students and teachers."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my front-end depth, full-stack breadth, "
                "and product-minded approach to Kami's engineering team. "
                "Thank you for your time and consideration."
            )
        elif 'engflow' in company_lower:
            opening = (
                "I am applying for the Implementation Engineer position at EngFlow. "
                "I am a software engineer with 10+ years of experience building and optimising "
                "complex systems across Java, Python, and C#/.NET, with deep expertise in "
                "Linux environments, Docker, AWS, and CI/CD pipelines. "
                "I am particularly interested in EngFlow because it helps developers save time "
                "by accelerating builds and tests — a problem I have personally experienced "
                "and cared about throughout my career."
            )
            body1 = (
                "In my previous roles, I have been responsible for developer workflows, build "
                "pipeline optimisation, and cross-team technical coordination. I have implemented "
                "CI/CD pipelines with Jenkins, Docker, and GitHub Actions, managed Linux-based "
                "production infrastructure, and mentored engineers on build practices and tooling. "
                "While I have not worked directly with Bazel, I have strong experience with "
                "build systems (Maven, Gradle, MSBuild) and a deep understanding of the "
                "challenges EngFlow solves — slow builds, dependency management, distributed "
                "caching, and developer productivity."
            )
            body2 = (
                "What attracts me to this role is the blend of technical depth and customer "
                "engagement. I enjoy troubleshooting complex issues, writing clear documentation, "
                "and helping teams adopt better practices — I have regularly partnered with "
                "product, QA, and operations teams to plan releases, manage risk, and improve "
                "delivery predictability. "
                "EngFlow's fully remote culture and async communication style also align well "
                "with how I work effectively across distributed teams."
            )
            closing = (
                "I would welcome the opportunity to contribute my technical breadth, customer-focused "
                "mindset, and passion for developer productivity to EngFlow's team. "
                "Thank you for your time and consideration."
            )
        elif 'vector' in company_lower or 'vts' in company_lower:
            opening = (
                "I am applying for the Senior Software Developer position at Vector Technology Services. "
                "I am a backend software engineer with 10+ years of experience building production "
                "systems in Java, Spring Cloud, and AWS, and I recently completed my Master of "
                "Computer and Information Sciences at AUT with First Class Honours. "
                "I am particularly interested in VTS because it is building the Diverge platform — "
                "a cloud-native energy data platform co-developed with AWS — and I want to contribute "
                "to meaningful work that powers a smarter, cleaner energy future."
            )
            body1 = (
                "This role's focus on Java, Spring, and AWS serverless technologies maps directly "
                "to my core expertise. I have architected and delivered Spring Cloud microservices "
                "for smart factory platforms across 10+ sites, designed REST APIs with database-backed "
                "workflows, and deployed containerised applications on AWS. "
                "I practise TDD, CI/CD, and clean architecture as part of my daily workflow, "
                "and I have experience with infrastructure-as-code concepts through Docker and "
                "automated deployment pipelines."
            )
            body2 = (
                "What attracts me to VTS is the engineer-led culture that emphasises XP techniques "
                "like TDD and pair programming, combined with the opportunity to work on a global-scale "
                "platform in collaboration with AWS. "
                "I thrive in stable, product-focused agile teams where I have a voice in what we build "
                "and how we build it, and I am equally passionate about mentoring others and helping "
                "the team improve its engineering practices."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my Java and AWS expertise, "
                "product-focused mindset, and collaborative approach to VTS's engineering team. "
                "Thank you for your time and consideration."
            )
        elif company_lower == 'enable':
            opening = (
                "I am applying for the Experienced Engineer position at Enable. "
                "I am a software engineer with 10+ years of experience building production "
                "systems in C#/.NET, ASP.NET, and SQL Server, and I recently completed my "
                "Master of Computer and Information Sciences at AUT with First Class Honours. "
                "I am particularly interested in Enable because it simplifies pricing and rebate "
                "management with an intelligent platform that helps companies increase profitability "
                "and operate at speed."
            )
            body1 = (
                "This role's focus on .NET, C#, ASP.NET Core, and T-SQL maps directly to my "
                "core expertise. I have delivered enterprise .NET systems including a SaaS platform "
                "with SQL Server backend, REST APIs, and CI/CD pipelines. I write clean, maintainable, "
                "performant code and practise code review, TDD, and agile methodologies as part of "
                "my daily workflow. "
                "I also bring TypeScript, JavaScript, HTML, and CSS experience from building "
                "full-stack web applications with React and Vue.js."
            )
            body2 = (
                "What attracts me to Enable is the combination of a well-funded, fast-growing company "
                "($291M in funding) with the opportunity to work on a product that solves real business "
                "problems for global clients. "
                "I am equally comfortable working independently or collaborating in a team, and I "
                "enjoy mentoring others, participating in code reviews, and contributing to a "
                "high-performance engineering culture."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my .NET expertise, problem-solving "
                "ability, and collaborative mindset to Enable's engineering team. "
                "Thank you for your time and consideration."
            )
        elif 'digital generationz' in company_lower:
            opening = (
                "I am applying for the AI Automation Engineer & Full-Stack Developer position at "
                "Digital Generationz. "
                "I am a software engineer with 10+ years of experience building production systems "
                "across Android, full-stack web, and .NET, and I recently completed my Master of "
                "Computer and Information Sciences at AUT with First Class Honours. "
                "I am drawn to Digital Generationz because it operates at the cutting edge of AI "
                "automation, building fast and shipping high-impact infrastructure without "
                "corporate legacy overhead."
            )
            body1 = (
                "My experience maps directly to what you are building. I developed a generative AI "
                "fashion system (ChatClothes) with diffusion models, CLIP embeddings, automated "
                "curation pipelines, and modern React-based interfaces — work that earned a Best "
                "Paper nomination at IVCNZ 2024. "
                "I have also built automated content pipelines, REST APIs, and CI/CD infrastructure "
                "across multiple projects, and I actively run local LLMs (Llama, Qwen) for daily "
                "workflow automation. I do not just prompt — I understand model architecture, "
                "data sovereignty, and how to write robust, maintainable code."
            )
            body2 = (
                "Beyond AI, I bring full-stack engineering depth: Android development (multiple "
                "production apps with millions of users), web ecosystems (React, TypeScript, "
                "WordPress, Vue.js), and backend systems (C#/.NET, Python, SQL Server). "
                "I have autonomous problem-solving instincts developed through years of building "
                "end-to-end systems, and I enjoy taking ownership of complex problems and seeing "
                "them through to production."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056), and "
                "my ChatClothes paper and other projects are linked from my CV. "
                "I would welcome the opportunity to contribute my AI automation expertise, "
                "full-stack depth, and autonomous engineering mindset to Digital Generationz's "
                "engineering team. Thank you for your time and consideration."
            )
        elif 'westpac' in company_lower:
            opening = (
                "I am applying for the Associate Engineer - Mobile position at Westpac. "
                "I am a software engineer with 10+ years of experience building production mobile "
                "applications, most recently as a Senior Android Developer at Alibaba where I delivered "
                "multiple high-impact Android apps using Kotlin and Java. "
                "I am drawn to Westpac because it builds financial tools that millions of New "
                "Zealanders rely on with confidence."
            )
            body1 = (
                "I have strong hands-on experience with Kotlin and Java across multiple production "
                "Android apps, including TaoBao (100M+ users), Youku (video streaming), and enterprise "
                "apps at Alibaba. I am comfortable with the full mobile development lifecycle — from "
                "architecture design and Jetpack Compose to CI/CD, unit testing, and production "
                "incident resolution. "
                "I also bring broader engineering skills across React, TypeScript, Git, Docker, and "
                "Agile practices, and I actively use AI tools responsibly to accelerate development "
                "while validating outputs and maintaining code quality."
            )
            body2 = (
                "What attracts me to this role is the opportunity to contribute to meaningful "
                "digital experiences in a collaborative, Agile environment while continuing to grow "
                "my technical capability. I value clean code, modern best practices, and knowledge "
                "sharing — and I am equally comfortable working independently on features or pairing "
                "with senior engineers to debug complex problems. "
                "I am based in Auckland, have full working rights, and am excited about building "
                "reliable, customer-focused mobile experiences at Westpac."
            )
            closing = (
                "Examples of my work are available on GitHub (github.com/leozhang2056). "
                "I would welcome the opportunity to contribute my mobile engineering expertise, "
                "collaborative mindset, and passion for continuous learning to Westpac's mobile "
                "engineering team. Thank you for your time and consideration."
            )
        else:
            company_lower = (company_name or '').strip().lower()

            # ---- helpers ----
            def _background_tagline() -> str:
                tagline = profile.get('career_identity', {}).get('tagline', '')
                return tagline.strip() if tagline else f"experience in {role_type} engineering and full-stack development"

            def _culture_reason() -> str:
                key = company_lower
                if key in _COMPANY_CULTURE_HOOKS:
                    return _COMPANY_CULTURE_HOOKS[key]
                for k, v in _COMPANY_CULTURE_HOOKS.items():
                    if k in key:
                        return v
                return "it focuses on building practical technology that delivers real value"

            def _team_name() -> str:
                key = company_lower
                if key in _COMPANY_TEAMS:
                    return _COMPANY_TEAMS[key]
                for k, v in _COMPANY_TEAMS.items():
                    if k in key:
                        return v
                return f"{company_name}'s engineering team"

            # === Para 1: "I am applying for..." (Rule 1-3) ===
            culture_reason = _culture_reason()
            tagline = _background_tagline()
            opening = (
                f"I am applying for the {target_role_title} position at {company_name}. "
                f"{tagline} "
                f"I am particularly interested in this opportunity because {culture_reason}"
            )
            if "aut" in company_lower or "auckland university of technology" in company_lower:
                opening += " As an AUT graduate, I am especially motivated by the opportunity to contribute to the university community through this role."

            # === Para 2: education/project evidence with linking sentence (Rule 4-5) ===
            body1_parts = []
            if role_type == 'ai' and pubs:
                first_pub = pubs[0]
                pub_venue = first_pub.get("venue", "")
                pub_year = first_pub.get("year", "")
                year_str = str(pub_year) if pub_year else ""
                venue_str = pub_venue.strip().rstrip(".")
                if year_str and year_str not in venue_str:
                    venue_str = f"{venue_str}, {year_str}"
                body1_parts.append(
                    f"I recently completed my Master of Computer and Information Sciences at "
                    f"Auckland University of Technology with First Class Honours. "
                    f"My thesis project involved designing and building a multimodal AI system "
                    f"from concept to working prototype — covering the full pipeline from data "
                    f"collection and model development to evaluation and integration. "
                    f"The project was accepted by {venue_str} and gave me hands-on experience "
                    f"developing AI systems that balance research innovation with usability, "
                    f"maintainability, and deployment considerations."
                )
            elif proj_name and proj_highlights:
                top_hl = proj_highlights[0][:120]
                # Lowercase first letter to flow after "I "
                top_hl = top_hl[0].lower() + top_hl[1:]
                body1_parts.append(
                    f"In my recent work on {proj_name}, "
                    f"I {top_hl}. "
                    f"This gave me practical experience delivering production systems "
                    f"that balance technical quality with real-world constraints."
                )
            else:
                body1_parts.append(
                    f"I have {years_str} years of software engineering experience "
                    f"building production systems from prototype through deployment."
                )

            # Differentiator (Rule 6)
            diff = _differentiator_hook(role_type)
            if diff:
                body1_parts.append(diff)

            body1 = " ".join(body1_parts)

            # === Para 3: attraction + experience + mindset (Rule 7-8) ===
            body2_parts = [
                f"What particularly attracted me to this role is {company_name}'s "
                f"emphasis on building technology that delivers practical impact."
            ]

            if years_str:
                body2_parts.append(
                    f"In addition to my academic work, I bring more than {years_str} years of "
                    f"software engineering experience across {role_type} and full-stack development. "
                    f"I have worked with APIs, CI/CD workflows, production systems, "
                    f"and cross-functional teams. This background has helped me develop "
                    f"a practical engineering mindset focused on reliability, collaboration, "
                    f"and continuous improvement."
                )

            body2 = " ".join(body2_parts)

            # === Closing: motivation + contribution + team name (Rule 9) ===
            team = _team_name()
            closing = (
                f"I am also highly motivated by the opportunity to work within a collaborative "
                f"team where learning, experimentation, and delivery are encouraged. "
                f"I would welcome the opportunity to contribute my technical background, "
                f"problem-solving ability, and hands-on development experience to {team}. "
                f"Thank you for your time and consideration."
            )

    else:  # zh fallback
        opening = "申请自荐信内容（中文）"
        body1 = "核心项目与经验描述"
        body2 = "在贵公司的展望"
        closing = "谢谢。"

    return {
        'opening': opening,
        'body1':   body1,
        'body2':   body2,
        'closing': closing,
    }


# ---------------------------------------------------------------------------
# CSS
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

    .cl-salutation {
      margin-top: 16px;
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
    contact_parts = []
    email = profile.get('contact', {}).get('email', '')
    phone = profile.get('contact', {}).get('phone', '')
    if email:
        contact_parts.append(html.escape(email))
    if phone:
        contact_parts.append(html.escape(phone))
    contact_str = " | ".join(contact_parts)
    
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
        {f'<div class="cl-contact">{contact_str}</div>' if contact_str else ''}
    </div>

    <div class="cl-salutation">Dear {html.escape(company_name)} Hiring Manager,</div>

    <div class="cl-body">
        <p>{html.escape(content['opening'])}</p>
        <p>{html.escape(content['body1'])}</p>
        <p>{html.escape(content['body2'])}</p>
        <p>{html.escape(content['closing'])}</p>
    </div>

    <div class="cl-sign">
        <div class="cl-sign-label">Kind regards,</div>
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
