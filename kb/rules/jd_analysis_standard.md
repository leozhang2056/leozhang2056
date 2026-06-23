# JD Analysis & CV Targeting Standard
# JD 分析与简历对标标准

> 每次拿到 JD，走完这套流程再生成。不是跑命令，是有理解的思考。

---

## 1. 读JD：拆解需求层次

不要只看关键词 list，要理解这个人在招什么。三层拆解：

### 1.1 硬技能（Must-have → Nice-to-have）
- **必须**：JD 里反复出现、加粗、放在第一段的。Java 出现5次"genuine Java strength matters" → 必须
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

---

## 3. 选模板 + 调内容

### 3.1 角色选择
| JD 特征 | 选哪个角色 |
|---------|-----------|
| 纯后端/Java为主 | `backend` |
| 前后端+AI | `fullstack` |
| 纯AI/ML | `ai` |
| 纯Android | `android` |

### 3.2 头衔适配（必须）
- CV 标题 = JD 标题，不保留默认头衔
- 不使用 `--title` 硬编码时，自动从 JD 第一行提取
- Summary 第2句替换为 JD 头衔
- Experience 顶部显示 Target role 行

### 3.3 技能排序
- JD 最关注的技术放对应类别第一项
- 不相关的技术往后放或移除
- 每类 3-5 项，避免换行

### 3.4 子弹选择
- **第一颗子弹必须直击JD最核心需求**（recruiter只读第一颗）
- 优先选包含 metric 的（Numbers sell）
- 优先选 end-to-end 场景的（从需求到交付）
- 包含 AI 相关的（ChatClothes, LLM, diffusions）
- 软实力用故事包装，不单独写 "Good communicator"

---

## 4. Recruiter 视角：30秒筛选动线

Recruiter 不读简历，只扫。你要设计他扫的路径。

### 前5秒 — 4个信号
| Recruiter 看 | 他要看到什么 | 你的简历必须有 |
|-------------|------------|---------------|
| 当前头衔 | 跟JD一样 | CV title = JD title |
| 公司名 | 听过/靠谱 | Chunxiao description 写清楚不是小作坊 |
| 时间线 | 无gap | 11年连贯，AUT 解释为研究 |
| 教育 | 相关学位 | AUT Master First Class Honours |

### 第6-15秒 — 3个技术信号
| Recruiter 找 | 在哪出现 | 优先级 |
|-------------|---------|--------|
| Java | 技能区第一条 | ⭐⭐⭐ |
| TypeScript | 技能区 Languages | ⭐⭐ |
| AI | 子弹 + Skill | ⭐⭐⭐ |
| product / end-to-end | Summary + 子弹 | ⭐⭐ |

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

## 5. 不做什么

- ❌ 不伪造 KB 没有的技能（Angular, Firebase → 用已有技能表达可迁移性）
- ❌ 不用 "Senior Backend Engineer" 这种默认头衔（JD里写了就不要用）
- ❌ 不把技能区塞满（每类 3-5 项，换行了就砍）
- ❌ 不单独列软技能标签（用故事证明）
- ❌ 不追求 JD 覆盖率 100%（杀不死的通用词如 "team", "quickly" 不用管）
- ❌ 不投降：有 gap 的想办法用已有证据兜底，不是直接放弃

---

## 6. Checklist（每次JD必过）

- [ ] 读完了JD全文，不是只扫了关键词
- [ ] 硬技能 → KB 证据 对比表做好了
- [ ] 软技能 → 子弹故事 映射做好了
- [ ] 选对了角色模板（android/backend/fullstack/ai）
- [ ] CV title = JD title
- [ ] Summary 第2句用 JD 头衔
- [ ] 技能区第一项 = JD 最看重的技术
- [ ] 前两颗子弹命中 JD 核心需求
- [ ] 有数字/metrics
- [ ] 不是模板简历（Target role 行 + 定制化子弹）
- [ ] Recruiter 30秒能扫完且得到所有信号

---

*Version: 2026-06-17*
