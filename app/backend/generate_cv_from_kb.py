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
import html
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import logging

# 设置日志
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 底层 IO 函数 —— 从 kb_io 导入（避免 kb_loader → generate_cv_from_kb 的循环依赖）
# ---------------------------------------------------------------------------
try:
    from kb_io import (  # type: ignore
        load_yaml,
        load_projects,
        load_all_bullets,
        load_project_relations,
    )
except ModuleNotFoundError:
    from app.backend.kb_io import (  # type: ignore
        load_yaml,
        load_projects,
        load_all_bullets,
        load_project_relations,
    )

# 保留私有名称供内部使用（历史调用方 / 测试不需要改动）
_load_all_bullets = load_all_bullets
_load_project_relations = load_project_relations

# 导入 PDF 生成函数（支持 `python generate.py` 将 app/backend 加入 path，或包导入 `app.backend.*`）
try:
    from generate_cv_html_to_pdf import html_to_pdf
except ModuleNotFoundError:
    from app.backend.generate_cv_html_to_pdf import html_to_pdf

try:
    from project_ranking import score_project_by_jd, sort_projects
except ModuleNotFoundError:
    from app.backend.project_ranking import score_project_by_jd, sort_projects

# 导入增强质量验证器
try:
    from cv_quality_validator import (
        generate_quality_report as run_enhanced_validation,
        format_quality_report_markdown,
    )
    ENHANCED_VALIDATOR_AVAILABLE = True
except ImportError:
    try:
        from app.backend.cv_quality_validator import (
            generate_quality_report as run_enhanced_validation,
            format_quality_report_markdown,
        )
        ENHANCED_VALIDATOR_AVAILABLE = True
    except ImportError:
        ENHANCED_VALIDATOR_AVAILABLE = False

try:
    from cv_post_generation_check import (
        build_post_check_markdown,
        print_post_check_summary,
        run_post_generation_check,
    )
    POST_CHECK_AVAILABLE = True
except ImportError:
    try:
        from app.backend.cv_post_generation_check import (
            build_post_check_markdown,
            print_post_check_summary,
            run_post_generation_check,
        )
        POST_CHECK_AVAILABLE = True
    except ImportError:
        POST_CHECK_AVAILABLE = False


# ============================================================================
# 常量定义
# ============================================================================

# 项目选择常量（控制篇幅：A4 约不超过两页）
DEFAULT_MAX_PROJECTS = 6
CV_MAX_PROJECTS_CAP = 7
CORE_PROJECT_COUNT = 3
DEFAULT_MAX_BULLETS = 3

# 文本长度限制
SUMMARY_MAX_CHARS_EN = 700
SUMMARY_MAX_CHARS_ZH = 460
# 项目副标题（summary 首行）：硬截断会产生 PDF 文本层的半词（如 voltag. / subs.）
OVERVIEW_MAX_CHARS = 245
SUMMARY_TRUNCATE_POINT = 120
SUMMARY_SAFE_TAIL_PHRASES_EN = (
    "based in Auckland, New Zealand.",
    "Full-time work rights in New Zealand.",
)

# 字符串处理常量
MAX_TERM_LENGTH = 24
MIN_TERM_LENGTH = 3

# JD匹配常量
MIN_JD_MATCH_PCT = 85.0
BUNDLE_SIZE_LIMIT = 120_000


# Use functions from text_utils module
from text_utils import (
    strip_parenthetical_notes as _strip_parenthetical_notes,
    join_items_within_budget as _join_comma_items_within_char_budget,
    compact_tech_stack as _compact_tech_stack_one_line,
    strip_html_tags,
    normalize_text_for_match,
    keyword_variant_candidates,
)


def _compact_tech_stack_one_line(
    tech_stack: Dict[str, Any],
    *,
    max_items: int = 8,
    max_chars: int = 140,
) -> str:
    """将 facts 中 tech_stack 压成一行短文本；条目去括号说明，长度按整词边界截断。"""
    if not isinstance(tech_stack, dict) or not tech_stack:
        return ""
    seen: set[str] = set()
    ordered: List[str] = []
    for _cat, techs in tech_stack.items():
        if not isinstance(techs, list):
            continue
        for t in techs:
            if not isinstance(t, str):
                continue
            x = _strip_parenthetical_notes(t)
            if not x:
                continue
            key = x.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(x)
            if len(ordered) >= max_items:
                break
        if len(ordered) >= max_items:
            break
    return _join_comma_items_within_char_budget(ordered, max_chars)


# ============================================================================
# 数据加载
# ============================================================================
# load_yaml / load_projects / _load_project_relations / _load_all_bullets
# 已迁移到 app/backend/kb_io.py，在模块顶部通过 kb_io 导入并绑定别名。
# 此处保留注释，便于代码搜索时定位。

# 排序和 JD 打分逻辑已抽离到 project_ranking.py，
# 本文件继续通过同名函数调用保持兼容。


