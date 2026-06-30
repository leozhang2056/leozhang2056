# JD Analysis & CV Targeting Standard
# JD 分析与简历对标标准

> 每次拿到 JD，走完这套流程再生成。纯分析工作流，输出规则见 `kb/rules/resume_output.md`。

---

## 1. 读JD：拆解需求层次

不要只看关键词 list，要理解这个人在招什么。三层拆解：

### 1.1 硬技能（Must-have → Nice-to-have）
- **必须**：JD 里反复出现、加粗、放在第一段的。Java 出现5次 "genuine Java strength matters" → 必须
- **重要**：明确列出但出现频率较低的。TypeScript, Angular
- **加分**："nice to have"、"preferred"、"bonus"。Firebase, GCP

### 1.2 软技能（Signal words）
不是列在"Requirements"里的，是通过描述工作日常泄露的：
- "Sit with stakeholders" → 需要面对面沟通、抗压
- "Carry a feature end to end" → 要ownership，不是接ticket
- "Build for the long run" → 代码质量意识，经历过维护期
- "Don't just build the wrong thing quickly" → 要有判断力，能说不

### 1.3 业务上下文
- 行业：construction tech / fintech / healthcare → 术语有差别
- 团队规模：startup vs enterprise → 对应决策范围
- 节奏：4-month sprint / fast iteration → 不是 waterfall
- 阶段：greenfield / legacy / maintenance → 对应什么样的挑战

---

## 2. 对KB：找证据 + 识差距

建立对比表格：

| JD 要求 | KB 证据 | 证明方式 | 状态 |
|---------|---------|---------|------|
| Java + Spring | Chunxiao Spring Cloud 微服务 | 子弹 + Skill | ✅ |
| TypeScript/Angular | TypeScript 在技能区；Vue.js 项目经验 | Skill + 可迁移叙述 | ⚠️ Angular 不在KB |
| AI integration | ChatClothes + LLM + Computer Vision | 子弹 + Skill | ✅ |
| End-to-end ownership | Smart factory 从需求到交付 | 子弹 + Summary | ✅ |
| Firebase | 无 | — | ❌ 不碰 |
| Construction tech | Smart factory 场景 | 类比 | ⚠️ 非直接 |

### 2.1 缺失项处理原则
- **不在 KB 的硬技能**（Angular, Firebase）：不伪造。用相邻技能兜底（TypeScript → 前端通用能力）
- **不在 KB 的软技能**（product instinct）：用子弹故事证明，不单独列成标题
- **不在 KB 的业务场景**（construction tech）：用相似场景类比（Smart factory → 工厂数字化转型）

### 2.2 JD 覆盖率目标
- 代码硬编码目标：**85%** KB可支持的JD关键词覆盖（`MIN_JD_MATCH_PCT = 85.0`，可通过 `--min-jd-match-pct` 调整）
- **这是软警报，不是硬门禁。** 不达85%不会阻止生成，仅在 match report 时标记 attention。
- 不追求100%覆盖率：`team`、`quickly`、`communication` 等通用词不用管。

<!-- EVOLVE: 2026-07-01 | source: session | issue: Auto-extracted keywords included generic words like features, codebase, monitor — inflated miss count -->
### 2.3 JD 关键词过滤（anti-generic-word）
Auto-extracted keywords 经常混入通用英语词，这些不应作为 CV 匹配目标：
- **过滤词（不计入覆盖率）：** `features`, `codebase`, `monitor`, `troubleshoot`, `solutions`, `practical`, `clear`, `modern`, `process`, `teams`, `issues`, `build`, `develop`, `design`, `data`, `test`
- **核心判断标准：** 如果一个词不能对应到具体技术栈或可验证的工程能力，它就不该是关键词
- **覆盖率报告时：** 区分 "technical keyword hits" 和 "generic word hits"，只报告前者

---

## 3. Company-Fit & 角色前研

### 生成前，弄清楚
- 公司业务领域和产品类型
- 技术栈信号
- 文化 / 价值观
- 团队规模和风险偏好

