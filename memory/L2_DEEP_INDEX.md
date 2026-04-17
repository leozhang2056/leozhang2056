# L2 深度索引（按需加载）

> 用途：提供“去哪读”的导航，不复制正文内容。

## 架构与命令
- `AGENTS.md`
  - 仓库定位、核心流程、关键命令
  - 适用场景：需要理解生成管线、命令入口、调试路径

## 全局事实与约束
- `.cursorrules`
  - 候选人关键事实、禁止事项、数据架构边界
  - 适用场景：涉及事实正确性、反幻觉约束、数据来源判定

## 简历生成专项规范
- `.cursor/rules/resume-generation-standards.mdc`
  - 输出顺序、内容优先级、布局/文案策略
  - 适用场景：CV 内容和版式调整

## 事实数据与配置
- `kb/profile.yaml`
- `kb/skills.yaml`
- `kb/achievements.yaml`
- `kb/project_relations.yaml`
- `projects/*/facts.yaml`
- `kb/generation_config.yaml`

## 验证与回归
- KB 验证：`python app/backend/validate.py`
- 测试回归：`pytest`

## 进化产物与复盘
- `memory/L2_EVOLVED_RULES.md`（每日提升规则，含评分与验证绑定）
- `memory/WEEKLY_LEARNINGS.md`（周度压缩）
- `memory/FAILURE_PATTERNS.md`（失败模式库）

## 建议读取策略
1. 默认只读 `L0 + L1`。
2. 任务触发后，从本索引挑 1-3 个最相关文件再加载。
3. 如果出现事实冲突，以 YAML 数据源为最终依据。
