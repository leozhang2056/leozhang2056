#!/usr/bin/env python3
"""
使用 Playwright 将 HTML 转换为 PDF
保持 LaTeX 模板风格和可点击链接
"""

import asyncio
from playwright.async_api import async_playwright
import yaml
import os
from datetime import datetime


def load_profile():
    """加载个人档案"""
    with open('kb/profile.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_html():
    """生成 HTML 简历内容 - 严格按照 LaTeX 模板结构"""
    profile = load_profile()
    
    contact = profile['personal_info']['contact']
    name = profile['personal_info'].get('preferred_name', profile['personal_info']['name'])
    
    html_content = f"""<!DOCTYPE html>
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
        
        /* Header - 严格按模板 */
        .header {{
            text-align: center;
            margin-bottom: 8px;
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
            line-height: 1.5;
        }}
        
        .contact a {{
            color: #000080;
            text-decoration: none;
        }}
        
        /* Section 标题 - 带下划线 */
        .section-title {{
            font-size: 12pt;
            font-weight: bold;
            color: #000080;
            text-transform: none;
            margin-top: 12px;
            margin-bottom: 6px;
            border-bottom: 1px solid #000;
            padding-bottom: 2px;
        }}
        
        /* Summary */
        .summary {{
            font-size: 10.5pt;
            text-align: left;
            line-height: 1.4;
            margin-bottom: 8px;
        }}
        
        /* Skills - 使用项目符号 */
        .skills-list {{
            list-style: disc;
            margin-left: 20px;
            font-size: 10.5pt;
            line-height: 1.5;
        }}
        
        .skills-list li {{
            margin-bottom: 3px;
        }}
        
        /* Experience */
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
        
        .job-company {{
            font-style: italic;
        }}
        
        .job-date {{
            color: #666;
        }}
        
        .job-role {{
            font-size: 10.5pt;
            margin-top: 2px;
            margin-bottom: 3px;
        }}
        
        .job-list {{
            list-style: disc;
            margin-left: 20px;
            font-size: 10pt;
            line-height: 1.4;
        }}
        
        .job-list li {{
            margin-bottom: 1px;
        }}
        
        /* Education */
        .edu-item {{
            margin-bottom: 10px;
        }}
        
        .edu-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-size: 10.5pt;
        }}
        
        .edu-title {{
            font-weight: bold;
        }}
        
        .edu-school {{
            font-style: italic;
        }}
        
        .edu-date {{
            color: #999;
        }}
        
        .edu-detail {{
            font-size: 10pt;
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
                padding: 0;
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
            <a href="mailto:{contact['email']}">&#9993; {contact['email']}</a> | 
            &#9990; {contact['phone']} | 
            &#9992; {contact['location']['city']}, {contact['location']['country']}
        </div>
    </div>
    
    <!-- Summary -->
    <div class="section-title">Summary</div>
    <div class="summary">
        Senior Android Developer with <strong>12+ years of experience</strong> building enterprise mobile and backend systems. Currently completing <strong>Master's in Computer and Information Sciences at AUT</strong> (graduating <strong>February 2026</strong>). Proven expertise in <strong>Android SDK, NDK, Java Spring Boot microservices</strong>, and <strong>full-stack delivery</strong>. Track record of leading teams and delivering high-scale systems with 99.9% uptime.
    </div>
    
    <!-- Key Skills -->
    <div class="section-title">Key Skills</div>
    <ul class="skills-list">
        <li><strong>Programming:</strong> Java, Kotlin, Python, JavaScript, Node.js, SQL, Bash</li>
        <li><strong>AI / ML:</strong> PyTorch, TensorFlow, OpenCV, YOLO, diffusion models, LLM fine-tuning</li>
        <li><strong>AI Coding Tools:</strong> Cursor, Trae, GitHub Copilot, Qwen, OpenAI API</li>
        <li><strong>Full-Stack:</strong> Spring Boot, Spring Cloud, MyBatis, Hibernate, Vue.js, HTML/CSS</li>
        <li><strong>DevOps & Cloud:</strong> Docker, Jenkins, Nginx, Git, CentOS, Ubuntu, Raspberry Pi, basic Azure</li>
        <li><strong>Databases:</strong> MySQL, Redis, MongoDB, SQLite, SQL Server</li>
        <li><strong>IoT Integration:</strong> UART, GPIO, barcode scanners, RFID, sensors, protocol adapters</li>
    </ul>
    
    <!-- Experience -->
    <div class="section-title">Experience</div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">ChatClothes Virtual Try-On (AI Thesis Project)</span>
            <span class="job-company">AUT, NZ</span>
            <span class="job-date">2024 -- 2026</span>
        </div>
        <div class="job-role"><strong>Sole developer</strong> of a multimodal AI try-on system with LLM control and edge deployment.</div>
        <ul class="job-list">
            <li><strong>Built</strong> modular pipeline: diffusion model (image generation) + YOLO (clothing detection) + LLM (prompt parsing)</li>
            <li><strong>Integrated</strong> ComfyUI + Dify for orchestration, supporting browser and offline operation</li>
            <li><strong>Optimized</strong> inference on Raspberry Pi 5, achieving low-latency edge performance</li>
            <li>Completed thesis 6 months early with demo and deployment guide</li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">Smart Factory Backend System</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2018 -- 2024</span>
        </div>
        <div class="job-role"><strong>Tech lead</strong> for a microservice-based textile factory system deployed across 5+ sites.</div>
        <ul class="job-list">
            <li><strong>Designed and implemented</strong> backend services with Spring Boot and MySQL/Redis</li>
            <li><strong>Managed</strong> CI/CD and deployment via Docker, Jenkins, and Nginx on Linux servers</li>
            <li><strong>Integrated</strong> RFID, barcode scanners, and conveyor systems for real-time process tracking</li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">Enterprise Messaging System</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2014 -- 2023</span>
        </div>
        <div class="job-role"><strong>Core Android & backend developer</strong> for real-time IM platform with 10,000+ daily users.</div>
        <ul class="job-list">
            <li><strong>Developed</strong> Android client using NDK-based TCP/UDP and backend using Spring Cloud + C++</li>
            <li><strong>Improved</strong> connection stability and reduced message latency to <strong>&lt;200ms</strong></li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">Other Projects & IoT Solutions</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2013 -- 2024</span>
        </div>
        <div class="job-role"><strong>Full-stack engineer</strong> for industrial, IoT, and public service applications.</div>
        <ul class="job-list">
            <li><strong>Developed</strong> forestry patrol app with GPS/photo logging and backend dashboard</li>
            <li><strong>Built</strong> smart cabinet SDKs controlling locks, sensors, and lights via Android + REST APIs</li>
            <li><strong>Implemented</strong> ad scheduling and monitoring for factory and retail displays</li>
            <li><strong>Automated</strong> deployment and monitoring to maintain 99.9% uptime</li>
        </ul>
    </div>
    
    <!-- Education -->
    <div class="section-title">Education</div>
    
    <div class="edu-item">
        <div class="edu-header">
            <span class="edu-title">Master of Computer and Information Sciences</span>
            <span class="edu-school">AUT, New Zealand</span>
            <span class="edu-date">Jul 2024 -- Feb 2026</span>
        </div>
        <div class="edu-detail">Research focus: AI, lightweight model deployment, virtual try-on. Thesis submitted early.</div>
    </div>
    
    <div class="edu-item">
        <div class="edu-header">
            <span class="edu-title">Bachelor of Software Engineering</span>
            <span class="edu-school">Hebei University of Science and Technology, China</span>
            <span class="edu-date">Jul 2009 -- Jun 2013</span>
        </div>
        <div class="edu-detail">Received National Scholarship. Trained in Java, databases, and backend system design.</div>
    </div>
    
    <!-- Licenses & Certifications -->
    <div class="section-title">Licenses & Certifications</div>
    <ul class="license-list">
        <li>
            <div class="license-content">
                <span><strong>Software Design Engineer Certificate</strong> — China Qualification Authority</span>
                <span class="license-date">2019</span>
            </div>
        </li>
        <li>
            <div class="license-content">
                <span><strong>Network Communication Security Administrator</strong> — China Qualification Authority</span>
                <span class="license-date">2017</span>
            </div>
        </li>
        <li>
            <div class="license-content">
                <span><strong>Science and Technology Achievement Award (Smart Manufacturing)</strong> — Hebei, China</span>
                <span class="license-date">2020</span>
            </div>
        </li>
        <li>
            <div class="license-content">
                <span><strong>IoT Fundamentals (MOOC)</strong> — Xi'an Jiaotong University</span>
                <span class="license-date">2020</span>
            </div>
        </li>
    </ul>
</body>
</html>"""
    
    return html_content


async def html_to_pdf(html_content, output_path):
    """使用 Playwright 将 HTML 转换为 PDF"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 加载 HTML 内容
        await page.set_content(html_content)
        
        # 等待字体加载
        await page.wait_for_timeout(1000)
        
        # 生成 PDF
        await page.pdf(
            path=output_path,
            format='A4',
            margin={
                'top': '15mm',
                'right': '15mm',
                'bottom': '15mm',
                'left': '15mm'
            },
            print_background=True
        )
        
        await browser.close()


def main():
    """主函数"""
    print("Generating HTML CV...")
    html_content = generate_html()
    
    # 保存 HTML（可选）
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    html_file = os.path.join(output_dir, f"CV_Leo_Zhang_{timestamp}.html")
    pdf_file = os.path.join(output_dir, f"CV_Leo_Zhang_{timestamp}.pdf")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML saved: {html_file}")
    
    # 转换为 PDF
    print("Converting to PDF...")
    asyncio.run(html_to_pdf(html_content, pdf_file))
    
    print(f"\nPDF generated: {pdf_file}")
    print(f"File size: {os.path.getsize(pdf_file) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
