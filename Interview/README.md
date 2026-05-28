# 常见面试题与回答 (Interview Q&A)

本文件夹存放面试复习资料。事实仍以 `kb/*.yaml` 和 `projects/*/facts.yaml` 为准；这里的 Markdown/YAML 是口语练习、索引和复习材料。

## 当前真源

- **行为面试完整口稿**：`behavioral_common_qa.md`。这是 STAR、Q1-Q45、追问、速查和素材收件箱的主文件。
- **结构化 YAML**：`technical.yaml`、`behavioral.yaml`、`role_specific.yaml`。这些用于 `python generate.py interview ...` 的快速列表/搜索，属于紧凑索引，不应覆盖完整口稿。
- **历史备份**：`qa_backup.md`。只用于回看旧版本，不作为并行维护源。

## 目录结构

| 文件 | 说明 |
|------|------|
| `interview_guide.md` | 面试流程指南：按开场、技术、行为、协作、学习、领导力拆分的快速准备清单 |
| `AUT_NZ_career_resources.md` | AUT 职业资源与新西兰招聘周期指南（面试准备与时间节点） |
| `index.yaml` | 库索引、使用指南、STAR 方法、准备清单 |
| `behavioral_common_qa.md` | 行为面试完整口稿：Part 1 高频主答、Part 2 故事索引、Part 3 Q1-Q45、Part 4 速查与素材草稿 |
| `technical.yaml` | 通用技术面试：自我介绍、职业转型、项目深挖、系统设计、AI/ML 等 |
| `behavioral.yaml` | 行为面试结构化索引（STAR 要点），用于 CLI 搜索；完整口语稿见 `behavioral_common_qa.md` |
| `role_specific.yaml` | 岗位特定：Android、Backend、AI/ML、IoT、Leadership、公司研究 |
| `qa_backup.md` | 旧快照，仅备份 |

## 问题条目格式（供新增/编辑参考）

每个问题建议包含：

- **id**: 唯一标识，如 `android_offline_sync`
- **question**: 英文或中文问题原文
- **answer_points**: 回答要点列表（必填）
- **evidence**: 引用的项目证据，格式为 `project: <project_id>`，可带 `highlight` / `metrics`
- **star_method**:（行为题可选）Situation / Task / Action / Result
- **tips**: 回答技巧
- **category** / **difficulty**:（technical/behavioral 中）分类与难度

**约束**：所有 evidence 必须对应 `projects/<id>/facts.yaml` 或 `kb/` 中已有内容，不得编造。

## 如何使用

- **面试前**：根据目标岗位打开对应文件，按 `index.yaml` 的 preparation_checklist 复习。
- **命令行**：在仓库根目录执行  
  `python generate.py interview --category technical`  
  或 `python generate.py interview --role android`  
  可按类别/岗位列出问题，支持关键词搜索。

## 维护

- 行为面试的新故事/新复盘先追加到 `behavioral_common_qa.md` 的 Appendix 收件箱；整理成熟后再同步到 Part 1 / Part 2 / Part 3。
- CLI 需要检索的问题可补充进对应 YAML，并补上 answer_points 与 evidence；不要把 YAML 当成完整口稿真源。
- 修改后无需运行校验脚本；如需与 facts 一致性检查，可后续在 CI 中加一步。
