# L1 学习队列（自动累计）

> 来源：每次 `sessionEnd` hook 自动追加。
> 作用：沉淀用户偏好、常见错误、改进建议，形成“越用越智能”的训练轨迹。

## Promote Rule
- 同类偏好/修正连续出现 >= 3 次，升级到长期规则（`L0_BOOTSTRAP.md` 或 `L2_DEEP_INDEX.md` 指向的规则文件）。
- 升级后在此记录“已提升到规则层”的时间戳，避免重复处理。

## Daily Merge
- 每天第一次会话结束时自动归并一次（由 `sessionEnd` hook 触发）。
- 归并结果输出到 `memory/L2_EVOLVED_RULES.md`。
- 归并游标状态记录在 `memory/.daily_merge_state.json`。

## Scoring + Verification
- 归并时会给每条提升项打分：`impact`、`confidence`、`frequency`。
- 每条提升项自动绑定验证命令（`validate.py` / `pytest` / 两者组合）。

## Learning Candidate - 2026-04-17 16:11:57
- Preferences:
  - （未提供）
- Mistakes/Regressions:
  - （未提供）
- Improvement Proposals:
  - （未提供）
- Promote Policy:
  - 若同类偏好连续出现 >= 3 次，提升到 L0/L2 规则层。

## Learning Candidate - 2026-04-17 16:12:10
- Preferences:
  - （未提供）
- Mistakes/Regressions:
  - （未提供）
- Improvement Proposals:
  - （未提供）
- Promote Policy:
  - 若同类偏好连续出现 >= 3 次，提升到 L0/L2 规则层。

## Learning Candidate - 2026-04-17 17:03:38
- Preferences:
  - （未提供）
- Mistakes/Regressions:
  - （未提供）
- Improvement Proposals:
  - （未提供）
- Promote Policy:
  - 若同类偏好连续出现 >= 3 次，提升到 L0/L2 规则层。

## Learning Candidate - 2026-04-17 Resume Tuning (EROAD)
- Preferences:
  - Summary 只讲重点与 JD 匹配，不复述下方 Key Skills / Experience 的已展示内容。
  - Key Skills 以“单行可读”为先：避免自动换行；必要时缩短词面（如 LLM FT、CI/CD），但不牺牲关键信息。
  - 对 fullstack 过滤基础项：去掉 IIS、Windows Server、以及含 Administration 的词。
  - AI 技能默认拆成两行（AI / ML + AI-Assisted Development），避免长行换行导致版面难看。
  - 数据库在 fullstack 必须保留且覆盖全面（MySQL/Redis/MongoDB/SQL Server/SQLite）。
  - 用户要求“加两行”时，优先补充量化结果与岗位匹配语句，不写空泛措辞。
- Mistakes/Regressions:
  - 曾出现“加内容但视觉上不变”，原因是 Summary 有长度预算导致被截断。
  - 曾因过度合并技能导致换行与信息损失。
- Improvement Proposals:
  - fullstack 英文 Summary 使用放宽预算，避免用户追加内容被静默裁剪。
  - 每次改动后都优先检查 Key Skills 的可视换行风险，再做词长微调。
  - 默认以“最小改动”进行排版修复（一次只减 1 个词或 1 项）。
- Promote Policy:
  - 若后续 2 次以上简历会话重复这些偏好，提升为长期规则并写入规则层文件。
