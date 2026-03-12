#!/usr/bin/env python3
"""
Career KB PDF Resume Generator (LEGACY)
使用 ReportLab 直接排版生成 PDF 简历。

说明：
- 本文件中的 Summary / Skills / Experience 文案大部分为硬编码，
  只在少量位置读取 `kb/profile.yaml` 等 KB 数据。
- 当前推荐的主简历内容管线是：
    app/backend/generate_cv_from_kb.py  →  HTML
    generate_cv_html_to_pdf.html_to_pdf →  PDF
  并通过根目录 `python generate.py cv ...` 调用。

建议：
- 如需继续维护 ReportLab 版本，可在后续改造为消费
  `generate_cv_from_kb.py` 产出的统一结构化简历数据，仅负责「皮肤/排版」。
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import yaml
import os
from datetime import datetime


class CVGenerator:
    def __init__(self, output_path):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        """设置自定义样式 - 参考 CV_Common.pdf 的配色"""
        # 定义配色方案
        self.color_primary = HexColor('#2c5282')  # 深蓝色 - 标题
        self.color_secondary = HexColor('#4a5568')  # 灰色 - 副标题
        self.color_text = HexColor('#1a202c')  # 深灰 - 正文
        self.color_light = HexColor('#718096')  # 浅灰 - 辅助文字
        self.color_link = HexColor('#3182ce')  # 蓝色 - 链接
        
        # 姓名样式
        self.styles.add(ParagraphStyle(
            name='Name',
            fontSize=26,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=8,
            textColor=self.color_primary,
            fontName='Helvetica-Bold'
        ))
        
        # 职位标题样式
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            fontSize=11,
            leading=13,
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=self.color_secondary,
            fontName='Helvetica'
        ))
        
        # 联系信息样式 - 带链接颜色
        self.styles.add(ParagraphStyle(
            name='Contact',
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=self.color_link,
            fontName='Helvetica'
        ))
        
        # 章节标题样式 - 带下划线效果
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=11,
            leading=13,
            spaceBefore=14,
            spaceAfter=8,
            textColor=self.color_primary,
            fontName='Helvetica-Bold'
        ))
        
        # 普通文本样式
        self.styles.add(ParagraphStyle(
            name='CVBody',
            fontSize=10,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=4,
            textColor=self.color_text,
            fontName='Helvetica'
        ))
        
        # 项目标题样式
        self.styles.add(ParagraphStyle(
            name='ProjectTitle',
            fontSize=10,
            leading=12,
            spaceBefore=10,
            spaceAfter=3,
            textColor=self.color_text,
            fontName='Helvetica-Bold'
        ))
        
        # 项目描述样式
        self.styles.add(ParagraphStyle(
            name='ProjectDesc',
            fontSize=9,
            leading=12,
            leftIndent=12,
            spaceAfter=2,
            textColor=self.color_secondary,
            fontName='Helvetica'
        ))
        
        # 技能分类样式
        self.styles.add(ParagraphStyle(
            name='SkillCategory',
            fontSize=10,
            leading=12,
            spaceBefore=8,
            spaceAfter=4,
            textColor=self.color_primary,
            fontName='Helvetica-Bold'
        ))
        
        # 技能列表样式 - 使用项目符号
        self.styles.add(ParagraphStyle(
            name='SkillList',
            fontSize=9,
            leading=12,
            leftIndent=12,
            spaceAfter=3,
            textColor=self.color_secondary,
            fontName='Helvetica'
        ))
        
    def load_profile(self):
        """加载个人档案数据"""
        with open('kb/profile.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_skills(self):
        """加载技能数据"""
        with open('kb/skills.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def create_header(self, profile):
        """创建页眉部分 - 带可点击链接"""
        from reportlab.platypus import KeepTogether
        
        elements = []
        
        # 姓名
        name = profile['personal_info'].get('preferred_name', profile['personal_info']['name'])
        elements.append(Paragraph(name, self.styles['Name']))
        
        # 职位标题
        elements.append(Paragraph("Senior Android Developer · Java Backend Engineer", self.styles['JobTitle']))
        
        # 联系信息 - 使用链接格式
        contact = profile['personal_info']['contact']
        email = contact['email']
        phone = contact['phone']
        location = f"{contact['location']['city']}, {contact['location']['country']}"
        
        # 创建带链接的联系信息行 - 使用 # 开头的颜色值
        contact_line = f'<a href="mailto:{email}" color="#3182ce">{email}</a> | {phone} | {location}'
        elements.append(Paragraph(contact_line, self.styles['Contact']))
        
        # 分隔线 - 使用主题色
        elements.append(HRFlowable(width="100%", thickness=1.5, color=self.color_primary))
        elements.append(Spacer(1, 10))
        
        return elements
    
    def create_summary(self, profile):
        """创建个人总结部分"""
        elements = []
        elements.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
        
        summary = """Senior Android Developer with <b>12+ years of experience</b> building enterprise mobile and 
        backend systems. Currently completing Master's in Computer and Information Sciences at AUT 
        (graduating <b>February 2026</b>). Proven expertise in <b>Android development</b> with hardware 
        integration, <b>Java Spring Boot microservices</b>, and full-stack delivery from mobile clients 
        to cloud infrastructure."""
        
        elements.append(Paragraph(summary, self.styles['CVBody']))
        elements.append(Spacer(1, 8))
        
        return elements
    
    def create_skills(self):
        """创建技能部分"""
        elements = []
        elements.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
        
        skills_data = [
            ("Primary Expertise", [
                "<b>Android:</b> Java, Kotlin, Android SDK, Jetpack, MVVM/MVP, NDK, JNI, SQLite, Room",
                "<b>Backend:</b> Spring Boot, Spring Cloud, REST APIs, Microservices, MyBatis, JPA",
                "<b>Databases:</b> MySQL, PostgreSQL, Oracle, Redis, MongoDB, SQL Server"
            ]),
            ("Supporting Skills", [
                "<b>Frontend:</b> Vue.js, JavaScript, HTML/CSS",
                "<b>DevOps:</b> Docker, Kubernetes, Jenkins, CI/CD, Nginx, Linux (CentOS/Ubuntu)",
                "<b>Data:</b> Kettle ETL, PowerBI, FineReport"
            ]),
            ("Additional Capabilities", [
                "<b>AI/ML:</b> PyTorch, TensorFlow, OpenCV, YOLO (thesis project)",
                "<b>AI-Assisted Development:</b> Cursor, GitHub Copilot, Claude Code, Antigravity, OpenCode",
                "<b>Security:</b> Reverse engineering with JADX, Xposed",
                "<b>IoT:</b> RFID, barcode scanners, sensors, MQTT, Modbus"
            ])
        ]
        
        for category, items in skills_data:
            elements.append(Paragraph(category, self.styles['SkillCategory']))
            for item in items:
                elements.append(Paragraph(f"• {item}", self.styles['SkillList']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def create_experience(self):
        """创建工作经历部分"""
        elements = []
        elements.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))
        
        # AUT
        elements.append(Paragraph("Auckland University of Technology (AUT) — New Zealand", self.styles['ProjectTitle']))
        elements.append(Paragraph("<i>Master's Student & AI Researcher</i> | Jul 2024 – Feb 2026", self.styles['CVBody']))
        elements.append(Paragraph("• <b>ChatClothes Virtual Try-On</b> — Developed multimodal AI system with PyTorch, YOLO, and LLM integration, submitted thesis 6 months early", self.styles['ProjectDesc']))
        elements.append(Spacer(1, 6))
        
        # Chunxiao
        elements.append(Paragraph("Chunxiao Technology Co., Ltd. — China", self.styles['ProjectTitle']))
        elements.append(Paragraph("<i>Technical Lead / Senior Software Engineer</i> | Jan 2013 – Jun 2024", self.styles['CVBody']))
        elements.append(Paragraph("<i>Promoted from Software Engineer to Technical Lead, leading cross-functional development teams</i>", self.styles['CVBody']))
        elements.append(Spacer(1, 4))
        
        # 项目经历
        projects = [
            ("Smart Factory System (2018 – 2024)", [
                "Architected Spring Boot microservices supporting 5+ manufacturing sites with 99.9% uptime",
                "Developed Android apps with RFID/barcode integration for shop-floor operations",
                "Built CI/CD pipelines with Docker, Jenkins, Nginx on Linux servers",
                "Improved production efficiency by 30%+ across factory bases"
            ]),
            ("Enterprise Messaging Platform (2014 – 2023)", [
                "Built Android client using NDK-based TCP/UDP, achieving <200ms message latency",
                "Developed backend with Spring Cloud supporting 10,000+ daily active users",
                "Processed 500K+ messages daily across Android, Web, and PC clients",
                "Implemented BI analytics with Kettle ETL, PowerBI dashboards"
            ]),
            ("Live Streaming Commerce System (2015 – 2018)", [
                "Built multi-language platform: Java/Kotlin Android, C++ NDK streaming core",
                "Implemented real-time features with WebSocket, HLS/M3U8 streaming",
                "Delivered 1,000+ concurrent viewer capacity with adaptive bitrate"
            ])
        ]
        
        for title, bullets in projects:
            elements.append(Paragraph(f"<b>{title}</b>", self.styles['CVBody']))
            for bullet in bullets:
                elements.append(Paragraph(f"• {bullet}", self.styles['ProjectDesc']))
            elements.append(Spacer(1, 4))
        
        elements.append(Spacer(1, 4))
        return elements
    
    def create_education(self, profile):
        """创建教育背景部分"""
        elements = []
        elements.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
        
        education = profile['education']
        
        # Master
        master = education[0]
        elements.append(Paragraph(f"<b>{master['degree']}</b>", self.styles['CVBody']))
        elements.append(Paragraph(f"{master['institution']}, {master['location']} | 2024 – 2026 (Feb)", self.styles['CVBody']))
        elements.append(Paragraph("• Research Focus: AI, Computer Vision, Edge Computing", self.styles['ProjectDesc']))
        elements.append(Paragraph("• Thesis: ChatClothes Virtual Try-On System (submitted early)", self.styles['ProjectDesc']))
        elements.append(Spacer(1, 4))
        
        # Bachelor
        bachelor = education[1]
        elements.append(Paragraph(f"<b>{bachelor['degree']}</b>", self.styles['CVBody']))
        elements.append(Paragraph(f"{bachelor['institution']}, {bachelor['location']} | 2009 – 2013", self.styles['CVBody']))
        elements.append(Paragraph("• National Scholarship recipient", self.styles['ProjectDesc']))
        
        return elements
    
    def generate(self):
        """生成完整简历"""
        print("Loading Career KB data...")
        profile = self.load_profile()
        
        print("Building CV sections...")
        elements = []
        
        # 构建各部分
        elements.extend(self.create_header(profile))
        elements.extend(self.create_summary(profile))
        elements.extend(self.create_skills())
        elements.extend(self.create_experience())
        elements.extend(self.create_education(profile))
        
        # 生成PDF
        print(f"Generating PDF: {self.output_path}")
        self.doc.build(elements)
        print("CV generated successfully!")
        
        return self.output_path


def main():
    """主函数"""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    output_path = os.path.join(output_dir, f"CV_Leo_Zhang_{timestamp}.pdf")
    
    generator = CVGenerator(output_path)
    result = generator.generate()
    
    print(f"\nOutput: {result}")
    print(f"File size: {os.path.getsize(result) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
