#!/usr/bin/env python3
"""
Dynamic Resume Generator (LEGACY)
从知识库动态生成简历,支持岗位定制。

注意：
- 本脚本为早期版本，主要用于实验「基于 kb/experience/work.yaml 的公司维度视角」。
- 当前推荐主线请使用仓库根目录的统一入口：
    python generate.py cv --role android|ai|backend|fullstack
- 简历内容（项目选择 / 排版 / 双语输出）以后都以 app/backend/generate_cv_from_kb.py 为准，
  本文件仅保留作参考或临时调试使用。
"""

import yaml
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ResumeConfig:
    """简历生成配置"""
    target_role: str = "full_stack"  # android, backend, ai, full_stack
    language: str = "en"
    max_projects: int = 5
    bullet_style: str = "strong_verbs"  # strong_verbs, narrative


class KBLoader:
    """知识库加载器"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent.parent.parent
        self.kb_dir = self.base_path / "kb"
        self.projects_dir = self.base_path / "projects"
    
    def load_profile(self) -> Dict[str, Any]:
        """加载个人档案"""
        profile_file = self.kb_dir / "profile.yaml"
        with open(profile_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_skills(self) -> Dict[str, Any]:
        """加载技能清单"""
        skills_file = self.kb_dir / "skills.yaml"
        with open(skills_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_experience(self) -> Dict[str, Any]:
        """加载工作经历"""
        exp_file = self.kb_dir / "experience" / "work.yaml"
        with open(exp_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_achievements(self) -> Dict[str, Any]:
        """加载成就奖项"""
        ach_file = self.kb_dir / "achievements.yaml"
        with open(ach_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """加载单个项目"""
        facts_file = self.projects_dir / project_id / "facts.yaml"
        if not facts_file.exists():
            return None
        with open(facts_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_projects_by_ids(self, project_ids: List[str]) -> List[Dict[str, Any]]:
        """根据 ID 列表加载项目"""
        projects = []
        for pid in project_ids:
            data = self.load_project(pid)
            if data:
                projects.append(data)
        return projects


class ResumeGenerator:
    """简历生成器"""
    
    def __init__(self, config: ResumeConfig = None):
        self.config = config or ResumeConfig()
        self.loader = KBLoader()
        
        # 角色到项目的映射
        self.role_project_map = {
            "android": [
                "enterprise-messaging",
                "smart-factory",
                "live-streaming-system",
                "picture-book-locker",
                "forest-patrol-inspection"
            ],
            "backend": [
                "smart-factory",
                "enterprise-messaging",
                "broadcast-control",
                "visit-system"
            ],
            "ai": [
                "chatclothes",
                "device-maintenance-prediction",
                "chinese-herbal-recognition"
            ],
            "full_stack": [
                "chatclothes",
                "smart-factory",
                "enterprise-messaging",
                "live-streaming-system",
                "iot-solutions"
            ]
        }
    
    def generate_html(self) -> str:
        """生成 HTML 简历"""
        # 加载数据
        profile = self.loader.load_profile()
        skills = self.loader.load_skills()
        experience = self.loader.load_experience()
        achievements = self.loader.load_achievements()
        
        # 根据 target_role 选择项目
        project_ids = self.role_project_map.get(
            self.config.target_role,
            self.role_project_map["full_stack"]
        )[:self.config.max_projects]
        projects = self.loader.load_projects_by_ids(project_ids)
        
        # 生成 HTML
        return self._build_html(profile, skills, experience, projects, achievements)
    
    def _build_html(self, profile: Dict, skills: Dict, experience: Dict, 
                    projects: List[Dict], achievements: Dict) -> str:
        """构建 HTML 内容"""
        contact = profile['personal_info']['contact']
        name = profile['personal_info'].get('preferred_name', profile['personal_info']['name'])
        
        # 选择合适的 summary
        summary_key = f"{self.config.target_role}_focus"
        summary = profile.get('career_identity', {}).get('summary_variants', {}).get(
            summary_key,
            profile.get('career_identity', {}).get('summary_variants', {}).get('default', '')
        )
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - CV</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Latin+Modern+Roman:wght@400;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Latin Modern Roman', 'Times New Roman', Georgia, serif;
            font-size: 11pt;
            line-height: 1.35;
            color: #000;
            max-width: 210mm;
            margin: 0 auto;
            padding: 15mm;
            background: white;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 8px;
        }}
        
        .name {{
            font-size: 24pt;
            font-weight: bold;
            color: #000080;
            margin-bottom: 6px;
        }}
        
        .contact {{
            font-size: 10.5pt;
            color: #000080;
            line-height: 1.5;
        }}
        
        .section-title {{
            font-size: 12pt;
            font-weight: bold;
            color: #000080;
            margin-top: 12px;
            margin-bottom: 6px;
            border-bottom: 1px solid #000;
            padding-bottom: 2px;
        }}
        
        .summary {{
            font-size: 10.5pt;
            line-height: 1.4;
            margin-bottom: 8px;
        }}
        
        .skills-list {{
            list-style: disc;
            margin-left: 20px;
            font-size: 10.5pt;
            line-height: 1.5;
        }}
        
        .skills-list li {{
            margin-bottom: 3px;
        }}
        
        .job {{
            margin-bottom: 10px;
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-size: 10.5pt;
        }}
        
        .job-title {{
            font-weight: bold;
        }}
        
        .job-list {{
            list-style: disc;
            margin-left: 20px;
            font-size: 10pt;
            line-height: 1.4;
        }}
        
        .edu-item {{
            margin-bottom: 10px;
        }}
        
        .edu-header {{
            display: flex;
            justify-content: space-between;
            font-size: 10.5pt;
        }}
        
        .edu-title {{
            font-weight: bold;
        }}
        
        .license-list {{
            list-style: none;
            font-size: 10pt;
        }}
        
        @media print {{
            body {{ padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="name">{name}</div>
        <div class="contact">
            {contact['email']} | {contact['phone']} | {contact['location']['city']}, {contact['location']['country']}
        </div>
    </div>
    
    <!-- Summary -->
    <div class="section-title">Summary</div>
    <div class="summary">{self._format_summary(summary)}</div>
    
    <!-- Skills -->
    <div class="section-title">Key Skills</div>
    <ul class="skills-list">
        {self._format_skills(skills)}
    </ul>
    
    <!-- Experience -->
    <div class="section-title">Experience</div>
    {self._format_experience(experience)}
    
    <!-- Education -->
    <div class="section-title">Education</div>
    {self._format_education(profile)}
    
    <!-- Certifications -->
    <div class="section-title">Licenses & Certifications</div>
    <ul class="license-list">
        {self._format_certifications(achievements)}
    </ul>
</body>
</html>"""
        
        return html
    
    def _format_summary(self, summary: str) -> str:
        """格式化摘要"""
        # 简单的格式化,可以后续增强
        return summary.strip()
    
    def _format_skills(self, skills: Dict) -> str:
        """格式化技能"""
        skill_groups = skills.get('skill_groups', {})
        
        # 根据目标角色选择重点技能组
        priority_groups = {
            "android": ["android_development", "backend_engineering", "ai_coding", "ai_ml"],
            "backend": ["backend_engineering", "devops", "ai_coding", "full_stack"],
            "ai": ["ai_ml", "ai_coding", "backend_engineering", "devops"],
            "full_stack": ["backend_engineering", "android_development", "ai_coding", "ai_ml", "devops"]
        }
        
        target_groups = priority_groups.get(self.config.target_role, priority_groups["full_stack"])
        
        lines = []
        for group_name in target_groups:
            if group_name in skill_groups:
                skill_list = skill_groups[group_name]
                group_label = group_name.replace('_', ' ').title()
                skills_str = ', '.join(skill_list[:8])
                lines.append(f"<li><strong>{group_label}:</strong> {skills_str}</li>")
        
        return '\n        '.join(lines)
    
    def _format_experience(self, experience: Dict) -> str:
        """格式化工作经历"""
        exps = experience.get('experiences', [])
        html_parts = []
        
        for exp in exps:
            company = exp.get('company', '')
            role = exp.get('role', '')
            location = exp.get('location', '')
            start = exp.get('start_date', '')
            end = exp.get('end_date', 'Present' if exp.get('current') else '')
            
            # 格式化日期
            date_range = f"{start.split('-')[0]} -- {end.split('-')[0] if end != 'Present' else 'Present'}"
            
            html_parts.append(f"""
    <div class="job">
        <div class="job-header">
            <span class="job-title">{role}</span>
            <span>{company}, {location}</span>
            <span>{date_range}</span>
        </div>
        <ul class="job-list">
            {self._format_projects(exp.get('projects', []))}
        </ul>
    </div>""")
        
        return '\n'.join(html_parts)
    
    def _format_projects(self, projects: List[Dict]) -> str:
        """格式化项目列表"""
        lines = []
        
        for proj in projects[:self.config.max_projects]:
            name = proj.get('name', '')
            highlights = proj.get('highlights', [])
            
            # 为每个 highlight 添加项目名称前缀(第一个)
            for i, highlight in enumerate(highlights[:4]):
                if i == 0:
                    lines.append(f"<li><strong>{name}:</strong> {highlight}</li>")
                else:
                    lines.append(f"<li>{highlight}</li>")
        
        return '\n            '.join(lines)
    
    def _format_education(self, profile: Dict) -> str:
        """格式化教育经历"""
        edu_list = profile.get('education', [])
        html_parts = []
        
        for edu in edu_list:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            start = edu.get('start_date', '')
            end = edu.get('end_date', '')
            
            highlights = edu.get('highlights', [])
            details = ' '.join(highlights[:2]) if highlights else ''
            
            html_parts.append(f"""
    <div class="edu-item">
        <div class="edu-header">
            <span class="edu-title">{degree}</span>
            <span>{institution}</span>
            <span>{start} -- {end}</span>
        </div>
        <div style="font-size: 10pt; margin-top: 2px;">{details}</div>
    </div>""")
        
        return '\n'.join(html_parts)
    
    def _format_certifications(self, achievements: Dict) -> str:
        """格式化证书"""
        certs = achievements.get('certifications', [])
        lines = []
        
        for cert in certs[:4]:
            name = cert.get('name', '')
            authority = cert.get('authority', '')
            year = cert.get('year', '')
            
            lines.append(f"""<li>
            <div style="display: flex; justify-content: space-between;">
                <span><strong>{name}</strong> — {authority}</span>
                <span style="color: #999;">{year}</span>
            </div>
        </li>""")
        
        return '\n        '.join(lines)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate resume from KB')
    parser.add_argument('--role', default='full_stack', 
                       choices=['android', 'backend', 'ai', 'full_stack'],
                       help='Target role')
    parser.add_argument('--output', default='outputs', help='Output directory')
    parser.add_argument('--max-projects', type=int, default=5, help='Max projects to include')
    
    args = parser.parse_args()
    
    # 创建配置
    config = ResumeConfig(
        target_role=args.role,
        max_projects=args.max_projects
    )
    
    # 生成简历
    generator = ResumeGenerator(config)
    html = generator.generate_html()
    
    # 保存文件
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    html_file = output_dir / f"CV_Leo_Zhang_{args.role}_{timestamp}.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Resume generated: {html_file}")
    print(f"  Target role: {args.role}")
    print(f"  Max projects: {args.max_projects}")


if __name__ == "__main__":
    main()