### Banking / financial / payment 角色
措辞偏好：
- 可靠性和运维稳定性
- 测试纪律和安全工程
- Cloud/infra 所有权和生产变更支持
- 跨职能 Agile 交付

### Developer 角色（一般）
- 强调：快速执行/快速迭代，强自我管理/ownership。
- 弱化 people-management 措辞。
- 避免在 Summary 中用 squad-leadership 框架，除非 JD 要求。

### 角色推断（`--role auto` 如何工作）
| JD 特征 | 选哪个角色 |
|---------|-----------|
| 纯后端/Java为主 | `backend` |
| 前后端+AI | `fullstack` |
| 纯AI/ML | `ai` |
| 纯Android | `android` |
| IoT/嵌入式/C/C++为主 | `embedded` |

### 按角色的关注点
- **Android:** Android SDK, Kotlin/Java, architecture, performance, hardware integration.
- **Backend:** Spring Cloud, microservices, APIs, databases, scalability, DevOps.
- **AI/ML:** Model training, CV/NLP, deployment, evaluation, research contributions.
- **Full-stack:** Cross-layer delivery, client + backend + deployment + integration.
- **Embedded:** IoT platforms, C/Linux, firmware, protocol implementation, device integration.

---

## 4. Recruiter 视角：30秒筛选动线

Recruiter 不读简历，只扫。你要设计他扫的路径。

### 前5秒 — 4个信号
| Recruiter 看 | 他要看到什么 | 你的简历必须有 |
|-------------|------------|---------------|
| 当前头衔 | 跟JD一样 | CV header title = JD title |
| 公司名 | 听过/靠谱 | Chunxiao description 写清楚不是小作坊 |
| 时间线 | 无gap | 11年连贯，AUT 解释为研究 |
| 教育 | 相关学位 | AUT Master First Class Honours |

### 第6-15秒 — 3个技术信号
| Recruiter 找 | 在哪出现 | 优先级 |
|-------------|---------|--------|
| JD 第一语言 | 技能区第一条 | ⭐⭐⭐ |
| 第二语言/框架 | 技能区 | ⭐⭐ |
| AI / 产品 / 端到端 | Summary + 子弹 | ⭐⭐⭐ |

### 第16-30秒 — 验证深度（读2-3颗子弹）
| 验证项 | 通关条件 | 不通关的表现 |
|-------|---------|------------|
| 技术深度 | "Architected Spring Cloud microservices..." | "Used Spring Boot" |
| 有数据 | "5,000 DAU", "30%+ efficiency" | 没有数字 |
| 见过问题 | OOM、100+ devices、跨团队 | CRUD only |
| 核心匹配 | Smart factory = 端到端交付 | 不相关的技术堆砌 |

### 30秒后 — 判断
- ✅ 头衔匹配 + 技能命中 + 有深度故事 + 不是海投 → 通过
- ❌ 头衔不匹配 OR 技能不相关 OR 子弹全是空话 OR 明显模板简历 → 扔

---

## 5. 不做什么（Pre-Generation Guardrails）

- ❌ 不伪造 KB 没有的技能（Angular, Firebase → 用已有技能表达可迁移性）
- ❌ 不追求 JD 覆盖率 100%（杀不死的通用词如 "team", "quickly" 不用管）
- ❌ 不投降：有 gap 的想办法用已有证据兜底，不是直接放弃

---

## 6. Checklist（每次JD必过 — 生成前）

- [ ] 读完了JD全文，不是只扫了关键词
- [ ] 硬技能 → KB 证据 对比表做好了
- [ ] 软技能 → 子弹故事 映射做好了
- [ ] 缺失项处理方案确定（不伪造，用相邻技能兜底）
- [ ] 公司业务域/文化/团队规模已了解（见 §3 Company-Fit）
- [ ] 选对了角色模板（android/backend/fullstack/ai/embedded）
- [ ] Recruiter 30秒动线设计已确认：头衔匹配 + 技能命中 + 深度故事

---

*Version: 2026-07-11 — reorganized: output formatting moved to resume_output.md; company-fit/role selection moved here from resume_output; trimmed checklist to pre-generation items; added 85% coverage note; removed output-formatting anti-patterns (merged into resume_output.md §10)*
