#!/usr/bin/env python3
"""
HTML → PDF 工具 & 旧版模板 (LEGACY)

当前角色定位：
- `html_to_pdf(html_content, output_path)` 是推荐使用的通用「HTML 转 PDF」工具，
  供 `generate_cv_from_kb.py`、`generate_cover_letter.py` 等主线调用。
- 本文件内的 `generate_html()` 与 `main()` 中的硬编码简历模板属于早期版本，
  内容已与 Career KB 主线不完全一致，仅作为参考 / 对比使用。

如果要生成正式简历/求职信，请优先使用仓库根目录的统一入口：
  python generate.py cv ...
  python generate.py cl ...
"""

import asyncio
import argparse
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
        <strong>Full-Stack Developer</strong> with <strong>12 years of experience</strong> across <strong>Android, Backend, AI, and Frontend</strong>. Deep expertise in <strong>Android SDK, NDK, Kotlin/Java</strong> for mobile development, <strong>Spring Boot microservices</strong> for backend systems, and <strong>AI/ML integration</strong> for intelligent features. Proven ability to deliver complete solutions from mobile apps to cloud infrastructure. Strong foundation in <strong>React/Vue.js, RESTful APIs, and DevOps</strong>, enabling end-to-end ownership across the entire technology stack.
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
        <div class="job-role"><strong>Sole developer</strong> of a multimodal AI virtual fitting system with LLM control and edge deployment capabilities.</div>
        <ul class="job-list">
            <li><strong>Architected</strong> end-to-end pipeline integrating diffusion models for image generation, YOLO for clothing detection, and LLMs for prompt interpretation</li>
            <li><strong>Developed</strong> modular workflow system with ComfyUI and Dify orchestration, supporting both browser-based and offline edge deployment</li>
            <li><strong>Optimized</strong> PyTorch inference for Raspberry Pi 5, achieving real-time performance with low-latency edge computing</li>
            <li><strong>Delivered</strong> complete thesis 6 months early with working demo, deployment guide, and comprehensive documentation</li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">Smart Factory System</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2018 -- 2024</span>
        </div>
        <div class="job-role"><strong>Technical Lead</strong> for enterprise manufacturing platform deployed across 5+ factory sites with 99.9% uptime.</div>
        <ul class="job-list">
            <li><strong>Architected</strong> Spring Boot microservices with Spring Cloud, supporting 5+ manufacturing sites and 1000+ concurrent users</li>
            <li><strong>Developed</strong> Android applications for shop-floor operations with RFID/barcode integration and offline-first design</li>
            <li><strong>Built</strong> CI/CD pipelines with Docker, Jenkins, and Nginx on Linux (CentOS/Ubuntu) servers</li>
            <li><strong>Integrated</strong> industrial IoT devices: RFID readers, barcode scanners, electronic scales, and conveyor systems</li>
            <li><strong>Improved</strong> production efficiency by 30%+ through real-time process tracking and automated workflows</li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">Enterprise Messaging Platform</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2014 -- 2023</span>
        </div>
        <div class="job-role"><strong>Core Android & Backend Developer</strong> for real-time IM system supporting 10,000+ daily active users.</div>
        <ul class="job-list">
            <li><strong>Built</strong> high-performance Android client using NDK-based TCP/UDP protocols, achieving <strong>&lt;200ms</strong> message latency</li>
            <li><strong>Developed</strong> scalable backend with Spring Cloud and C++ native modules, processing 500K+ messages daily</li>
            <li><strong>Implemented</strong> cross-platform support (Android, Web, PC) with real-time synchronization</li>
            <li><strong>Created</strong> BI analytics infrastructure with Kettle ETL pipelines and PowerBI dashboards for user behavior analysis</li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">Live Streaming Commerce System</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2015 -- 2018</span>
        </div>
        <div class="job-role"><strong>Full-Stack Developer</strong> for multi-language live streaming platform with 1,000+ concurrent viewers.</div>
        <ul class="job-list">
            <li><strong>Built</strong> multi-language architecture: Java/Kotlin Android, C++ NDK streaming core, ASP.NET web admin, Python analytics</li>
            <li><strong>Implemented</strong> real-time streaming with WebSocket, RTMP ingestion, and HLS/M3U8 adaptive bitrate delivery</li>
            <li><strong>Developed</strong> low-latency streaming engine handling 1,000+ concurrent viewers with adaptive quality (360p-1080p)</li>
            <li><strong>Created</strong> Lua-based configuration system for dynamic business rules and hot-swappable settings</li>
        </ul>
    </div>
    
    <div class="job">
        <div class="job-header">
            <span class="job-title">IoT Solutions & Smart Hardware</span>
            <span class="job-company">Chunxiao Technology Co., Ltd., China</span>
            <span class="job-date">2013 -- 2024</span>
        </div>
        <div class="job-role"><strong>Full-Stack Engineer</strong> for industrial IoT, smart hardware, and public service applications.</div>
        <ul class="job-list">
            <li><strong>Developed</strong> forestry patrol mobile app with GPS tracking, offline maps, and photo-based risk reporting</li>
            <li><strong>Built</strong> smart locker/book cabinet systems with Android control, sensor integration, and REST API backend</li>
            <li><strong>Created</strong> reusable hardware SDKs for RFID, barcode scanners, and industrial sensors (UART/RS232/Modbus)</li>
            <li><strong>Implemented</strong> Vue.js dashboards for real-time monitoring, data visualization, and equipment management</li>
            <li><strong>Deployed</strong> digital signage and broadcast control systems with MQTT-based remote management</li>
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
        <div class="edu-detail">Research focus: AI, lightweight model deployment, virtual try-on. GPA: A. Thesis submitted early.</div>
    </div>
    
    <div class="edu-item">
        <div class="edu-header">
            <span class="edu-title">Bachelor of Software Engineering</span>
            <span class="edu-school">Hebei University of Science and Technology, China</span>
            <span class="edu-date">Jul 2009 -- Jun 2013</span>
        </div>
        <div class="edu-detail">Received National Scholarship. GPA: 3.5/4.0. Trained in Java, databases, and backend system design.</div>
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
        
        # 加载 HTML 内容（wait_until 避免偶发未渲染完就导出 PDF）
        await page.set_content(html_content, wait_until='load')
        
        # 等待布局稳定
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
    """旧版模板主函数（需显式确认）"""
    parser = argparse.ArgumentParser(description="LEGACY CV template generator")
    parser.add_argument(
        "--legacy-ok",
        action="store_true",
        help="Acknowledge this generates an outdated hardcoded template.",
    )
    args = parser.parse_args()

    if not args.legacy_ok:
        print("This is a legacy script with hardcoded resume content.")
        print("Use unified pipeline instead: python generate.py cv ...")
        print("If you still want the legacy output, run with --legacy-ok.")
        return

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