# ---------------------------------------------------------------------------
# 利用 project_relations 增强项目组合（同一时间线/叙事线）
# ---------------------------------------------------------------------------
# _load_project_relations 已迁移到 kb_io.py，顶部通过别名绑定保持向后兼容。


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

    excluded_ids / pinned_ids / preferred_replacements 均从
    generation_config.yaml 的 project_selection 块读取，不硬编码。
    """
    if not all_projects:
        return []

    try:
        from generation_config import load_generation_config  # type: ignore
    except ModuleNotFoundError:
        from app.backend.generation_config import load_generation_config  # type: ignore

    _sel_cfg = load_generation_config().get("project_selection", {})
    excluded_ids: set = set(_sel_cfg.get("excluded_ids", []))
    _pinned_map: Dict = _sel_cfg.get("pinned_ids", {})
    pinned_ids: List[str] = _pinned_map.get(role_type, _pinned_map.get("default", []))
    preferred_replacements: List[str] = _sel_cfg.get("preferred_replacements", [])

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
        seen: set = set()
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

    # 先取若干"核心项目"
    core_count = min(CORE_PROJECT_COUNT, max_projects, len(ranked))
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
    seen_extra: set = set()
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
        {'key': 'android_core', 'label_en': 'Core Android', 'label_zh': '核心 Android', 'max': 8, 'field': 'name'},
        {'key': 'android_system_low_level', 'label_en': 'System & Low-level', 'label_zh': '系统与底层', 'max': 8, 'field': 'name'},
        {'key': 'android_testing', 'label_en': 'Testing', 'label_zh': '测试', 'max': 5, 'field': 'name'},
        {'key': 'mobile_platform_tools', 'label_en': 'Mobile & Release', 'label_zh': '移动端与发布', 'max': 5, 'field': 'name'},
        {'key': 'methodology_practices', 'label_en': 'Practices',    'label_zh': '工程实践',         'max': 3, 'field': 'name'},
        {'key': 'programming_languages', 'label_en': 'Languages',    'label_zh': '编程语言',         'max': 5, 'field': 'name'},
        {'key': 'frontend',       'label_en': 'Cross-platform / Web', 'label_zh': '跨平台 / Web',     'max': 3, 'field': 'name'},
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 5, 'field': 'name'},
        {'key': 'backend',        'label_en': 'API Integration',      'label_zh': 'API 集成',        'max': 6, 'field': 'name'},
        {'key': 'devops',         'label_en': 'DevOps & CI/CD',       'label_zh': 'DevOps & CI/CD',  'max': 7, 'field': 'name'},
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
        {'key': 'programming_languages', 'label_en': 'Languages',     'label_zh': '编程语言',         'max': 5, 'field': 'name'},
        {'key': 'frontend',       'label_en': 'Frontend',             'label_zh': '前端',             'max': 3, 'field': 'name'},
        {'key': 'backend',        'label_en': 'Backend & APIs',       'label_zh': '后端与 API',       'max': 5, 'field': 'name'},
        {'key': 'devops',         'label_en': 'Cloud & DevOps',       'label_zh': '云与 DevOps',      'max': 6, 'field': 'name'},
        {'key': 'methodology_practices', 'label_en': 'Quality & Practices', 'label_zh': '质量与工程实践', 'max': 3, 'field': 'name'},
        {'key': 'ai_ml',          'label_en': 'AI / ML',              'label_zh': 'AI / ML',         'max': 3, 'field': 'name'},
        {'key': 'ai_coding_tools','label_en': 'AI-Assisted Development', 'label_zh': 'AI 辅助开发',   'max': 3, 'field': 'name'},
        {'key': 'iot_hardware',   'label_en': 'IoT / Hardware',       'label_zh': 'IoT / 硬件',      'max': 3, 'field': 'name'},
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
    # 只匹配「, and.」这类断裂从句，勿用 ,? 否则 "Zealand." 中的 and. 会被误替换成句号
    cleaned = re.sub(r",\s*and\s*\.", ".", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"/\s*$", "", cleaned)

    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+,", ",", cleaned)
    cleaned = re.sub(r"\s+\.", ".", cleaned)
    cleaned = re.sub(r"\(\s*\)", "", cleaned)
    cleaned = re.sub(r"[,;/]\s*[,;/]", ", ", cleaned)
    # 如果最终结尾没有句号，补一个句号，避免“被截断感”
    if cleaned and re.search(r"[A-Za-z0-9\u4e00-\u9fff\)]$", cleaned):
        cleaned = cleaned + "."
    return cleaned.strip(" ,;")


def _ensure_summary_tail_phrase(text: str, lang: str, role_type: str) -> str:
    """确保英文 Android Summary 不因行宽折叠而丢失关键尾句。"""
    if not isinstance(text, str) or not text.strip():
        return text
    if lang != "en" or role_type != "android":
        return text
    lowered = text.lower()
    for phrase in SUMMARY_SAFE_TAIL_PHRASES_EN:
        if phrase.lower() in lowered:
            return text
    # 仅在未包含这些尾句时补最短且稳定的一句，避免出现 "New Zeal." 这类截断观感。
    base = text.rstrip()
    if base and not base.endswith(('.', '!', '?')):
        base += "."
    return f"{base} Based in Auckland, New Zealand."


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
    kws_lower = [k.lower() for k in (jd_keywords or [])]

    def _prioritize_by_jd(names: List[str]) -> List[str]:
        if not jd_keywords:
            return names
        hit = [n for n in names if any(k in n.lower() for k in kws_lower)]
        miss = [n for n in names if n not in hit]
        return hit + miss

    # fullstack：中度合并技能行；保持密度同时避免单行过长换行导致版面空洞
    if role_type == 'fullstack':
        merged_rows = [
            ('core', 'Core', '核心', ['programming_languages', 'backend'], 8),
            ('frontend', 'Frontend', '前端', ['frontend'], 4),
            ('delivery', 'DevOps & Delivery', 'DevOps 与交付', ['devops', 'methodology_practices'], 8),
            ('ai_tools', 'AI / Tooling', 'AI / 工具链', ['ai_ml', 'ai_coding_tools'], 6),
            ('iot', 'IoT / Hardware', 'IoT / 硬件', ['iot_hardware'], 3),
        ]
        for _, label_en, label_zh, keys, max_count in merged_rows:
            merged_names: List[str] = []
            seen = set()
            for key in keys:
                extract_cap = max_count * 2 if key == 'devops' else max_count
                raw = skills_data.get(key)
                if not raw:
                    continue
                names = _extract_skill_names(raw, extract_cap)
                if role_type == 'fullstack' and key == 'devops':
                    names = [
                        n for n in names
                        if n not in {'IIS', 'Windows Server', 'Linux System Administration'}
                        and 'administration' not in n.lower()
                    ]
                for n in names:
                    k = n.lower().strip()
                    if k and k not in seen:
                        seen.add(k)
                        merged_names.append(n)
            merged_names = _prioritize_by_jd(merged_names)[:max_count]
            if not merged_names:
                continue
            label = label_en if lang == 'en' else label_zh
            lines.append(f'<strong>{label}:</strong> {", ".join(merged_names)}')
        return '<br>\n        '.join(lines)

    for cfg in config:
        key = cfg['key']
        # Android targeted CVs: hide explicit testing row unless JD asks for testing.
        if (
            role_type == 'android'
            and key == 'android_testing'
            and kws_lower
            and not any(t in " ".join(kws_lower) for t in ['test', 'testing', 'junit', 'mockk', 'espresso'])
        ):
            continue
        label = cfg['label_en'] if lang == 'en' else cfg['label_zh']
        raw = skills_data.get(key)
        if not raw:
            continue

        extract_cap = cfg['max']
        if role_type == 'fullstack' and key == 'devops':
            extract_cap = cfg['max'] * 2
        names = _extract_skill_names(raw, extract_cap)
        if not names:
            continue

        # fullstack：省略过于基础/人人会写的项，避免 DevOps 行过长换行
        if role_type == 'fullstack' and key == 'devops':
            names = [
                n for n in names
                if n not in {'IIS', 'Windows Server', 'Linux System Administration'}
                and 'administration' not in n.lower()
            ]
            if not names:
                continue

        # JD 命中的技能排前面
        names = _prioritize_by_jd(names)

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
        if len(t) < MIN_TERM_LENGTH:
            continue
        score = min(len(t), MAX_TERM_LENGTH)
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
    """补充一条证据导向成果句（固定表达，避免随机模板腔）。"""
    variants_zh = {
        "android": "在移动端交付中持续关注稳定性与可维护性，具备复杂现场问题排查与上线保障经验。",
        "backend": "在后端交付中强调可观测性、性能与稳定发布，能够支撑长期生产负载。",
        "ai": "在 AI 项目中兼顾模型效果与工程落地，能够将原型推进到可运行流程。",
        "fullstack": "具备跨前后端协同交付能力，关注可测试性、发布节奏与线上稳定性。",
    }

    variants_en = {
        "android": "Delivery focus includes runtime stability, maintainable architecture, and production debugging under field constraints.",
        "backend": "Delivery focus includes observability, performance tuning, and stable release practices for long-lived services.",
        "ai": "Delivery focus balances model quality with production readiness, from prototype to runnable pipelines.",
        "fullstack": "Delivery focus spans frontend-backend integration, testability, and reliable production rollout.",
    }

    variants = variants_zh if lang == "zh" else variants_en
    return variants.get(role_type) or variants.get("fullstack", "")


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
            # Job posting artifacts
            "new", "full", "time", "hours", "ago", "mid", "level",
            "information", "technology", "position", "posted", "behalf",
            "partner", "company", "currently", "chrome", "firefox", "safari",
            "google", "microsoft", "apple", "mozilla", "smartrecruiters",
            "linkedin", "indeed", "glassdoor", "monster", "dice", "ziprecruiter",
            
            # Generic job terms
            "senior", "junior", "experienced", "skills", "team", "project",
            "development", "engineer", "developer", "required", "preferred",
            "responsibilities", "qualifications", "requirements", "benefits",
            "opportunities", "career", "growth", "environment", "culture",
            
            # Verb phrases
            "develop", "design", "implement", "maintain", "support", "work",
            "collaborate", "communicate", "lead", "manage", "create", "build",
            
            # Common fillers
            "including", "such", "other", "various", "multiple", "different",
            "strong", "excellent", "good", "solid", "proven", "demonstrated",
            "ability", "knowledge", "experience", "familiarity", "understanding",
            
            # Time/location
            "remote", "office", "hybrid", "onsite", "location", "salary", "range",
            "competitive", "benefits", "package", "equity", "bonus", "vacation",
            
            # Single letters/numbers
            "a", "an", "the", "and", "or", "but", "if", "then", "when", "where",
            "how", "why", "what", "who", "which", "this", "that", "these", "those",
        }
        normed: List[str] = []
        seen = set()
        for kw in kws:
            kw_norm = str(kw or "").strip()
            if len(kw_norm) < MIN_TERM_LENGTH:
                continue
            kw_lower = kw_norm.lower()
            if kw_lower in bad:
                continue
            
            # Boost technical terms: those with special chars, mixed case, or known tech abbreviations
            is_technical = (
                any(char in kw_norm for char in ['/', '-', '.', '&']) or
                any(c.isupper() for c in kw_norm) or
                kw_lower in {"api", "sql", "aws", "git", "mvn", "jdk", "sdk", "jwt", "xml", "json", "http", "rest", "tcp", "udp", "html", "css", "js", "ui", "ux", "ai", "ml", "dl", "nlp", "cv", "llm", "rag", "orm", "ioc", "aop", "tdd", "bdd", "ci", "cd", "agile", "scrum", "kanban", "docker", "kubernetes", "k8s", "jenkins", "github", "gitlab", "bitbucket", "jira", "confluence", "slack", "zoom", "teams", "excel", "word", "powerpoint", "outlook"}
            )
            
            # Filter out very short generic words unless technical
            if len(kw_norm) <= 3 and not is_technical and kw_lower not in {"ios", "mac", "web", "app", "dev", "ops", "dba"}:
                continue
            
            key = kw_lower
            if key in seen:
                continue
            seen.add(key)
            normed.append(kw_norm)
        return normed

    # 加粗关键词（角色相关的核心词）
    bold_terms: Dict[str, List[str]] = {
        'android': ['Android', 'Kotlin', 'Jetpack Compose', 'Coroutines', 'NDK'],
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
        s = s.strip()
        return re.sub(r"[,;\s]+$", "", s)

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
        s = s.strip()
        return re.sub(r"[,;\s]+$", "", s)

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
        s = s.strip()
        return re.sub(r"[,;\s]+$", "", s)

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
    # 添加变体避免重复
    edu_variants_zh = [
        "AUT（Auckland University of Technology）计算机与信息科学硕士毕业，获一等荣誉学位。",
        "毕业于AUT（奥克兰理工大学），主修计算机与信息科学，获得一等荣誉学位。",
        "在奥克兰理工大学完成计算机与信息科学硕士学位，取得一等荣誉。",
    ]
    edu_variants_en = [
        "Graduated from Auckland University of Technology (AUT) with a Master's in Computer and Information Sciences and First Class Honours.",
        "Earned a Master's degree in Computer and Information Sciences from AUT with First Class Honours.",
        "Completed Master's studies at Auckland University of Technology, achieving First Class Honours in Computer and Information Sciences.",
    ]
    
    if lang == "zh":
        edu_lead = random.choice(edu_variants_zh)
        has_aut = ("AUT" in text or "奥克兰理工大学" in text)
        has_first_class = ("一等荣誉" in text or "First Class" in text)
        if not has_aut:
            text = f"{edu_lead} {text}"
        elif not has_first_class:
            text = f"{text} 获一等荣誉学位。"
    else:
        edu_lead = random.choice(edu_variants_en)
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
        cut = _last_sentence_period_index(s, max_chars + 1)
        if cut > SUMMARY_TRUNCATE_POINT:
            return s[: cut + 1]
        # 预算内找不到完整句号时，不做硬截断，避免出现半句/半词。
        return s

    # JD：少量加粗即可（过多 <strong> 像模板/AI 堆砌；关键词更应落在 Experience bullet）
    normed_kws = _normalize_jd_keywords(jd_keywords)
    if normed_kws:
        jd_bold_limit = 2 if role_type == "android" else 5
        for i, kw_norm in enumerate(normed_kws):
            if i >= jd_bold_limit:
                break
            if re.search(re.escape(kw_norm), text, flags=re.IGNORECASE):
                text = _bold_first(text, kw_norm)

    # 固定成果句（非随机），提升稳定性并降低模板腔；
    # 对 fullstack / android 省略，避免与 profile 总结重复堆叠。
    if role_type not in {"android", "fullstack"}:
        evidence_sentence = _role_evidence_sentence(role_type, lang)
        if evidence_sentence and evidence_sentence not in text:
            text = f"{text} {evidence_sentence}"

    # 控制 Summary 长度（目标：5–6 行左右）；Android 英文略放宽，减少句号截断吃掉末尾地点句
    _sum_budget = SUMMARY_MAX_CHARS_ZH if lang == "zh" else SUMMARY_MAX_CHARS_EN
    if lang == "en" and role_type == "android":
        _sum_budget = min(900, _sum_budget + 140)
    text = _trim_summary(text, _sum_budget)
    text = _ensure_summary_tail_phrase(text, lang, role_type)
    text = _final_summary_sanity_fix(text)

    return _remove_edge_terms(text)


# ---------------------------------------------------------------------------
# Experience —— 项目 bullet points
# ---------------------------------------------------------------------------

def _load_all_bullets(base: Path) -> List[Dict[str, Any]]:
    """
    加载 kb/bullets/*.yaml 中的所有要点，支持错误处理。
    """
    kb_dir = base / 'kb'
    bullets_dir = kb_dir / 'bullets'
    results: List[Dict[str, Any]] = []

    if not bullets_dir.exists():
        logger.warning("Bullets directory not found")
        return results

    if not bullets_dir.is_dir():
        logger.error("Bullets path is not a directory")
        return results

    for bullet_file in bullets_dir.glob('*.yaml'):
        try:
            with open(bullet_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data is None:
                    logger.warning(f"Empty bullets file: {bullet_file.name}")
                    continue

            bullets_list = data.get('bullets', [])
            if not isinstance(bullets_list, list):
                logger.warning(f"Invalid bullets structure in {bullet_file.name}")
                continue

            for b in bullets_list:
                if isinstance(b, dict):
                    results.append(b)
                else:
                    logger.warning(f"Invalid bullet entry in {bullet_file.name}: {type(b)}")

            logger.debug(f"Loaded {len(bullets_list)} bullets from {bullet_file.name}")

        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {bullet_file.name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading {bullet_file.name}: {e}")

    logger.info(f"Loaded {len(results)} total bullet entries")
    return results


_BULLET_LEADING_VERB_RE = re.compile(r"^\s*(?:[•\-\*]\s*)?([A-Za-z]+)")


def _bullet_leading_verb(text: str) -> str:
    """取 bullet 英文首词（常为动词），用于同一项目下避免 Built/Developed 连打。"""
    m = _BULLET_LEADING_VERB_RE.match(text or "")
    return m.group(1).lower() if m else ""


def _score_bullet_variant_quality(text: str, jd_keywords: Optional[List[str]] = None) -> float:
    """Prefer bullet variants that read like strong, evidence-backed resume lines."""
    if not isinstance(text, str):
        return 0.0

    raw = text.strip()
    if not raw:
        return 0.0

    score = 0.0
    text_lower = raw.lower()
    first_word = _bullet_leading_verb(raw)

    strong_verbs = {
        "built", "developed", "implemented", "designed", "architected", "optimized",
        "delivered", "shipped", "integrated", "engineered", "launched", "automated",
        "reduced", "improved", "deployed", "created",
    }
    weak_verbs = {"helped", "assisted", "supported", "worked", "participated"}

    if first_word in strong_verbs:
        score += 1.0
    elif first_word in weak_verbs:
        score -= 0.4
    elif first_word:
        score += 0.2

    if any(char.isdigit() for char in raw) or "%" in raw:
        score += 0.8

    tech_patterns = [
        r"\b(Java|Kotlin|Python|Spring|Android|Compose|Redis|Docker|Kubernetes|MySQL|PostgreSQL|MongoDB|AWS|Azure|GCP|REST|API|SDK|NDK|JNI|GIS|MQTT|WebSocket)\b",
        r"\b(microservice|pipeline|offline|telemetry|latency|uptime|cache|queue|encryption|deployment|monitoring)\b",
    ]
    if any(re.search(p, raw, re.IGNORECASE) for p in tech_patterns):
        score += 0.6

    scope_patterns = [
        r"\b(users?|customers?|sites?|factories?|devices?|services?|modules?|apps?|projects?)\b",
        r"\b(production|enterprise|field|regional|national|global|cross-team)\b",
    ]
    if any(re.search(p, raw, re.IGNORECASE) for p in scope_patterns):
        score += 0.35

    word_count = len(raw.split())
    if 11 <= word_count <= 28:
        score += 0.5
    elif word_count < 8:
        score -= 0.5
    elif word_count > 34:
        score -= 0.35

    if jd_keywords:
        kws_lower = [k.lower() for k in jd_keywords if isinstance(k, str) and k.strip()]
        hit_count = sum(1 for kw in kws_lower if kw in text_lower)
        score += min(hit_count * 0.25, 0.75)

    return score


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

    # 量化指标加分（包含数字或百分比的bullet更可信）
    bullet_text = ' '.join(bullet.get('variants', [])).lower()
    if any(char.isdigit() for char in bullet_text) or '%' in bullet_text or 'qps' in bullet_text.lower():
        score += 0.3

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

    pid = (
        str(project.get("project_id") or project.get("_project_dir") or "")
        .strip()
        .lower()
    )
    scored: List[Dict] = []
    for b in all_bullets:
        ev_raw = b.get("evidence") or []
        ev_list = [str(e).strip().lower() for e in ev_raw if e]
        # 要点库若声明了 evidence，则只允许落在对应 project_id 上，避免 NDK 消息类要点误配到 GIS 等项目
        if ev_list and pid and pid not in ev_list:
            continue
        s = _score_bullet_for_project(b, project, role_type, jd_keywords)
        if s > 0:
            scored.append({'bullet': b, 'score': s})

    if not scored:
        return []

    scored.sort(key=lambda x: x['score'], reverse=True)

    result: List[str] = []
    used_leading_verbs: set[str] = set()

    for item in scored:
        if len(result) >= max_bullets:
            break
        b = item['bullet']
        variants = b.get('variants') or []
        if not isinstance(variants, list) or not variants:
            original = b.get('original')
            if isinstance(original, str):
                ov = _bullet_leading_verb(original)
                if ov:
                    used_leading_verbs.add(ov)
                result.append(original)
            continue

        # 变体选择同时看质量与 JD 贴合度，不只按关键词命中数排序。
        chosen = None
        scored_variants: List[tuple[float, int, str]] = []
        for v in variants:
            if not isinstance(v, str):
                continue
            vb = _bullet_leading_verb(v)
            verb_freshness = 1 if vb and vb not in used_leading_verbs else 0
            quality_score = _score_bullet_variant_quality(v, jd_keywords)
            scored_variants.append((quality_score, verb_freshness, v))

        if scored_variants:
            scored_variants.sort(key=lambda x: (x[0], x[1]), reverse=True)
            chosen = scored_variants[0][2]

        if isinstance(chosen, str):
            cvb = _bullet_leading_verb(chosen)
            if cvb:
                used_leading_verbs.add(cvb)
            result.append(chosen)

    return result[:max_bullets]


def generate_project_bullet_points(
    project: Dict,
    max_bullets: int = DEFAULT_MAX_BULLETS,
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

    def _diversify_bullet_openers_en(items: List[str]) -> List[str]:
        """弱化英文 bullet 的重复起手词（如连续 Built/Developed）。"""
        if not items:
            return items

        starter_pool = {
            "built": ["Engineered", "Delivered", "Shipped", "Produced"],
            "developed": ["Implemented", "Engineered", "Crafted", "Produced"],
            "implemented": ["Delivered", "Engineered", "Introduced", "Executed"],
            "designed": ["Architected", "Defined", "Planned", "Framed"],
            "architected": ["Structured", "Shaped", "Defined", "Framed"],
            "integrated": ["Wired", "Linked", "Merged", "Connected"],
            "created": ["Established", "Introduced", "Produced", "Added"],
            "optimized": ["Tuned", "Refined", "Tightened", "Streamlined"],
            "delivered": ["Shipped", "Released", "Rolled out", "Provided"],
            "owned": ["Ran", "Stewarded", "Drove", "Operated"],
            "applied": ["Used", "Leveraged", "Employed", "Deployed"],
            "deployed": ["Released", "Shipped", "Rolled out", "Published"],
            "combined": ["Merged", "Blended", "Paired", "Unified"],
        }

        used_starters: Dict[str, int] = {}
        out: List[str] = []

        for idx, raw in enumerate(items):
            t = (raw or "").strip()
            if not t:
                continue
            m = re.match(r"^([A-Za-z]+)(\b.*)$", t)
            if not m:
                out.append(t)
                continue

            starter = m.group(1)
            rest = m.group(2)
            key = starter.lower()

            if key in starter_pool:
                seen = used_starters.get(key, 0)
                if seen > 0:
                    repls = starter_pool[key]
                    repl = repls[(seen - 1) % len(repls)]
                    t = repl + rest
                used_starters[key] = seen + 1
            else:
                used_starters[key] = used_starters.get(key, 0) + 1

            out.append(t)

        return out

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

    # 英文：先尝试 bullets 库（ChatClothes + Android：最多从库取 2 条，留 1 条给 facts 里的移动端/论文要点）
    bullets_from_lib: List[str] = []
    lib_cap = max_bullets
    if lang == "en" and role_type == "android":
        _pid = str(project.get("project_id") or project.get("_project_dir") or "").strip().lower()
        if _pid == "chatclothes":
            lib_cap = min(2, max_bullets)
    if all_bullets is not None:
        bullets_from_lib = _select_bullets_for_project(
            project,
            all_bullets,
            role_type=role_type,
            jd_keywords=jd_keywords,
            max_bullets=lib_cap,
        )

    # 如果从 bullets 库已经拿到了足够的条目，直接返回（仍做英文起手词去重）
    if len(bullets_from_lib) >= max_bullets:
        cleaned = [
            _remove_edge_terms(b)
            for b in bullets_from_lib
            if not _is_management_bullet(b)
        ]
        cleaned = [b for b in cleaned if b][:max_bullets]
        if lang == "en":
            cleaned = _diversify_bullet_openers_en(cleaned)
        return cleaned

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

    def _split_compound_bullet(text: str) -> List[str]:
        """将误拼接为一条的“ - ”链式 bullet 拆分回多条。"""
        if not isinstance(text, str):
            return []
        t = text.strip()
        if not t:
            return []
        # 仅在明显是链式拼接时拆分，避免破坏正常短横线表达。
        if t.count(" - ") >= 1:
            parts = [p.strip(" -") for p in re.split(r"\s+-\s+", t) if p.strip()]
            if len(parts) > 1:
                return parts
        return [t]

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
        if cleaned_b:
            for part in _split_compound_bullet(cleaned_b):
                if part and part not in combined:
                    combined.append(part)
                if len(combined) >= max_bullets:
                    break
        if len(combined) >= max_bullets:
            break

    # 不做硬截断，避免出现半句/断句。
    # 版面长度由项目数与 bullet 数控制。

    if not combined:
        combined = ['Delivered the solution end-to-end from requirements through release.']

    final_items = combined[:max_bullets]
    # Android 岗：ChatClothes 把含 PWA / 手持端的要点置顶，避免埋在纯 ML 句后面
    if lang == "en" and role_type == "android":
        _cpid = str(project.get("project_id") or project.get("_project_dir") or "").strip().lower()
        if _cpid == "chatclothes":
            mobile_first: List[str] = []
            rest_items: List[str] = []
            for it in final_items:
                low = (it or "").lower()
                if any(k in low for k in ("pwa", "android chrome", "handheld")):
                    mobile_first.append(it)
                else:
                    rest_items.append(it)
            if mobile_first:
                final_items = mobile_first + rest_items
    if lang == 'en':
        final_items = _diversify_bullet_openers_en(final_items)
    return final_items


def _last_sentence_period_index(text: str, before_index: int) -> int:
    """
    最大的 i < before_index 且 text[i] == '.'，且不是小数点（如 99.9%）。
    避免 rfind('.') 把「99.」当成句末，造成 overview / summary 残句。
    """
    if before_index <= 0 or not text:
        return -1
    lim = min(before_index - 1, len(text) - 1)
    for i in range(lim, -1, -1):
        if text[i] != ".":
            continue
        prev_d = i > 0 and text[i - 1].isdigit()
        next_d = i + 1 < len(text) and text[i + 1].isdigit()
        if prev_d and next_d:
            continue
        return i
    return -1


def _clip_overview_one_line(raw: Optional[str], max_chars: int) -> str:
    """
    取 summary/overview 的首行，并优先在句号处截断。
    若预算内没有完整句子，则保留原句，避免 PDF 文本层出现半词（如 voltag. / subs.）。
    """
    if not isinstance(raw, str) or not raw.strip():
        return ""
    line = raw.strip().split("\n")[0].strip()
    line = _remove_edge_terms(line)
    if len(line) <= max_chars:
        return line
    cut = _last_sentence_period_index(line, max_chars + 1)
    if cut > int(max_chars * 0.45):
        return line[: cut + 1]
    sp = line.rfind(" ", 0, max_chars)
    if sp > int(max_chars * 0.45):
        return line[:sp]
    return line[:max_chars]


def _timeline_year_from_field(project: Dict, field: str) -> int:
    """从 timeline.start / timeline.end 取四位年份，用于排序。"""
    tl = project.get("timeline") or {}
    if not isinstance(tl, dict):
        return 0
    raw = str(tl.get(field) or "").strip()
    if len(raw) < 4 or not raw[:4].isdigit():
        return 0
    try:
        return int(raw[:4])
    except ValueError:
        return 0


def _sort_chunxiao_subprojects_by_timeline(projects: List[Dict]) -> List[Dict]:
    """
    春晓同一雇主下的子项目：按结束年份降序（最近在前），结束年相同则按开始年份降序。
    避免阅读上时间线跳跃。
    """
    return sorted(
        projects,
        key=lambda p: (
            _timeline_year_from_field(p, "end"),
            _timeline_year_from_field(p, "start"),
        ),
        reverse=True,
    )


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


def _work_entry_date_label(exp: Dict, lang: str) -> str:
    """春晓合并雇主行日期：只显示年份区间（如 2013 – 2024），不显示月份。"""

    def _year_only(raw) -> str:
        if raw is None:
            return ""
        s = str(raw).strip()
        if len(s) >= 4 and s[:4].isdigit():
            return s[:4]
        return ""

    start = exp.get("start_date")
    end = exp.get("end_date")
    current = bool(exp.get("current"))
    left = _year_only(start)
    if current:
        right = "Present" if lang == "en" else "至今"
    else:
        right = _year_only(end)
    if left and right:
        return f"{left} – {right}"
    return left or right


def _chunxiao_progression_blurb(exp: Dict, lang: str) -> str:
    """
    春晓合并雇主下的职级一句话：只展示职级阶梯，不写每段年份，避免与表头总任期、子项目时间叠在一起显得乱。
    YAML 里 positions 建议从新到旧排列；展示顺序为当前 → 更早。
    """
    positions = exp.get("positions") or []
    if not isinstance(positions, list) or not positions:
        return ""
    titles: List[str] = []
    for p in positions:
        if not isinstance(p, dict):
            continue
        title = (p.get("title") or "").strip()
        if title:
            titles.append(title)
    if not titles:
        return ""

    seen = set()
    uniq_titles: List[str] = []
    for t in titles:
        if t in seen:
            continue
        seen.add(t)
        uniq_titles.append(t)

    # 新 → 旧（与 work.yaml positions 常见写法一致；若 YAML 是旧→新则反转为新→旧）
    ordered = list(uniq_titles)
    if len(ordered) >= 2:
        y0 = _progression_period_start_year(positions[0])
        y1 = _progression_period_start_year(positions[1])
        if y0 and y1 and y0 < y1:
            ordered = list(reversed(ordered))

    sep = " → " if lang == "zh" else " → "
    if lang == "zh":
        return "职级：" + sep.join(ordered) + "。"
    return "Progression: " + sep.join(ordered) + "."


def _progression_period_start_year(pos: Any) -> int:
    """从 position.period 取开始年，用于判断 YAML 中 positions 排序方向。"""
    if not isinstance(pos, dict):
        return 0
    raw = str(pos.get("period") or "")
    m = re.search(r"(20\d{2})", raw)
    return int(m.group(1)) if m else 0


def _project_employer_bucket(project: Dict) -> str:
    """aut | chunxiao | other — 用于合并同一雇主下的多段项目时间线。"""
    inst = project.get("institution") or {}
    iname = (inst.get("name") or "").strip() if isinstance(inst, dict) else ""
    ul = iname.upper()
    if iname and ("AUT" in ul or "AUCKLAND UNIVERSITY OF TECHNOLOGY" in ul):
        return "aut"
    comp = project.get("company") or {}
    cname = (comp.get("name") or "").strip() if isinstance(comp, dict) else ""
    if "Chunxiao" in cname or "春晓" in cname:
        return "chunxiao"
    return "other"


def _find_chunxiao_work_entry(work_yaml: Optional[Dict]) -> Optional[Dict]:
    if not work_yaml or not isinstance(work_yaml, dict):
        return None
    for exp in work_yaml.get("experiences") or []:
        if not isinstance(exp, dict):
            continue
        c = str(exp.get("company") or "")
        if "Chunxiao" in c or "春晓" in c:
            return exp
    return None


def _experience_blocks_ordered(projects: List[Dict]) -> List[tuple]:
    """
    将项目序列拆成 (kind, [projects])：
    - single: 非春晓连续段中的单个项目
    - cx_group: 连续的春晓项目合并展示
    """
    blocks: List[tuple] = []
    i = 0
    n = len(projects)
    while i < n:
        if _project_employer_bucket(projects[i]) == "chunxiao":
            j = i
            group: List[Dict] = []
            while j < n and _project_employer_bucket(projects[j]) == "chunxiao":
                group.append(projects[j])
                j += 1
            blocks.append(("cx_group", group))
            i = j
        else:
            blocks.append(("single", [projects[i]]))
            i += 1
    return blocks


def _render_one_project_job_html(
    project: Dict,
    lang: str,
    role_type: str,
    all_bullets: Optional[List[Dict]],
    jd_keywords: Optional[List[str]],
    used_bullets_norm: set,
    *,
    include_company_column: bool,
    wrapper_class: str = "job",
) -> str:
    """渲染单个项目经历卡片（可选隐藏公司列，用于春晓雇主下的子项目）。"""

    def _normalize_bullet_for_dedupe(text: str) -> str:
        t = _strip_html_tags(text or "")
        t = re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
        return t

    if lang == 'zh':
        name = (project.get('name_cn')
                or project.get('name')
                or project.get('project_id', ''))
    else:
        name = project.get('name') or project.get('project_id', '')

    company_info = project.get('company', {})
    institution = project.get('institution', {})
    if isinstance(institution, dict) and institution.get('name'):
        company = institution['name']
    elif isinstance(company_info, dict) and company_info.get('name'):
        company = company_info['name']
    else:
        company = ('Chunxiao Technology Co., Ltd.'
                   if lang == 'en' else '春晓科技有限公司')

    if lang == 'zh':
        role = (project.get('role_cn') or project.get('role') or '').strip()
    else:
        role = (project.get('role') or '').strip()

    date_range = _fmt_date_range(project)

    tech_stack = project.get('tech_stack', {})
    tech_line = _compact_tech_stack_one_line(tech_stack)
    tech_display = (
        f'<div class="job-tech"><strong>Tech:</strong> {html.escape(tech_line)}</div>'
        if tech_line
        else ""
    )

    if lang == 'zh':
        overview_raw = (project.get('overview_cn')
                        or project.get('summary_cn')
                        or project.get('summary', ''))
    else:
        overview_raw = project.get('overview') or project.get('summary', '')
    if isinstance(overview_raw, str):
        overview = _clip_overview_one_line(overview_raw, OVERVIEW_MAX_CHARS)
    else:
        overview = ''

    bullets = generate_project_bullet_points(
        project,
        lang=lang,
        role_type=role_type,
        all_bullets=all_bullets,
        jd_keywords=jd_keywords,
    )
    deduped_bullets: List[str] = []
    for b in bullets:
        nb = _normalize_bullet_for_dedupe(b)
        if not nb:
            continue
        if nb in used_bullets_norm:
            continue
        used_bullets_norm.add(nb)
        deduped_bullets.append(b)

    if not deduped_bullets and bullets:
        deduped_bullets = [bullets[0]]

    bullets = deduped_bullets
    bullets_html = '\n            '.join(f'<li>{b}</li>' for b in bullets)

    safe_name = html.escape(str(name))
    safe_company = html.escape(str(company))
    safe_date = html.escape(str(date_range))
    safe_role = html.escape(str(role))
    safe_overview = html.escape(str(overview)) if overview else ""

    if include_company_column:
        header_row = f'''<tr>
          <td class="jh-title">{safe_name}</td>
          <td class="jh-company">{safe_company}</td>
          <td class="jh-date">{safe_date}</td>
        </tr>'''
    else:
        header_row = f'''<tr>
          <td class="jh-title">{safe_name}</td>
          <td class="jh-date">{safe_date}</td>
        </tr>'''

    return f'''
    <div class="{wrapper_class}">
      <table class="job-header-table">
        {header_row}
      </table>
      <div class="job-role"><strong>{safe_role}</strong>{" — " + safe_overview if safe_overview else ""}</div>
      {tech_display}
      <ul class="job-list">
        {bullets_html}
      </ul>
    </div>'''


def _render_chunxiao_employer_group_html(
    cx_projects: List[Dict],
    work_entry: Optional[Dict],
    lang: str,
    role_type: str,
    all_bullets: Optional[List[Dict]],
    jd_keywords: Optional[List[str]],
    used_bullets_norm: set,
) -> str:
    """单一雇主（春晓）+ 总任职时间 + 子项目阶段。"""
    company_name = "Chunxiao Technology Co., Ltd."
    location = "China"
    role_title = "Technical Lead / Senior Software Engineer"
    if work_entry:
        company_name = str(work_entry.get("company") or company_name)
        location = str(work_entry.get("location") or location)
        role_title = str(work_entry.get("role") or role_title)

    date_lbl = _work_entry_date_label(work_entry, lang) if work_entry else ""
    progression = _chunxiao_progression_blurb(work_entry, lang) if work_entry else ""
    progression_html = (
        f'<div class="employer-progression">{html.escape(progression)}</div>'
        if progression
        else ""
    )

    loc_html = f'<span class="employer-loc"> — {html.escape(location)}</span>' if location else ""

    subs: List[str] = []
    for p in cx_projects:
        subs.append(
            _render_one_project_job_html(
                p, lang, role_type, all_bullets, jd_keywords, used_bullets_norm,
                include_company_column=False,
                wrapper_class="sub-project",
            )
        )

    return f'''
    <div class="job job-employer">
      <table class="job-header-table">
        <tr>
          <td class="jh-title employer-company" colspan="2">{html.escape(company_name)}{loc_html}</td>
          <td class="jh-date">{html.escape(date_lbl)}</td>
        </tr>
      </table>
      <div class="job-role"><strong>{html.escape(role_title)}</strong></div>
      {progression_html}
      {''.join(subs)}
    </div>'''


def generate_experience_section(
    projects: List[Dict],
    lang: str = 'en',
    role_type: str = 'fullstack',
    all_bullets: Optional[List[Dict]] = None,
    jd_keywords: Optional[List[str]] = None,
    work_experience_yaml: Optional[Dict] = None,
) -> str:
    """将已排序的项目列表渲染为 HTML（春晓多项目合并为单一雇主时间线）。"""
    used_bullets_norm: set[str] = set()
    cx_entry = _find_chunxiao_work_entry(work_experience_yaml)
    parts: List[str] = []

    for kind, group in _experience_blocks_ordered(projects):
        if kind == "single":
            parts.append(
                _render_one_project_job_html(
                    group[0], lang, role_type, all_bullets, jd_keywords, used_bullets_norm,
                    include_company_column=True,
                    wrapper_class="job",
                )
            )
        else:
            cx_ordered = _sort_chunxiao_subprojects_by_timeline(group)
            parts.append(
                _render_chunxiao_employer_group_html(
                    cx_ordered, cx_entry, lang, role_type, all_bullets, jd_keywords, used_bullets_norm,
                )
            )

    return '\n'.join(parts)


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
# Licenses & Certifications + Publications + Interests
# ---------------------------------------------------------------------------

def _achievement_year_sort_key(item: Dict) -> int:
    """用于证书/奖项排序：整数年份或字符串中的四位年份（取最大）。"""
    y = item.get("year")
    if isinstance(y, int):
        return y
    if isinstance(y, str) and y.strip():
        found = re.findall(r"\d{4}", y)
        if found:
            return max(int(x) for x in found)
    return 0


def generate_licenses_section(achievements: Dict, lang: str = 'en') -> str:
    """从 achievements.yaml 生成证书、奖项条目（按时间新近优先统一排序）。"""
    raw_certs = [c for c in (achievements.get("certifications") or []) if isinstance(c, dict)]
    raw_awards = [a for a in (achievements.get("awards") or []) if isinstance(a, dict)]
    awards_pick = sorted(raw_awards, key=_achievement_year_sort_key, reverse=True)[:2]

    merged: List[Dict] = [{**c, "_lc_kind": "cert"} for c in raw_certs]
    merged.extend({**a, "_lc_kind": "award"} for a in awards_pick)
    merged.sort(key=_achievement_year_sort_key, reverse=True)

    lines = []
    for row in merged:
        name = row.get("name", "")
        authority = row.get("authority", "")
        year = row.get("year", "")
        if row.get("_lc_kind") == "award":
            category = (row.get("category") or "").strip()
            display = f"{name} ({category})" if category else name
        else:
            display = name
        lines.append(
            f'<li><div class="lc-row">'
            f'<span><strong>{html.escape(str(display))}</strong> — {html.escape(str(authority))}</span>'
            f'<span class="lc-date">{html.escape(str(year))}</span>'
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
        title = pub.get('title', '')
        venue = pub.get('venue', '')
        year = pub.get('year', '')
        doi = pub.get('doi', '')
        url = pub.get('url', '')

        link = f"https://doi.org/{doi}" if doi else (url or "")
        title_html = (
            f'<a href="{html.escape(link, quote=True)}" style="color:#1a3a6a;">{html.escape(str(title))}</a>'
            if link
            else html.escape(str(title))
        )

        year_text = html.escape(str(year))
        venue_text = html.escape(str(venue))
        venue_year = venue_text if (year_text and year_text in venue_text) else f"{venue_text}, {year_text}"

        link_html = (
            f'<span style="color:#1a4a8a;font-size:9.2pt;"> | '
            f'<a href="{html.escape(link, quote=True)}" style="color:#1a4a8a;">{html.escape(link)}</a></span>'
            if link
            else ""
        )

        lines.append(
            f'<li><div class="lc-row lc-row-pub">'
            f'<span><strong>{title_html}</strong><br>'
            f'<span style="color:#444;font-size:9.5pt;">{venue_year}</span>{link_html}</span>'
            f'<span class="lc-date"></span>'
            f'</div></li>'
        )

    return '\n'.join(lines)


def generate_interests_section(profile: Dict, lang: str = 'en') -> str:
    """从 profile.yaml 生成 Interests（始终放在最后，低优先级补充信息）。"""
    career = profile.get('career_identity', {}) if isinstance(profile, dict) else {}
    if lang == 'zh':
        interests = career.get('interests_zh') or []
    else:
        interests = career.get('interests_en') or []

    if not interests or not isinstance(interests, list):
        return ''

    return '\n'.join(f'<li>{html.escape(str(x))}</li>' for x in interests if str(x).strip())


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
      font-family: 'Times New Roman', Cambria, Georgia, serif;
      font-size: 11.6pt;
      line-height: 1.36;
      color: #111;
      max-width: 210mm;
      margin: 0 auto;
      padding: 0;
      background: #fff;
      hyphens: none;
      -webkit-hyphens: none;
      word-break: normal;
      overflow-wrap: break-word;
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
      font-family: 'Times New Roman', Georgia, serif;
      font-size: 21pt;
      font-weight: 600;
      color: #111;
      letter-spacing: 0.2px;
      margin-bottom: 5px;
      text-align: center;
    }

    .cv-name a { color: #111; }

    .cv-contact {
      font-size: 10pt;
      color: #1a4a8a;
      line-height: 1.55;
      text-align: center;
    }

    .cv-contact a { color: #1a4a8a; }

    .cv-contact-primary {
      margin-bottom: 4px;
      line-height: 1.5;
    }

    /* 页眉内联 SVG（定位 / 品牌），与 10pt 正文视觉中线一致 */
    .cv-header-icon {
      width: 14px;
      height: 14px;
      vertical-align: -0.2em;
      display: inline-block;
      margin-right: 4px;
      flex-shrink: 0;
    }

    .cv-header-icon-loc {
      color: #1a4a8a;
    }

    /* 社交：图标与文字在链接内垂直居中；整段链接与同行用 middle 对齐 */
    a.cv-social-link {
      color: #1a4a8a;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      line-height: 1;
      vertical-align: middle;
      font-size: inherit;
    }

    a.cv-social-link .cv-header-icon {
      vertical-align: middle;
      margin-right: 0;
    }

    a.cv-social-link:hover {
      text-decoration: underline;
    }

    .cv-contact-secondary {
      font-size: 9.5pt;
      color: #1a4a8a;
      margin-top: 3px;
      line-height: 1.45;
    }

    /* ── Section title ───────────────────────────────── */
    .section-title {
      font-family: 'Times New Roman', Georgia, serif;
      font-size: 13.2pt;
      font-weight: 600;
      color: #1a4d96;
      font-variant: small-caps;
      margin-top: 9px;
      margin-bottom: 5px;
      border-bottom: 0.8px solid #8a8a8a;
      padding-bottom: 1px;
      letter-spacing: 0.7px;
      line-height: 1.1;
    }

    .section-title::first-letter {
      font-size: 1.12em;
      position: relative;
      top: 0.04em;
    }

    /* ── Summary ─────────────────────────────────────── */
    .cv-summary {
      text-align: justify;
      color: #222;
      margin-bottom: 4px;
      hyphens: none;
      -webkit-hyphens: none;
      word-break: normal;
    }

    /* ── Skills ──────────────────────────────────────── */
    .cv-skills {
      margin-bottom: 4px;
      line-height: 1.55;
    }

    /* ── Experience ──────────────────────────────────── */
    .job {
      margin-bottom: 6px;
      page-break-inside: avoid;
    }

    .job-tech {
      font-size: 10.4pt;
      color: #444;
      margin-bottom: 2px;
      line-height: 1.35;
      hyphens: none;
      -webkit-hyphens: none;
      word-break: normal;
    }

    .job-header-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 1px;
    }

    .jh-title {
      font-weight: 700;
      font-size: 11.2pt;
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
      font-size: 10.5pt;
      width: 20%;
      text-align: right;
      padding: 0;
      white-space: nowrap;
      vertical-align: baseline;
    }

    .job-role {
      font-size: 10.9pt;
      color: #333;
      margin-bottom: 3px;
      hyphens: none;
      -webkit-hyphens: none;
      word-break: normal;
    }

    .job-list {
      margin: 0;
      padding-left: 18px;
      font-size: 10.9pt;
      color: #222;
    }

    .job-list li {
      margin-bottom: 1px;
      line-height: 1.35;
    }

    /* 允许春晓雇主块跨页，避免上一页大块留白（子项目可在页间断开） */
    .job-employer {
      margin-bottom: 8px;
      page-break-inside: auto;
      break-inside: auto;
    }

    .employer-company {
      font-weight: 700;
      font-size: 11.2pt;
    }

    .employer-loc {
      font-weight: 400;
      font-style: italic;
      color: #444;
      font-size: 10.7pt;
    }

    .employer-progression {
      font-size: 10.4pt;
      color: #444;
      margin-bottom: 4px;
      line-height: 1.35;
    }

    .sub-project {
      margin: 4px 0 6px 10px;
      padding-left: 10px;
      border-left: 2px solid #cfd8ea;
      page-break-inside: auto;
      break-inside: auto;
    }

    .sub-project .job-header-table .jh-title {
      width: 62%;
    }

    .sub-project .jh-date {
      width: 38%;
      text-align: right;
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
      font-size: 10.5pt;
    }

    .eh-date {
      color: #777;
      font-size: 10.5pt;
      width: 18%;
      text-align: right;
      padding: 0;
      white-space: nowrap;
      vertical-align: baseline;
    }

    .edu-detail {
      font-size: 10.4pt;
      color: #444;
      margin-top: 2px;
    }

    /* ── Licenses / Publications ─────────────────────── */
    .lc-list {
      list-style: none;
      margin: 0;
      padding: 0;
      font-size: 10.4pt;
    }

    .lc-list li {
      margin-bottom: 3px;
    }

    .lc-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      line-height: 1.28;
      gap: 10px;
    }

    .lc-date {
      color: #777;
      font-size: 9.5pt;
      margin-left: 8px;
      white-space: nowrap;
      text-align: right;
      min-width: 44px;
    }

    .lc-row-pub {
      display: block;
    }

    /* ── Print ───────────────────────────────────────── */
    @media print {
      body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    }
