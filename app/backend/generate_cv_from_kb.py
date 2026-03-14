#!/usr/bin/env python3
"""
从 Career KB YAML 文件生成简历 PDF
Generate CV PDF from Career KB YAML files

支持:
  - 多角色 (android / ai / backend / fullstack)
  - JD 关键词驱动的动态项目排序
  - 中英文双语输出
  - 高质量 HTML/PDF 排版
"""

import yaml
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# 导入 PDF 生成函数
from generate_cv_html_to_pdf import html_to_pdf


# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------

def load_yaml(file_path) -> Dict:
    """加载 YAML 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_projects(projects_dir) -> List[Dict]:
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

    return projects


# ---------------------------------------------------------------------------
# 项目排序 —— 静态优先级 + JD 关键词得分
# ---------------------------------------------------------------------------

# 静态基础优先级（不依赖 JD，作为 tiebreaker）
_BASE_PRIORITY: Dict[str, int] = {
    'chatclothes': 10,
    'enterprise-messaging': 20,
    'smart-factory': 30,
    'live-streaming-system': 40,
    'visual-gateway': 50,
    'device-maintenance-prediction': 60,
    'chinese-herbal-recognition': 70,
    'iot-solutions': 80,
    'exhibition-robot': 90,
    'picture-book-locker': 100,
    'forest-patrol-inspection': 110,
    'smart-power': 120,
    'boobit': 130,
    'broadcast-control': 140,
    'visit-system': 150,
    'school-attendance': 160,
    'patent-search-system': 170,
}

# 角色预设：当没有 JD 关键词时使用的固定排序
_ROLE_PROJECT_ORDER: Dict[str, List[str]] = {
    'android': [
        'enterprise-messaging', 'smart-factory', 'iot-solutions',
        'chatclothes', 'picture-book-locker', 'visual-gateway',
    ],
    'ai': [
        'chatclothes', 'device-maintenance-prediction', 'chinese-herbal-recognition',
        'exhibition-robot', 'enterprise-messaging', 'smart-factory',
    ],
    'backend': [
        'enterprise-messaging', 'smart-factory', 'live-streaming-system',
        'chatclothes', 'iot-solutions', 'visual-gateway',
    ],
    'fullstack': [
        'chatclothes', 'enterprise-messaging', 'smart-factory',
        'live-streaming-system', 'iot-solutions',
    ],
}


def score_project_by_jd(project: Dict, jd_keywords: List[str]) -> float:
    """根据 JD 关键词对单个项目打分（复用 kb_query.py 的逻辑）"""
    if not jd_keywords:
        return 0.0

    score = 0.0
    kws_lower = [k.lower() for k in jd_keywords]

    # keywords 字段命中 +1
    proj_kws = [k.lower() for k in project.get('keywords', [])]
    for kw in kws_lower:
        if kw in proj_kws:
            score += 1.0

    # related_to_roles 命中 +0.5
    roles = [r.lower() for r in project.get('related_to_roles', [])]
    for kw in kws_lower:
        if any(kw in r for r in roles):
            score += 0.5

    # tech_stack 命中 +0.8
    tech_stack = project.get('tech_stack', {})
    all_techs: List[str] = []
    for tech_list in tech_stack.values():
        if isinstance(tech_list, list):
            all_techs.extend([t.lower() for t in tech_list if isinstance(t, str)])
    for kw in kws_lower:
        if any(kw in t for t in all_techs):
            score += 0.8

    # highlights 命中 +0.3（文本相关性；highlights 项可能是 str 或 dict）
    raw_highlights = project.get('highlights', [])
    parts = []
    for h in raw_highlights:
        if isinstance(h, str):
            parts.append(h)
        elif isinstance(h, dict):
            parts.append(h.get('en') or h.get('zh') or h.get('text') or '')
    highlights_text = ' '.join(parts).lower()
    for kw in kws_lower:
        if kw in highlights_text:
            score += 0.3

    return score


def sort_projects(
    projects: List[Dict],
    role_type: str = 'fullstack',
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = 5,
) -> List[Dict]:
    """
    排序逻辑：
    1. 如果有 JD 关键词 → JD 得分为主键（降序），静态优先级为次键（升序）
    2. 如果没有 JD 关键词 → 用角色预设顺序
    返回前 max_projects 个
    """
    role_order = _ROLE_PROJECT_ORDER.get(role_type, _ROLE_PROJECT_ORDER['fullstack'])

    def get_base_priority(p: Dict) -> int:
        pid = p.get('_project_dir', '')
        # 先查角色预设
        for idx, role_pid in enumerate(role_order):
            if role_pid in pid.lower():
                return idx
        # 再查全局静态优先级
        for key, val in _BASE_PRIORITY.items():
            if key in pid.lower():
                return 200 + val
        return 9999

    if jd_keywords:
        for p in projects:
            p['_jd_score'] = score_project_by_jd(p, jd_keywords)
        sorted_projects = sorted(
            projects,
            key=lambda p: (-p.get('_jd_score', 0), get_base_priority(p))
        )
    else:
        sorted_projects = sorted(projects, key=get_base_priority)

    return sorted_projects[:max_projects]


# ---------------------------------------------------------------------------
# 利用 project_relations 增强项目组合（同一时间线/叙事线）
# ---------------------------------------------------------------------------


def _load_project_relations(base: Path) -> Dict:
    """加载 kb/project_relations.yaml（不存在时返回空 dict）"""
    kb_dir = base / 'kb'
    rel_file = kb_dir / 'project_relations.yaml'
    if not rel_file.exists():
        return {}
    try:
        with open(rel_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _build_project_id(project: Dict) -> str:
    """从 facts 中提取 project_id（fallback: _project_dir）"""
    pid = project.get('project_id')
    if isinstance(pid, str) and pid:
        return pid
    dir_name = project.get('_project_dir', '')
    return str(dir_name)


def _select_projects_with_relations(
    all_projects: List[Dict],
    role_type: str,
    jd_keywords: Optional[List[str]],
    max_projects: int,
    relations_data: Dict,
) -> List[Dict]:
    """
    在 sort_projects 的基础上，利用 project_relations 中的时间线/叙事信息
    尝试补充 1–2 个与核心项目同一阶段或强关联的项目，让故事更连贯。
    """
    if not all_projects:
        return []

    # 需要排除/替换的项目（会话偏好）
    excluded_ids = {"exhibition-robot"}

    # 强制保留的“最重要项目”：无论角色/JD 如何，都必须出现（并置顶）
    pinned_ids = ["chatclothes", "smart-factory"]
    # Android 场景下优先保留地图/GIS相关项目（如 EROAD 车队/位置类业务更匹配）
    if role_type == "android":
        pinned_ids.append("forest-patrol-inspection")
    # 优先替换展会机器人为更相关项目（智慧电力/IoT）
    preferred_replacements = ["smart-power", "iot-solutions"]
    max_projects = max(max_projects, len(pinned_ids))

    ranked = sort_projects(all_projects, role_type, jd_keywords, max_projects=max_projects)
    ranked = [p for p in ranked if _build_project_id(p) not in excluded_ids]
    # 在任何情况下都保证 pinned 项目在列表内且置顶
    id_to_project: Dict[str, Dict] = {}
    for p in all_projects:
        pid = _build_project_id(p)
        if pid:
            id_to_project[pid] = p

    def _apply_pins(items: List[Dict]) -> List[Dict]:
        items_by_id = {_build_project_id(p): p for p in items}
        pinned: List[Dict] = []
        for pid in pinned_ids:
            p = items_by_id.get(pid) or id_to_project.get(pid)
            if p:
                pinned.append(p)
        replacements: List[Dict] = []
        for pid in preferred_replacements:
            p = items_by_id.get(pid) or id_to_project.get(pid)
            if p:
                replacements.append(p)
        # 去重并保持原顺序（先 pinned，再 items）
        seen: set[str] = set()
        out: List[Dict] = []
        for p in pinned + replacements + items:
            pid = _build_project_id(p)
            if not pid or pid in seen or pid in excluded_ids:
                continue
            seen.add(pid)
            out.append(p)
            if len(out) >= max_projects:
                break
        return out

    if len(ranked) >= max_projects:
        return _apply_pins(ranked)[:max_projects]

    # 先取若干“核心项目”
    core_count = min(3, max_projects, len(ranked))
    core = ranked[:core_count]

    selected_ids = {_build_project_id(p) for p in core}

    # 从 timeline_groups 补充同一阶段项目
    extra_candidates: List[str] = []
    tl_groups = (relations_data or {}).get('timeline_groups', {})
    if isinstance(tl_groups, dict):
        # 反向索引：项目 → 所在 timeline_groups key
        project_to_groups: Dict[str, List[str]] = {}
        for gkey, gval in tl_groups.items():
            for pid in gval.get('projects', []) or []:
                project_to_groups.setdefault(pid, []).append(gkey)

        for p in core:
            pid = _build_project_id(p)
            for gkey in project_to_groups.get(pid, []):
                group = tl_groups.get(gkey, {})
                for other_pid in group.get('projects', []) or []:
                    if other_pid and other_pid not in selected_ids:
                        extra_candidates.append(other_pid)

    # 从 relations 边补充 one-hop 关联项目
    relations_list = (relations_data or {}).get('relations', []) or []
    for rel in relations_list:
        pf = rel.get('from')
        pt = rel.get('to')
        if not pf or not pt:
            continue
        if pf in selected_ids and pt not in selected_ids:
            extra_candidates.append(pt)
        elif pt in selected_ids and pf not in selected_ids:
            extra_candidates.append(pf)

    # 按原 ranked 顺序过滤 extra，避免完全打乱优先级
    ordered_extra: List[Dict] = []
    seen_extra: set[str] = set()
    extra_set = set(extra_candidates)
    for p in ranked[core_count:]:
        pid = _build_project_id(p)
        if pid in extra_set and pid not in selected_ids and pid not in seen_extra:
            ordered_extra.append(p)
            seen_extra.add(pid)
        if len(core) + len(ordered_extra) >= max_projects:
            break

    combined = core + ordered_extra
    # 若仍不足，再从 ranked 剩余部分中填满
    if len(combined) < max_projects:
        for p in ranked[core_count:]:
            if p in combined:
                continue
            combined.append(p)
            if len(combined) >= max_projects:
                break

    return _apply_pins(combined)[:max_projects]


# ---------------------------------------------------------------------------
# 技能展示 —— 从 skills.yaml 动态读取，根据角色调整顺序
# ---------------------------------------------------------------------------

# 各角色的技能分组顺序和展示配置
_ROLE_SKILL_CONFIG: Dict[str, List[Dict]] = {
    'android': [
        {'key': 'android',        'label_en': 'Android',             'label_zh': 'Android',        'max': 7, 'field': 'name'},
        {'key': 'programming_languages', 'label_en': 'Languages',    'label_zh': '编程语言',         'max': 5, 'field': 'name'},
        {'key': 'backend',        'label_en': 'Backend Integration',  'label_zh': '后端集成',         'max': 6, 'field': 'name'},
        {'key': 'devops',         'label_en': 'DevOps & CI/CD',       'label_zh': 'DevOps & CI/CD',  'max': 6, 'field': 'name'},
        {'key': 'databases',      'label_en': 'Databases',            'label_zh': '数据库',           'max': 5, 'field': 'name'},
        {'key': 'ai_ml',          'label_en': 'AI / ML',              'label_zh': 'AI / ML',         'max': 4, 'field': 'name'},
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 5, 'field': 'name'},
    ],
    'ai': [
        {'key': 'ai_ml',          'label_en': 'AI / ML',              'label_zh': 'AI / ML',         'max': 8, 'field': 'name'},
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 5, 'field': 'name'},
        {'key': 'programming_languages', 'label_en': 'Languages',     'label_zh': '编程语言',         'max': 5, 'field': 'name'},
        {'key': 'backend',        'label_en': 'Backend & APIs',       'label_zh': '后端 & API',      'max': 5, 'field': 'name'},
        {'key': 'devops',         'label_en': 'DevOps & Cloud',       'label_zh': 'DevOps & 云',     'max': 5, 'field': 'name'},
        {'key': 'iot_hardware',   'label_en': 'IoT',                  'label_zh': 'IoT',             'max': 4, 'field': 'name'},
    ],
    'backend': [
        {'key': 'backend',        'label_en': 'Backend Engineering',  'label_zh': '后端开发',         'max': 8, 'field': 'name'},
        {'key': 'programming_languages', 'label_en': 'Languages',     'label_zh': '编程语言',         'max': 5, 'field': 'name'},
        {'key': 'databases',      'label_en': 'Databases',            'label_zh': '数据库',           'max': 6, 'field': 'name'},
        {'key': 'devops',         'label_en': 'DevOps & Cloud',       'label_zh': 'DevOps & 云',     'max': 6, 'field': 'name'},
        {'key': 'android',        'label_en': 'Mobile / Android',     'label_zh': '移动端 / Android', 'max': 4, 'field': 'name'},
        {'key': 'ai_ml',          'label_en': 'AI / ML',              'label_zh': 'AI / ML',         'max': 4, 'field': 'name'},
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 5, 'field': 'name'},
    ],
    'fullstack': [
        {'key': 'programming_languages', 'label_en': 'Languages',     'label_zh': '编程语言',         'max': 6, 'field': 'name'},
        {'key': 'ai_ml',          'label_en': 'AI / ML',              'label_zh': 'AI / ML',         'max': 6, 'field': 'name'},
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 5, 'field': 'name'},
        {'key': 'backend',        'label_en': 'Full-Stack',           'label_zh': '全栈开发',         'max': 6, 'field': 'name'},
        {'key': 'devops',         'label_en': 'DevOps & Cloud',       'label_zh': 'DevOps & 云',     'max': 6, 'field': 'name'},
        {'key': 'databases',      'label_en': 'Databases',            'label_zh': '数据库',           'max': 5, 'field': 'name'},
        {'key': 'iot_hardware',   'label_en': 'IoT / Hardware',       'label_zh': 'IoT / 硬件',      'max': 4, 'field': 'name'},
    ],
}


def _extract_skill_names(category_data, max_count: int) -> List[str]:
    """从 skills.yaml 分类数据中提取技能名称"""
    if isinstance(category_data, list):
        names = []
        for item in category_data:
            if isinstance(item, dict):
                names.append(item.get('name', ''))
            elif isinstance(item, str):
                names.append(item)
        return [n for n in names if n][:max_count]
    elif isinstance(category_data, dict):
        # 扁平化嵌套 dict（如旧格式的 devops: {containerization: [...], ...}）
        names = []
        for v in category_data.values():
            if isinstance(v, list):
                names.extend([str(x) for x in v if x])
        return names[:max_count]
    return []


def _remove_edge_terms(text: str) -> str:
    """移除不希望出现的 edge/边缘相关表述。"""
    if not isinstance(text, str) or not text:
        return text

    cleaned = text
    patterns = [
        r"<strong>\s*edge\s*</strong>",
        r"<strong>\s*边缘\s*</strong>",
        r"\bedge\s*ai\b",
        r"\bedge[-\s]?deployment\b",
        r"\bedge computing\b",
        r"\bedge/latency constraints\b",
        r"cloud/edge deployment",
        r"边缘部署",
        r"边缘计算",
        r"端侧部署",
        r"端侧",
        r"边缘",
    ]
    for p in patterns:
        cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE)

    # 修复删除关键词后遗留的断裂短语
    # 保留语义完整：cloud/edge deployment -> cloud deployment
    cleaned = re.sub(r"cloud/\s*", "cloud ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\band cloud\s*$", "and cloud deployment", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\band cloud([,.;])", r"and cloud deployment\1", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r",?\s*and\s*\.", ".", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"/\s*$", "", cleaned)

    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+,", ",", cleaned)
    cleaned = re.sub(r"\s+\.", ".", cleaned)
    cleaned = re.sub(r"\(\s*\)", "", cleaned)
    cleaned = re.sub(r"[,;/]\s*[,;/]", ", ", cleaned)
    # 如果最终结尾没有句号，补一个句号，避免“被截断感”
    if cleaned and re.search(r"[A-Za-z0-9\u4e00-\u9fff]$", cleaned):
        cleaned = cleaned + "."
    return cleaned.strip(" ,;")


def generate_skills_section(
    skills_data: Dict,
    role_type: str = 'fullstack',
    lang: str = 'en',
    jd_keywords: Optional[List[str]] = None,
) -> str:
    """
    从 skills.yaml 动态生成技能展示 HTML。
    按角色配置调整分组顺序；如有 JD 关键词，命中的技能会排前面。
    """
    config = _ROLE_SKILL_CONFIG.get(role_type, _ROLE_SKILL_CONFIG['fullstack'])
    lines: List[str] = []

    for cfg in config:
        key = cfg['key']
        label = cfg['label_en'] if lang == 'en' else cfg['label_zh']
        raw = skills_data.get(key)
        if not raw:
            continue

        names = _extract_skill_names(raw, cfg['max'])
        if not names:
            continue

        # JD 命中的技能排前面
        if jd_keywords:
            kws_lower = [k.lower() for k in jd_keywords]
            hit = [n for n in names if any(k in n.lower() for k in kws_lower)]
            miss = [n for n in names if n not in hit]
            names = hit + miss

        names = names[:cfg['max']]
        lines.append(f'<strong>{label}:</strong> {", ".join(names)}')

    return '<br>\n        '.join(lines)


# ---------------------------------------------------------------------------
# Summary —— 完全从 KB 读取，不硬编码
# ---------------------------------------------------------------------------

def generate_summary(
    profile: Dict,
    role_type: str = 'fullstack',
    lang: str = 'en',
    jd_keywords: Optional[List[str]] = None,
) -> str:
    """
    从 profile.yaml 的 summary_variants 读取，不硬编码任何文本。
    如果对应 variant 不存在，降级到 default。
    """
    career = profile.get('career_identity', {})
    variants_key = 'summary_variants_zh' if lang == 'zh' else 'summary_variants'
    summaries = career.get(variants_key) or career.get('summary_variants', {})

    role_map = {
        'android': 'android_focus',
        'ai':      'ai_focus',
        'backend': 'java_focus',
        'fullstack': 'default',
    }
    variant_key = role_map.get(role_type, 'default')
    text = summaries.get(variant_key) or summaries.get('default', '')

    # 将 YAML 多行字符串里的换行+空白压缩成单空格
    text = re.sub(r'\s+', ' ', text).strip()

    if not text:
        return ''

    def _bold_first(s: str, term: str) -> str:
        """
        加粗首次出现的 term（尽量避免重复加粗导致的嵌套 <strong>）。
        """
        if not term:
            return s
        # 若已经存在 <strong>term</strong>（忽略大小写），则不再替换
        already = re.search(rf"<strong>\s*{re.escape(term)}\s*</strong>", s, flags=re.IGNORECASE)
        if already:
            return s
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        return pattern.sub(lambda m: f"<strong>{m.group()}</strong>", s, count=1)

    # 加粗关键词（角色相关的核心词）
    bold_terms: Dict[str, List[str]] = {
        'android': ['Android', 'Kotlin', 'Android SDK', 'Jetpack', 'NDK'],
        'ai':      ['AI', 'LLM', 'RAG', 'diffusion', 'computer vision', 'edge'],
        'backend': ['Spring Boot', 'Java', 'microservice', 'REST', 'API'],
        'fullstack': ['full-stack', 'Android', 'Spring Boot', 'AI'],
    }
    for term in bold_terms.get(role_type, []):
        text = _bold_first(text, term)

    # 开发岗弱化团队管理措辞（Summary 中尤其明显）
    def _strip_management_phrases(s: str) -> str:
        # 英文常见管理表达
        s = re.sub(r"\bteam leadership\b", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\bmanaging cross-functional teams?\b", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\bled cross-functional teams?\b", "", s, flags=re.IGNORECASE)
        # 中文常见管理表达
        s = s.replace("团队管理", "")
        s = s.replace("带团队", "")
        s = s.replace("管理跨职能团队", "")
        # 清理多余空白/标点
        s = re.sub(r"\s+,", ",", s)
        s = re.sub(r"\s{2,}", " ", s)
        s = re.sub(r"\s+\.", ".", s)
        return s.strip(" ,.;")

    text = _strip_management_phrases(text)

    # Summary 保持 4–5 行：重点放在 JD 匹配关键词，但不写成“Highlights”模块
    def _trim_summary(s: str, max_chars: int) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) <= max_chars:
            return s
        cut = s.rfind(".", 0, max_chars)
        if cut > 120:
            return s[:cut + 1]
        return s[:max_chars].rstrip(" ,;") + "…"

    # 若有 JD 关键词，将首次出现的位置加粗（避免重复强调）
    if jd_keywords:
        for kw in jd_keywords:
            if not kw:
                continue
            # 过滤明显无意义的词（避免把“New/Full/time/ago”等加粗）
            kw_norm = str(kw).strip()
            if len(kw_norm) < 3:
                continue
            if kw_norm.lower() in {
                "new", "full", "time", "hours", "ago", "mid", "level",
                "information", "technology", "position", "posted", "behalf",
                "partner", "company", "currently",
                "edge", "chrome", "firefox", "safari",
                "google", "microsoft", "apple", "mozilla", "smartrecruiters"
            }:
                continue
            if re.search(re.escape(kw_norm), text, flags=re.IGNORECASE):
                text = _bold_first(text, kw_norm)

    # 控制 Summary 长度（目标：4–5 行左右）
    text = _trim_summary(text, 560 if lang == "en" else 380)

    return _remove_edge_terms(text)


# ---------------------------------------------------------------------------
# Experience —— 项目 bullet points
# ---------------------------------------------------------------------------

def _load_all_bullets(base: Path) -> List[Dict]:
    """
    加载 kb/bullets/*.yaml 中的所有要点。

    注意：这里只做最小加载，不复用 kb_query.KBQuery，避免不必要耦合。
    """
    kb_dir = base / 'kb'
    bullets_dir = kb_dir / 'bullets'
    results: List[Dict] = []

    if not bullets_dir.exists():
        return results

    for bullet_file in bullets_dir.glob('*.yaml'):
        try:
            with open(bullet_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            for b in data.get('bullets', []):
                if isinstance(b, dict):
                    results.append(b)
        except Exception:
            # 出错时静默跳过单个文件，不影响整体生成
            continue
    return results


def _score_bullet_for_project(
    bullet: Dict,
    project: Dict,
    role_type: str,
    jd_keywords: Optional[List[str]] = None,
) -> float:
    """根据项目 / 角色 / JD 关键词给单条 bullet 打分"""
    score = 0.0

    pid = (project.get('project_id')
           or project.get('_project_dir', '')).lower()
    evidence = [str(e).lower() for e in bullet.get('evidence', [])]
    if pid and pid in evidence:
        score += 2.0

    # 项目 tags：来自 keywords + tech_stack + related_to_roles
    proj_tags: List[str] = []
    proj_tags.extend([str(k).lower() for k in project.get('keywords', [])])

    tech_stack = project.get('tech_stack', {})
    for v in tech_stack.values():
        if isinstance(v, list):
            proj_tags.extend(str(x).lower() for x in v)

    proj_tags.extend(str(r).lower() for r in project.get('related_to_roles', []))

    bullet_tags = [str(t).lower() for t in bullet.get('tags', [])]
    for t in bullet_tags:
        if t in proj_tags:
            score += 1.0

    # 角色相关加一点权重（android/backend/ai/fullstack）
    role_kw = role_type.lower()
    if role_kw in bullet_tags:
        score += 0.8

    # JD 关键词命中
    if jd_keywords:
        kws_lower = [k.lower() for k in jd_keywords]
        variants_text = ' '.join(bullet.get('variants', [])).lower()
        for kw in kws_lower:
            if kw in variants_text or kw in bullet_tags:
                score += 0.5

    return score


def _select_bullets_for_project(
    project: Dict,
    all_bullets: List[Dict],
    role_type: str,
    jd_keywords: Optional[List[str]],
    max_bullets: int,
) -> List[str]:
    """
    从 bullets 库中为单个项目挑选合适的 bullet 变体（英文）。

    规则：
    - 优先使用 evidence 中直接指向该 project_id 的条目；
    - 再按 tags 与项目/角色/JD 关键词的命中得分排序；
    - 对每个 bullet 选择 1 个最合适的 variant。
    """
    if not all_bullets:
        return []

    scored: List[Dict] = []
    for b in all_bullets:
        s = _score_bullet_for_project(b, project, role_type, jd_keywords)
        if s > 0:
            scored.append({'bullet': b, 'score': s})

    if not scored:
        return []

    scored.sort(key=lambda x: x['score'], reverse=True)

    result: List[str] = []
    kws_lower = [k.lower() for k in (jd_keywords or [])]

    for item in scored:
        if len(result) >= max_bullets:
            break
        b = item['bullet']
        variants = b.get('variants') or []
        if not isinstance(variants, list) or not variants:
            original = b.get('original')
            if isinstance(original, str):
                result.append(original)
            continue

        # 如果有 JD 关键词，优先选择包含关键词的变体
        chosen = None
        if kws_lower:
            for v in variants:
                if not isinstance(v, str):
                    continue
                v_lower = v.lower()
                if any(kw in v_lower for kw in kws_lower):
                    chosen = v
                    break

        if not chosen:
            chosen = variants[0]

        if isinstance(chosen, str):
            result.append(chosen)

    return result[:max_bullets]


def generate_project_bullet_points(
    project: Dict,
    max_bullets: int = 4,
    lang: str = 'en',
    role_type: str = 'fullstack',
    all_bullets: Optional[List[Dict]] = None,
    jd_keywords: Optional[List[str]] = None,
) -> List[str]:
    """
    从项目 facts 生成 bullet points。

    - 英文：优先使用 kb/bullets/*.yaml 中匹配当前项目/角色/JD 的变体；
      不足或无匹配时回退到 facts.yaml.highlights / impact / achievements。
    - 中文：暂时只使用 facts.yaml 内的中文/英文 highlights，不使用英文 bullets 库。
    """

    def _is_management_bullet(text: str) -> bool:
        """
        开发岗简历弱化“团队管理/带团队”表述：
        - 过滤明显的管理/带人措辞
        - 保留“跨团队协作/评审/敏捷”等工程协作表达
        """
        if not text:
            return False
        t = text.strip().lower()

        # English management/people-leading signals
        en_bad = (
            "led and mentored",
            "led a team",
            "managed a team",
            "mentored",
            "people management",
            "hiring",
            "direct reports",
            "team leadership",
            "line management",
        )
        # Chinese management/people-leading signals
        zh_bad = (
            "带领",
            "带队",
            "管理团队",
            "团队管理",
            "人员管理",
            "培养",
            "导师",
            "招聘",
            "直线汇报",
        )

        # Allowlist for engineering collaboration (should not be removed)
        allow = ("code review", "reviews", "agile", "scrum", "collaborat", "cross-team", "跨团队", "代码评审", "敏捷")

        if any(a in t for a in allow):
            return False
        return any(p in t for p in en_bad) or any(p in text for p in zh_bad)

    # 中文版本暂不混用英文 bullets 库
    if lang == 'zh':
        highlights = project.get('highlights_cn') or project.get('highlights', [])
        bullets = [
            h for h in highlights
            if isinstance(h, str) and h.strip() and not _is_management_bullet(h)
        ]
        bullets = [_remove_edge_terms(b) for b in bullets]
        bullets = [b for b in bullets if b]
        if bullets:
            return bullets[:max_bullets]

        impact = [
            i for i in project.get('impact', [])
            if isinstance(i, str) and not _is_management_bullet(i)
        ]
        impact = [_remove_edge_terms(b) for b in impact]
        impact = [b for b in impact if b]
        if impact:
            return impact[:max_bullets]

        processed = []
        for item in project.get('achievements', []):
            if isinstance(item, str):
                if not _is_management_bullet(item):
                    cleaned_item = _remove_edge_terms(item)
                    if cleaned_item:
                        processed.append(cleaned_item)
            elif isinstance(item, dict):
                desc = item.get('description', '')
                if desc:
                    if not _is_management_bullet(desc):
                        cleaned_desc = _remove_edge_terms(desc)
                        if cleaned_desc:
                            processed.append(cleaned_desc)
        if processed:
            return processed[:max_bullets]

        return ['主导项目从需求到上线的完整交付。']

    # 英文：先尝试 bullets 库
    bullets_from_lib: List[str] = []
    if all_bullets is not None:
        bullets_from_lib = _select_bullets_for_project(
            project,
            all_bullets,
            role_type=role_type,
            jd_keywords=jd_keywords,
            max_bullets=max_bullets,
        )

    # 如果从 bullets 库已经拿到了足够的条目，直接返回
    if len(bullets_from_lib) >= max_bullets:
        cleaned = [
            _remove_edge_terms(b)
            for b in bullets_from_lib
            if not _is_management_bullet(b)
        ]
        cleaned = [b for b in cleaned if b]
        return cleaned[:max_bullets]

    remaining = max_bullets - len(bullets_from_lib)

    # 然后使用 facts.yaml 的 highlights / impact / achievements 作为补充
    highlights = project.get('highlights', [])
    fact_bullets = [
        h for h in highlights
        if isinstance(h, str) and h.strip() and not _is_management_bullet(h)
    ]
    fact_bullets = [_remove_edge_terms(b) for b in fact_bullets]
    fact_bullets = [b for b in fact_bullets if b]
    if not fact_bullets:
        impact = [
            i for i in project.get('impact', [])
            if isinstance(i, str) and not _is_management_bullet(i)
        ]
        impact = [_remove_edge_terms(b) for b in impact]
        impact = [b for b in impact if b]
        if impact:
            fact_bullets = impact
        else:
            processed = []
            for item in project.get('achievements', []):
                if isinstance(item, str):
                    if not _is_management_bullet(item):
                        cleaned_item = _remove_edge_terms(item)
                        if cleaned_item:
                            processed.append(cleaned_item)
                elif isinstance(item, dict):
                    desc = item.get('description', '')
                    if desc:
                        if not _is_management_bullet(desc):
                            cleaned_desc = _remove_edge_terms(desc)
                            if cleaned_desc:
                                processed.append(cleaned_desc)
            fact_bullets = processed

    combined: List[str] = []
    combined.extend(
        [
            _remove_edge_terms(b)
            for b in bullets_from_lib
            if not _is_management_bullet(b)
        ]
    )
    combined = [b for b in combined if b]
    for b in fact_bullets:
        if len(combined) >= max_bullets:
            break
        # 简单去重
        cleaned_b = _remove_edge_terms(b)
        if cleaned_b and cleaned_b not in combined:
            combined.append(cleaned_b)

    if not combined:
        combined = ['Developed and delivered full solution independently.']

    return combined[:max_bullets]


def _fmt_date_range(project: Dict) -> str:
    """格式化项目时间段，只显示年份"""
    timeline = project.get('timeline', {})
    if isinstance(timeline, dict):
        start = str(timeline.get('start', ''))
        end   = str(timeline.get('end', ''))
    else:
        start = str(project.get('start_date', ''))
        end   = str(project.get('end_date', ''))

    start_yr = start[:4] if start and start != 'None' else ''
    end_yr   = end[:4]   if end   and end   != 'None' else ''

    if start_yr and end_yr and start_yr != end_yr:
        return f'{start_yr} – {end_yr}'
    return start_yr or end_yr or ''


def generate_experience_section(
    projects: List[Dict],
    lang: str = 'en',
    role_type: str = 'fullstack',
    all_bullets: Optional[List[Dict]] = None,
    jd_keywords: Optional[List[str]] = None,
) -> str:
    """将已排序的项目列表渲染为 HTML"""
    html_parts = []

    for project in projects:
        # 项目名称
        if lang == 'zh':
            name = (project.get('name_cn')
                    or project.get('name')
                    or project.get('project_id', ''))
        else:
            name = project.get('name') or project.get('project_id', '')

        # 公司 / 机构
        company_info = project.get('company', {})
        institution  = project.get('institution', {})
        if isinstance(institution, dict) and institution.get('name'):
            company = institution['name']
        elif isinstance(company_info, dict) and company_info.get('name'):
            company = company_info['name']
        else:
            company = ('Chunxiao Technology Co., Ltd.'
                       if lang == 'en' else '春晓科技有限公司')

        date_range = _fmt_date_range(project)

        # 角色
        if lang == 'zh':
            role = project.get('role_cn') or project.get('role', '')
        else:
            role = project.get('role', '')
        if not role:
            role = 'Developer' if lang == 'en' else '开发工程师'

        # 一句话描述（summary 第一句，最多 160 字符）
        if lang == 'zh':
            overview_raw = (project.get('overview_cn')
                            or project.get('summary_cn')
                            or project.get('summary', ''))
        else:
            overview_raw = project.get('overview') or project.get('summary', '')
        if isinstance(overview_raw, str):
            overview = overview_raw.strip().split('\n')[0][:160]
        else:
            overview = ''
        overview = _remove_edge_terms(overview)

        # Bullet points
        bullets = generate_project_bullet_points(
            project,
            lang=lang,
            role_type=role_type,
            all_bullets=all_bullets,
            jd_keywords=jd_keywords,
        )
        bullets_html = '\n            '.join(f'<li>{b}</li>' for b in bullets)

        html_parts.append(f'''
    <div class="job">
      <table class="job-header-table">
        <tr>
          <td class="jh-title">{name}</td>
          <td class="jh-company">{company}</td>
          <td class="jh-date">{date_range}</td>
        </tr>
      </table>
      <div class="job-role"><strong>{role}</strong>{" — " + overview if overview else ""}</div>
      <ul class="job-list">
        {bullets_html}
      </ul>
    </div>''')

    return '\n'.join(html_parts)


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------

def generate_education_section(profile: Dict, lang: str = 'en') -> str:
    """从 profile.yaml 生成教育经历"""
    education = profile.get('education', [])
    parts = []

    def _short_institution(name: str) -> str:
        """压缩过长院校名，减少意外换行。"""
        if not name:
            return name
        n = name.strip()
        # AUT 空间足够，保留全称
        if 'Auckland University of Technology' in n:
            return n
        if 'Hebei University of Science and Technology' in n:
            return 'Hebei Univ. of Sci. & Tech.'
        # 通用压缩
        n = n.replace('University', 'Univ.')
        n = n.replace('Technology', 'Tech.')
        n = n.replace('Science', 'Sci.')
        n = n.replace(' and ', ' & ')
        return n

    for edu in education:
        if lang == 'zh':
            degree      = edu.get('degree_cn') or edu.get('degree', '')
            institution = edu.get('institution_cn') or edu.get('institution', '')
            location    = edu.get('location_cn') or edu.get('location', '')
            research    = edu.get('research_focus_cn') or edu.get('research_focus', [])
            honors      = edu.get('honors_cn') or edu.get('honors', [])
            highlights  = edu.get('highlights_cn') or edu.get('highlights', [])
        else:
            degree      = edu.get('degree', '')
            institution = edu.get('institution', '')
            location    = edu.get('location', '')
            research    = edu.get('research_focus', [])
            honors      = edu.get('honors', [])
            highlights  = edu.get('highlights', [])

        start = (edu.get('start_date') or '')[:4]
        end   = (edu.get('end_date')   or '')[:4]
        date_range = f'{start} – {end}' if start and end else start or end

        details = []
        if research:
            lbl = 'Research focus' if lang == 'en' else '研究方向'
            details.append(f'{lbl}: {", ".join(research)}')
        if honors:
            lbl = 'Honors' if lang == 'en' else '荣誉'
            details.append(f'{lbl}: {", ".join(honors)}')
        if highlights:
            details.append('. '.join(highlights))

        # 学校短名（减少换行）
        inst_short = _short_institution(institution)

        parts.append(f'''
    <div class="edu-item">
      <table class="edu-header-table">
        <tr>
          <td class="eh-degree">{degree}</td>
          <td class="eh-school">{inst_short}, {location}</td>
          <td class="eh-date">{date_range}</td>
        </tr>
      </table>
      <div class="edu-detail">{" · ".join(details)}</div>
    </div>''')

    return '\n'.join(parts)


# ---------------------------------------------------------------------------
# Licenses & Certifications + Publications
# ---------------------------------------------------------------------------

def generate_licenses_section(achievements: Dict, lang: str = 'en') -> str:
    """从 achievements.yaml 生成证书、奖项条目"""
    certifications = achievements.get('certifications', [])
    awards         = achievements.get('awards', [])
    lines = []

    for cert in certifications:
        name      = cert.get('name', '')
        authority = cert.get('authority', '')
        year      = cert.get('year', '')
        lines.append(
            f'<li><div class="lc-row">'
            f'<span><strong>{name}</strong> — {authority}</span>'
            f'<span class="lc-date">{year}</span>'
            f'</div></li>'
        )

    for award in awards[:2]:
        name      = award.get('name', '')
        category  = award.get('category', '')
        authority = award.get('authority', '')
        year      = award.get('year', '')
        display   = f'{name} ({category})' if category else name
        lines.append(
            f'<li><div class="lc-row">'
            f'<span><strong>{display}</strong> — {authority}</span>'
            f'<span class="lc-date">{year}</span>'
            f'</div></li>'
        )

    return '\n'.join(lines)


def generate_publications_section(achievements: Dict, lang: str = 'en') -> str:
    """从 achievements.yaml 生成发表记录（如有）"""
    pubs = achievements.get('publications', [])
    if not pubs:
        return ''

    lines = []
    for pub in pubs:
        title  = pub.get('title', '')
        venue  = pub.get('venue', '')
        year   = pub.get('year', '')
        ptype  = pub.get('type', '')
        doi    = pub.get('doi', '')
        url    = pub.get('url', '')
        status = pub.get('status', '')
        note   = pub.get('note', '')

        # 链接
        link = doi or url
        title_html = (f'<a href="https://doi.org/{doi}" style="color:#1a3a6a;">{title}</a>'
                      if doi else
                      (f'<a href="{url}" style="color:#1a3a6a;">{title}</a>' if url else title))

        suffix_parts = []
        if status:
            suffix_parts.append(status.capitalize())
        if note:
            suffix_parts.append(note)
        suffix = f' <span style="color:#555;font-size:9.5pt;">({"; ".join(suffix_parts)})</span>' if suffix_parts else ''

        lines.append(
            f'<li><div class="lc-row">'
            f'<span><strong>{title_html}</strong>{suffix}<br>'
            f'<span style="color:#444;font-size:9.5pt;">{venue}, {year}</span></span>'
            f'<span class="lc-date"></span>'
            f'</div></li>'
        )

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS = """
    @page {
      size: A4;
      margin: 14mm 14mm 14mm 14mm;
    }

    *, *::before, *::after {
      box-sizing: border-box;
    }

    body {
      font-family: 'Segoe UI', 'Arial', sans-serif;
      font-size: 10.5pt;
      line-height: 1.38;
      color: #111;
      max-width: 210mm;
      margin: 0 auto;
      padding: 0;
      background: #fff;
    }

    a { color: #1a4a8a; text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* ── Header ─────────────────────────────────────── */
    .cv-header {
      text-align: center;
      margin-bottom: 10px;
      padding-bottom: 6px;
    }

    .cv-name {
      font-size: 22pt;
      font-weight: 700;
      color: #1a3a6a;
      letter-spacing: 0.5px;
      margin-bottom: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
    }

    .cv-name a { color: #1a3a6a; }

    .social-icon {
      width: 17px;
      height: 17px;
      vertical-align: middle;
      display: inline-block;
      flex-shrink: 0;
    }

    .cv-contact {
      font-size: 10pt;
      color: #1a4a8a;
      line-height: 1.6;
    }

    .cv-contact a { color: #1a4a8a; }

    /* ── Section title ───────────────────────────────── */
    .section-title {
      font-size: 11.5pt;
      font-weight: 700;
      color: #1a3a6a;
      margin-top: 11px;
      margin-bottom: 5px;
      border-bottom: 1.5px solid #1a3a6a;
      padding-bottom: 2px;
      letter-spacing: 0.2px;
    }

    /* ── Summary ─────────────────────────────────────── */
    .cv-summary {
      text-align: justify;
      color: #222;
      margin-bottom: 4px;
    }

    /* ── Skills ──────────────────────────────────────── */
    .cv-skills {
      margin-bottom: 4px;
      line-height: 1.55;
    }

    /* ── Experience ──────────────────────────────────── */
    .job {
      margin-bottom: 9px;
      page-break-inside: avoid;
    }

    .job-header-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 1px;
    }

    .jh-title {
      font-weight: 700;
      font-size: 10.5pt;
      width: 38%;
      padding: 0;
      vertical-align: baseline;
    }

    .jh-company {
      font-style: italic;
      color: #444;
      width: 42%;
      text-align: right;
      padding: 0;
      vertical-align: baseline;
    }

    .jh-date {
      color: #777;
      font-size: 9.8pt;
      width: 20%;
      text-align: right;
      padding: 0;
      white-space: nowrap;
      vertical-align: baseline;
    }

    .job-role {
      font-size: 10pt;
      color: #333;
      margin-bottom: 3px;
    }

    .job-list {
      margin: 0;
      padding-left: 18px;
      font-size: 10pt;
      color: #222;
    }

    .job-list li {
      margin-bottom: 2px;
      line-height: 1.4;
    }

    /* ── Education ───────────────────────────────────── */
    .edu-item {
      margin-bottom: 8px;
      page-break-inside: avoid;
    }

    .edu-header-table {
      width: 100%;
      border-collapse: collapse;
    }

    .eh-degree {
      font-weight: 700;
      width: 36%;
      padding: 0;
      vertical-align: baseline;
    }

    .eh-school {
      font-style: italic;
      color: #444;
      width: 46%;
      text-align: right;
      padding: 0;
      vertical-align: baseline;
      white-space: nowrap;
      font-size: 9.8pt;
    }

    .eh-date {
      color: #777;
      font-size: 9.8pt;
      width: 18%;
      text-align: right;
      padding: 0;
      white-space: nowrap;
      vertical-align: baseline;
    }

    .edu-detail {
      font-size: 9.8pt;
      color: #444;
      margin-top: 2px;
    }

    /* ── Licenses / Publications ─────────────────────── */
    .lc-list {
      list-style: none;
      margin: 0;
      padding: 0;
      font-size: 10pt;
    }

    .lc-list li {
      margin-bottom: 4px;
    }

    .lc-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .lc-date {
      color: #777;
      font-size: 9.5pt;
      margin-left: 8px;
      white-space: nowrap;
    }

    /* ── Print ───────────────────────────────────────── */
    @media print {
      body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    }
"""


# ---------------------------------------------------------------------------
# HTML 组装
# ---------------------------------------------------------------------------

_LINKEDIN_SVG = """<svg class="social-icon" viewBox="0 0 24 24" fill="#0077B5">
  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
</svg>"""

_GITHUB_SVG = """<svg class="social-icon" viewBox="0 0 24 24" fill="#181717">
  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
</svg>"""


def generate_html_from_kb(
    role_type: str = 'fullstack',
    lang: str = 'en',
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = 5,
    company_name: Optional[str] = None,
    target_role_title: Optional[str] = None,
) -> str:
    """从 KB 生成完整 HTML"""

    # ── 标签 ──
    labels = {
        'en': {
            'summary':  'Summary',
            'skills':   'Key Skills',
            'exp':      'Experience',
            'edu':      'Education',
            'licenses': 'Licenses & Certifications',
        },
        'zh': {
            'summary':  '个人简介',
            'skills':   '核心技能',
            'exp':      '工作经历',
            'edu':      '教育背景',
            'licenses': '证书与认证',
        },
    }
    lbl = labels.get(lang, labels['en'])

    # ── 加载数据 ──
    base = Path(__file__).parent.parent.parent   # repo root
    kb_dir = base / 'kb'
    profile         = load_yaml(kb_dir / 'profile.yaml')
    skills_data     = load_yaml(kb_dir / 'skills.yaml')
    achievements    = load_yaml(kb_dir / 'achievements.yaml')
    all_projects    = load_projects(base / 'projects')
    bullets_data    = _load_all_bullets(base)
    relations_data  = _load_project_relations(base)

    # ── 个人信息 ──
    personal = profile.get('personal_info', {})
    name     = personal.get('preferred_name') or personal.get('name', 'Leo Zhang')
    contact  = personal.get('contact', {})
    email    = contact.get('email', '')
    phone    = contact.get('phone', '')
    loc      = contact.get('location', {})
    city     = loc.get('city', '')
    country  = loc.get('country', '')

    # ── 生成各部分 ──
    summary      = generate_summary(profile, role_type, lang, jd_keywords=jd_keywords)
    skills_html  = generate_skills_section(skills_data, role_type, lang, jd_keywords)
    sorted_projs = _select_projects_with_relations(
        all_projects,
        role_type=role_type,
        jd_keywords=jd_keywords,
        max_projects=max_projects,
        relations_data=relations_data,
    )
    exp_html     = generate_experience_section(
        sorted_projs,
        lang=lang,
        role_type=role_type,
        all_bullets=bullets_data,
        jd_keywords=jd_keywords,
    )
    edu_html     = generate_education_section(profile, lang)
    lic_html     = generate_licenses_section(achievements, lang)
    # Publications：按需求不在简历中展示
    pub_section = ''

    # ── 目标职位 / 公司（显示在简历顶部） ──
    default_titles = {
        'android':   'Senior Android Developer',
        'backend':   'Senior Backend Engineer (Java/Spring)',
        'ai':        'AI Engineer (Computer Vision / LLM)',
        'fullstack': 'Senior Full-Stack Engineer',
    }
    title_text = (target_role_title or default_titles.get(role_type, 'Software Engineer')).strip()
    company_text = (company_name or 'Target Company').strip()
    target_line = f'{title_text} · {company_text}' if company_text else title_text

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>{name} — {title_text} — CV</title>
  <style>{_CSS}</style>
</head>
<body>

  <!-- Header -->
  <div class="cv-header">
    <div class="cv-name">
      <a href="https://www.linkedin.com/in/leo-zhang-305626280/">{name}</a>
      <a href="https://www.linkedin.com/in/leo-zhang-305626280/">{_LINKEDIN_SVG}</a>
      <a href="https://github.com/leozhang2056">{_GITHUB_SVG}</a>
    </div>
    <div style="margin-top:4px;font-size:11.5pt;color:#1a3a6a;font-weight:600;">
      {target_line}
    </div>
    <div class="cv-contact">
      <a href="mailto:{email}">&#9993;&nbsp;{email}</a>
      &nbsp;|&nbsp; &#9990;&nbsp;{phone}
      &nbsp;|&nbsp; &#9679;&nbsp;{city}, {country}
    </div>
  </div>

  <!-- Summary -->
  <div class="section-title">{lbl['summary']}</div>
  <div class="cv-summary">{summary}</div>

  <!-- Key Skills -->
  <div class="section-title">{lbl['skills']}</div>
  <div class="cv-skills">{skills_html}</div>

  <!-- Experience -->
  <div class="section-title">{lbl['exp']}</div>
  {exp_html}

  <!-- Education -->
  <div class="section-title">{lbl['edu']}</div>
  {edu_html}
  {pub_section}

  <!-- Licenses & Certifications -->
  <div class="section-title">{lbl['licenses']}</div>
  <ul class="lc-list">
{lic_html}
  </ul>

</body>
</html>'''

    return html


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def _slugify_company(company_name: Optional[str]) -> str:
    """
    将公司名转换为安全的文件名片段，例如:
    'Jobgether' -> 'Jobgether', 'Datacom Ltd.' -> 'Datacom-Ltd'
    """
    if not company_name:
        return ""
    # 保留字母数字，其他转为横杠，压缩连续横杠
    import re as _re
    slug = ''.join(ch if ch.isalnum() else '-' for ch in company_name.strip())
    slug = _re.sub(r'-{2,}', '-', slug).strip('-')
    return slug


async def generate_cv_from_kb(
    output_path: Optional[str] = None,
    role_type: str = 'fullstack',
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = 5,
    company_name: Optional[str] = None,
    target_role_title: Optional[str] = None,
):
    """
    从 KB 生成中英文两份简历 PDF。

    Args:
        output_path:   英文版输出路径（可选，若提供则优先生效）
        role_type:     android | ai | backend | fullstack
        jd_keywords:   JD 关键词列表，驱动项目和技能排序
        max_projects:  最多显示几个项目（默认 5）
        company_name:  投递公司名称；若提供且未显式指定 output_path，
                       将在文件名中追加公司名，便于区分不同公司的简历。
    """
    # 经验/项目不要太少：至少 5 个（且 ChatClothes/智能工厂会额外固定置顶）
    max_projects = max(int(max_projects or 0), 5)

    today = datetime.now().strftime('%Y%m%d')
    today_dir = datetime.now().strftime('%Y-%m-%d')
    repo_root = Path(__file__).parent.parent.parent
    outputs_dir = repo_root / 'outputs'
    outputs_dir.mkdir(exist_ok=True)
    dated_outputs_dir = outputs_dir / today_dir
    dated_outputs_dir.mkdir(exist_ok=True)

    if output_path:
        en_path = str(output_path)
        zh_path = en_path.replace('.pdf', '_CN.pdf')
    else:
        role_tag_lower = role_type.lower()
        company_slug = _slugify_company(company_name)
        suffix = f"_{company_slug}" if company_slug else ""
        en_path = str(dated_outputs_dir / f'CV_Leo_Zhang_{today}_{role_tag_lower}{suffix}.pdf')
        zh_path = str(dated_outputs_dir / f'CV_Leo_Zhang_{today}_{role_tag_lower}{suffix}_CN.pdf')

    role_tag = role_type.upper()
    print(f"\nGenerating CV [{role_tag}] from Career KB...")
    if jd_keywords:
        print(f"  JD keywords: {jd_keywords}")

    # 英文版
    html_en      = generate_html_from_kb(
        role_type, 'en', jd_keywords, max_projects,
        company_name=company_name,
        target_role_title=target_role_title,
    )
    html_en_path = en_path.replace('.pdf', '.html')
    with open(html_en_path, 'w', encoding='utf-8') as f:
        f.write(html_en)
    print(f"  EN HTML → {html_en_path}")
    await html_to_pdf(html_en, en_path)
    print(f"  EN PDF  → {en_path}  ({os.path.getsize(en_path)/1024:.1f} KB)")
    # 清理中间产物：HTML
    try:
        os.remove(html_en_path)
    except Exception:
        pass

    # 中文版
    html_zh      = generate_html_from_kb(
        role_type, 'zh', jd_keywords, max_projects,
        company_name=company_name,
        target_role_title=target_role_title,
    )
    html_zh_path = zh_path.replace('.pdf', '.html')
    with open(html_zh_path, 'w', encoding='utf-8') as f:
        f.write(html_zh)
    print(f"  CN HTML → {html_zh_path}")
    await html_to_pdf(html_zh, zh_path)
    print(f"  CN PDF  → {zh_path}  ({os.path.getsize(zh_path)/1024:.1f} KB)")
    # 清理中间产物：HTML
    try:
        os.remove(html_zh_path)
    except Exception:
        pass

    return en_path, zh_path


if __name__ == '__main__':
    import asyncio
    asyncio.run(generate_cv_from_kb())
