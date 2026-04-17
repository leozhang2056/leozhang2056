# 分层记忆系统（Layered Memory）

本目录用于让 AI 在每次会话重载后，快速进入最佳状态，避免反复全仓扫描。

## 设计目标
- 启动阶段只读取最小必要信息，30 秒内进入可执行状态。
- 任务阶段读取当前上下文和待办，保证跨会话连续性。
- 深度阶段按需下钻详细规则，避免每次都加载长文档。

## 三层结构
- `L0 启动层`：`memory/L0_BOOTSTRAP.md`
  - 仅保留关键事实、关键入口、固定启动流程。
  - 推荐作为每次新会话第一读取文件。
- `L1 工作层`：`memory/L1_SESSION_STATE.md`
  - 记录当前目标、进度、阻塞、下一步。
  - 每次任务结束后更新，作为会话接力点。
- `L2 深度层`：`memory/L2_DEEP_INDEX.md`
  - 只做“索引与跳转”，不重复正文。
  - 按任务类型指向 `AGENTS.md`、`.cursorrules`、`kb/*` 等详细来源。

## 会话启动协议（建议固化）
1. 读取 `memory/L0_BOOTSTRAP.md`。
2. 读取 `memory/L1_SESSION_STATE.md`。
3. 如需执行具体任务，再根据 `memory/L2_DEEP_INDEX.md` 跳转加载详细文档。

## 每日归并进化（已自动化）
- `sessionEnd` 会自动写入：
  - `memory/L1_SESSION_STATE.md`（会话工作记忆）
  - `memory/L1_LEARNING_QUEUE.md`（学习候选队列）
- 每天第一次 `sessionEnd` 会执行一次“每日归并”：
  - 从学习队列中提取当日新增经验
  - 同类项当日出现次数 `>=3` 时提升到 `memory/L2_EVOLVED_RULES.md`
  - 提升项会附带 `impact/confidence/frequency` 与验证命令绑定
  - 状态记录在 `memory/.daily_merge_state.json`，避免同一天重复归并

## 质量与演进闭环（已自动化）
- 质量闸门：每次会话结束检查 `goal/next_action/improvements`，缺失会记录 `QUALITY_FAIL`。
- 失败案例库：`memory/FAILURE_PATTERNS.md` 自动记录回归模式（触发条件/正确做法/检查点）。
- 周度压缩：每周自动生成 `memory/WEEKLY_LEARNINGS.md`，提炼 Top 高频经验防止记忆膨胀。

## 维护原则
- 单一事实源：同一事实只在一个文件完整维护，其他文件仅引用路径。
- 低耦合：L0 不放长规则，L1 不放架构细节，L2 不复制内容。
- 可审计：L1 中记录“最近变更文件”和“验证命令”。