"""


# ---------------------------------------------------------------------------
# HTML 组装
# ---------------------------------------------------------------------------

# 页眉用内联 SVG；实心对称 map pin（仅外轮廓、无中心圆孔，小字号/PDF 更清晰）
_CV_ICON_LOC_SVG = (
    '<svg class="cv-header-icon cv-header-icon-loc" xmlns="http://www.w3.org/2000/svg" '
    'viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" '
    'd="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7z"/>'
    '</svg>'
)

_CV_ICON_LINKEDIN_SVG = (
    '<svg class="cv-header-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    'aria-hidden="true" focusable="false">'
    '<path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 '
    '0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 '
    '3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 '
    '0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 '
    '2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 '
    '23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>'
    '</svg>'
)

_CV_ICON_GITHUB_SVG = (
    '<svg class="cv-header-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    'aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 '
    '11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 '
    '1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 '
    '0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 '
    '1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 '
    '0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 '
    '0-6.627-5.373-12-12-12z"/>'
    '</svg>'
)


def generate_html_from_kb(
    role_type: str = 'fullstack',
    lang: str = 'en',
    jd_keywords: Optional[List[str]] = None,
    max_projects: int = DEFAULT_MAX_PROJECTS,
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
            'pub':      'Publications',
            'interests': 'Interests',
        },
        'zh': {
            'summary':  '个人简介',
            'skills':   '核心技能',
            'exp':      '工作经历',
            'edu':      '教育背景',
            'licenses': '证书与认证',
            'pub':      '发表成果',
            'interests': '兴趣',
        },
    }
    lbl = labels.get(lang, labels['en'])

    # ── 加载数据 ──
    base = Path(__file__).parent.parent.parent   # repo root
    kb_dir = base / 'kb'
    profile         = load_yaml(kb_dir / 'profile.yaml')
    skills_data     = load_yaml(kb_dir / 'skills.yaml')
    achievements    = load_yaml(kb_dir / 'achievements.yaml')
    work_exp_yaml   = load_yaml(kb_dir / 'experience' / 'work.yaml')
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
    city        = (loc.get('city') or '').strip()
    country     = (loc.get('country') or '').strip()
    city_cn     = (loc.get('city_cn') or '').strip()
    country_cn  = (loc.get('country_cn') or '').strip()
    linkedin    = (contact.get('linkedin') or '').strip()
    github      = (contact.get('github') or 'https://github.com/leozhang2056').strip()

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
        work_experience_yaml=work_exp_yaml,
    )
    edu_html     = generate_education_section(profile, lang)
    lic_html     = generate_licenses_section(achievements, lang)
    pub_html     = generate_publications_section(achievements, lang)
    pub_section = (
        f'<div class="section-title">{lbl["pub"]}</div>\n'
        f'  <ul class="lc-list">\n{pub_html}\n  </ul>'
        if pub_html
        else ''
    )
    interests_html = generate_interests_section(profile, lang)
    career = profile.get('career_identity', {}) if isinstance(profile, dict) else {}
    include_interests = bool(interests_html) and bool(career.get('include_interests_in_cv', False))
    interests_section = (
        f'<div class="section-title">{lbl["interests"]}</div>\n'
        f'  <ul class="lc-list">\n{interests_html}\n  </ul>'
        if include_interests
        else ''
    )

    # ── 目标职位 / 公司（仅用于内部命名，不在简历顶部显示） ──
    default_titles = {
        'android':   'Senior Android Developer',
        'backend':   'Senior Backend Engineer (Java/Spring)',
        'ai':        'AI Engineer (Computer Vision / LLM)',
        'fullstack': 'Senior Full-Stack Engineer',
    }
    title_text = (target_role_title or default_titles.get(role_type, 'Software Engineer')).strip()

    _safe_name = html.escape(name)
    _li = html.escape(linkedin, quote=True) if linkedin else ""
    _gh = html.escape(github, quote=True) if github else ""
    _safe_email = html.escape(email or "", quote=True)
    _disp_email = html.escape(email or "")
    _disp_phone = html.escape(phone or "")

    if lang == 'zh':
        loc_city = city_cn or city
        loc_ctry = country_cn or country
    else:
        loc_city = city
        loc_ctry = country
    if loc_city and loc_ctry:
        # EN: e.g. Auckland,NZ; ZH: 奥克兰，新西兰
        location_line = f"{loc_city}，{loc_ctry}" if lang == 'zh' else f"{loc_city},{loc_ctry}"
    else:
        location_line = (loc_city or loc_ctry or "").strip()

    contact_primary_bits: List[str] = [
        f'<a href="mailto:{_safe_email}">&#9993;&nbsp;{_disp_email}</a>',
        f'&#9990;&nbsp;{_disp_phone}',
    ]
    if location_line:
        contact_primary_bits.append(f'{_CV_ICON_LOC_SVG}{html.escape(location_line)}')
    if linkedin:
        contact_primary_bits.append(
            f'<a href="{_li}" class="cv-social-link">{_CV_ICON_LINKEDIN_SVG}LinkedIn</a>'
        )
    if github:
        contact_primary_bits.append(
            f'<a href="{_gh}" class="cv-social-link">{_CV_ICON_GITHUB_SVG}GitHub</a>'
        )
    contact_primary_row = (
        f'<div class="cv-contact-primary">'
        f'{"&nbsp;|&nbsp;".join(contact_primary_bits)}'
        f'</div>'
    )

    contact_secondary = ""

    html_doc = f'''<!DOCTYPE html>
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
      {_safe_name}
    </div>
    <div class="cv-contact">
      {contact_primary_row}
    </div>
    {contact_secondary}
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

  <!-- Education（置于 Experience 与 Licenses 之间） -->
  <div class="section-title">{lbl['edu']}</div>
  {edu_html}

  <!-- Licenses & Certifications -->
  <div class="section-title">{lbl['licenses']}</div>
  <ul class="lc-list">
{lic_html}
  </ul>

  {pub_section}

  {interests_section}

</body>
</html>'''

    return html_doc


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
    if len(plain) > BUNDLE_SIZE_LIMIT:
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
    历史行为：向 Summary 尾部注入缺失 JD 词以抬覆盖率（易产生「关键词对齐」腔调）。
    已关闭；JD 贴合由 Experience 与 Key Skills 承担。保留签名供调用方不变。
    """
    return html


