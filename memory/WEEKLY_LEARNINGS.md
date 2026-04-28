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

## 2026-W17
- Source lines: 75
- Top learnings:
  - [1x] ai 技能默认拆成两行（ai / ml + ai-assisted development）,避免长行换行导致版面难看.
  - [1x] fullstack 英文 summary 使用放宽预算,避免用户追加内容被静默裁剪.
  - [1x] key skills 以“单行可读”为先：避免自动换行；必要时缩短词面（如 llm ft、ci/cd）,但不牺牲关键信息.
  - [1x] summary 只讲重点与 jd 匹配,不复述下方 key skills / experience 的已展示内容.
  - [1x] 升级后在此记录“已提升到规则层”的时间戳,避免重复处理.
  - [1x] 同类偏好/修正连续出现 >= 3 次,升级到长期规则（`l0_bootstrap.md` 或 `l2_deep_index.md` 指向的规则文件）.
  - [1x] 对 fullstack 过滤基础项：去掉 iis、windows server、以及含 administration 的词.
  - [1x] 归并时会给每条提升项打分：`impact`、`confidence`、`frequency`.
  - [1x] 归并游标状态记录在 `memory/.daily_merge_state.json`.
  - [1x] 归并结果输出到 `memory/l2_evolved_rules.md`.
  - [1x] 数据库在 fullstack 必须保留且覆盖全面（mysql/redis/mongodb/sql server/sqlite）.
  - [1x] 曾出现“加内容但视觉上不变”,原因是 summary 有长度预算导致被截断.
  - [1x] 曾因过度合并技能导致换行与信息损失.
  - [1x] 每天第一次会话结束时自动归并一次（由 `sessionend` hook 触发）.
  - [1x] 每条提升项自动绑定验证命令（`validate.py` / `pytest` / 两者组合）.
  - [1x] 每次改动后都优先检查 key skills 的可视换行风险,再做词长微调.
  - [1x] 用户要求“加两行”时,优先补充量化结果与岗位匹配语句,不写空泛措辞.
  - [1x] 若后续 2 次以上简历会话重复这些偏好,提升为长期规则并写入规则层文件.
  - [1x] 默认以“最小改动”进行排版修复（一次只减 1 个词或 1 项）.
