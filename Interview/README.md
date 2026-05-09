# 常见面试题与回答 (Interview Q&A)

本文件夹**专门存放常见面试题及回答**，采用结构化 YAML，与仓库内 `kb/`、`projects/` 中的事实一致，便于面试前复习和回答时引用项目证据。

## 目录结构

| 文件 | 说明 |
|------|------|
| `index.yaml` | 库索引、使用指南、STAR 方法、准备清单 |
| `technical.yaml` | 通用技术面试：自我介绍、职业转型、项目深挖、系统设计、AI/ML 等 |
| `behavioral.yaml` | 行为面试（STAR）：优势/劣势、失败、冲突、抗压、主动性等 |
| `role_specific.yaml` | 岗位特定：Android、Backend、AI/ML、IoT、Leadership、公司研究 |

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

- 面试后可将新被问到的问题补充进对应 yaml，并补上 answer_points 与 evidence。
- 修改后无需运行校验脚本；如需与 facts 一致性检查，可后续在 CI 中加一步。