def _print_quality_metrics(html: str, jd_keywords: Optional[List[str]], role_type: str, min_target_pct: float) -> None:
    """打印生成质量指标，包括长度、关键词覆盖等。"""
    plain = _strip_html_tags(html)
    word_count = len(plain.split())
    char_count = len(plain)
    hits: List[str] = []
    misses: List[str] = []
    coverage: float = 100.0

    print(f"  Quality Metrics → Words: {word_count}, Chars: {char_count}")
    
    if jd_keywords:
        hits, misses, coverage = _jd_match_hits_misses_coverage(html, jd_keywords)
        print(f"  JD Coverage → {coverage:.1f}% ({len(hits)}/{len(jd_keywords)} hits)")
        if misses:
            print(f"  Missed JD terms → {', '.join(misses[:5])}" + ("..." if len(misses) > 5 else ""))
    
    # 检查是否有管理术语（应该很少）
    management_terms = ["led", "managed", "mentored", "team leadership"]
    mgmt_count = sum(1 for term in management_terms if term.lower() in plain.lower())
    if mgmt_count > 0:
        print(f"  Management terms detected → {mgmt_count} (consider minimizing for dev roles)")
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
    max_projects: int = DEFAULT_MAX_PROJECTS,
    company_name: Optional[str] = None,
    target_role_title: Optional[str] = None,
    generate_zh: bool = False,
    generate_quality_report: bool = False,
    generate_jd_annotated_pdf: bool = False,
    min_jd_match_pct: float = 85.0,
    write_review_bundle: bool = False,
    keep_html: bool = False,
    strict_kb: bool = True,
    run_post_check: bool = True,
):
    """
    从 KB 生成简历 PDF（默认仅英文，可选中文）。

    Args:
        output_path:   英文版输出路径（可选，若提供则优先生效）
        role_type:     android | ai | backend | fullstack
        jd_keywords:   JD 关键词列表，驱动项目和技能排序
        max_projects:  最多显示几个项目（默认 6，代码内封顶以控制约两页 A4）
        company_name:  投递公司名称；若提供且未显式指定 output_path，
                       将在文件名中追加公司名，便于区分不同公司的简历。
        generate_zh:   是否生成中文简历（默认 False）
        generate_quality_report: 是否生成质量报告（默认 False）
        generate_jd_annotated_pdf: 是否额外生成 JD 标注版 PDF（默认 False）
        min_jd_match_pct: 对「KB 支持的」JD 词的目标最低覆盖率（默认 85）；<=0 关闭自动补词
        write_review_bundle: 是否写出供第二个 AI 评审的 Markdown 包（默认 False）
        keep_html: 为 True 时保留与 PDF 同名的中间 .html，便于核对版式（默认删中间件）
        strict_kb: 为 True 时在生成前进行 KB 严格校验，失败则直接中止生成（默认 True）
        run_post_check: 为 True 时在生成英文 PDF 后运行流畅度/版式/JD 覆盖检查并写出 *_POST_CHECK.md（默认 True）
    """
    # 篇幅：默认约两页 A4；至少保留 pinned 核心项目数（Android 含 forest-patrol）
    _min_slots = 3 if role_type == "android" else 2
    mp = int(max_projects or DEFAULT_MAX_PROJECTS)
    max_projects = max(_min_slots, min(mp, CV_MAX_PROJECTS_CAP))

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

    # Fail-fast: KB 不通过结构校验时直接中止，避免输出“悄悄降级”的 PDF。
    if strict_kb:
        try:
            from kb_loader import KBLoader  # type: ignore
        except ModuleNotFoundError:
            from app.backend.kb_loader import KBLoader  # type: ignore

        kb_loader = KBLoader(repo_root)
        kb_loader.load_all(strict=True)

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
    _print_quality_metrics(html_en, safe_jd_keywords, role_type, min_target_pct=min_jd_match_pct)

    rb_hits, rb_misses, rb_cov = _jd_match_hits_misses_coverage(html_en, safe_jd_keywords)
    if run_post_check and POST_CHECK_AVAILABLE:
        try:
            post_report = run_post_generation_check(
                html_en,
                safe_jd_keywords,
                rb_hits,
                rb_misses,
                rb_cov,
                min_jd_match_pct,
            )
            print_post_check_summary(post_report, min_jd_match_pct)
            post_md_path = str(Path(en_path).with_name(f"{Path(en_path).stem}_POST_CHECK.md"))
            with open(post_md_path, "w", encoding="utf-8") as pf:
                pf.write(build_post_check_markdown(post_report, min_jd_match_pct))
            print(f"  POST CHECK MD → {post_md_path}")
        except Exception as e:
            print(f"  Warning: post-generation check failed: {e}")
    elif run_post_check and not POST_CHECK_AVAILABLE:
        print("  POST CHECK → skipped (cv_post_generation_check not importable)")

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
        print("  AI REVIEW BUNDLE → skipped (use --with-review-bundle)")

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
    # 清理中间产物：HTML（默认删除，避免误以为旧 PDF 未更新时可加 --keep-html 对照）
    if not keep_html:
        try:
            os.remove(html_en_path)
        except Exception:
            pass
    else:
        print(f"  EN HTML (kept) → {html_en_path}")

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
        if not keep_html:
            try:
                os.remove(html_zh_path)
            except Exception:
                pass
        else:
            print(f"  CN HTML (kept) → {html_zh_path}")
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
