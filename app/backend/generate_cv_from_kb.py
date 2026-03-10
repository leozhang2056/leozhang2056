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


def generate_summary(profile, role_type='fullstack'):
    """根据角色类型生成 Summary"""
    personal = profile.get('personal_info', {})
    career = profile.get('career_identity', {})
    
    # 使用 profile 中的 summary_variants 或生成新的
    summaries = career.get('summary_variants', {})
    
    if role_type == 'android':
        return summaries.get('android_focus', summaries.get('default', ''))
    elif role_type == 'ai':
        return summaries.get('ai_focus', summaries.get('default', ''))
    else:
        # Full-stack 版本
        return """<strong>Full-Stack Developer</strong> with <strong>12 years of experience</strong> across <strong>Android, Backend, AI, and Frontend</strong>. 
        Deep expertise in <strong>Android SDK, NDK, Kotlin/Java</strong> for mobile development, <strong>Spring Boot microservices</strong> for backend systems, 
        and <strong>AI/ML integration</strong> for intelligent features. Proven ability to deliver complete solutions from mobile apps to cloud infrastructure. 
        Strong foundation in <strong>React/Vue.js, RESTful APIs, and DevOps</strong>, enabling end-to-end ownership across the entire technology stack."""


def generate_skills_section(skills_data, max_categories=7):
    """生成技能部分"""
    skills_lines = []
    
    # Programming Languages
    languages = skills_data.get('programming_languages', [])
    lang_names = [l['name'] for l in languages[:6]]
    if lang_names:
        skills_lines.append(f"<strong>Programming:</strong> {', '.join(lang_names)}")
    
    # AI/ML - ai_ml 是列表格式
    ai_ml = skills_data.get('ai_ml', [])
    if ai_ml and isinstance(ai_ml, list):
        ai_names = [item['name'] for item in ai_ml[:5] if isinstance(item, dict)]
        if ai_names:
            skills_lines.append(f"<strong>AI / ML:</strong> {', '.join(ai_names)}")
    
    # AI Coding Tools
    ai_coding = skills_data.get('ai_coding_tools', [])
    if ai_coding and isinstance(ai_coding, list):
        ai_coding_names = [item['name'] for item in ai_coding[:5] if isinstance(item, dict)]
        if ai_coding_names:
            skills_lines.append(f"<strong>AI Coding Tools:</strong> {', '.join(ai_coding_names)}")
    
    # Backend / Full-Stack - backend 可能是列表或字典
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
        skills_lines.append(f"<strong>Full-Stack:</strong> {', '.join(backend_items)}")
    
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
        skills_lines.append(f"<strong>DevOps & Cloud:</strong> {', '.join(devops_items)}")
    
    # Databases
    databases = skills_data.get('databases', {})
    db_items = []
    if isinstance(databases, dict):
        if databases.get('relational'):
            db_items.extend(databases['relational'][:3])
        if databases.get('nosql'):
            db_items.extend(databases['nosql'][:2])
    if db_items:
        skills_lines.append(f"<strong>Databases:</strong> {', '.join(db_items)}")
    
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
        skills_lines.append(f"<strong>Mobile:</strong> {', '.join(mobile_items)}")
    
    return '<br>\n        '.join(skills_lines[:max_categories])


def generate_project_bullet_points(project_facts, max_bullets=4):
    """从项目 facts 生成 bullet points"""
    achievements = project_facts.get('achievements', [])
    
    # 如果没有 achievements，尝试从 highlights 或 impact
    if not achievements:
        highlights = project_facts.get('highlights', [])
        impact = project_facts.get('impact', [])
        
        # 合并并返回
        combined = highlights + impact
        if combined:
            return combined[:max_bullets]
        
        # 最后的 fallback
        return [
            "Led development and delivery from concept to completion",
            "Implemented core features using modern technologies"
        ][:max_bullets]
    
    return achievements[:max_bullets]


