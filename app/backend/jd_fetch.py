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
import json
from typing import List, Optional, Tuple


TECH_TOKEN_WHITELIST = {
    "python", "java", "kotlin", "javascript", "typescript", "node.js", "nodejs",
    "react", "next.js", "angular", "angularjs", "graphql", "rest", "api",
    "docker", "kubernetes", "azure", "aws", "gcp", "redis", "mysql", "postgresql",
    "mongodb", "c#", "c++", "golang", "go", "jenkins", "sentry", "bugsnag",
    "rabbitmq", "playwright", "selenium", "cursor", "claude",
    "fastapi", "pytorch", "tensorflow", "opencv", "yolo", "llm", "rag",
    "comfyui", "dify", "ollama",
    "kafka", "activemq", "spring", "mybatis", "hibernate",
    "vue", "vue.js", "vuejs", "redux", "webpack", "vite",
    "bitrise", "github actions", "gitlab",
    "raspberry pi", "raspberry",
    "android", "kotlin", "jetpack", "compose", "mvvm", "ndk",
    "firebase", "ssl", "tls", "jwt", "oauth",
    "microservices", "microservice",
    "serverless", "lambda", "ecs", "eks", "s3",
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

        # SPA / Workday 等站点：可见正文在 #root 注入前几乎为空，但 og:description 与 JSON-LD 含完整 JD。
        embedded_chunks: List[str] = []

        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if og_desc and og_desc.get("content"):
            embedded_chunks.append(str(og_desc["content"]).strip())

        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            c = str(meta_desc["content"]).strip()
            if c and c not in embedded_chunks:
                embedded_chunks.append(c)

        def _collect_jobposting_descriptions(obj: object) -> None:
            if isinstance(obj, dict):
                types = obj.get("@type")
                is_posting = types == "JobPosting" or (
                    isinstance(types, list) and "JobPosting" in types
                )
                if is_posting:
                    desc = obj.get("description")
                    if desc and str(desc).strip():
                        embedded_chunks.append(str(desc).strip())
                for v in obj.values():
                    _collect_jobposting_descriptions(v)
            elif isinstance(obj, list):
                for it in obj:
                    _collect_jobposting_descriptions(it)

        for script in soup.find_all("script"):
            stype = (script.get("type") or "").lower()
            if "ld+json" not in stype:
                continue
            raw = (script.string or script.get_text() or "").strip()
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            _collect_jobposting_descriptions(data)

        def _dedupe_chunks(chunks: List[str]) -> List[str]:
            out: List[str] = []
            seen: set[str] = set()
            for ch in chunks:
                key = re.sub(r"\s+", " ", ch)[:240].lower()
                if key in seen:
                    continue
                seen.add(key)
                out.append(ch)
            return out

        embedded_chunks = _dedupe_chunks(embedded_chunks)

        # 去掉 script/style（在提取 JSON-LD 之后）
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        body_text = "\n".join(lines)

        if len(body_text) < 400 and embedded_chunks:
            return "\n\n".join(embedded_chunks)
        if embedded_chunks:
            merged = "\n\n".join(embedded_chunks + [body_text]).strip()
            return merged
        return body_text
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
        # ── common English function words ──
        "and", "the", "with", "for", "you", "your", "our", "are", "will",
        "this", "that", "these", "those", "have", "has", "had", "from",
        "into", "about", "its", "its", "been", "being", "while", "within",
        "who", "whom", "which", "what", "where", "when", "why", "how",
        "can", "could", "would", "should", "shall", "may", "might", "must",
        "not", "but", "all", "any", "also", "both", "each", "every", "few",
        "more", "most", "much", "many", "some", "such", "than", "then",
        "there", "here", "after", "before", "between", "through", "during",
        "because", "just", "like", "very", "too", "only", "even", "still",
        "already", "yet", "always", "never", "often", "once", "well",
        "also", "though", "although", "else", "however", "whether",
        "upon", "without", "across", "along", "among", "around",
        "under", "over", "above", "below", "off", "down", "up",
        "them", "they", "their", "these", "those", "itself",
        "him", "her", "his", "my", "mine", "me", "we", "us",
        "am", "is", "was", "were", "be", "been", "being",
        "do", "does", "did", "done", "doing",
        "get", "got", "gets", "getting",
        "make", "makes", "made", "making",
        "use", "uses", "used", "using",
        "take", "takes", "took", "taking",
        "come", "comes", "came", "coming",
        "know", "knows", "knew", "knowing",
        "see", "sees", "saw", "seeing",
        "say", "says", "said", "saying",
        "look", "looks", "looked", "looking",
        "need", "needs", "needed", "needing",
        "help", "helps", "helped", "helping",
        "want", "wants", "wanted", "wanting",
        "keep", "keeps", "kept", "keeping",
        "set", "sets", "setting",
        "put", "puts", "putting",
        "run", "runs", "running",
        "let", "lets", "letting",
        "go", "goes", "went", "gone", "going",
        "new", "old", "high", "low", "long", "short",
        "big", "small", "large", "great", "good", "better", "best",
        "first", "last", "next", "previous", "other", "another",
        "able", "alongside", "apply", "applying", "bring", "bringing",
        "called", "doing", "ensure", "everyone", "everything",
        "hire", "hiring", "hired", "includes", "including", "included",
        "life", "looking", "maintain", "maintaining", "means",
        "provide", "provides", "providing", "really", "right",
        "something", "start", "status", "support", "supports", "supported", "supporting",
        "things", "together", "upon", "various", "within",
        "yet", "alongside",
        # ── generic JD boilerplate ──
        "job", "role", "team", "work", "working",
        "engineer", "engineers", "developer", "developers",
        "senior", "junior", "lead", "manager", "managers",
        "software", "experience", "years",
        "responsibilities", "requirements", "skills",
        "ability", "strong", "excellent",
        "preferred", "nice", "plus",
        "least", "including", "across",
        "candidates", "company", "companies",
        "culture", "deliver", "delivers", "delivered", "delivering",
        "help", "helps",
        "improve", "improves", "improved", "improving",
        "learn", "learns", "learned",
        "people", "perform", "performs", "performed",
        "processes",
        "within",
        # ── generic context terms (low ranking value) ──
        "day", "daily", "home", "join", "own", "owned", "owner",
        "call", "browse", "knowledge", "shape", "based", "city",
        "fixed", "works", "workplace", "benefits", "purpose",
        "annual", "leave", "office", "campus", "students", "staff",
        "university", "auckland", "zealand", "posted", "ago",
        # ── login/nav noise ──
        "linkedin", "login", "sign", "password",
        "privacy", "agreement", "policy", "cookie",
        "email", "phone", "show", "forgot",
        "logged", "clicking", "continue", "agree",
        "user", "updated", "professional", "world",
        # ── browser/nav noise ──
        "google", "microsoft", "apple",
        "mozilla", "chrome", "edge", "safari", "firefox",
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


