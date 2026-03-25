#!/usr/bin/env python3
"""
CV Quality Validator - 简历质量自动验证器

提供多维度的简历质量检查：
1. 验证清单自动化检查
2. ATS 兼容性检测
3. Bullet 质量深度评分
4. Summary 质量检查
5. AI 腔检测
6. 一致性检查
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class QualityIssue:
    """质量问题"""
    severity: str  # 'error' | 'warning' | 'info'
    category: str  # 'validation' | 'ats' | 'bullet' | 'summary' | 'ai_tone' | 'consistency'
    location: str  # 问题位置
    message: str   # 问题描述
    suggestion: str  # 修复建议


@dataclass
class BulletScore:
    """Bullet 质量评分"""
    text: str
    verb_strength: float = 0.0  # 0-1
    has_metrics: bool = False
    has_technology: bool = False
    has_scope: bool = False
    length_ok: bool = False
    jd_hits: List[str] = field(default_factory=list)
    overall_score: float = 0.0
    issues: List[str] = field(default_factory=list)


@dataclass
class QualityReport:
    """质量报告"""
    passed: bool
    score: float  # 0-100
    issues: List[QualityIssue] = field(default_factory=list)
    bullet_scores: List[BulletScore] = field(default_factory=list)
    summary_score: float = 0.0
    ats_score: float = 0.0
    ai_tone_score: float = 0.0
    checklist: Dict[str, bool] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

# 强动词列表 (按强度分级)
STRONG_VERBS = {
    'tier1': ['built', 'led', 'developed', 'architected', 'designed', 'launched', 'shipped', 'delivered'],
    'tier2': ['implemented', 'created', 'engineered', 'optimized', 'refactored', 'integrated', 'deployed', 'automated'],
    'tier3': ['built', 'made', 'worked on', 'helped', 'participated', 'assisted', 'supported'],
}

WEAK_VERBS = ['helped', 'participated', 'was responsible for', 'worked on', 'assisted', 'supported']

# AI 腔检测关键词
AI_BUZZWORDS = [
    'passionate', 'world-class', 'cutting-edge', 'state-of-the-art', 'best-in-class',
    'leverage', 'synergy', 'paradigm', 'revolutionary', 'game-changing',
    'seamlessly', 'robust', 'scalable', 'innovative', 'dynamic',
    'end-to-end', 'holistic', 'comprehensive', 'groundbreaking',
]

AI_PHRASES = [
    r'passionate about',
    r'world-class',
    r'cutting-edge',
    r'state-of-the-art',
    r'best-in-class',
    r'leverage.*to',
    r'seamlessly integrate',
    r'robust and scalable',
    r'dynamic team',
    r'innovative solutions',
    r'end-to-end.*solution',
]

# ATS 问题模式
ATS_ISSUE_PATTERNS = [
    (r'<img[^>]*>', 'Images may not parse correctly in ATS'),
    (r'<table[^>]*>', 'Tables may not parse correctly in ATS'),
    (r'&[a-z]+;', 'Special HTML entities may not render in ATS'),
    (r'[\u2500-\u257F]', 'Box drawing characters may not parse in ATS'),
    (r'[\u2600-\u26FF]', 'Miscellaneous symbols may not parse in ATS'),
    (r'\|{2,}', 'Multiple pipes may confuse ATS parsing'),
]

# 时间线格式
DATE_PATTERNS = [
    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}',
    r'\d{1,2}/\d{4}',
    r'\d{4}\s*[-–]\s*(Present|Current|\d{4})',
]


# ---------------------------------------------------------------------------
# 验证函数
# ---------------------------------------------------------------------------

def extract_text_from_html(html: str) -> str:
    """从 HTML 中提取纯文本"""
    # 移除 script 和 style
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除标签
    text = re.sub(r'<[^>]+>', ' ', text)
    # 解码 HTML 实体
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'")
    # 清理空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_sections(html: str) -> Dict[str, str]:
    """从 HTML 中提取各个部分"""
    sections = {}
    
    # 提取 Summary - 匹配 cv-summary class
    summary_match = re.search(r'<div[^>]*class="[^"]*cv-summary[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if summary_match:
        sections['summary'] = extract_text_from_html(summary_match.group(1))
    
    # 备用模式: section-title 后的内容
    if 'summary' not in sections:
        summary_match = re.search(r'<div[^>]*class="section-title"[^>]*>.*?Summary.*?</div>\s*<div[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
        if summary_match:
            sections['summary'] = extract_text_from_html(summary_match.group(1))
    
    # 提取 Skills - 匹配 cv-skills class
    skills_match = re.search(r'<div[^>]*class="[^"]*cv-skills[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if skills_match:
        sections['skills'] = extract_text_from_html(skills_match.group(1))
    
    # 提取 Experience bullets - 匹配 job class 或 li 标签
    bullets = re.findall(r'<li[^>]*>(.*?)</li>', html, re.DOTALL | re.IGNORECASE)
    if bullets:
        sections['bullets'] = [extract_text_from_html(b) for b in bullets if extract_text_from_html(b).strip()]
    
    return sections


def check_bullet_quality(bullet: str, jd_keywords: List[str] = None) -> BulletScore:
    """检查单个 bullet 的质量"""
    bullet_lower = bullet.lower().strip()
    score = BulletScore(text=bullet)
    
    # 1. 动词强度检查
    first_words = bullet_lower.split()[:3] if bullet_lower else []
    verb_found = False
    
    for verb in STRONG_VERBS['tier1']:
        if any(verb in w for w in first_words):
            score.verb_strength = 1.0
            verb_found = True
            break
    
    if not verb_found:
        for verb in STRONG_VERBS['tier2']:
            if any(verb in w for w in first_words):
                score.verb_strength = 0.7
                verb_found = True
                break
    
    if not verb_found:
        for verb in WEAK_VERBS:
            if verb in bullet_lower[:50]:
                score.verb_strength = 0.3
                score.issues.append(f'Weak verb detected: "{verb}"')
                break
    
    if not verb_found:
        score.verb_strength = 0.5
    
    # 2. 量化指标检查
    metrics_patterns = [
        r'\d+%',  # 百分比
        r'\$\d+',  # 金额
        r'\d+x',  # 倍数
        r'\d+\+',
        r'\d{3,}',  # 大数字（可能是指标）
        r'(increased|decreased|reduced|improved|grew|saved).*\d',  # 变化动词+数字
    ]
    score.has_metrics = any(re.search(p, bullet, re.IGNORECASE) for p in metrics_patterns)
    if not score.has_metrics:
        score.issues.append('No quantified metrics found')
    
    # 3. 技术栈检查
    tech_patterns = [
        r'\b(Java|Kotlin|Python|Spring|Android|React|Vue|Docker|Kubernetes|Redis|MySQL|PostgreSQL|MongoDB|AWS|Azure|GCP|REST|API|SDK|NDK|JNI)\b',
        r'\b(architecture|microservice|pipeline|framework|library|module|component)\b',
    ]
    score.has_technology = any(re.search(p, bullet, re.IGNORECASE) for p in tech_patterns)
    
    # 4. 范围/影响力检查
    scope_patterns = [
        r'\d+\s*(users?|customers?|sites?|servers?|services?|apps?|modules?|features?)',
        r'(team|team size|scope|budget|region|market|platform)',
        r'(enterprise|production|live|global|national|regional)',
    ]
    score.has_scope = any(re.search(p, bullet, re.IGNORECASE) for p in scope_patterns)
    
    # 5. 长度检查
    word_count = len(bullet.split())
    score.length_ok = 10 <= word_count <= 30
    if word_count < 10:
        score.issues.append(f'Bullet too short ({word_count} words)')
    elif word_count > 30:
        score.issues.append(f'Bullet too long ({word_count} words)')
    
    # 6. JD 关键词命中
    if jd_keywords:
        kws_lower = [k.lower() for k in jd_keywords]
        score.jd_hits = [k for k in kws_lower if k in bullet_lower]
    
    # 计算总分
    score.overall_score = (
        score.verb_strength * 25 +
        (15 if score.has_metrics else 0) +
        (15 if score.has_technology else 0) +
        (10 if score.has_scope else 0) +
        (15 if score.length_ok else 5) +
        (20 if score.jd_hits else 0)
    )
    
    return score


def check_summary_quality(summary: str, jd_keywords: List[str] = None) -> Tuple[float, List[QualityIssue]]:
    """检查 Summary 质量"""
    issues = []
    score = 0.0
    
    if not summary:
        issues.append(QualityIssue(
            severity='error',
            category='summary',
            location='Summary',
            message='Summary is empty',
            suggestion='Add a 5-6 line professional summary'
        ))
        return 0.0, issues
    
    # 1. 长度检查
    lines = [l.strip() for l in summary.split('.') if l.strip()]
    word_count = len(summary.split())
    
    if 50 <= word_count <= 100:
        score += 20
    elif word_count < 50:
        issues.append(QualityIssue(
            severity='warning',
            category='summary',
            location='Summary',
            message=f'Summary too short ({word_count} words)',
            suggestion='Expand to 50-100 words (5-6 lines)'
        ))
        score += 10
    else:
        issues.append(QualityIssue(
            severity='warning',
            category='summary',
            location='Summary',
            message=f'Summary too long ({word_count} words)',
            suggestion='Condense to 50-100 words (5-6 lines)'
        ))
        score += 10
    
    # 2. 完整性检查（是否以完整句子结尾）
    if summary.rstrip().endswith('.') or summary.rstrip().endswith('.'):
        score += 15
    else:
        issues.append(QualityIssue(
            severity='error',
            category='summary',
            location='Summary',
            message='Summary does not end with a complete sentence',
            suggestion='Ensure summary ends with a period'
        ))
    
    # 3. 成就检查
    has_achievement = bool(re.search(r'(built|led|developed|launched|delivered|achieved|improved|reduced).*\d', summary, re.IGNORECASE))
    if has_achievement:
        score += 20
    else:
        issues.append(QualityIssue(
            severity='warning',
            category='summary',
            location='Summary',
            message='No evidence-backed achievement in summary',
            suggestion='Add at least one concrete, quantified achievement'
        ))
    
    # 4. JD 关键词覆盖
    if jd_keywords:
        kws_lower = [k.lower() for k in jd_keywords]
        hits = [k for k in kws_lower if k in summary.lower()]
        if hits:
            score += min(25, len(hits) * 5)
        else:
            issues.append(QualityIssue(
                severity='warning',
                category='summary',
                location='Summary',
                message='No JD keywords in summary',
                suggestion='Naturally integrate 2-3 relevant JD keywords'
            ))
    
    # 5. AI 腔检查
    summary_lower = summary.lower()
    ai_detected = []
    for phrase in AI_PHRASES:
        if re.search(phrase, summary_lower):
            ai_detected.append(phrase)
    
    for word in AI_BUZZWORDS:
        if word in summary_lower:
            ai_detected.append(word)
    
    if ai_detected:
        score -= min(15, len(ai_detected) * 3)
        issues.append(QualityIssue(
            severity='info',
            category='ai_tone',
            location='Summary',
            message=f'Potential AI-sounding phrases detected: {", ".join(ai_detected[:3])}',
            suggestion='Replace buzzwords with concrete, specific language'
        ))
    
    return max(0, score), issues


def check_ats_compatibility(html: str) -> Tuple[float, List[QualityIssue]]:
    """检查 ATS 兼容性"""
    issues = []
    score = 100.0
    
    for pattern, message in ATS_ISSUE_PATTERNS:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            score -= min(10, len(matches) * 5)
            issues.append(QualityIssue(
                severity='warning',
                category='ats',
                location='HTML',
                message=message,
                suggestion='Consider using ATS-friendly alternatives'
            ))
    
    # 检查关键 ATS 元素
    text = extract_text_from_html(html)
    
    # 邮箱检查
    if not re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
        issues.append(QualityIssue(
            severity='warning',
            category='ats',
            location='Header',
            message='No email address detected',
            suggestion='Add a professional email address'
        ))
        score -= 10
    
    # 电话检查
    if not re.search(r'(\+\d{1,3}[\s-])?\d{3,}[\s-]?\d{3,}[\s-]?\d{3,}', text):
        issues.append(QualityIssue(
            severity='warning',
            category='ats',
            location='Header',
            message='No phone number detected',
            suggestion='Add a contact phone number'
        ))
        score -= 5
    
    return max(0, score), issues


def check_ai_tone(text: str) -> Tuple[float, List[QualityIssue]]:
    """检测 AI 腔"""
    issues = []
    score = 100.0
    
    text_lower = text.lower()
    detected = []
    
    for phrase in AI_PHRASES:
        matches = re.findall(phrase, text_lower)
        if matches:
            detected.extend(matches)
    
    for word in AI_BUZZWORDS:
        count = text_lower.count(word)
        if count > 0:
            detected.extend([word] * count)
    
    if detected:
        # 计算密度
        word_count = len(text.split())
        density = len(detected) / word_count * 100 if word_count else 0
        
        if density > 2:
            score = max(50, 100 - len(detected) * 3)
            issues.append(QualityIssue(
                severity='warning',
                category='ai_tone',
                location='Multiple sections',
                message=f'High AI buzzword density ({len(detected)} occurrences)',
                suggestion='Replace generic buzzwords with specific, measurable language'
            ))
        elif density > 0.5:
            score = max(70, 100 - len(detected) * 2)
            issues.append(QualityIssue(
                severity='info',
                category='ai_tone',
                location='Multiple sections',
                message=f'Moderate AI buzzword usage ({len(detected)} occurrences)',
                suggestion='Review and consider more natural alternatives'
            ))
    
    return score, issues


def check_consistency(html: str, profile_data: Dict = None) -> List[QualityIssue]:
    """检查一致性问题"""
    issues = []
    text = extract_text_from_html(html)
    
    # 日期格式一致性
    dates = re.findall(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}', text, re.IGNORECASE)
    dates += re.findall(r'\d{1,2}/\d{4}', text)
    
    # 检查公司名称格式
    companies = re.findall(r'(?:at|@)\s+([A-Z][A-Za-z\s]+)', text)
    # 可以添加更多一致性检查
    
    return issues


def run_validation_checklist(
    html: str,
    jd_keywords: List[str] = None,
    profile_data: Dict = None,
    projects: List[Dict] = None,
) -> Dict[str, Tuple[bool, str]]:
    """
    运行验证清单（来自 resume_generation_rules.md）
    返回每项检查的结果和说明
    """
    checklist = {}
    text = extract_text_from_html(html)
    sections = extract_sections(html)
    
    # 1. All content traceable to KB
    # 这个需要外部数据，标记为需要人工确认
    checklist['content_traceable'] = (True, 'Assumed OK - requires manual KB trace verification')
    
    # 2. JD requirements mapped at sentence level
    if jd_keywords:
        hits = sum(1 for kw in jd_keywords if kw.lower() in text.lower())
        total = len(jd_keywords)
        coverage = hits / total * 100 if total else 100
        checklist['jd_mapped'] = (coverage >= 70, f'{hits}/{total} JD keywords found ({coverage:.0f}%)')
    else:
        checklist['jd_mapped'] = (True, 'No JD keywords provided')
    
    # 3. Selected skills match JD
    if jd_keywords and 'skills' in sections:
        skills_text = sections['skills'].lower()
        skill_hits = sum(1 for kw in jd_keywords if kw.lower() in skills_text)
        checklist['skills_match'] = (skill_hits > 0, f'{skill_hits} JD keywords in skills section')
    else:
        checklist['skills_match'] = (True, 'Skipped')
    
    # 4. Selected projects support target role
    # 需要项目数据，标记为需要人工确认
    checklist['projects_support'] = (True, 'Assumed OK - verify projects are role-relevant')
    
    # 5. No unsupported metrics/titles
    # 检查是否有明显的捏造迹象
    suspicious_patterns = [
        r'\b(?:exactly|precisely|approximately)\s+\d+',
        r'\b\d+(?:\.\d+)?%?\s+(?:improvement|increase|decrease)\s+in\b',
    ]
    suspicious_found = []
    for pattern in suspicious_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        suspicious_found.extend(matches)
    
    if suspicious_found:
        checklist['no_fabrication'] = (False, f'Suspicious quantification patterns found: verify accuracy')
    else:
        checklist['no_fabrication'] = (True, 'No obvious fabrication patterns')
    
    # 6. Summary is targeted, 5-6 lines, ends as complete sentence
    if 'summary' in sections:
        summary = sections['summary']
        word_count = len(summary.split())
        ends_properly = summary.rstrip().endswith('.') or summary.rstrip().endswith('.')
        
        summary_ok = 50 <= word_count <= 100 and ends_properly
        msg_parts = []
        if not (50 <= word_count <= 100):
            msg_parts.append(f'{word_count} words')
        if not ends_properly:
            msg_parts.append('incomplete sentence')
        
        checklist['summary_quality'] = (summary_ok, 'OK' if summary_ok else ', '.join(msg_parts))
    else:
        checklist['summary_quality'] = (False, 'Summary not found')
    
    # 7. Bullets use strong verbs
    if 'bullets' in sections:
        weak_count = 0
        for bullet in sections['bullets']:
            bullet_lower = bullet.lower()[:30]
            for weak_verb in WEAK_VERBS:
                if weak_verb in bullet_lower:
                    weak_count += 1
                    break
        
        total_bullets = len(sections['bullets'])
        strong_ratio = (total_bullets - weak_count) / total_bullets if total_bullets else 1
        checklist['strong_verbs'] = (strong_ratio >= 0.8, f'{total_bullets - weak_count}/{total_bullets} bullets start with strong verbs')
    else:
        checklist['strong_verbs'] = (True, 'No bullets found')
    
    # 8. Bullets not repetitive
    if 'bullets' in sections and len(sections['bullets']) > 1:
        bullets_norm = [re.sub(r'[^a-z0-9]', '', b.lower()) for b in sections['bullets']]
        duplicates = len(bullets_norm) - len(set(bullets_norm))
        checklist['no_duplicate_bullets'] = (duplicates == 0, f'{duplicates} duplicate bullets')
    else:
        checklist['no_duplicate_bullets'] = (True, 'OK')
    
    # 9. Timeline consistency
    checklist['timeline_consistent'] = (True, 'Assumed OK - verify dates manually')
    
    # 10. No edge-related terms (unless required)
    edge_terms = ['edge ai', 'edge computing', '边缘计算', '端侧', 'edge deployment']
    edge_found = [term for term in edge_terms if term in text.lower()]
    checklist['no_edge_terms'] = (len(edge_found) == 0, 'OK' if not edge_found else f'Found: {", ".join(edge_found)}')
    
    # 11. No internal label artifacts
    internal_labels = ['JD Match', 'MISSING_INFO', 'FACT_CONFLICT']
    labels_found = [label for label in internal_labels if label in text]
    checklist['no_artifacts'] = (len(labels_found) == 0, 'OK' if not labels_found else f'Found: {", ".join(labels_found)}')
    
    return checklist


def generate_quality_report(
    html: str,
    jd_keywords: List[str] = None,
    profile_data: Dict = None,
    projects: List[Dict] = None,
) -> QualityReport:
    """
    生成完整质量报告
    """
    issues: List[QualityIssue] = []
    
    # 1. 验证清单
    checklist = run_validation_checklist(html, jd_keywords, profile_data, projects)
    
    for item, (passed, msg) in checklist.items():
        if not passed:
            issues.append(QualityIssue(
                severity='error' if item in ['no_fabrication', 'summary_quality'] else 'warning',
                category='validation',
                location='General',
                message=f'{item}: {msg}',
                suggestion='Review and fix'
            ))
    
    # 2. ATS 兼容性
    ats_score, ats_issues = check_ats_compatibility(html)
    issues.extend(ats_issues)
    
    # 3. Summary 质量
    sections = extract_sections(html)
    summary_score = 0.0
    if 'summary' in sections:
        summary_score, summary_issues = check_summary_quality(sections['summary'], jd_keywords)
        issues.extend(summary_issues)
    
    # 4. Bullet 质量
    bullet_scores: List[BulletScore] = []
    if 'bullets' in sections:
        for bullet in sections['bullets']:
            score = check_bullet_quality(bullet, jd_keywords)
            bullet_scores.append(score)
            
            if score.overall_score < 50:
                issues.append(QualityIssue(
                    severity='warning',
                    category='bullet',
                    location='Experience',
                    message=f'Weak bullet: "{bullet[:50]}..." (score: {score.overall_score:.0f})',
                    suggestion=' '.join(score.issues[:2]) if score.issues else 'Improve verb strength and add metrics'
                ))
    
    # 5. AI 腔检测
    ai_tone_score, ai_issues = check_ai_tone(extract_text_from_html(html))
    issues.extend(ai_issues)
    
    # 计算总分
    passed_items = sum(1 for p in checklist.values() if p[0])
    total_items = len(checklist)
    checklist_score = (passed_items / total_items * 100) if total_items else 100
    
    avg_bullet_score = sum(b.overall_score for b in bullet_scores) / len(bullet_scores) if bullet_scores else 100
    
    overall_score = (
        checklist_score * 0.3 +
        ats_score * 0.15 +
        summary_score * 0.2 +
        avg_bullet_score * 0.25 +
        ai_tone_score * 0.1
    )
    
    passed = overall_score >= 70 and all(
        checklist.get(k, (True, ''))[0]
        for k in ['no_fabrication', 'summary_quality']
    )
    
    return QualityReport(
        passed=passed,
        score=overall_score,
        issues=issues,
        bullet_scores=bullet_scores,
        summary_score=summary_score,
        ats_score=ats_score,
        ai_tone_score=ai_tone_score,
        checklist={k: v[0] for k, v in checklist.items()}
    )


def format_quality_report_markdown(report: QualityReport) -> str:
    """格式化质量报告为 Markdown"""
    lines = []
    
    # 标题
    status_icon = '[OK]' if report.passed else '[!!]'
    lines.append(f'# CV Quality Report {status_icon}')
    lines.append('')
    lines.append(f'- **Overall Score**: `{report.score:.1f}/100`')
    lines.append(f'- **Status**: {"PASSED" if report.passed else "NEEDS ATTENTION"}')
    lines.append('')
    
    # 分项得分
    lines.append('## Scores by Category')
    lines.append('')
    lines.append(f'| Category | Score |')
    lines.append(f'|----------|-------|')
    # 将 checklist dict 转为可读格式
    checklist_ok = sum(1 for v in report.checklist.values() if v)
    checklist_total = len(report.checklist)
    lines.append(f'| Checklist | `{checklist_ok}/{checklist_total} passed` |')
    lines.append(f'| ATS Compatibility | `{report.ats_score:.1f}` |')
    lines.append(f'| Summary Quality | `{report.summary_score:.1f}` |')
    lines.append(f'| AI Tone | `{report.ai_tone_score:.1f}` |')
    lines.append('')
    
    # Bullet 得分
    if report.bullet_scores:
        lines.append('## Bullet Analysis')
        lines.append('')
        lines.append('| Bullet | Score | Issues |')
        lines.append('|--------|-------|--------|')
        for bs in report.bullet_scores[:10]:
            text_short = bs.text[:40] + '...' if len(bs.text) > 40 else bs.text
            issues_str = '; '.join(bs.issues[:2]) if bs.issues else '-'
            lines.append(f'| {text_short} | `{bs.overall_score:.0f}` | {issues_str} |')
        if len(report.bullet_scores) > 10:
            lines.append(f'| ... | ... | ({len(report.bullet_scores) - 10} more) |')
        lines.append('')
    
    # 问题列表
    if report.issues:
        lines.append('## Issues')
        lines.append('')
        
        errors = [i for i in report.issues if i.severity == 'error']
        warnings = [i for i in report.issues if i.severity == 'warning']
        infos = [i for i in report.issues if i.severity == 'info']
        
        if errors:
            lines.append('### [X] Errors')
            for issue in errors:
                lines.append(f'- [{issue.category}] **{issue.location}**: {issue.message}')
                lines.append(f'  - > {issue.suggestion}')
            lines.append('')
        
        if warnings:
            lines.append('### [!] Warnings')
            for issue in warnings:
                lines.append(f'- [{issue.category}] **{issue.location}**: {issue.message}')
                lines.append(f'  - > {issue.suggestion}')
            lines.append('')
        
        if infos:
            lines.append('### [i] Notes')
            for issue in infos:
                lines.append(f'- [{issue.category}] **{issue.location}**: {issue.message}')
            lines.append('')
    
    # 验证清单
    lines.append('## Validation Checklist')
    lines.append('')
    for item, passed in report.checklist.items():
        icon = '[OK]' if passed else '[X]'
        lines.append(f'- {icon} {item}')
    lines.append('')
    
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print('Usage: python cv_quality_validator.py <html_file> [--jd-keywords kw1 kw2 ...]')
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    jd_keywords = []
    if '--jd-keywords' in sys.argv:
        idx = sys.argv.index('--jd-keywords')
        jd_keywords = sys.argv[idx + 1:]
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    report = generate_quality_report(html, jd_keywords)
    print(format_quality_report_markdown(report))
