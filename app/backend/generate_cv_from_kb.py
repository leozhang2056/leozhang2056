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

# 导入增强质量验证器
try:
    from cv_quality_validator import (
        generate_quality_report as run_enhanced_validation,
        format_quality_report_markdown,
    )
    ENHANCED_VALIDATOR_AVAILABLE = True
except ImportError:
    ENHANCED_VALIDATOR_AVAILABLE = False


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
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 5, 'field': 'name'},
        {'key': 'backend',        'label_en': 'API Integration',      'label_zh': 'API 集成',        'max': 6, 'field': 'name'},
        {'key': 'devops',         'label_en': 'DevOps & CI/CD',       'label_zh': 'DevOps & CI/CD',  'max': 6, 'field': 'name'},
        {'key': 'databases',      'label_en': 'Databases',            'label_zh': '数据库',           'max': 5, 'field': 'name'},
        {'key': 'ai_ml',          'label_en': 'AI / ML',              'label_zh': 'AI / ML',         'max': 4, 'field': 'name'},
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

def _pick_concrete_jd_terms_for_summary(normed_kws: List[str], limit: int = 4) -> List[str]:
    """
    从 JD 词里挑出更像「具体技术/工具」的项，避免 Summary 变成逗号分隔的关键词墙（ATS/人工都易判为模板或 AI 腔）。
    """
    if not normed_kws:
        return []
    generic_penalty = {
        "engineering", "development", "experience", "agile", "team", "mentoring",
        "leadership", "customer", "stakeholder", "communication", "collaboration",
        "innovation", "passionate", "proactive", "world-class", "dynamic",
    }
    scored: List[tuple] = []
    for kw in normed_kws:
        t = str(kw).strip()
        if len(t) < 2:
            continue
        score = min(len(t), 24)
        tl = t.lower()
        if "/" in t or "-" in t or "." in t:
            score += 5
        if any(c.isupper() for c in t):
            score += 2
        if tl in generic_penalty:
            score -= 8
        if len(t) <= 4 and tl.isalpha() and tl not in {"api", "sql", "aws", "git", "mvc", "mvp", "sdk", "iot"}:
            score -= 3
        scored.append((score, t))
    scored.sort(key=lambda x: (-x[0], x[1].lower()))
    out: List[str] = []
    seen = set()
    for _, t in scored:
        k = t.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(t)
        if len(out) >= limit:
            break
    return out if out else normed_kws[:limit]


def _build_jd_summary_tail(concrete_terms: List[str], lang: str) -> str:
    """一句自然话融入 JD 技术词，避免罗列整表关键词。"""
    if not concrete_terms:
        return ""
    if lang == "zh":
        if len(concrete_terms) >= 3:
            a, b, c = concrete_terms[0], concrete_terms[1], concrete_terms[2]
            return f"与岗位相关的技术栈包括 {a}、{b}、{c} 等；交付上坚持可测、可评审、可上线的工程习惯。"
        return f"与岗位相关的实践包括{'、'.join(concrete_terms)}；交付上坚持可测、可评审与稳定发布。"
    if len(concrete_terms) >= 3:
        a, b, c = concrete_terms[0], concrete_terms[1], concrete_terms[2]
        return (
            f"Hands-on with {a}, {b}, and {c}. "
            f"I ship with tests, code review, and stable release discipline."
        )
    if len(concrete_terms) == 2:
        a, b = concrete_terms[0], concrete_terms[1]
        return f"Hands-on with {a} and {b}, with the same rigor on tests, review, and production stability."
    return f"Hands-on with {concrete_terms[0]}, with practical focus on tests, review, and production stability."


