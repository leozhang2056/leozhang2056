---
description: "Reflect on generation session, extract learnings, update rules — self-evolving quality loop"
---

# Evolve — 自主进化技能

每次 CV/CL 生成后执行，反思质量报告和会话反馈，将可复用的教训沉淀到规则文件中。

## 执行步骤

### Phase 1: 回顾 (Review)

收集本次会话中的所有信号：

```bash
# 1. 最新质量报告
ls -lt outputs/*/CV_*_QUALITY.md | head -3
cat "$(ls -t outputs/*/CV_*_QUALITY.md | head -1)"

# 2. Post-check 报告
cat "$(ls -t outputs/*/CV_*_POST_CHECK.md 2>/dev/null | head -1)"

# 3. 最近的 CL 生成
ls -lt outputs/*/CoverLetter_*.pdf | head -3
```

记录以下数据点：
- Overall quality score
- PASS / NEEDS ATTENTION status
- Summary quality score
- Fluency score
- JD coverage %
- All warning items and error items
- Duplicate bullets
- Weak bullets (score < 60)
- User 在会话中提出的具体修改要求和反馈

### Phase 2: 分析 (Analyze)

对照现有规则，逐项分析每个问题：

**问题分类：**
| 类别 | 含义 | 处理方式 |
|------|------|---------|
| 规则缺失 | 当前规则没覆盖的问题 | 新增规则 |
| 规则不足 | 有规则但约束不够强 | 升级为 hard constraint |
| 规则冲突 | 两条规则互相矛盾 | 选择更优的，删除另一条 |
| 执行偏差 | 规则存在但生成器没遵守 | 标记给生成器维护者 |
| 一次性问题 | 特定 JD 的特殊情况 | 不需要新规则 |

**关键检查点：**
- Summary 是否严格 5 句、≤ 100 词？
- Skills 分类数量是否 ≤ 6？（避免堆叠）
- 是否有重复 phrase（同一短语 ≥ 4 次）？
- 项目选择是否匹配 JD 技术栈？
- CL 是否与 CV 内容重复？
- CL 是否突出了软能力和个人价值？
- 用户在会话中明确纠正了什么？

### Phase 3: 对比 (Compare)

读取当前规则文件，确认哪些问题已有规则覆盖：

```bash
# 检查规则文件
cat kb/rules/resume_output.md
cat kb/rules/jd_analysis_standard.md
cat kb/cv_base_template.yaml | head -50  # summary 结构
```

生成对比矩阵：

| 问题 | 现有规则 | 规则强度 | 需要动作 |
|------|---------|---------|---------|
| Summary 超 100 词 | §3 五句结构 | soft | → 升级为 hard |
| Skills 类别过多 | 无 | — | → 新增规则 |
| CL 与 CV 重复 | §9 CL 规则 | 部分 | → 补充 |

### Phase 4: 决策 (Decide)

对每个需要动作的项，决定：

1. **写入哪个文件？**
   - 通用生成规则 → `kb/rules/resume_output.md`
   - JD 分析规则 → `kb/rules/jd_analysis_standard.md`
   - CL 特定规则 → `kb/rules/resume_output.md` §9
   - 模板结构问题 → `kb/cv_base_template.yaml`

2. **什么类型的更新？**
   - `ADD` — 新增规则段落
   - `UPGRADE` — 将 soft constraint 升级为 hard constraint
   - `REFINE` — 修改现有规则的措辞或参数
   - `DEPRECATE` — 废止过时的规则

3. **需要用户确认吗？**
   - 参数调整（如阈值变化）→ 直接应用
   - 结构性变更（如新增规则类别）→ 先展示，确认后写入

### Phase 5: 写入 (Apply)

执行规则更新。每次更新必须包含：

```markdown
<!-- EVOLVE: {date} | source: {session_summary} | issue: {what_failed} -->
```

更新后验证：
```bash
python -m pytest tests/ -v -k kb
```

### Phase 6: 记忆 (Log)

将本次进化记录写入 memory：

文件名: `evolve-{date}.md`
内容:
- 触发原因（哪个质量问题）
- 决策过程
- 写入的规则变更
- 验证结果

## 输出格式

完成后向用户展示：

```
🔬 Evolve — 本次进化总结

发现的问题: N 个
├── 规则缺失: X 个 → 已新增
├── 规则不足: Y 个 → 已升级
├── 一次性问题: Z 个 → 已忽略
└── 执行偏差: W 个 → 已标记

写入的变更:
├── resume_output.md: 新增 §X.Y ...
├── jd_analysis_standard.md: 升级 ...
└── cv_base_template.yaml: 修改 ...

下次生成预期改善: {具体描述}
```

## 使用时机

- CV/CL 质量分数 < 85 时自动建议执行
- 用户明确要求 "反思" / "进化" / "沉淀规则"
- 会话中用户多次纠正同一类问题
- 每 5 次生成后建议执行一次常规回顾
