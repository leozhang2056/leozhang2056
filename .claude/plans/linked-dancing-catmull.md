# Plan: 重新组织 CV/CL 生成规则

## Context

CV 和 CL 生成系统经过多轮迭代，存在以下核心问题：
1. **CV JD 覆盖率修复被禁用** — `_ensure_min_jd_keyword_coverage_html()` 是空函数，导致覆盖率永远不达标
2. **CL 缺乏质量验证** — 没有字数、语气、JD 对齐检查
3. **CL generic 模板公式化** — 4 段固定结构，JD 关键词集成浅层
4. **大量死代码** — 未使用的 hooks、重复的 summary 执行、空函数
5. **规则分散** — `resume_output.md` 定义了规则但没有被代码强制执行

---

## Phase 1: 修复损坏代码（高影响，低风险）

### 1.1 实现 JD 覆盖率修复
**文件**: `app/backend/generate_cv_from_kb.py` line 4238
- 当前: 返回 HTML 不变
- 改为: 当覆盖率 < 目标时，对 Experience bullets 做定向修改
  - 找到缺失的 JD 关键词
  - 对最相关的 bullet 做自然语言改写，融入缺失词
  - 上限 3 个词，避免不自然
  - 修改后重新运行 fluency 检查确保不降分

### 1.2 删除死代码 `_apply_jd_sentence1_alignment()`
**文件**: `app/backend/generate_cv_from_kb.py` lines 1514-1527
- 删除整个 `if normed_kws:` 块（调用空函数 + 冗余 summary 执行）
- 删除函数定义 (line 733-744)

### 1.3 删除重复 summary 执行
**文件**: `app/backend/generate_cv_from_kb.py` line 1511
- 删除第二次 `_enforce_summary_five_sentences()` 调用

### 1.4 启用 CL 未使用的 hooks
**文件**: `app/backend/generate_cover_letter.py` generic template
- 在 body1 段落：优先用 `_WHY_ME_HOOKS[company]`（如匹配），否则用 `_differentiator_hook(role_type)` 替代固定 `_SOFT_SKILLS`
- 不影响已有的公司专属模板（它们在 else 分支之前已 return）

---

## Phase 2: CL 质量验证（新功能）

### 2.1 创建 `app/backend/cl_quality_validator.py`
新建 ~150 行，参照 `cv_post_generation_check.py` 模式：
- 字数检查: 250-400 词
- 段落数: 3-5 段
- 语气检查: AI buzzwords 检测
- JD 关键词出现率: 报告型（不阻断生成）
- 输出 `*_CL_CHECK.md`

### 2.2 集成到 CL 生成流程
**文件**: `app/backend/generate_cover_letter.py` line ~1280
- PDF 生成前调用 `run_cl_quality_check()`
- 打印摘要到 stdout
- 可选写 `*_CL_CHECK.md`
- 不阻断生成（advisory）

### 2.3 添加 CL 测试
**新文件**: `tests/test_cover_letter.py`
- generic 模板输出 4 段
- 公司专属模板跳过 generic
- 字数在 250-400 范围
- JD 关键词出现在输出中
- 不同 role_type 都能正常输出

---

## Phase 3: CL Generic 模板改进

### 3.1 改进 JD 关键词集成（body2）
**文件**: `app/backend/generate_cover_letter.py` lines 999-1052
- 当前: "Your JD highlights X, Y, Z" 列表式
- 改为: 每个关键词关联一个具体项目经验，写成叙事句
- 例如: "Your need for React and TypeScript maps to my work on [project], where I built [outcome]"

### 3.2 改进 opening 段落
**文件**: `app/backend/generate_cover_letter.py` lines 948-959
- 当前: "{tagline}, I am drawn to {company} because..."
- 改为: 先直接点明申请意图，再接文化契合和背景

---

## Phase 4: 规则整合（可维护性）

### 4.1 创建 `app/backend/generation_rules.py`
新建 ~100 行，从 `resume_output.md` 提取可执行常量：
- Summary 规则: 句数、长度、禁止词
- Bullet 规则: 强动词、禁止短语、去重
- CL 规则: 字数、段落、语气
- 供 CV 和 CL 生成器共同 import

### 4.2 重构 CV post-check 使用共享规则
**文件**: `app/backend/cv_post_generation_check.py`
- 替换内联的 `TEMPLATE_TONE_PATTERNS` 为 import from `generation_rules.py`

### 4.3 重构 CL validator 使用共享规则
**文件**: `app/backend/cl_quality_validator.py`
- import from `generation_rules.py`

---

## 关键文件清单

| 文件 | 改动类型 |
|------|----------|
| `app/backend/generate_cv_from_kb.py` | 修复 3 个损坏函数，删除死代码 |
| `app/backend/generate_cover_letter.py` | 启用 hooks，改进 generic 模板 |
| `app/backend/cl_quality_validator.py` | 新建 CL 质量验证器 |
| `app/backend/generation_rules.py` | 新建共享规则常量 |
| `app/backend/cv_post_generation_check.py` | 重构使用共享规则 |
| `tests/test_cover_letter.py` | 新建 CL 测试 |
| `kb/rules/resume_output.md` | 不改动（作为权威规则源） |

## 验证方式

1. 重新生成今天 3 个职位的 CV + CL，对比 JD 覆盖率是否提升
2. 检查 CL 字数、段落结构是否合理
3. 运行 `python -m pytest tests/ -v` 确保无回归
4. 检查 CL 输出不再有公式化套话
