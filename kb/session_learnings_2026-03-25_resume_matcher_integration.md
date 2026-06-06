# Session Learnings (2026-03-25)
# Resume-Matcher 能力整合沉淀

## 本次整合目标
将 `Resume-Matcher` 中“可复用且对本项目收益最高”的能力映射到当前 Career KB 体系，优先做本地优先、可验证、可维护的落地，而不是引入额外复杂前后端系统。

## 已整合能力（可直接使用）
- 主简历 + JD 定制流程：继续以 `kb/` 作为 master resume 数据源。
- JD 匹配可视化：按需使用 `python generate.py cv --with-jd-annotated` 输出 `*_JD_Annotated.pdf`（命中高亮 + hit/miss + match score）。
- 主简历默认不再生成标注 PDF；终端仍会输出 JD 覆盖率，并对 KB 支持词默认以 **≥85%** 为目标（可在 Summary 末尾自动补一行对齐词，仍遵守反幻觉）。
- 反幻觉关键词门控：JD 词先过 KB 证据过滤，再参与排序和生成。
- 求职信生成：沿用同一证据链，保证与简历一致。
- 申请邮件生成（新增）：`generate.py email` 输出可直接发送的邮件文本。

## 本次会话新增固化（ANZ/纽航阶段）
- JD 处理从“关键词匹配”升级为“逐句要求映射”：
  - 职责 / must-have / preferred 都要有落点，不可只看命中率。
- 输出质量红线：
  - 不允许截断句（例如 `Designed and de.` 这类半句）。
  - 不允许机械化拼接尾句（例如生硬关键词尾巴）影响可读性。
- 默认输出策略调整：
  - 保留主 PDF；
  - 不默认生成/保留 `.md` 旁路文件；
  - 仅在显式参数下才生成 second-AI review bundle。
- 公司背景先行：
  - 先读公司业务语境与文化，再写“投其所好”版本。
  - 对金融/支付类岗位优先强调：可靠性、测试纪律、安全与生产变更支持。

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
