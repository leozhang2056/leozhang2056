# Weekly Learnings

> 每周压缩高价值经验，防止记忆膨胀。
> 由 `sessionEnd` hook 自动更新。

## 2026-W16
- Source lines: 27
- Top learnings:
  - [1x] 升级后在此记录“已提升到规则层”的时间戳,避免重复处理.
  - [1x] 同类偏好/修正连续出现 >= 3 次,升级到长期规则（`l0_bootstrap.md` 或 `l2_deep_index.md` 指向的规则文件）.
  - [1x] 归并时会给每条提升项打分：`impact`、`confidence`、`frequency`.
  - [1x] 归并游标状态记录在 `memory/.daily_merge_state.json`.
  - [1x] 归并结果输出到 `memory/l2_evolved_rules.md`.
  - [1x] 每天第一次会话结束时自动归并一次（由 `sessionend` hook 触发）.
  - [1x] 每条提升项自动绑定验证命令（`validate.py` / `pytest` / 两者组合）.
