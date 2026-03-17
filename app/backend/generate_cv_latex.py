#!/usr/bin/env python3
"""
Career KB LaTeX Resume Generator (LEGACY)
基于 LaTeX 模板生成专业简历。

说明：
- 本脚本中的 Summary / Skills / Experience 内容基本为手写硬编码，
  只少量读取 `kb/profile.yaml` 里的姓名和联系方式。
- 目前推荐的简历内容管线是：
    app/backend/generate_cv_from_kb.py  +  generate_cv_html_to_pdf.html_to_pdf
  并通过根目录命令行入口 `python generate.py cv ...` 调用。

建议：
- 如需 LaTeX 版本，仅将本脚本视为「早期模板示例」，后续可以改为消费
  由 `generate_cv_from_kb.py` 生成的统一结构化数据。
"""

import yaml
import os
import argparse
from datetime import datetime


def load_profile():
    """加载个人档案"""
    with open('kb/profile.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_latex_cv():
    """生成 LaTeX 简历内容"""
    profile = load_profile()
    
    contact = profile['personal_info']['contact']
    name = profile['personal_info'].get('preferred_name', profile['personal_info']['name'])
    
    latex_content = r"""\documentclass[a4paper,12pt]{article}
\input{myPackage.tex}

\newcommand{\cvsection}[1]{\section*{\textcolor{darkblue}{#1}}}

\begin{document}
\pagestyle{empty}

% -------------------- Header --------------------
\begin{tabularx}{\linewidth}{@{} C @{}}
\Huge
"""
    
    # Header with name and links
    latex_content += f"""\\href{{https://www.linkedin.com/in/leo-zhang-305626280/}}
{{{name}~\\raisebox{{-0.3ex}}{{\\includegraphics[height=1.8ex]{{images/linkedin.png}}}}~
\\href{{https://github.com/leozhang2056}}
{{\\raisebox{{-0.3ex}}{{\\includegraphics[height=2ex]{{images/github.png}}}}}}
}} \\\\[0pt]

\\href{{mailto:{contact['email']}}}{{\\raisebox{{-0.05\\height}}\\faEnvelope ~ {contact['email']}}} \\ $|$ 
\\href{{tel:{contact['phone'].replace(' ', '')}}}{{\\raisebox{{-0.05\\height}}\\faMobile ~ {contact['phone']}}} \\ $|$ 
\\href{{https://maps.app.goo.gl/CdzudR6FUy9tHDX97}}{{\\raisebox{{-0.05\\height}}\\faMapMarker ~ {contact['location']['city']}, {contact['location']['country']}}} \\\\
\\end{{tabularx}}

% -------------------- Summary --------------------
\\cvsection{{Summary}}
\\small{{
Senior Android Developer with \\textbf{{12+ years of experience}} building enterprise mobile and backend systems. Currently completing \\textbf{{Master's in Computer and Information Sciences}} at \\textbf{{AUT}}, graduating \\textbf{{February 2026}}.

Over \\textbf{{12 years of experience}} in \\textbf{{Android development, Java backend, AI integration, and IoT systems}}, delivering enterprise solutions in \\textbf{{industrial automation, mobile platforms, and edge AI}}.
Proficient in \\textbf{{Android SDK, Spring Boot, Docker, PyTorch, and microservice architecture}}, with hands-on expertise in \\textbf{{AI-driven applications, full-stack systems, and cloud deployment}}.
}}

% -------------------- Key Skills --------------------
\\cvsection{{Key Skills}}
\\small{{
\\begin{{itemize}}[leftmargin=1em, itemsep=3pt]
  \\item \\textbf{{Android:}} Java, Kotlin, Android SDK, Jetpack, MVVM/MVP, NDK, JNI, SQLite, Room
  \\item \\textbf{{Backend:}} Spring Boot, Spring Cloud, REST APIs, Microservices, MyBatis, JPA
  \\item \\textbf{{Databases:}} MySQL, PostgreSQL, Oracle, Redis, MongoDB, SQL Server, SQLite
  \\item \\textbf{{DevOps:}} Docker, Kubernetes, Jenkins, CI/CD, Nginx, Linux (CentOS/Ubuntu)
  \\item \\textbf{{Data:}} Kettle ETL, PowerBI, FineReport
  \\item \\textbf{{AI / ML:}} PyTorch, TensorFlow, OpenCV, YOLO, diffusion models, LLM (thesis project)
  \\item \\textbf{{Security:}} Reverse engineering with JADX, Xposed
  \\item \\textbf{{IoT:}} RFID, barcode scanners, sensors, MQTT, Modbus
\\end{{itemize}}
}}

% -------------------- Experience --------------------
\\cvsection{{Experience}}
\\small{{

\\textbf{{ChatClothes Virtual Try-On (AI Thesis Project)}} \\hfill \\textit{{AUT, NZ}} \\hfill \\textcolor{{gray}}{{2024 -- 2026}} \\\\
\\textbf{{Sole developer}} of a multimodal AI try-on system with LLM control and edge deployment.
\\begin{{itemize}}[nosep, leftmargin=1em, itemsep=3pt]
  \\item \\textbf{{Built}} modular pipeline: diffusion model (image generation) + YOLO (clothing detection) + LLM (prompt parsing)
  \\item \\textbf{{Integrated}} ComfyUI + Dify for orchestration, supporting browser and offline operation
  \\item \\textbf{{Optimized}} inference on Raspberry Pi 5, achieving low-latency edge performance
  \\item Completed thesis 6 months early with demo and deployment guide
\\end{{itemize}}

\\vspace{{4pt}}

\\textbf{{Smart Factory System}} \\hfill \\textit{{Chunxiao Technology Co., Ltd., China}} \\hfill \\textcolor{{gray}}{{2018 -- 2024}} \\\\
\\textbf{{Technical Lead}} for a microservice-based textile factory system deployed across 5+ sites.
\\begin{{itemize}}[nosep, leftmargin=1em, itemsep=3pt]
  \\item \\textbf{{Architected}} Spring Boot microservices supporting 5+ manufacturing sites with 99.9\\% uptime
  \\item \\textbf{{Developed}} Android apps for shop-floor operations with RFID/barcode integration
  \\item \\textbf{{Built}} CI/CD pipelines with Docker, Jenkins, Nginx on Linux servers
  \\item \\textbf{{Improved}} production efficiency by 30\\%+ across factory bases
\\end{{itemize}}

\\vspace{{4pt}}

\\textbf{{Enterprise Messaging Platform}} \\hfill \\textit{{Chunxiao Technology Co., Ltd., China}} \\hfill \\textcolor{{gray}}{{2014 -- 2023}} \\\\
\\textbf{{Core Android \\& backend developer}} for real-time IM platform with 10,000+ daily users.
\\begin{{itemize}}[nosep, leftmargin=1em, itemsep=3pt]
  \\item \\textbf{{Built}} Android client using NDK-based TCP/UDP, achieving \\textbf{{<200ms}} message latency
  \\item \\textbf{{Developed}} backend with Spring Cloud supporting 10,000+ daily active users
  \\item \\textbf{{Processed}} 500K+ messages daily across Android, Web, and PC clients
  \\item \\textbf{{Implemented}} BI analytics with Kettle ETL, PowerBI dashboards
\\end{{itemize}}

\\vspace{{4pt}}

\\textbf{{Live Streaming Commerce System}} \\hfill \\textit{{Chunxiao Technology Co., Ltd., China}} \\hfill \\textcolor{{gray}}{{2015 -- 2018}} \\\\
\\textbf{{Full-stack developer}} for multi-language live streaming platform.
\\begin{{itemize}}[nosep, leftmargin=1em, itemsep=3pt]
  \\item \\textbf{{Built}} multi-language platform: Java/Kotlin Android, C++ NDK streaming core, ASP.NET web admin
  \\item \\textbf{{Implemented}} real-time features with WebSocket, HLS/M3U8 streaming
  \\item \\textbf{{Delivered}} 1,000+ concurrent viewer capacity with adaptive bitrate
\\end{{itemize}}

\\vspace{{4pt}}

\\textbf{{IoT Solutions}} \\hfill \\textit{{Chunxiao Technology Co., Ltd., China}} \\hfill \\textcolor{{gray}}{{2013 -- 2024}} \\\\
\\textbf{{Full-stack engineer}} for industrial, IoT, and public service applications.
\\begin{{itemize}}[nosep, leftmargin=1em, itemsep=3pt]
  \\item \\textbf{{Developed}} Android apps for smart lockers, forest patrol, energy management systems
  \\item \\textbf{{Built}} Vue.js dashboards for real-time monitoring and data visualization
  \\item \\textbf{{Created}} reusable hardware SDKs for RFID, barcode, sensor integration
\\end{{itemize}}
}}

% -------------------- Education --------------------
\\cvsection{{Education}}
\\small{{
\\textbf{{Master of Computer and Information Sciences}} \\hfill \\textit{{AUT, New Zealand}} \\hfill \\textcolor{{lightgray}}{{Jul 2024 -- Feb 2026}} \\\\
Research focus: AI, Computer Vision, Edge Computing. Thesis submitted 6 months early.

\\vspace{{6pt}}

\\textbf{{Bachelor of Software Engineering}} \\hfill \\textit{{Hebei University of Science and Technology, China}} \\hfill \\textcolor{{lightgray}}{{Jul 2009 -- Jun 2013}} \\\\
National Scholarship recipient. Trained in Java, databases, and backend system design.
}}

\\end{{document}}
"""
    
    return latex_content


def main():
    """旧版 LaTeX 模板主函数（需显式确认）"""
    parser = argparse.ArgumentParser(description="LEGACY LaTeX CV template generator")
    parser.add_argument(
        "--legacy-ok",
        action="store_true",
        help="Acknowledge this generates an outdated hardcoded template.",
    )
    args = parser.parse_args()

    if not args.legacy_ok:
        print("This is a legacy script with hardcoded resume content.")
        print("Use unified pipeline instead: python generate.py cv ...")
        print("If you still want the legacy .tex output, run with --legacy-ok.")
        return

    print("Generating LaTeX CV...")
    
    latex_content = generate_latex_cv()
    
    # 保存到 outputs 目录
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"CV_Leo_Zhang_{timestamp}.tex")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"LaTeX file generated: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")
    print("\nTo compile to PDF:")
    print(f"1. Copy {output_file} to templates/Latex/")
    print("2. Run: pdflatex CV_Leo_Zhang_*.tex")
    print("3. Or upload to Overleaf to compile online")


if __name__ == "__main__":
    main()
