#!/usr/bin/env python3
"""
JD 抓取与关键词提取工具

用途：
- 从公开招聘链接抓取 JD 文本；
- 或从本地 JD 文本文件中读取内容；
- 提取一组用于简历生成的关键词（用于传给 jd_keywords）。

说明：
- 这是一个尽量「弱依赖」的实现：
  - 优先使用 requests + BeautifulSoup 做 HTML 提取；
  - 如果缺少依赖，会给出友好提示并返回空文本/空关键词。
- LinkedIn 等需登录的站点：可提供 Cookie 以抓取 JD，见 _get_linkedin_cookies()。
  请勿将 Cookie 写入代码或提交到仓库；使用环境变量或本地文件（已 gitignore）。
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Optional, Tuple


TECH_TOKEN_WHITELIST = {
    "python", "java", "kotlin", "javascript", "typescript", "node.js", "nodejs",
    "react", "next.js", "angular", "angularjs", "graphql", "rest", "api",
    "docker", "kubernetes", "azure", "aws", "gcp", "redis", "mysql", "postgresql",
    "mongodb", "c#", "c++", "golang", "go", "jenkins", "sentry", "bugsnag",
    "rabbitmq", "playwright", "selenium", "cursor", "claude",
}


def _parse_cookie_string(cookie_str: str) -> dict:
    """把 'name1=value1; name2=value2' 转为 requests 可用的 Cookie 字典。"""
    out = {}
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def _get_linkedin_cookies() -> Optional[dict]:
    """
    从环境变量 LINKEDIN_JD_COOKIES 或项目根目录下的 .linkedin_cookies 文件读取 Cookie。
    仅用于 JD 抓取，不写入任何默认文件；.linkedin_cookies 已加入 .gitignore，请勿提交。
    """
    raw = os.environ.get("LINKEDIN_JD_COOKIES", "").strip()
    if raw:
        return _parse_cookie_string(raw)
    # 尝试项目根目录下的 .linkedin_cookies 文件（仅包含一行 cookie 字符串）
    for base in (Path(__file__).resolve().parent.parent.parent, Path.cwd()):
        path = base / ".linkedin_cookies"
        if path.exists():
            try:
                raw = path.read_text(encoding="utf-8", errors="ignore").strip()
                if raw:
                    return _parse_cookie_string(raw)
            except Exception:
                pass
            break
    return None


def fetch_jd_text_from_url(url: str, cookies: Optional[dict] = None) -> str:
    """
    从公开网页抓取 JD 文本（粗略正文提取）。

    cookies: 可选，用于需登录的站点（如 LinkedIn），格式为 {'name': 'value', ...}。
    返回纯文本字符串；如果失败则返回空字符串。
    """
    try:
        import requests  # type: ignore
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError:
        # 依赖缺失时不中断主流程，由上层决定是否降级为手动 jd_keywords
        print(
            "Warning: requests / beautifulsoup4 not installed; cannot fetch JD URL automatically. "
            "Install dependencies from `requirements.txt` or provide --jd-keywords manually."
        )
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(url, timeout=15, cookies=cookies or {}, headers=headers)
        resp.raise_for_status()
    except Exception as e:
        print(f"Warning: failed to fetch JD URL `{url}`: {e}")
        return ""

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        # 去掉 script/style
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        # 清理多余空白
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return "\n".join(lines)
    except Exception as e:
        print(f"Warning: failed to parse JD HTML from `{url}`: {e}")
        return ""


def load_jd_text_from_file(path: str | Path) -> str:
    """
    从本地 JD 文件（.txt / .md 等）读取文本。
    """
    p = Path(path)
    if not p.exists():
        print(f"Warning: JD file not found: {p}")
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Warning: failed to read JD file: {e}")
        return ""


def extract_keywords_from_text(text: str, max_keywords: int = 20) -> List[str]:
    """
    从 JD 文本中提取一组简单关键词，用于驱动项目/技能排序。

    策略（启发式，刻意保持「保守」）：
    - 拆分出由字母/数字/+/# 组成的 token；
    - 过滤长度 < 3 的 token；
    - 过滤常见英语停用词 和 通用职位词（engineer, developer 等）；
    - **按出现频次降序排序**：高频词更可能是 JD 核心要求，单次噪声词排后；
    - 保留顺序去重，最多 max_keywords 个。
    """
    if not text:
        return []

    tokens = re.findall(r"[A-Za-z0-9#+\.]{3,}", text)
    if not tokens:
        return []

    stopwords = {
        "and",
        "the",
        "with",
        "for",
        "you",
        "your",
        "our",
        "are",
        "will",
        "this",
        "that",
        "have",
        "has",
        "from",
        "into",
        "about",
        "job",
        "role",
        "team",
        "work",
        "working",
        "engineer",
        "developer",
        "senior",
        "junior",
        "lead",
        "manager",
        "software",
        "experience",
        "years",
        "responsibilities",
        "requirements",
        "skills",
        "ability",
        "strong",
        "excellent",
        "preferred",
        "nice",
        "plus",
        "must",
        "least",
        "including",
        "across",
        # 登录/错误页常见词，避免被当作 JD 关键词
        "linkedin",
        "login",
        "sign",
        "password",
        "privacy",
        "agreement",
        "policy",
        "cookie",
        "email",
        "phone",
        "show",
        "forgot",
        "keep",
        "logged",
        "clicking",
        "continue",
        "agree",
        "user",
        "updated",
        "professional",
        "world",
        # 职位站点导航/浏览器噪声词（避免误命中 JD）
        "google",
        "microsoft",
        "apple",
        "mozilla",
        "chrome",
        "edge",
        "safari",
        "firefox",
        "smartrecruiters",
    }

    # Step 1: count occurrences of each normalized token
    freq: dict[str, int] = {}
    canonical: dict[str, str] = {}  # norm -> first seen display form
    for tk in tokens:
        norm = tk.strip().strip(".").lower()
        if not norm or len(norm) < 3:
            continue
        if norm in stopwords:
            continue
        # 过滤纯数字
        if norm.isdigit():
            continue
        freq[norm] = freq.get(norm, 0) + 1
        if norm not in canonical:
            canonical[norm] = tk.strip().strip(".,;:")  # keep first display form, trim punctuation

    if not freq:
        return []

    def _is_likely_technical(norm_token: str, raw_token: str) -> bool:
        if norm_token in TECH_TOKEN_WHITELIST:
            return True
        if any(ch in raw_token for ch in {"+", "#", ".", "/"}):
            return True
        # Mixed-case/upper acronyms often indicate tech terms (API, SQL, JWT)
        if any(ch.isupper() for ch in raw_token):
            return True
        return False

    # Step 2: apply frequency floor for non-technical one-off tokens
    # This helps noisy job pages (e.g. site navigation text) without dropping stack terms.
    filtered_norms: List[str] = []
    for norm in freq.keys():
        raw = canonical.get(norm, norm)
        if freq[norm] >= 2 or _is_likely_technical(norm, raw):
            filtered_norms.append(norm)

    if not filtered_norms:
        return []

    # Step 3: sort by frequency descending, then alphabetically for ties
    sorted_norms = sorted(filtered_norms, key=lambda n: (-freq[n], n))

    # Step 4: emit up to max_keywords display-form tokens
    keywords: List[str] = []
    for norm in sorted_norms:
        keywords.append(canonical[norm])
        if len(keywords) >= max_keywords:
            break

    return keywords



def derive_keywords_from_url(
    url: str,
    max_keywords: int = 20,
    cookies: Optional[dict] = None,
) -> Tuple[str, List[str]]:
    """
    便捷函数：从 URL 抓取 JD 文本并提取关键词。

    cookies: 可选。若为 None 且 URL 包含 linkedin.com，会尝试从环境变量
    LINKEDIN_JD_COOKIES 或项目根目录 .linkedin_cookies 文件读取。
    返回 (jd_text, keywords)。
    """
    if cookies is None and "linkedin.com" in url.lower():
        cookies = _get_linkedin_cookies()
        if cookies:
            print("  Using LinkedIn cookies from LINKEDIN_JD_COOKIES or .linkedin_cookies")
    text = fetch_jd_text_from_url(url, cookies=cookies)
    kws = extract_keywords_from_text(text, max_keywords=max_keywords) if text else []
    return text, kws


