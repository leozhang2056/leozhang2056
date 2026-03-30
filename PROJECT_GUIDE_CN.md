# Career KB & AI 简历生成器 — 项目说明（给人和 AI 看）

> 注意：本文件不是 README.md，用于**白板/项目内部说明**，帮助 Cursor、Claude、Copilot 等 AI 快速理解本项目结构与用途。

---

## 一、项目定位

本项目是一个 **个人作品集 + 职业知识库 + AI 简历生成系统**，目标是：

* 把我的项目、经历、技能、成果 **结构化存储** 为知识库（KB）
* 当出现新的招聘 JD 时，

    * 从 KB 中检索最相关的内容
    * 在**不新增事实**的前提下，自动生成一份**岗位定制简历**
* 同一份 KB 同时用于：

    * 作品集展示
    * 简历生成
    * Cover Letter / Profile 文案生成

核心理念：

> 把职业经历当作数据来管理，把简历当作软件来"编译"。

---

## 二、这个项目解决什么问题？

传统流程：

* 每来一个岗位 → 手动改一次简历
* 不同方向（Android / Backend / AI / QA）→ 多份简历来回维护
* 容易：

    * 忘了改某段
    * 内容前后不一致
    * 夸大或写错细节

本项目的目标流程：

1. 只维护一份 **结构化知识库（KB）**
2. 输入 JD + 目标岗位参数
3. 系统自动：

    * 检索最相关经历 / 项目 / 技能
    * 组装简历结构
    * 对 bullet points 做岗位对齐改写（不新增事实）
4. 输出：

    * 可投递的简历（Markdown / LaTeX / PDF / DOCX）
    * 可选 trace 文件（标注每条内容来自哪里）

---

## 三、仓库结构说明

项目采用 **"一个项目 = 一个文件夹"** 的结构，既适合作为作品集展示，也便于 AI 与生成系统按项目粒度检索与引用证据。

```
.
├── PROJECT_GUIDE_CN.md          # 本说明文件（项目白板说明）
├── README.md                    # 对外展示的简要说明
├── generate.py                  # 统一 CLI 入口（所有生成操作从这里调用）
├── requirements.txt             # Python 依赖
│
├── projects/                    # 17 个真实项目（作品集主体）
│   ├── chatclothes/             # AI 服装推荐 + IEEE 论文
│   ├── smart-factory/           # 工业 IoT + AI 预测
│   ├── enterprise-messaging/    # 企业即时通讯（Android + Java）
│   ├── broadcast-control/       # 电视台播出控制系统
│   ├── boobit/                  # ...
│   ├── broadcast-control/
│   ├── chinese-herbal-recognition/
│   ├── device-maintenance-prediction/
│   ├── exhibition-robot/
│   ├── forest-patrol-inspection/
│   ├── iot-solutions/
│   ├── live-streaming-system/
│   ├── patent-search-system/
│   ├── picture-book-locker/
│   ├── school-attendance/
│   ├── smart-power/
│   ├── visit-system/
│   └── visual-gateway/
│       ├── README.md            # 项目说明（给人和 AI 看）
│       ├── facts.yaml           # 结构化事实（给程序/RAG 用）
│       └── images/              # 架构图、结果图、截图等证据素材
│
├── kb/                          # 职业知识库（跨项目汇总层）
│   ├── profile.yaml             # 基本信息、Summary 变体、目标岗位
│   ├── skills.yaml              # 技能清单（分组/熟练度/证据）
│   ├── achievements.yaml        # 论文、奖项、证书（First Class Honours 等）
│   ├── project_relations.yaml   # 项目关联关系（叙事线索）
│   ├── resume_generation_rules.md  # 简历生成规则与约束
│   ├── ai_input_spec.md         # AI 输入规范
│   ├── generation_config.yaml    # 生成参数配置（角色推断关键词/项目排序权重）
│   ├── experience/              # 工作 / 研究经历（YAML）
│   ├── bullets/                 # 可复用要点库（按方向/岗位）
│   ├── schema/                  # 数据 Schema 定义
│   │   └── project_facts_schema.yaml
│   └── interview_qa/            # 面试问答库
│       ├── index.yaml           # 题目索引
│       ├── technical.yaml       # 技术题（要点）
│       ├── behavioral.yaml      # 行为题（要点）
│       ├── role_specific.yaml   # 岗位专项题（要点）
│       └── scripts.md           # 完整英文口语回答稿（33 题，可背诵）
│
├── app/                         # 简历生成系统
│   └── backend/
│       ├── generate_cv_from_kb.py      # 核心：从 KB 生成 Markdown 简历
│       ├── generate_cover_letter.py    # 求职信生成
│       ├── generate_cv_dynamic.py      # 动态简历生成
│       ├── generate_cv_html_to_pdf.py  # HTML→PDF 导出
│       ├── generate_cv_latex.py        # LaTeX 导出
│       ├── generate_cv_pdf.py          # PDF 导出
│       ├── kb_validation.py            # 统一验证逻辑（供 CLI 与 Loader 复用）
│       ├── validate.py                 # KB 数据验证（修改 facts.yaml 后必须运行）
│       ├── kb_query.py                 # KB 查询工具
│       ├── facts_normalizer.py         # 数据规范化（内部使用）
│       ├── interview_qa_cli.py         # 面试 Q&A 命令行工具
│       └── jd_fetch.py                 # JD 抓取工具
│
├── templates/                   # 简历 / 求职信模板
│   ├── resume_base.tex          # LaTeX 模板
│   └── coverletter_base.md      # 求职信模板
│
├── outputs/                     # 生成结果（加入 .gitignore）
└── transcripts/                 # 会话记录
```