def _role_evidence_sentence(role_type: str, lang: str) -> str:
    """基于已确认事实补充一条可证据化成果句。"""
    if lang == "zh":
        if role_type == "android":
            return "过往项目已在高并发移动业务与多站点生产环境稳定落地，验证了复杂场景下的工程交付能力。"
        if role_type == "backend":
            return "主导并交付 5+ 站点微服务平台，长期维持 99.9% 可用性，并在制造场景实现 30%+ 效率提升。"
        return "覆盖企业级移动端与后端系统交付，含 10,000+ DAU、5+ 站点落地与 99.9% 可用性目标。"
    if role_type == "android":
        return "Proven outcomes include stable delivery in high-concurrency mobile workloads and multi-site production environments."
    if role_type == "backend":
        return "Proven outcomes include microservice delivery across 5+ production sites, 99.9% uptime targets, and 30%+ efficiency gains."
    return "Proven outcomes include enterprise delivery at 10,000+ DAU scale, 5+ production-site rollouts, and 99.9% uptime targets."


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

    def _normalize_jd_keywords(kws: Optional[List[str]]) -> List[str]:
        if not kws:
            return []
        bad = {
            "new", "full", "time", "hours", "ago", "mid", "level",
            "information", "technology", "position", "posted", "behalf",
            "partner", "company", "currently", "chrome", "firefox", "safari",
            "google", "microsoft", "apple", "mozilla", "smartrecruiters",
        }
        normed: List[str] = []
        seen = set()
        for kw in kws:
            kw_norm = str(kw or "").strip()
            if len(kw_norm) < 3:
                continue
            if kw_norm.lower() in bad:
                continue
            key = kw_norm.lower()
            if key in seen:
                continue
            seen.add(key)
            normed.append(kw_norm)
        return normed

    # 加粗关键词（角色相关的核心词）
    bold_terms: Dict[str, List[str]] = {
        'android': ['Android', 'Kotlin', 'Android SDK', 'Jetpack', 'NDK'],
        'ai':      ['AI', 'LLM', 'RAG', 'diffusion', 'computer vision'],
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

    # 去掉毕业时间/在读时间等教育时间线表达，保留岗位能力与业务亮点
    def _strip_grad_timeline(s: str) -> str:
        s = re.sub(
            r"\b(master'?s student|graduating\s+[A-Za-z]+\s+\d{4}|graduating\s+\d{4}|expected graduation[^\.,;]*|in computer and information sciences at AUT)\b",
            "",
            s,
            flags=re.IGNORECASE,
        )
        s = re.sub(r"(硕士在读|即将毕业|预计毕业|毕业于?\s*\d{4}\s*年?\d{0,2}\s*月?)", "", s)
        s = re.sub(r"(202[4-9]\s*年?\s*\d{0,2}\s*月?\s*毕业)", "", s)
        s = re.sub(r"\s{2,}", " ", s)
        s = re.sub(r"\s+,", ",", s)
        s = re.sub(r"\s+\.", ".", s)
        return s.strip(" ,.;")

    def _cleanup_broken_clauses(s: str) -> str:
        """
        清理删除片段后遗留的断裂连接词，例如:
        - "..., and, Over 10 years..." -> "..., Over 10 years..."
        - "... and." -> "..."
        """
        s = re.sub(r"\band,\s*", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\band\s+(?=[,.;])", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(and|or)\.\s*", ". ", s, flags=re.IGNORECASE)
        s = re.sub(r",\s*,", ", ", s)
        s = re.sub(r"\s{2,}", " ", s)
        s = re.sub(r"\s+,", ",", s)
        s = re.sub(r"\s+\.", ".", s)
        return s.strip(" ,.;")

    def _final_summary_sanity_fix(s: str) -> str:
        """
        末尾兜底修复，避免出现半句/断句异常：
        - 删除残留连接词片段
        - 保证输出为完整句（英文以句号结尾）
        """
        if not s:
            return s
        s = _cleanup_broken_clauses(s)

        # 常见残句模式兜底
        bad_patterns = [
            r",\s*(and|or)\s*,",
            r"\b(and|or)\s*,\s*[A-Z]",
            r"\b(and|or)\s*$",
            r"\s+\.\s*\.",
        ]
        for p in bad_patterns:
            s = re.sub(p, ", ", s, flags=re.IGNORECASE)

        s = re.sub(r"\s{2,}", " ", s).strip(" ,;")
        if lang == "en" and s and not re.search(r"[.!?]$", s):
            s = s + "."
        return s

    text = _strip_grad_timeline(text)
    text = _cleanup_broken_clauses(text)

    # 按用户偏好：Summary 明确写 AUT 毕业 + 计算机专业 + First Class Honours（不写具体毕业时间）
    if lang == "zh":
        edu_lead = "AUT（Auckland University of Technology）计算机与信息科学硕士毕业，获一等荣誉学位。"
        has_aut = ("AUT" in text or "奥克兰理工大学" in text)
        has_first_class = ("一等荣誉" in text or "First Class" in text)
        if not has_aut:
            text = f"{edu_lead} {text}"
        elif not has_first_class:
            text = f"{text} 获一等荣誉学位。"
    else:
        edu_lead = (
            "Graduated from Auckland University of Technology (AUT) "
            "with a Master's in Computer and Information Sciences and First Class Honours."
        )
        has_aut = ("Auckland University of Technology" in text or "AUT" in text)
        has_first_class = ("First Class Honours" in text or "First Class" in text)
        if not has_aut:
            text = f"{edu_lead} {text}"
        elif not has_first_class:
            text = f"{text} Awarded First Class Honours."

    # Summary 保持 5–6 行：重点放在 JD 匹配关键词，但不写成“Highlights”模块
    def _trim_summary(s: str, max_chars: int) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) <= max_chars:
            return s
        cut = s.rfind(".", 0, max_chars)
        if cut > 120:
            return s[:cut + 1]
        return s[:max_chars].rstrip(" ,;") + "…"

    # JD：少量加粗即可（过多 <strong> 像模板/AI 堆砌；关键词更应落在 Experience bullet）
    normed_kws = _normalize_jd_keywords(jd_keywords)
    if normed_kws:
        jd_bold_limit = 5
        for i, kw_norm in enumerate(normed_kws):
            if i >= jd_bold_limit:
                break
            if re.search(re.escape(kw_norm), text, flags=re.IGNORECASE):
                text = _bold_first(text, kw_norm)

        hit_count = sum(1 for kw in normed_kws if re.search(re.escape(kw), text, flags=re.IGNORECASE))
        target_hits = 5 if role_type == "android" else 4
        if hit_count < target_hits:
            concrete = _pick_concrete_jd_terms_for_summary(normed_kws, 4)
            tail = _build_jd_summary_tail(concrete, lang)
            if tail:
                text = f"{text} {tail}"

    # 增加一条可证据化成果句，提升吸引力与可信度
    evidence_sentence = _role_evidence_sentence(role_type, lang)
    if evidence_sentence and evidence_sentence not in text:
        text = f"{text} {evidence_sentence}"

    # 控制 Summary 长度（目标：5–6 行左右）
    text = _trim_summary(text, 700 if lang == "en" else 460)
    text = _final_summary_sanity_fix(text)

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
    used_bullets_norm: set[str] = set()

    def _normalize_bullet_for_dedupe(text: str) -> str:
        t = _strip_html_tags(text or "")
        t = re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
        return t

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
        # 跨项目去重：减少“同一句话在多个项目重复出现”的阅读疲劳
        deduped_bullets: List[str] = []
        for b in bullets:
            nb = _normalize_bullet_for_dedupe(b)
            if not nb:
                continue
            if nb in used_bullets_norm:
                continue
            used_bullets_norm.add(nb)
            deduped_bullets.append(b)

        # 若去重后为空，回退原 bullets 的第一条，保证每个项目至少有一个要点
        if not deduped_bullets and bullets:
            deduped_bullets = [bullets[0]]

        bullets = deduped_bullets
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
    def _emphasize_first_class(s: str) -> str:
        """在教育条目中突出一等荣誉。"""
        if not isinstance(s, str) or not s:
            return s
        s = re.sub(r"\bFirst Class Honours\b", "<strong>First Class Honours</strong>", s, flags=re.IGNORECASE)
        s = s.replace("一等荣誉学位", "<strong>一等荣誉学位</strong>")
        s = s.replace("一等荣誉", "<strong>一等荣誉</strong>")
        return s

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
        details = [_emphasize_first_class(d) for d in details]

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
      width: 44%;
      padding: 0;
      vertical-align: baseline;
      white-space: nowrap;
    }

    .eh-school {
      font-style: italic;
      color: #444;
      width: 38%;
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

    # ── 目标职位 / 公司（仅用于内部命名，不在简历顶部显示） ──
    default_titles = {
        'android':   'Senior Android Developer',
        'backend':   'Senior Backend Engineer (Java/Spring)',
        'ai':        'AI Engineer (Computer Vision / LLM)',
        'fullstack': 'Senior Full-Stack Engineer',
    }
    title_text = (target_role_title or default_titles.get(role_type, 'Software Engineer')).strip()

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


def _strip_html_tags(text: str) -> str:
    """移除 HTML 标签，返回纯文本。"""
    if not isinstance(text, str):
        return ""
    return re.sub(r"<[^>]+>", " ", text)


def _normalize_keywords(jd_keywords: Optional[List[str]]) -> List[str]:
    """规范化 JD 关键词（去重、过滤空值）。"""
    if not jd_keywords:
        return []
    out: List[str] = []
    seen = set()
    for kw in jd_keywords:
        if not kw:
            continue
        k = str(kw).strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out


def _normalize_text_for_match(text: str) -> str:
    """统一匹配文本，减少大小写/符号差异导致的误判。"""
    t = (text or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def _keyword_variant_candidates(keyword: str) -> List[str]:
    """
    生成关键词的常见变体，提升与 JD 语义一致的匹配鲁棒性。
    例如: REST APIs -> REST API, restful api
    """
    raw = (keyword or "").strip().lower()
    if not raw:
        return []
    variants = {raw}
    variants.add(raw.replace("apis", "api"))
    variants.add(raw.replace("restful", "rest"))
    variants.add(raw.replace("&", "and"))
    variants.add(raw.replace("/", " "))
    return [v for v in variants if v]


def _keyword_hits_in_text(text: str, keywords: List[str]) -> List[str]:
    """返回在文本中命中的关键词列表。"""
    if not text or not keywords:
        return []
    t = _normalize_text_for_match(text)
    hits: List[str] = []
    for kw in keywords:
        kw_hit = False
        for v in _keyword_variant_candidates(kw):
            nv = _normalize_text_for_match(v)
            if nv and nv in t:
                kw_hit = True
                break
        if kw_hit:
            hits.append(kw)
    return hits


def _build_kb_evidence_corpus(base: Path) -> str:
    """
    构建可用于“反幻觉过滤”的证据语料：
    - skills.yaml
    - projects/*/facts.yaml 的关键词/技术栈/亮点/角色关联
    """
    texts: List[str] = []
    try:
        skills_data = load_yaml(base / "kb" / "skills.yaml")
        texts.append(str(skills_data))
    except Exception:
        pass

    try:
        projects = load_projects(base / "projects")
        for p in projects:
            texts.extend([str(x) for x in p.get("keywords", []) if x])
            texts.extend([str(x) for x in p.get("related_to_roles", []) if x])
            for h in p.get("highlights", []) or []:
                if isinstance(h, str):
                    texts.append(h)
            tech_stack = p.get("tech_stack", {}) or {}
            for vals in tech_stack.values():
                if isinstance(vals, list):
                    texts.extend([str(v) for v in vals if v])
    except Exception:
        pass

    return _normalize_text_for_match(" ".join(texts))


def _filter_jd_keywords_by_kb_evidence(
    jd_keywords: Optional[List[str]],
    base: Path,
) -> tuple[List[str], List[str]]:
    """
    反幻觉过滤：仅保留在 KB 证据语料中可支撑的 JD 关键词。
    返回: (supported_keywords, filtered_out_keywords)
    """
    normalized_kws = _normalize_keywords(jd_keywords)
    if not normalized_kws:
        return [], []

    corpus = _build_kb_evidence_corpus(base)
    supported: List[str] = []
    filtered: List[str] = []
    for kw in normalized_kws:
        hit = False
        for v in _keyword_variant_candidates(kw):
            nv = _normalize_text_for_match(v)
            if nv and nv in corpus:
                hit = True
                break
        if hit:
            supported.append(kw)
        else:
            filtered.append(kw)
    return supported, filtered


def _jd_match_hits_misses_coverage(
    html_en: str,
    jd_keywords: Optional[List[str]],
) -> tuple[List[str], List[str], float]:
    """返回 (hits, misses, coverage_pct)，基于与 _keyword_hits_in_text 相同规则。"""
    normalized_kws = _normalize_keywords(jd_keywords)
    if not normalized_kws:
        return [], [], 100.0
    cv_text = _strip_html_tags(html_en)
    hits = sorted(set(_keyword_hits_in_text(cv_text, normalized_kws)))
    misses = [k for k in normalized_kws if k not in hits]
    coverage = (len(hits) / len(normalized_kws) * 100.0) if normalized_kws else 100.0
    return hits, misses, coverage


def _pretty_jd_kw_for_summary_tail(kw: str) -> str:
    """将规范化关键词转为可读片段，并保证仍能被匹配器命中（子串落在归一化文本中）。"""
    k = (kw or "").strip().lower()
    if not k:
        return ""
    known: Dict[str, str] = {
        "ui/ux": "UI/UX",
        "restful apis": "RESTful APIs",
        "jetpack compose": "Jetpack Compose",
        "android sdk": "Android SDK",
        "clean code": "clean code",
        "bug fixing": "bug fixing",
        "product squad": "product squad",
        "backend engineers": "backend engineers",
        "mobile architecture": "mobile architecture",
    }
    if k in known:
        return known[k]
    if k in ("aws", "api", "ndk", "jwt", "sql"):
        return k.upper()
    return " ".join(w.capitalize() for w in k.split())


def _inject_jd_coverage_tail_into_summary_html(html: str, missing_kws: List[str]) -> str:
    """
    在英文简历 Summary 区块末尾追加一句，显式包含仍未命中的 supported 关键词，
    用于在反幻觉前提下拉高 JD 覆盖率（默认目标 >=85%）。
    """
    if not missing_kws:
        return html
    tail_bits = [_pretty_jd_kw_for_summary_tail(m) for m in missing_kws if m]
    if not tail_bits:
        return html
    tail_plain = " Additional role alignment: " + ", ".join(tail_bits) + "."
    # Summary 内已有 HTML；追加纯文本即可（避免未转义 < 破坏结构）
    pattern = re.compile(
        r'(<div class="cv-summary">)([\s\S]*?)(</div>\s*\n\s*\n\s*<!-- Key Skills -->)',
        re.MULTILINE,
    )
    m = pattern.search(html)
    if not m:
        # 降级：仅匹配第一个 cv-summary 闭合
        pattern2 = re.compile(r'(<div class="cv-summary">)([\s\S]*?)(</div>)', re.MULTILINE)
        m2 = pattern2.search(html)
        if not m2:
            return html
        return pattern2.sub(
            lambda mm: mm.group(1) + mm.group(2) + tail_plain + mm.group(3),
            html,
            count=1,
        )
    return (
        html[: m.start()]
        + m.group(1)
        + m.group(2)
        + tail_plain
        + m.group(3)
        + html[m.end() :]
    )


def _load_cv_external_review_prompt(repo_root: Path) -> str:
    p = repo_root / "kb" / "ai_prompts" / "cv_external_review.md"
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return "(Missing file: kb/ai_prompts/cv_external_review.md)\n"


def build_cv_review_bundle_markdown(
    repo_root: Path,
    role_type: str,
    company_name: Optional[str],
    target_role_title: Optional[str],
    jd_raw: Optional[List[str]],
    supported_kws: List[str],
    filtered_kws: List[str],
    html_en: str,
    hits: List[str],
    misses: List[str],
    coverage: float,
) -> str:
    """
    供「第二个 AI」评审用的单文件 Markdown：含岗位关键词上下文、匹配度、简历全文、评审提示词与回填区。
    """
    plain = _strip_html_tags(html_en)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) > 120_000:
        plain = plain[:120_000] + "\n\n[truncated for bundle size]"

    prompt = _load_cv_external_review_prompt(repo_root)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: List[str] = [
        "# CV Review Bundle (for a second AI)",
        "",
        f"- Generated: `{now}`",
        f"- Role: `{role_type}`",
        f"- Company: `{company_name or 'n/a'}`",
        f"- Target title: `{target_role_title or 'n/a'}`",
        "",
        "## Job context (keywords)",
        "",
        f"- JD keywords (raw): `{list(jd_raw or [])}`",
        f"- JD keywords (KB-supported, used in generation): `{supported_kws}`",
        f"- JD keywords (filtered out by anti-hallucination): `{filtered_kws}`",
        "",
        "## Match metrics (KB-supported terms only)",
        "",
        f"- Coverage: **{coverage:.1f}%** ({len(hits)}/{len(supported_kws) if supported_kws else 0})",
        f"- Hits: `{', '.join(hits) if hits else 'none'}`",
        f"- Misses: `{', '.join(misses) if misses else 'none'}`",
        "",
        "## CV plain text (review this)",
        "",
        "```text",
        plain,
        "```",
        "",
        "---",
        "",
        "## Instructions for the reviewer AI (copy the prompt file below into your second AI)",
        "",
        prompt,
        "",
        "---",
        "",
        "## After review: paste the second AI response here, then regenerate the CV in Cursor/KB",
        "",
        "### Pasted reviewer output",
        "",
        "(paste here)",
        "",
        "### Edits applied in KB (checklist)",
        "",
        "- [ ] `kb/profile.yaml` — summary / identity",
        "- [ ] `kb/skills.yaml` — skills rows",
        "- [ ] `projects/*/facts.yaml` — project bullets",
        "",
        "Regenerate:",
        "`python generate.py cv --role <role> --company \"...\" --jd-keywords ...`",
        "",
    ]
    return "\n".join(lines)


def _ensure_min_jd_keyword_coverage_html(
    html: str,
    supported_kws: List[str],
    min_pct: float,
) -> str:
    """
    若 supported 关键词在正文中的覆盖率低于 min_pct，则向 Summary 注入缺失词，直至达标或无可补词。
    仅作用于已通过 KB 证据过滤的关键词，不引入幻觉词。
    """
    if min_pct <= 0 or not supported_kws:
        return html
    out = html
    for _ in range(6):
        _hits, misses, cov = _jd_match_hits_misses_coverage(out, supported_kws)
        if cov >= min_pct or not misses:
            break
        out = _inject_jd_coverage_tail_into_summary_html(out, misses)
    return out


def _print_jd_match_metrics_for_cv(
    html_en: str,
    jd_keywords: Optional[List[str]],
    min_target_pct: float = 85.0,
) -> None:
    """
    每次生成简历时输出轻量级 JD 匹配指标：
    - 匹配度（覆盖率）
    - 命中关键词
    - 未命中关键词
    """
    normalized_kws = _normalize_keywords(jd_keywords)
    if not normalized_kws:
        print("  JD MATCH → skipped (no JD keywords)")
        return

    hits, misses, coverage = _jd_match_hits_misses_coverage(html_en, jd_keywords)

    print(f"  JD MATCH → {len(hits)}/{len(normalized_kws)} ({coverage:.1f}%)")
    print(f"  JD HIT KW → {', '.join(hits) if hits else 'none'}")
    print(f"  JD MISS KW → {', '.join(misses) if misses else 'none'}")
    if min_target_pct > 0 and coverage < min_target_pct:
        print(
            f"  JD ALERT → match below target (<{min_target_pct:.0f}%); "
            "tighten JD keywords or add KB evidence for missing terms"
        )


def _highlight_keywords_in_html(html_content: str, keywords: List[str]) -> str:
    """
    在 HTML 文本节点中高亮 JD 命中关键词，避免修改标签本身。
    """
    if not html_content or not keywords:
        return html_content

    # 长词优先，避免短词先替换导致长词无法匹配
    ordered = sorted(set(keywords), key=lambda x: len(x), reverse=True)
    tags_and_text = re.split(r"(<[^>]+>)", html_content)

    def _highlight_text_segment(seg: str) -> str:
        out = seg
        for kw in ordered:
            if not kw:
                continue
            pattern = re.compile(
                rf"(?<![A-Za-z0-9])({re.escape(kw)})(?![A-Za-z0-9])",
                flags=re.IGNORECASE,
            )
            out = pattern.sub(r'<mark class="jd-hit">\1</mark>', out)
        return out

    result_parts: List[str] = []
    for part in tags_and_text:
        if part.startswith("<") and part.endswith(">"):
            result_parts.append(part)
        else:
            result_parts.append(_highlight_text_segment(part))
    return "".join(result_parts)


def _inject_jd_annotation_styles(html_content: str) -> str:
    style = """
  <style>
    mark.jd-hit {
      background: #fff3a3;
      color: #111;
      padding: 0 1px;
      border-radius: 2px;
    }
    .jd-annotation-legend {
      margin-top: 10px;
      font-size: 9.5pt;
      color: #333;
      border-top: 1px dashed #9ca3af;
      padding-top: 6px;
      line-height: 1.45;
    }
  </style>
"""
    if "</head>" in html_content:
        return html_content.replace("</head>", f"{style}\n</head>", 1)
    return html_content


def _inject_jd_annotation_legend(
    html_content: str,
    supported_kws: List[str],
    hits: List[str],
    misses: List[str],
    coverage_pct: float,
) -> str:
    legend = f"""
  <div class="jd-annotation-legend">
    <strong>JD Annotation</strong><br>
    JD match score: {coverage_pct:.1f}% ({len(hits)}/{len(supported_kws) if supported_kws else 0})<br>
    Supported keywords: {", ".join(supported_kws) if supported_kws else "none"}<br>
    Hit keywords: {", ".join(hits) if hits else "none"}<br>
    Miss keywords: {", ".join(misses) if misses else "none"}
  </div>
"""
    if "</body>" in html_content:
        return html_content.replace("</body>", f"{legend}\n</body>", 1)
    return html_content + legend


def _build_quality_report_markdown(
    role_type: str,
    jd_keywords: Optional[List[str]],
    max_projects: int,
    company_name: Optional[str],
    target_role_title: Optional[str],
) -> str:
    """
    生成质量报告（Markdown）：
    - JD 关键词覆盖率
    - 低匹配项目
    - 弱匹配 bullet
    - 重复 bullet
    - 候选替换项目建议
    """
    base = Path(__file__).parent.parent.parent
    kb_dir = base / 'kb'

    profile = load_yaml(kb_dir / 'profile.yaml')
    skills_data = load_yaml(kb_dir / 'skills.yaml')
    all_projects = load_projects(base / 'projects')
    bullets_data = _load_all_bullets(base)
    relations_data = _load_project_relations(base)

    selected_projects = _select_projects_with_relations(
        all_projects,
        role_type=role_type,
        jd_keywords=jd_keywords,
        max_projects=max_projects,
        relations_data=relations_data,
    )

    normalized_kws = _normalize_keywords(jd_keywords)

    summary_text = _strip_html_tags(
        generate_summary(profile, role_type=role_type, lang='en', jd_keywords=jd_keywords)
    )
    skills_html = generate_skills_section(
        skills_data,
        role_type=role_type,
        lang='en',
        jd_keywords=jd_keywords,
    )
    skills_text = _strip_html_tags(skills_html)

    bullet_rows: List[Dict[str, str]] = []
    selected_scores: List[Dict[str, Any]] = []
    for p in selected_projects:
        pid = _build_project_id(p)
        pname = p.get('name') or pid
        score = score_project_by_jd(p, jd_keywords or []) if normalized_kws else 0.0
        selected_scores.append({'project_id': pid, 'name': pname, 'score': score})

        bullets = generate_project_bullet_points(
            p,
            lang='en',
            role_type=role_type,
            all_bullets=bullets_data,
            jd_keywords=jd_keywords,
        )
        for b in bullets:
            bullet_rows.append({'project_id': pid, 'project_name': str(pname), 'bullet': str(b)})

    exp_text = ' '.join([r['bullet'] for r in bullet_rows])

    # Coverage by section
    summary_hits = _keyword_hits_in_text(summary_text, normalized_kws)
    skills_hits = _keyword_hits_in_text(skills_text, normalized_kws)
    exp_hits = _keyword_hits_in_text(exp_text, normalized_kws)

    all_hits = sorted(set(summary_hits + skills_hits + exp_hits))
    coverage_pct = (len(all_hits) / len(normalized_kws) * 100.0) if normalized_kws else 100.0

    # Weak bullets: no JD keyword hit
    weak_bullets: List[Dict[str, str]] = []
    if normalized_kws:
        for row in bullet_rows:
            if not _keyword_hits_in_text(row['bullet'], normalized_kws):
                weak_bullets.append(row)

    # Duplicate bullet detection (normalized text)
    seen_bullets: Dict[str, List[Dict[str, str]]] = {}
    for row in bullet_rows:
        norm = re.sub(r'[^a-z0-9]+', ' ', row['bullet'].lower()).strip()
        if not norm:
            continue
        seen_bullets.setdefault(norm, []).append(row)
    duplicate_groups = [rows for rows in seen_bullets.values() if len(rows) > 1]

    # Replacement suggestions (highest unselected JD score)
    replacement_suggestions: List[Dict[str, Any]] = []
    if normalized_kws:
        selected_ids = {_build_project_id(p) for p in selected_projects}
        unselected = [p for p in all_projects if _build_project_id(p) not in selected_ids]
        ranked_unselected = sorted(
            [
                {
                    'project_id': _build_project_id(p),
                    'name': p.get('name') or _build_project_id(p),
                    'score': score_project_by_jd(p, normalized_kws),
                }
                for p in unselected
            ],
            key=lambda x: x['score'],
            reverse=True,
        )
        replacement_suggestions = [x for x in ranked_unselected if x['score'] > 0][:3]

    selected_scores_sorted = sorted(selected_scores, key=lambda x: x['score'])
    low_match_projects = [x for x in selected_scores_sorted if x['score'] <= 0] if normalized_kws else []

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title_text = (target_role_title or 'Software Engineer').strip()
    company_text = (company_name or 'Target Company').strip()

    lines: List[str] = []
    lines.append('# CV Quality Report')
    lines.append('')
    lines.append(f'- Generated at: `{now_str}`')
    lines.append(f'- Role: `{role_type}`')
    lines.append(f'- Target: `{title_text}` @ `{company_text}`')
    lines.append(f'- Selected projects: `{len(selected_projects)}`')
    lines.append('')

    lines.append('## Keyword Coverage')
    if normalized_kws:
        lines.append(f'- JD keywords ({len(normalized_kws)}): `{", ".join(normalized_kws)}`')
        lines.append(f'- Coverage: `{len(all_hits)}/{len(normalized_kws)} ({coverage_pct:.1f}%)`')
        lines.append(f'- Summary hits: `{", ".join(summary_hits) if summary_hits else "none"}`')
        lines.append(f'- Skills hits: `{", ".join(skills_hits) if skills_hits else "none"}`')
        lines.append(f'- Experience hits: `{", ".join(exp_hits) if exp_hits else "none"}`')
    else:
        lines.append('- No JD keywords provided; coverage check skipped.')
    lines.append('')

    lines.append('## Selected Projects (Score)')
    if normalized_kws:
        for x in sorted(selected_scores, key=lambda t: t['score'], reverse=True):
            lines.append(f"- `{x['name']}` (`{x['project_id']}`): `{x['score']:.2f}`")
    else:
        for x in selected_scores:
            lines.append(f"- `{x['name']}` (`{x['project_id']}`)")
    lines.append('')

    lines.append('## Weak Areas')
    if not normalized_kws:
        lines.append('- No JD keywords provided; weak match analysis skipped.')
    else:
        if low_match_projects:
            lines.append('- Low-match projects (JD score <= 0):')
            for x in low_match_projects:
                lines.append(f"  - `{x['name']}` (`{x['project_id']}`)")
        else:
            lines.append('- No low-match projects detected.')

        if weak_bullets:
            lines.append(f'- Weak bullets without JD keyword hit: `{len(weak_bullets)}`')
            for row in weak_bullets[:8]:
                lines.append(f"  - `{row['project_name']}`: {row['bullet']}")
            if len(weak_bullets) > 8:
                lines.append(f'  - ... and `{len(weak_bullets) - 8}` more')
        else:
            lines.append('- All bullets hit at least one JD keyword.')

        if duplicate_groups:
            lines.append(f'- Duplicate bullets detected: `{len(duplicate_groups)}` group(s)')
            for grp in duplicate_groups[:5]:
                lines.append(f"  - Duplicate text appears `{len(grp)}` times:")
                lines.append(f"    - {grp[0]['bullet']}")
        else:
            lines.append('- No duplicate bullets detected.')
    lines.append('')

    lines.append('## Replacement Suggestions')
    if replacement_suggestions:
        for x in replacement_suggestions:
            lines.append(f"- Consider `{x['name']}` (`{x['project_id']}`), JD score `{x['score']:.2f}`")
    else:
        lines.append('- No high-confidence replacement project found.')

    return '\n'.join(lines).rstrip() + '\n'


async def generate_cv_from_kb(
    output_path: Optional[str] = None,
    role_type: str = 'fullstack',
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = 5,
    company_name: Optional[str] = None,
    target_role_title: Optional[str] = None,
    generate_zh: bool = False,
    generate_quality_report: bool = False,
    generate_jd_annotated_pdf: bool = False,
    min_jd_match_pct: float = 85.0,
    write_review_bundle: bool = True,
):
    """
    从 KB 生成简历 PDF（默认仅英文，可选中文）。

    Args:
        output_path:   英文版输出路径（可选，若提供则优先生效）
        role_type:     android | ai | backend | fullstack
        jd_keywords:   JD 关键词列表，驱动项目和技能排序
        max_projects:  最多显示几个项目（默认 5）
        company_name:  投递公司名称；若提供且未显式指定 output_path，
                       将在文件名中追加公司名，便于区分不同公司的简历。
        generate_zh:   是否生成中文简历（默认 False）
        generate_quality_report: 是否生成质量报告（默认 False）
        generate_jd_annotated_pdf: 是否额外生成 JD 标注版 PDF（默认 False）
        min_jd_match_pct: 对「KB 支持的」JD 词的目标最低覆盖率（默认 85）；<=0 关闭自动补词
        write_review_bundle: 是否写出供第二个 AI 评审的 Markdown 包（默认 True）
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
        zh_path = en_path.replace('.pdf', '_CN.pdf') if generate_zh else None
    else:
        role_tag_lower = role_type.lower()
        company_slug = _slugify_company(company_name)
        suffix = f"_{company_slug}" if company_slug else ""
        en_path = str(dated_outputs_dir / f'CV_Leo_Zhang_{today}_{role_tag_lower}{suffix}.pdf')
        zh_path = (
            str(dated_outputs_dir / f'CV_Leo_Zhang_{today}_{role_tag_lower}{suffix}_CN.pdf')
            if generate_zh else None
        )

    role_tag = role_type.upper()
    print(f"\nGenerating CV [{role_tag}] from Career KB...")
    safe_jd_keywords, filtered_jd_keywords = _filter_jd_keywords_by_kb_evidence(
        jd_keywords,
        repo_root,
    )
    if jd_keywords:
        print(f"  JD keywords(raw): {jd_keywords}")
    if safe_jd_keywords:
        print(f"  JD keywords(supported): {safe_jd_keywords}")
    if filtered_jd_keywords:
        print(f"  JD keywords(filtered anti-hallucination): {filtered_jd_keywords}")

    # 英文版
    html_en      = generate_html_from_kb(
        role_type, 'en', safe_jd_keywords, max_projects,
        company_name=company_name,
        target_role_title=target_role_title,
    )
    html_en = _ensure_min_jd_keyword_coverage_html(
        html_en,
        safe_jd_keywords,
        min_jd_match_pct,
    )
    html_en_path = en_path.replace('.pdf', '.html')
    with open(html_en_path, 'w', encoding='utf-8') as f:
        f.write(html_en)
    print(f"  EN HTML → {html_en_path}")
    await html_to_pdf(html_en, en_path)
    print(f"  EN PDF  → {en_path}  ({os.path.getsize(en_path)/1024:.1f} KB)")
    _print_jd_match_metrics_for_cv(
        html_en,
        safe_jd_keywords,
        min_target_pct=min_jd_match_pct,
    )

    rb_hits, rb_misses, rb_cov = _jd_match_hits_misses_coverage(html_en, safe_jd_keywords)
    if write_review_bundle:
        bundle_md = build_cv_review_bundle_markdown(
            repo_root=repo_root,
            role_type=role_type,
            company_name=company_name,
            target_role_title=target_role_title,
            jd_raw=jd_keywords,
            supported_kws=safe_jd_keywords,
            filtered_kws=filtered_jd_keywords,
            html_en=html_en,
            hits=rb_hits,
            misses=rb_misses,
            coverage=rb_cov,
        )
        bundle_path = str(Path(en_path).with_name(f"{Path(en_path).stem}_AI_REVIEW_BUNDLE.md"))
        with open(bundle_path, "w", encoding="utf-8") as bf:
            bf.write(bundle_md)
        print(f"  AI REVIEW BUNDLE → {bundle_path}")
    else:
        print("  AI REVIEW BUNDLE → skipped (--no-review-bundle)")

    annotated_path: Optional[str] = None
    if generate_jd_annotated_pdf and safe_jd_keywords:
        annotated_path = en_path.replace(".pdf", "_JD_Annotated.pdf")
        cv_text = _strip_html_tags(html_en)
        jd_hits = sorted(set(_keyword_hits_in_text(cv_text, safe_jd_keywords)))
        jd_misses = [k for k in safe_jd_keywords if k not in jd_hits]
        jd_coverage_pct = (len(jd_hits) / len(safe_jd_keywords) * 100.0) if safe_jd_keywords else 100.0
        html_en_annotated = _highlight_keywords_in_html(html_en, jd_hits)
        html_en_annotated = _inject_jd_annotation_styles(html_en_annotated)
        html_en_annotated = _inject_jd_annotation_legend(
            html_en_annotated,
            supported_kws=safe_jd_keywords,
            hits=jd_hits,
            misses=jd_misses,
            coverage_pct=jd_coverage_pct,
        )
        await html_to_pdf(html_en_annotated, annotated_path)
        print(f"  EN PDF (JD Annotated) → {annotated_path}  ({os.path.getsize(annotated_path)/1024:.1f} KB)")
    else:
        print("  EN PDF (JD Annotated) → skipped (use --with-jd-annotated)")
    # 清理中间产物：HTML
    try:
        os.remove(html_en_path)
    except Exception:
        pass

    # 中文版（可选）
    if generate_zh and zh_path:
        html_zh      = generate_html_from_kb(
            role_type, 'zh', safe_jd_keywords, max_projects,
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
    else:
        print("  CN PDF  → skipped")

    # 质量报告（按需生成，默认关闭以减少生成耗时）
    if generate_quality_report:
        try:
            # 基础质量报告（项目选择分析）
            quality_report = _build_quality_report_markdown(
                role_type=role_type,
                jd_keywords=safe_jd_keywords,
                max_projects=max_projects,
                company_name=company_name,
                target_role_title=target_role_title,
            )
            
            # 增强质量验证（ATS、AI腔、Bullet质量等）
            enhanced_section = ""
            if ENHANCED_VALIDATOR_AVAILABLE:
                try:
                    enhanced_report = run_enhanced_validation(
                        html_en,
                        jd_keywords=safe_jd_keywords,
                        profile_data=None,  # 可传入 profile 数据
                        projects=None,      # 可传入 projects 数据
                    )
                    enhanced_section = "\n\n---\n\n" + format_quality_report_markdown(enhanced_report)
                    
                    # 如果质量不过关，打印警告
                    if not enhanced_report.passed:
                        print(f"  [!!] Quality check: NEEDS ATTENTION (score: {enhanced_report.score:.1f})")
                    else:
                        print(f"  [OK] Quality check: PASSED (score: {enhanced_report.score:.1f})")
                except Exception as e:
                    print(f"  Warning: enhanced validation failed: {e}")
            
            report_path = str(Path(en_path).with_name(f"{Path(en_path).stem}_QUALITY.md"))
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(quality_report + enhanced_section)
            print(f"  QA RPT -> {report_path}")
        except Exception as e:
            print(f"Warning: failed to generate CV quality report: {e}")
    else:
        print("  QA RPT → skipped")

    return en_path, zh_path, annotated_path


if __name__ == '__main__':
    import asyncio
    asyncio.run(generate_cv_from_kb())