def generate_experience_section(projects, max_projects=5):
    """生成工作经历部分"""
    # 选择最近/最重要的项目
    selected_projects = projects[:max_projects]
    
    experience_html = []
    
    for project in selected_projects:
        # 支持两种格式: project.name 或直接 name
        project_info = project.get('project', {})
        name = project_info.get('name') or project.get('name') or project.get('project_id', 'Unknown Project')
        
        # 获取公司信息
        company_info = project.get('company', {})
        if isinstance(company_info, dict):
            company = company_info.get('name') or 'Chunxiao Technology Co., Ltd.'
        else:
            company = 'Chunxiao Technology Co., Ltd.'
        
        # 获取时间
        timeline = project.get('timeline', {})
        if isinstance(timeline, dict):
            start_date = timeline.get('start', '')
            end_date = timeline.get('end', '')
        else:
            start_date = project.get('start_date', '')
            end_date = project.get('end_date', '')
        
        # 格式化日期
        date_range = f"{start_date} -- {end_date}" if start_date and end_date else "2022"
        
        # 角色
        team = project.get('team', {})
        role = team.get('role', 'Developer')
        
        # Overview
        overview = project.get('overview', '')
        if isinstance(overview, str):
            overview_text = overview.strip().split('\n')[0][:100]
        else:
            overview_text = 'Full-stack development project'
        
        # Achievements
        achievements = generate_project_bullet_points(project)
        bullets_html = '\n            '.join([f'<li>{a}</li>' for a in achievements])
        
        project_html = f'''
    <div class="job">
        <div class="job-header">
            <span class="job-title">{name}</span>
            <span class="job-company">{company}</span>
            <span class="job-date">{date_range}</span>
        </div>
        <div class="job-role"><strong>{role}</strong> - {overview_text}</div>
        <ul class="job-list">
            {bullets_html}
        </ul>
    </div>'''
        
        experience_html.append(project_html)
    
    return '\n'.join(experience_html)


def generate_education_section(profile):
    """从 profile.yaml 生成教育部分"""
    education = profile.get('education', [])
    edu_html = []
    
    for edu in education:
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
        research = edu.get('research_focus', [])
        if research:
            details.append(f"Research focus: {', '.join(research)}")
        
        # Honors
        honors = edu.get('honors', [])
        if honors:
            details.append(f"Honors: {', '.join(honors)}")
        
        # Highlights
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


def generate_licenses_section(achievements):
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


def generate_html_from_kb(role_type='fullstack'):
    """从 KB 生成完整 HTML"""
    
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
    summary = generate_summary(profile, role_type)
    skills_section = generate_skills_section(skills)
    experience_section = generate_experience_section(projects)
    education_section = generate_education_section(profile)
    licenses_section = generate_licenses_section(achievements)
    
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
        }}
        
        .job-company {{
            font-style: italic;
            color: #333;
        }}
        
        .job-date {{
            color: #999;
            font-size: 10pt;
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
        }}
        
        .edu-school {{
            font-style: italic;
            color: #333;
        }}
        
        .edu-date {{
            color: #999;
            font-size: 10pt;
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
    <div class="section-title">Summary</div>
    <div class="summary">
        {summary}
    </div>
    
    <!-- Key Skills -->
    <div class="section-title">Key Skills</div>
    <div class="skills">
        {skills_section}
    </div>
    
    <!-- Experience -->
    <div class="section-title">Experience</div>
    {experience_section}
    
    <!-- Education -->
    <div class="section-title">Education</div>
    {education_section}
    
    <!-- Licenses & Certifications -->
    <div class="section-title">Licenses & Certifications</div>
    <ul class="license-list">
{licenses_section}
    </ul>
</body>
</html>'''
    
    return html


async def generate_cv_from_kb(output_path=None, role_type='fullstack'):
    """主函数：从 KB 生成简历 PDF"""
    
    if output_path is None:
        today = datetime.now().strftime('%Y%m%d')
        output_path = f'outputs/CV_Leo_Zhang_{today}_KB.pdf'
    
    print("Generating CV from Career KB...")
    
    # 生成 HTML
    html_content = generate_html_from_kb(role_type)
    
    # 保存 HTML（用于调试）
    html_path = output_path.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML saved: {html_path}")
    
    # 转换为 PDF
    await html_to_pdf(html_content, output_path)
    
    print(f"\nPDF generated: {output_path}")
    
    # 获取文件大小
    file_size = os.path.getsize(output_path)
    print(f"File size: {file_size / 1024:.1f} KB")
    
    return output_path


if __name__ == '__main__':
    import asyncio
    
    # 生成简历
    asyncio.run(generate_cv_from_kb())