### 每个项目文件夹的职责

* `README.md`：面向**人类与 AI**的项目说明（背景、角色、技术栈、架构、成果、链接）
* `facts.yaml`：面向**程序与 RAG**的结构化事实（用于检索、排序、受控改写）
* `images/`：**证据素材**（架构图、实验结果、截图、Demo 等），供 README 与生成系统引用

---

## 三·附、GitHub Profile README（本仓库根目录 `README.md`）

本仓库 **`username/username`** 形态时，根目录 `README.md` 会显示在 **GitHub 个人主页**顶部，维护约定如下：

* **贡献热力图**：官方个人主页上的贡献日历 **不能** 嵌进任意 README；可用第三方 SVG 近似。当前采用 [ghchart.rshah.org](https://ghchart.rshah.org/)，URL 形态 `https://ghchart.rshah.org/<可选十六进制色>/<GitHub用户名>`（例：配色 `216e39`）。若偶发加载失败，可试无配色 `https://ghchart.rshah.org/<用户名>`。
* **不要嵌入**：`github-readme-stats`、`github-readme-streak-stats` 等易被限流或超时，在 GitHub 上常显示 **裂图**，本仓库 **不再使用**。
* **Publications**：与 **`kb/achievements.yaml`** 的 `publications`、**`projects/chatclothes/facts.yaml`** 里 `evidence` / `type: publication` **保持一致**；在 KB 增删改论文/书稿后，记得 **同步改 `README.md`**。建议顺序：IVCNZ 已发表论文 → IGI Global 书章（若在审须写明）→ 硕士学位论文。
* **版式**：`GitHub activity` 可只保留标题 + 图，减少长说明与易失效外链。

---

## 四、知识库（KB）设计原则

* **单一事实来源（Single Source of Truth）**

    * 所有关于"我做过什么"的事实，只存在于 `kb/` 和 `projects/*/facts.yaml`
    * 简历 / Profile / Cover Letter 都是从 KB 生成的产物

* **结构化优先**

    * 项目 / 经历 / 技能使用 YAML 描述
    * 每条信息尽量包含：

        * 做了什么（Action）
        * 用了什么（Tech）
        * 解决什么问题（Problem）
        * 产生什么结果（Result / Metric）
        * 证据链接（GitHub / 论文 / 图片 / Demo）

* **面向检索与重组**

    * 每个项目 / 经历都是可被单独检索、组合、排序的最小单元

---

## 五、生成系统（Resume Compiler）工作流

1. 输入：

    * 招聘 JD
    * 目标岗位（如 android / backend / ai / fullstack）
    * 风格参数（篇幅、偏技术/偏业务、ATS 友好度等）

2. 系统流程：

    * 从 JD 提取关键词与职责信号
    * 在 KB 中做相似度检索 / 规则过滤
    * 选出最相关的项目、经历、技能条目
    * 先用规则拼出简历骨架
    * 再用 LLM 对 bullet points 做**受控改写**（仅限已有事实）

3. 输出：

    * 一份岗位定制简历
    * （可选）trace / evidence 文件，标注每条内容来源

---

## 六、重要约束（防止 AI 胡编）

* AI **不允许**：

    * 新增不存在的项目/公司/职责
    * 编造指标或成果
    * 把"熟悉/了解"升级成"负责/主导"
    * 修改已确认的关键事实（见下节）

* 如果 KB 中缺信息：

    * 应提示 `MISSING_INFO`
    * 先补充 KB，再重新生成

* 修改 `facts.yaml` 后**必须**运行：

    ```bash
    python app/backend/validate.py
    ```

---

## 七、已确认的关键事实（不得修改）

| 字段 | 值 |
|------|-----|
| 姓名 | Yuchao Zhang（Leo Zhang） |
| 毕业时间 | **February 2026** |
| 学位 | Master of Computer and Information Sciences @ AUT |
| 荣誉 | **First Class Honours，GPA 8.25/9.0** |
| 工作经验 | **10+ years** |
| 论文 | ChatClothes，DOI `10.1109/IVCNZ67716.2025.11281834` |
| 论文提交 | 提前 6 个月提交 |
| 目标岗位 | Android / Java 后端 / AI/ML / 全栈（全方向覆盖） |
| 面试语言 | **英文** |

---

## 八、快速上手

### 环境验证

```bash
# 安装依赖
pip install -r requirements.txt

# 验证 KB 数据完整性
python app/backend/validate.py
```

### 生成简历

```bash
# 查看所有可用命令
python generate.py --help

# 生成 Android 岗位简历（Markdown）
python generate.py cv --role android

# 生成 Backend 岗位简历
python generate.py cv --role backend

# 生成求职信
python generate.py cl --role android --company "Target Corp"
```

### 面试 Q&A

```bash
# 启动面试问答 CLI
python app/backend/interview_qa_cli.py
```

完整的回答稿（33 题，可直接背诵）在：`kb/interview_qa/scripts.md`

---

## 九、当前状态（2026-03 更新）

* [x] 知识库 Schema 设计完成（`kb/schema/project_facts_schema.yaml`）
* [x] 17 个真实项目全部转换为 YAML（`projects/*/facts.yaml`）
* [x] KB 数据验证器（`app/backend/validate.py`）
* [x] 核心简历生成器（`app/backend/generate_cv_from_kb.py`）
* [x] 求职信生成器（`app/backend/generate_cover_letter.py`）
* [x] 统一 CLI 入口（`generate.py`）
* [x] 面试 Q&A 库（33 题完整英文口语回答稿，`kb/interview_qa/scripts.md`）
* [ ] PDF / DOCX 导出管线（部分实现，HTML→PDF 可用）
* [ ] Web UI（规划中）
* [ ] 面试 Q&A 回答稿按《Behavioral Interviews for Software Engineers》原则优化

---

## 十、给 AI 协作者的提示

* 本项目的"事实来源"仅限 `kb/` 目录和 `projects/*/facts.yaml`
* 任何简历内容生成或改写，都必须基于 KB
* **修改 `facts.yaml` 后必须运行 `python app/backend/validate.py`**
* **新增项目必须遵循 `kb/schema/project_facts_schema.yaml`**
* 优先保持：

    * 可追溯性
    * 可复现性
    * 不夸大、不虚构
