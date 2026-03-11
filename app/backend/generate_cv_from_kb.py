#!/usr/bin/env python3
"""
从 Career KB YAML 文件生成简历 PDF
Generate CV PDF from Career KB YAML files
"""

import yaml
import os
from datetime import datetime
from pathlib import Path

# 导入原有的 PDF 生成函数
from generate_cv_html_to_pdf import html_to_pdf


def load_yaml(file_path):
    """加载 YAML 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_projects(projects_dir):
    """加载所有项目的 facts.yaml"""
    projects = []
    projects_path = Path(projects_dir)
    
    for project_dir in projects_path.iterdir():
        if project_dir.is_dir():
            facts_file = project_dir / 'facts.yaml'
            if facts_file.exists():
                try:
                    facts = load_yaml(facts_file)
                    if facts:
                        facts['_project_dir'] = project_dir.name
                        projects.append(facts)
                except Exception as e:
                    print(f"Warning: Failed to load {facts_file}: {e}")
    
    # 按时间排序（如果有日期）
    return projects


def generate_summary(profile, role_type='fullstack', lang='en'):
    """根据角色类型生成 Summary"""
    personal = profile.get('personal_info', {})
    career = profile.get('career_identity', {})
    
    summaries = career.get('summary_variants', {})
    
    if lang == 'zh':
        if role_type == 'android':
            return """<strong>高级 Android 开发工程师</strong>，拥有 <strong>12 年移动开发经验</strong>，其中 <strong>10 年以上企业级 Android 应用</strong>开发经验。
        精通 <strong>Kotlin、协程、Jetpack Compose</strong>，熟练运用 <strong>Dagger 依赖注入、WorkManager、Paging</strong>等架构组件。
        具备 <strong>CI/CD 容器化部署</strong>经验，擅长<strong>跨团队协作</strong>和客户沟通，致力于交付高质量的移动解决方案。"""
        elif role_type == 'ai':
            return """<strong>AI 全栈开发工程师</strong>，拥有 <strong>12 年开发经验</strong>，近期专注于 <strong>AI/ML</strong> 研究与应用落地。
        硕士论文项目 ChatClothes 采用 <strong>LoRA 微调、本地模型部署（Ollama）</strong>实现虚拟试衣系统，
        具备 <strong>Android、后端、前端</strong>全栈开发能力。"""
        else:
            return """<strong>全栈开发工程师</strong>，拥有 <strong>12 年开发经验</strong>，涵盖 <strong>Android、后端、AI 及前端</strong>全领域。
        深耕 <strong>Android SDK、NDK、Kotlin/Java</strong> 移动端开发，<strong>Spring Boot 微服务</strong>后端架构，
        以及 <strong>AI/ML</strong> 智能功能集成。具备从移动端到云端基础设施的完整交付能力。
        扎实掌握 <strong>Vue.js/React、RESTful API 及 DevOps</strong>，具备端到端全栈技术所有权。"""
    
    if role_type == 'android':
        return """<strong>Senior Android Software Engineer</strong> with <strong>12 years of mobile development experience</strong>, including <strong>10+ years in enterprise Android applications</strong>.
        Expert in <strong>Kotlin, Coroutines, and Jetpack Compose</strong>, proficient with <strong>Dagger dependency injection, WorkManager, and Paging</strong> architecture components.
        Experienced in <strong>CI/CD containerization and DevOps practices</strong>, with strong collaboration and customer-facing skills, committed to delivering high-quality mobile solutions."""
    elif role_type == 'ai':
        return summaries.get('ai_focus', summaries.get('default', ''))
    else:
        return """<strong>Full-Stack Developer</strong> with <strong>12 years of experience</strong> across <strong>Android, Backend, AI, and Frontend</strong>. 
        Deep expertise in <strong>Android SDK, NDK, Kotlin/Java</strong> for mobile development, <strong>Spring Boot microservices</strong> for backend systems, 
        and <strong>AI/ML integration</strong> for intelligent features. Proven ability to deliver complete solutions from mobile apps to cloud infrastructure. 
        Strong foundation in <strong>React/Vue.js, RESTful APIs, and DevOps</strong>, enabling end-to-end ownership across the entire technology stack."""


def generate_skills_section(skills_data, max_categories=7, lang='en', role_type='fullstack'):
    """生成技能部分"""
    skills_lines = []
    
    # 语言标签
    labels = {
        'en': {'programming': 'Programming', 'ai_ml': 'AI / ML', 'ai_coding': 'AI Coding Tools', 
               'fullstack': 'Full-Stack', 'devops': 'DevOps & Cloud', 'databases': 'Databases', 'mobile': 'Mobile'},
        'zh': {'programming': '编程语言', 'ai_ml': '人工智能/机器学习', 'ai_coding': 'AI 编程工具',
               'fullstack': '全栈开发', 'devops': 'DevOps 与云', 'databases': '数据库', 'mobile': '移动端'}
    }
    label = labels.get(lang, labels['en'])
    
    # Android 职位特殊技能展示
    if role_type == 'android':
        if lang == 'en':
            skills_lines.append(f"<strong>Android Development:</strong> Kotlin, Java, Android SDK, Jetpack Compose, Coroutines, Flow")
            skills_lines.append(f"<strong>Architecture:</strong> MVVM, Dagger/Hilt DI, WorkManager, Paging, Room, Retrofit")
            skills_lines.append(f"<strong>DevOps & CI/CD:</strong> Docker, Jenkins, GitHub Actions, Gradle, Firebase")
            skills_lines.append(f"<strong>Backend Integration:</strong> RESTful APIs, Spring Boot, Node.js, GraphQL")
            skills_lines.append(f"<strong>Databases:</strong> SQLite, Room, MySQL, Redis, MongoDB")
            skills_lines.append(f"<strong>Testing & Quality:</strong> JUnit, Espresso, Mockito, CI/CD pipelines")
            return '<br>\n        '.join(skills_lines[:max_categories])
        else:
            skills_lines.append(f"<strong>Android 开发:</strong> Kotlin, Java, Android SDK, Jetpack Compose, Coroutines, Flow")
            skills_lines.append(f"<strong>架构组件:</strong> MVVM, Dagger/Hilt 依赖注入, WorkManager, Paging, Room, Retrofit")
            skills_lines.append(f"<strong>DevOps & CI/CD:</strong> Docker, Jenkins, GitHub Actions, Gradle, Firebase")
            skills_lines.append(f"<strong>后端集成:</strong> RESTful APIs, Spring Boot, Node.js, GraphQL")
            skills_lines.append(f"<strong>数据库:</strong> SQLite, Room, MySQL, Redis, MongoDB")
            skills_lines.append(f"<strong>测试与质量:</strong> JUnit, Espresso, Mockito, CI/CD 流水线")
            return '<br>\n        '.join(skills_lines[:max_categories])
    
    # Programming Languages
    languages = skills_data.get('programming_languages', [])
    lang_names = [l['name'] for l in languages[:6]]
    if lang_names:
        skills_lines.append(f"<strong>{label['programming']}:</strong> {', '.join(lang_names)}")
    
    # AI/ML
    ai_ml = skills_data.get('ai_ml', [])
    if ai_ml and isinstance(ai_ml, list):
        ai_names = [item['name'] for item in ai_ml[:5] if isinstance(item, dict)]
        if ai_names:
            skills_lines.append(f"<strong>{label['ai_ml']}:</strong> {', '.join(ai_names)}")
    
    # AI Coding Tools
    ai_coding = skills_data.get('ai_coding_tools', [])
    if ai_coding and isinstance(ai_coding, list):
        ai_coding_names = [item['name'] for item in ai_coding[:5] if isinstance(item, dict)]
        if ai_coding_names:
            skills_lines.append(f"<strong>{label['ai_coding']}:</strong> {', '.join(ai_coding_names)}")
    
    # Backend / Full-Stack
    backend = skills_data.get('backend', [])
    backend_items = []
    if isinstance(backend, list):
        backend_names = [item['name'] for item in backend[:5] if isinstance(item, dict)]
        backend_items = backend_names
    elif isinstance(backend, dict):
        if backend.get('frameworks'):
            backend_items.extend(backend['frameworks'][:3])
        if backend.get('api_standards'):
            backend_items.extend(backend['api_standards'][:2])
    if backend_items:
        skills_lines.append(f"<strong>{label['fullstack']}:</strong> {', '.join(backend_items)}")
    
    # DevOps & Cloud
    devops = skills_data.get('devops', {})
    devops_items = []
    if isinstance(devops, dict):
        if devops.get('containerization'):
            devops_items.extend(devops['containerization'][:2])
        if devops.get('cicd'):
            devops_items.extend(devops['cicd'][:2])
        if devops.get('cloud_platforms'):
            devops_items.extend(list(devops['cloud_platforms'].keys())[:2])
    if devops_items:
        skills_lines.append(f"<strong>{label['devops']}:</strong> {', '.join(devops_items)}")
    
    # Databases
    databases = skills_data.get('databases', {})
    db_items = []
    if isinstance(databases, dict):
        if databases.get('relational'):
            db_items.extend(databases['relational'][:3])
        if databases.get('nosql'):
            db_items.extend(databases['nosql'][:2])
    if db_items:
        skills_lines.append(f"<strong>{label['databases']}:</strong> {', '.join(db_items)}")
    
    # Mobile / Android
    mobile = skills_data.get('mobile_development', {})
    mobile_items = []
    if isinstance(mobile, dict):
        if mobile.get('android'):
            mobile_items.extend(mobile['android'][:4])
    elif isinstance(mobile, list):
        mobile_names = [item['name'] for item in mobile[:4] if isinstance(item, dict)]
        mobile_items = mobile_names
    if mobile_items:
        skills_lines.append(f"<strong>{label['mobile']}:</strong> {', '.join(mobile_items)}")
    
    return '<br>\n        '.join(skills_lines[:max_categories])


def generate_project_bullet_points(project_facts, max_bullets=4, lang='en'):
    """从项目 facts 生成 bullet points - 使用自然描述风格"""
    
    # 根据语言选择 highlights
    if lang == 'zh':
        highlights = project_facts.get('highlights_cn', []) or project_facts.get('highlights', [])
    else:
        highlights = project_facts.get('highlights', [])
    if highlights:
        # 只取字符串类型的 highlights
        return [h for h in highlights[:max_bullets] if isinstance(h, str)]
    
    # 其次使用 impact
    impact = project_facts.get('impact', [])
    if impact:
        return [i for i in impact[:max_bullets] if isinstance(i, str)]
    
    # 最后使用 achievements，但简化处理
    achievements = project_facts.get('achievements', [])
    processed = []
    for item in achievements[:max_bullets]:
        if isinstance(item, str):
            processed.append(item)
        elif isinstance(item, dict):
            # 只取 description，去掉 metric
            desc = item.get('description', '')
            if desc:
                processed.append(desc)
    
    if processed:
        return processed
    
    # 最后的 fallback - 从 tech_stack 生成
    tech_stack = project_facts.get('tech_stack', {})
    if tech_stack:
        return ["Developed full-stack solution using modern technologies"]
    
    return ["Led development and delivery from concept to completion"]


def sort_projects_by_importance(projects):
    """按重要性排序项目"""
    # 定义项目优先级（数字越小越重要）
    # 前5个是指定优先级，其余按时间排序（越近越靠前）
    priority_map = {
        'chatclothes': 1,                   # 硕士项目 (2024-2025)
        'enterprise-messaging': 2,          # 大项目 (2014-2023)
        'smart-factory': 3,                 # 大项目 (2018-2024)
        'iot-solutions': 4,                 # 提到第4位
        'picture-book-locker': 5,           # 提到第5位
        # 其余项目按时间排序，时间近的优先级数字小
        'smart-power': 10,                  # 2021-2022
        'boobit': 11,                       # 2022
        'broadcast-control': 12,            # 2020
        'visual-gateway': 13,               # 2019
        'forest-patrol-inspection': 14,     # 2019
        'chinese-herbal-recognition': 15,   # 2019
        'device-maintenance-prediction': 16,# 2019
        'visit-system': 17,                 # 2018
        'exhibition-robot': 18,             # 2017
        'school-attendance': 19,            # 2016
        'live-streaming-system': 20,        # 2015-2018
        'patent-search-system': 21,         # 2013-2014
    }
    
    def get_priority(project):
        project_id = project.get('_project_dir', '')
        # 从项目 ID 中提取基本名称（去掉时间戳等）
        for key in priority_map:
            if key in project_id.lower():
                return priority_map[key]
        return 99  # 默认最低优先级
    
    return sorted(projects, key=get_priority)


def generate_experience_section(projects, lang='en', max_projects=5):
    """生成工作经历部分"""
    # 按重要性排序项目
    sorted_projects = sort_projects_by_importance(projects)
    # 选择前 N 个项目
    selected_projects = sorted_projects[:max_projects]
    
    experience_html = []
    
    for project in selected_projects:
        # 支持两种格式: project.name 或直接 name
        project_info = project.get('project', {})
        # 根据语言选择名称
        if lang == 'zh':
            name = project.get('name_cn') or project_info.get('name_cn') or project.get('name') or project_info.get('name') or project.get('project_id', 'Unknown Project')
        else:
            name = project_info.get('name') or project.get('name') or project.get('project_id', 'Unknown Project')
        
        # 获取公司/机构信息
        institution = project.get('institution', {})
        company_info = project.get('company', {})
        
        if isinstance(institution, dict) and institution.get('name'):
            company = institution['name']
        elif isinstance(company_info, dict) and company_info.get('name'):
            company = company_info['name']
        else:
            company = 'Chunxiao Technology Co., Ltd.' if lang == 'en' else '春晓科技有限公司'
        
        # 获取时间
        timeline = project.get('timeline', {})
        if isinstance(timeline, dict):
            start_date = timeline.get('start', '')
            end_date = timeline.get('end', '')
        else:
            start_date = project.get('start_date', '')
            end_date = project.get('end_date', '')
        
        # 格式化日期 - 只保留年份
        if start_date and end_date:
            # 提取年份 (2024-11 -> 2024)
            start_year = start_date.split('-')[0] if '-' in str(start_date) else str(start_date)
            end_year = end_date.split('-')[0] if '-' in str(end_date) else str(end_date)
            date_range = f"{start_year} -- {end_year}" if start_year != end_year else start_year
        else:
            date_range = "2022"
        
        # 角色 - 优先使用 role_cn (中文) 或 role (英文)，然后是 team.role
        if lang == 'zh':
            role = project.get('role_cn', '') or project.get('role', '')
        else:
            role = project.get('role', '')
        if not role:
            team = project.get('team', {})
            if lang == 'zh':
                role = team.get('role_cn', '') or team.get('role', '')
            else:
                role = team.get('role', '')
        if not role:
            role = 'Developer' if lang == 'en' else '开发工程师'
        
        # Overview - 生成项目描述（支持多种字段名）
        # 根据语言选择 overview/summary
        if lang == 'zh':
            overview = project.get('overview_cn') or project.get('summary_cn') or project.get('overview') or project.get('summary', '')
        else:
            overview = project.get('overview') or project.get('summary', '')
        if isinstance(overview, str) and overview.strip():
            overview_text = overview.strip().split('\n')[0][:150]
        else:
            # 从 type 和 category 生成描述
            project_type = project.get('type', 'Project' if lang == 'en' else '项目')
            categories = project.get('category', [])
            if categories:
                if lang == 'en':
                    overview_text = f"{project_type} focusing on {', '.join(categories[:2])}"
                else:
                    overview_text = f"{project_type}，专注于{', '.join(categories[:2])}"
            else:
                overview_text = project_type
        
        # Achievements
        achievements = generate_project_bullet_points(project, lang=lang)
        bullets_html = '\n            '.join([f'<li>{a}</li>' for a in achievements])
        
        project_html = f'''
    <div class="job">
        <table class="job-header-table" style="width: 100%; border-collapse: collapse; margin-bottom: 2px;">
            <tr>
                <td class="job-title" style="font-weight: bold; font-size: 10.5pt; width: 35%; text-align: left; padding: 0;">{name}</td>
                <td class="job-company" style="font-style: italic; color: #333; width: 45%; text-align: right; padding: 0;">{company}</td>
                <td class="job-date" style="color: #999; font-size: 10pt; width: 20%; text-align: right; padding: 0;">{date_range}</td>
            </tr>
        </table>
        <div class="job-role"><strong>{role}</strong> - {overview_text}</div>
        <ul class="job-list">
            {bullets_html}
        </ul>
    </div>'''
        
        experience_html.append(project_html)
    
    return '\n'.join(experience_html)


def generate_education_section(profile, lang='en'):
    """从 profile.yaml 生成教育部分"""
    education = profile.get('education', [])
    edu_html = []
    
    for edu in education:
        # 根据语言选择字段
        if lang == 'zh':
            degree = edu.get('degree_cn', '') or edu.get('degree', '')
            institution = edu.get('institution_cn', '') or edu.get('institution', '')
            location = edu.get('location_cn', '') or edu.get('location', '')
        else:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            location = edu.get('location', '')
        
        start = edu.get('start_date', '')
        end = edu.get('end_date', '')
        
        # 格式化日期
        start_fmt = start[:4] if start else ''
        end_fmt = end[:4] if end else ''
        date_range = f"{start_fmt} -- {end_fmt}" if start_fmt and end_fmt else ''
        
        # 构建详情
        details = []
        
        # Research focus
        if lang == 'zh':
            research = edu.get('research_focus_cn', []) or edu.get('research_focus', [])
        else:
            research = edu.get('research_focus', [])
        if research:
            label_research = 'Research focus' if lang == 'en' else '研究方向'
            details.append(f"{label_research}: {', '.join(research)}")
        
        # Honors
        if lang == 'zh':
            honors = edu.get('honors_cn', []) or edu.get('honors', [])
        else:
            honors = edu.get('honors', [])
        if honors:
            label_honors = 'Honors' if lang == 'en' else '荣誉'
            details.append(f"{label_honors}: {', '.join(honors)}")
        
        # Highlights
        if lang == 'zh':
            highlights = edu.get('highlights_cn', []) or edu.get('highlights', [])
        else:
            highlights = edu.get('highlights', [])
        if highlights:
            details.append('. '.join(highlights))
        
        # 学校名称简化
        school_short = institution.split(',')[0] if ',' in institution else institution
        
        edu_html.append(f'''
    <div class="edu-item">
        <div class="edu-header">
            <span class="edu-title">{degree}</span>
            <span class="edu-school">{school_short}, {location}</span>
            <span class="edu-date">{date_range}</span>
        </div>
        <div class="edu-detail">{' '.join(details)}</div>
    </div>''')
    
    return '\n'.join(edu_html)


def generate_licenses_section(achievements, lang='en'):
    """从 achievements.yaml 生成证书部分"""
    certifications = achievements.get('certifications', [])
    awards = achievements.get('awards', [])
    
    licenses_html = []
    
    # 添加证书
    for cert in certifications:
        name = cert.get('name', '')
        authority = cert.get('authority', '')
        year = cert.get('year', '')
        
        licenses_html.append(f'''
        <li>
            <div class="license-content">
                <span><strong>{name}</strong> — {authority}</span>
                <span class="license-date">{year}</span>
            </div>
        </li>''')
    
    # 添加奖项
    for award in awards[:2]:  # 只取前2个奖项
        name = award.get('name', '')
        category = award.get('category', '')
        authority = award.get('authority', '')
        year = award.get('year', '')
        
        display_name = f"{name} ({category})" if category else name
        
        licenses_html.append(f'''
        <li>
            <div class="license-content">
                <span><strong>{display_name}</strong> — {authority}</span>
                <span class="license-date">{year}</span>
            </div>
        </li>''')
    
    return '\n'.join(licenses_html)


def generate_html_from_kb(role_type='fullstack', lang='en'):
    """从 KB 生成完整 HTML"""
    
    # 语言映射
    labels = {
        'en': {
            'summary': 'Summary',
            'skills': 'Key Skills',
            'experience': 'Experience',
            'education': 'Education',
            'licenses': 'Licenses & Certifications'
        },
        'zh': {
            'summary': '个人简介',
            'skills': '核心技能',
            'experience': '工作经历',
            'education': '教育背景',
            'licenses': '证书认证'
        }
    }
    label = labels.get(lang, labels['en'])
    
    # 加载数据
    kb_dir = Path('kb')
    profile = load_yaml(kb_dir / 'profile.yaml')
    skills = load_yaml(kb_dir / 'skills.yaml')
    achievements = load_yaml(kb_dir / 'achievements.yaml')
    projects = load_projects('projects')
    
    # 提取个人信息
    personal = profile.get('personal_info', {})
    name = personal.get('preferred_name', personal.get('name', 'Leo Zhang'))
    email = personal.get('contact', {}).get('email', '')
    phone = personal.get('contact', {}).get('phone', '')
    location = personal.get('contact', {}).get('location', {})
    city = location.get('city', '')
    country = location.get('country', '')
    
    # 生成各部分
    summary = generate_summary(profile, role_type, lang)
    skills_section = generate_skills_section(skills, lang=lang, role_type=role_type)
    experience_section = generate_experience_section(projects, lang=lang)
    education_section = generate_education_section(profile, lang=lang)
    licenses_section = generate_licenses_section(achievements, lang=lang)
    
    # 构建完整 HTML（使用原有模板结构）
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{name} - CV</title>
    <style>
        @page {{
            size: A4;
            margin: 15mm;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10.5pt;
            line-height: 1.35;
            color: #000;
            max-width: 210mm;
            margin: 0 auto;
            padding: 0;
        }}
        
        /* Header */
        .header {{
            text-align: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
        }}
        
        .name {{
            font-size: 24pt;
            font-weight: bold;
            color: #000080;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        
        .name a {{
            color: #000080;
            text-decoration: none;
        }}
        
        .social-icon {{
            width: 18px;
            height: 18px;
            vertical-align: middle;
            display: inline-block;
        }}
        
        .contact {{
            font-size: 10.5pt;
            color: #000080;
        }}
        
        .contact a {{
            color: #000080;
            text-decoration: none;
        }}
        
        /* Section titles */
        .section-title {{
            font-size: 12pt;
            font-weight: bold;
            color: #000080;
            margin-top: 12px;
            margin-bottom: 6px;
            border-bottom: 1.5px solid #000080;
            padding-bottom: 2px;
        }}
        
        /* First section title should not have top margin */
        .section-title:first-of-type {{
            margin-top: 0;
        }}
        
        /* Summary */
        .summary {{
            text-align: justify;
            margin-bottom: 8px;
        }}
        
        /* Skills */
        .skills {{
            margin-bottom: 8px;
        }}
        
        /* Experience */
        .job {{
            margin-bottom: 10px;
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 2px;
        }}
        
        .job-title {{
            font-weight: bold;
            font-size: 10.5pt;
            flex: 0 0 auto;
            margin-right: 10px;
        }}
        
        .job-company {{
            font-style: italic;
            color: #333;
            flex: 0 0 auto;
            width: 200px;
            text-align: right;
            margin-right: 10px;
        }}
        
        .job-date {{
            color: #999;
            font-size: 10pt;
            flex: 0 0 auto;
            width: 90px;
            text-align: right;
        }}
        
        .job-role {{
            font-size: 10pt;
            margin-bottom: 3px;
            color: #333;
        }}
        
        .job-list {{
            margin: 0;
            padding-left: 20px;
            font-size: 10pt;
        }}
        
        .job-list li {{
            margin-bottom: 2px;
        }}
        
        /* Education */
        .edu-item {{
            margin-bottom: 8px;
        }}
        
        .edu-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}
        
        .edu-title {{
            font-weight: bold;
            flex: 0 0 auto;
            margin-right: 10px;
        }}
        
        .edu-school {{
            font-style: italic;
            color: #333;
            flex: 1 1 auto;
            text-align: right;
            margin-right: 10px;
        }}
        
        .edu-date {{
            color: #999;
            font-size: 10pt;
            flex: 0 0 auto;
            min-width: 80px;
            text-align: right;
        }}
        
        .edu-detail {{
            font-size: 10pt;
            color: #333;
            margin-top: 2px;
        }}
        
        /* Licenses */
        .license-list {{
            list-style: none;
            margin-left: 0;
            padding-left: 0;
            font-size: 10pt;
            line-height: 1.5;
        }}
        
        .license-list li {{
            margin-bottom: 4px;
            display: block;
        }}
        
        .license-content {{
            display: flex;
            justify-content: space-between;
        }}
        
        .license-date {{
            color: #999;
            margin-left: 10px;
            text-align: right;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <div class="name">
            <a href="https://www.linkedin.com/in/leo-zhang-305626280/">{name}</a>
            <a href="https://www.linkedin.com/in/leo-zhang-305626280/">
                <svg class="social-icon" viewBox="0 0 24 24" fill="#0077B5">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
            </a>
            <a href="https://github.com/leozhang2056">
                <svg class="social-icon" viewBox="0 0 24 24" fill="#181717">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
            </a>
        </div>
        <div class="contact">
            <a href="mailto:{email}">&#9993; {email}</a> | 
            &#9990; {phone} | 
            &#9992; {city}, {country}
        </div>
    </div>
    
    <!-- Summary -->
    <div class="section-title">{label['summary']}</div>
    <div class="summary">
        {summary}
    </div>
    
    <!-- Key Skills -->
    <div class="section-title">{label['skills']}</div>
    <div class="skills">
        {skills_section}
    </div>
    
    <!-- Experience -->
    <div class="section-title">{label['experience']}</div>
    {experience_section}
    
    <!-- Education -->
    <div class="section-title">{label['education']}</div>
    {education_section}
    
    <!-- Licenses & Certifications -->
    <div class="section-title">{label['licenses']}</div>
    <ul class="license-list">
{licenses_section}
    </ul>
</body>
</html>'''
    
    return html


async def generate_cv_from_kb(output_path=None, role_type='fullstack'):
    """主函数：从 KB 生成中英文两份简历 PDF"""
    
    today = datetime.now().strftime('%Y%m%d')
    
    # 英文版
    if output_path:
        en_path = output_path
        # 中文版：在 .pdf 前加上 _CN
        zh_path = en_path.replace('.pdf', '_CN.pdf')
    else:
        en_path = f'outputs/CV_Leo_Zhang_{today}_KB.pdf'
        zh_path = f'outputs/CV_Leo_Zhang_{today}_KB_CN.pdf'
    
    print("Generating CV from Career KB...")
    
    # 生成英文版
    html_en = generate_html_from_kb(role_type, lang='en')
    html_en_path = en_path.replace('.pdf', '.html')
    with open(html_en_path, 'w', encoding='utf-8') as f:
        f.write(html_en)
    print(f"EN HTML saved: {html_en_path}")
    await html_to_pdf(html_en, en_path)
    print(f"EN PDF generated: {en_path} ({os.path.getsize(en_path)/1024:.1f} KB)")
    
    # 生成中文版
    html_zh = generate_html_from_kb(role_type, lang='zh')
    html_zh_path = zh_path.replace('.pdf', '.html')
    with open(html_zh_path, 'w', encoding='utf-8') as f:
        f.write(html_zh)
    print(f"CN HTML saved: {html_zh_path}")
    await html_to_pdf(html_zh, zh_path)
    print(f"CN PDF generated: {zh_path} ({os.path.getsize(zh_path)/1024:.1f} KB)")
    
    return en_path, zh_path


if __name__ == '__main__':
    import asyncio
    
    # 生成简历
    asyncio.run(generate_cv_from_kb())
