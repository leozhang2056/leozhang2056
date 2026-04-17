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
