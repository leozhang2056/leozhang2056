# Session Learnings (2026-03-25)
# Resume-Matcher 能力整合沉淀

## 本次整合目标
将 `Resume-Matcher` 中“可复用且对本项目收益最高”的能力映射到当前 Career KB 体系，优先做本地优先、可验证、可维护的落地，而不是引入额外复杂前后端系统。

## 已整合能力（可直接使用）
- 主简历 + JD 定制流程：继续以 `kb/` 作为 master resume 数据源。
- JD 匹配可视化：默认输出 `*_JD_Annotated.pdf`（命中高亮 + hit/miss + match score）。
- 反幻觉关键词门控：JD 词先过 KB 证据过滤，再参与排序和生成。
- 求职信生成：沿用同一证据链，保证与简历一致。
- 申请邮件生成（新增）：`generate.py email` 输出可直接发送的邮件文本。

## 新增工作流命令
```bash
# 申请邮件（英文）
python generate.py email --role backend --company "Datacom" --title "Senior Backend Engineer"

# 申请邮件（自动识别角色 + 从 JD 页面抽词）
python generate.py email --role auto --jd-url "<job-url>" --company "Air New Zealand" --title "Software Engineer"
```

## 设计取舍（为何这样整合）
- 不直接搬运 Resume-Matcher 的完整 Web 架构：当前仓库核心是“个人职业 KB + 生成引擎”，CLI 更轻量、可控。
- 优先整合“结果质量相关能力”：
  - JD 证据匹配
  - 命中可解释性
  - 同源内容多文档输出（CV / Cover Letter / Email）
- 避免引入不可控依赖和额外运维成本。

## 后续可继续整合的方向
- 细化“多 JD 对比评分”报告：增加按职责维度（must-have / preferred）的分层覆盖率。
- 增加“关键词差距建议”文本：给出可补强的项目/技能证据点。
- 增加邮件模板变体（冷启动投递 / 内推跟进 / 面试后跟进）。
