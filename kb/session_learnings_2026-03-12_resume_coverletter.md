# Session Learnings (2026-03-12)
# 简历与求职信会话沉淀

## 目标
将本次高频偏好固化为项目默认行为，减少重复指令，提升后续生成质量与一致性。

## 已固化的关键偏好（Resume）
- 依据 JD 自动选择角色（android / backend / ai / fullstack），但在 JD 噪声大时可由标题/人工关键词兜底。
- 输出文件名带公司名。
- 简历输出后删除中间 HTML，仅保留 PDF。
- Summary：
  - 4-5 行，必须完整收尾（避免残句、截断）。
  - 重点突出 JD 匹配，且自然融入，不使用 `Highlights:` 标签。
  - 开发岗强调“快速开发/快速迭代 + 强自我管理/ownership”。
  - 去除 edge/边缘相关表述（除非目标 JD 明确要求）。
- Skills：
  - 不出现 `JD Match` 这类实现标签。
  - Android 技能标签用 `Android`（非 `Android Development`）。
  - AI-Assisted Development 工具固定：
    `Cursor, GitHub Copilot, Claude Code, Antigravity, OpenCode`。
  - 版式尽量一行更均衡，必要时控制每行技能数量。
- Experience：
  - 至少 5 个项目。
  - 固定保留：`chatclothes`, `smart-factory`。
  - Android 场景优先加入：`forest-patrol-inspection`（离线地图/GIS匹配）。
  - 开发岗弱化“团队管理”措辞，强调技术交付与结果。
- Education：
  - `Auckland University of Technology` 保持全称（不缩写 AUT）。
  - 优化学校显示，减少尴尬断行。
- Publications：不展示。

## 已固化的关键偏好（Cover Letter）
- 根据岗位 technical requirements 定制，不泛化。
- 若页眉已有联系方式，结尾不重复电话/邮箱。
- 偏工程岗位时，突出：
  - 技术匹配（语言/框架/架构）
  - 快速执行与稳定交付
  - 自我管理与跨职能协作

## 抽词与噪声治理
- 增加职位页噪声词过滤（浏览器名、登录页词、分享弹窗词等）。
- 过滤 `edge/chrome/firefox/safari/...` 等非岗位能力关键词，避免污染 Summary/Skills。

## 维护约定
- 每次会话结束后，若出现“用户重复强调 >=2 次”的偏好，优先升级为默认规则或生成逻辑。
- 优先沉淀到 `kb/` 规则文档与 `.cursor/rules/`，再体现在代码实现中。
- 每次生成简历/求职信前，必须先提炼目标公司的业务与文化要点，并在正文中体现“公司贴合度”。
