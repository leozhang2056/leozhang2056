# Behavioral Interview — Leo Zhang

## 目录（概要）

| 块 | 概要 | 跳转 |
|----|------|------|
| 一 | **文档说明 + 规则**：简报、事实来源、自填临场规则 | [→](#section-doc-about) |
| A | **临场口语**：10 题；**①** 两档时长，**②—⑩** 每题一版 | [→](#section-oral-only) |
| B | **题型与 STAR**：B1 高频分类题 + B2 十题骨架备忘 | [→](#section-part-b) |
| D | **工具箱**：模板、注意事项、练习方法论、口语句型（D1–D4） | [→](#section-toolbox) |
| C | **逐题英文稿**：Q1–Q45 口语 Script + 主故事速览 | [→](#section-5-scripts) |
| 附录 | **个人素材**：草稿模板与收件箱 | [→](#section-appendix) |

> 细粒度锚点（如 `oral-01`、`b1-03`、`q-12`、`d3-04`）在**正文各小节标题上方**；需要时搜索 `id="q-12"` 或先打开 C 节再按 `### 12)` 等标题浏览。

---

<a id="section-doc-about"></a>
## 第一部分 · 文档说明 + 规则

本文件是 **Behavioral 面试**用：英文口稿（**A**）、题型与 STAR（**B**）、工具句（**D**）、逐题（**C**）。

### 规则（可在此往下加你自己的）

- **先想为什么问**，再答到点上（别只堆经历）。
- **事实**：数字与经历只来自 `kb/*.yaml`、`projects/*/facts.yaml`；我会在对话中提到新的事实，要持久化到项目中。
- **口语**：短句、好念；**常用词**优先；**A** 主练，**C** 当辞典；临场改口，别背稿腔。
- **篇幅**：**①** 备 **30 秒 + 1 分钟** 两档；**②—⑩** 与 **C 节**每题 **一版**口稿即可，长短临场伸缩。
- **STAR**：心里过 **S→T→A→R**；正文里用 **一行中文提示（关键词）** 帮你对齐，英文口稿保持简洁。
- **改结构**：尽量别删 `oral-*` / `q-*` / `section-*` 锚点。


---
<a id="section-oral-only"></a>
## A. 临场开口

> **版面**：**①** = **30 秒 + 1 分钟**；**②—⑩** = **每题一版**。下方 **提示（STAR）** 为中文关键词，英文为口稿。

<a id="oral-01"></a>
### ① Tell me about yourself

**提示（STAR）**：（S）奥克兰工程师；（T）让对方记住方向 + 资格；（A）Android / Java 后端 / Web + 最近 AUT + 代表项目一句；（R）**full-time** NZ + 想加入对方团队。

#### 30 秒版（约 30s）

Hi, I'm **Leo Zhang**, a software engineer in **Auckland, New Zealand**. About **ten years** — **Android**, **Java** on the **server**, **web** when needed, plus **AI**.

I just finished **AUT**, **Master of Computer and Information Sciences**, **First Class Honours**, **applied AI**. Main stories: **ChatClothes** (**Pi 5**, local **LLM**, **LoRA**), **Smart Factory** (**many plants**, **IoT**, **~30%** efficiency), **Enterprise Messaging** (**NDK**, **fast** messages, **5,000 DAU**).

**Full-time work rights** in NZ — I'd love to bring **mobile + backend + AI** to your team.

#### 1 分钟版（约 60–90s）

Hi, I'm **Leo Zhang**, in **Auckland**. I've built **real products** for about **ten years** — mostly **Android** and **Java** **backends**, sometimes **web** when we ship the **whole** stack.

I recently finished **AUT** — **First Class Honours**, **applied AI**. **ChatClothes** was my thesis: **AI** that runs **offline** on **small hardware** — **local LLM** (**Ollama**), **LoRA**, **Raspberry Pi 5**, and I **handed in six months early**.

At work I've been on **Smart Factory** — **shop-floor** apps, **devices**, **Java** services, rolled out to **many factory sites** over **years**, about **30%** **efficiency** gain, **strong uptime**. And **Enterprise Messaging** — **NDK** **C/C++** path, **sub-200ms**, **Spring Cloud** on the server side, **5,000** **daily users**, **heavy** message volume.

I'm on a **work visa** with **full-time** rights. I want a team where I mix **solid coding** with **AI** — and **get products out** to users.

<a id="oral-02"></a>
### ② Complex technical problem

**提示（STAR）**：（S）企业即时通讯要后台也实时收消息；（T）Android 省电会杀后台，且要平衡耗电；（A）系统优先级 + 白名单 + widget + 第三方通道（如 JPush）+ 被杀后重同步 + 已读未读对账；（R）消息更及时、漏消息更少、一致性更稳。

One hard problem I worked on was **real-time messaging** on Android. The app needed to receive messages in the background, but Android may kill background apps to save battery.

So first I had to understand Android system behavior: **process priority**, **why apps get killed**, and what we could do to reduce that risk.

I used a layered approach. We guided users to add the app to the battery whitelist. We added a home-screen widget to improve app priority. We also used a third-party push channel (like **JPush**) so incoming push could wake the app and trigger sync. On top of that, we added other small reliability steps to improve survival chance.

The result was better message timeliness and fewer missed messages in background cases. What I learned is: on Android, one trick is not enough - you need multiple layers.

Another hard part was the trade-off between **real-time** and **battery**. If keep-alive is too aggressive, battery gets worse. If it's too weak, messages arrive late. So we tuned heartbeat/reconnect strategy and used push wake-up where possible.

We also planned for process death. If the app got killed, we restored session and ran fast re-sync on reconnect/resume. We used sent/delivered/read state checks to reduce message loss risk.

And yes, we saw edge bugs like "read state updated, but UI did not show it." We added stronger state reconciliation between local cache and server state, plus UI refresh triggers after ack.

<a id="oral-03"></a>
### ③ Conflict with a teammate

**提示（STAR）**：（S）同事抗拒 code review；（T）不伤关系也要保质量；（A）先 1:1 听原因，再改成私下、具体、短结对；（R）评审恢复，质量和节奏都回来。

In **Enterprise Messaging**, I had a teammate who pushed back on **code review** a lot.  
At first it looked like a skill issue, but after a **1:1** talk I found it was more about trust — they had bad experiences with public criticism before.

So I changed the way we worked: feedback was **private**, **specific**, and focused on code, not person. For tricky parts, we did short **pairing** sessions instead of long comment threads.

After that, review speed got better, code quality improved, and our release rhythm stayed stable.  
What I learned is simple: in team conflict, fixing the **communication style** is often as important as fixing the code.

**Case B（可选：技术选型分歧）**
**提示（STAR）**：（S）新项目技术栈分歧；（T）平衡熟悉度与长期适配；（A）拉 PM/TL/团队做时间与风险评估；（R）共识方案，减少争执。

In one new project, I had a teammate with very deep experience in older stacks like **C#** and **C++**.  
He preferred familiar tools for delivery control, while I thought some newer parts fit the new requirements better.

Instead of arguing by preference, we brought in the **PM**, **team lead**, and the team to evaluate options together: delivery time, risk, maintainability, and how well each stack matched the project direction.

That changed the discussion from "my tech vs your tech" to "what is best for this project now and later."  
We aligned on a practical plan, and the team moved forward with less friction.

**Case C（可选：跨部门沟通冲突）**
**提示（STAR）**：（S）产品给高压需求且技术成本高；（T）避免空口答应又不伤协作；（A）讲清技术边界 + 成本 + 分期折中；（R）达成可上线版本。

In cross-team work, product teams sometimes ask for features that look simple from user view, but are expensive or risky to build, and still want them live very fast.

When that happens, I don't just say "no." I explain the technical reason in plain language, show the real cost and risk, and offer options: **MVP now**, full version later, or phased rollout.

We compare trade-offs together — time, quality, and user impact — and pick a plan both sides can commit to.

That way, we avoid fake promises, still ship something useful on time, and keep trust between product and engineering.

<a id="oral-04"></a>
### ④ Failure

**提示（STAR）**：三选一。**Case A** 数据标注估错；**Case B** 发版未切 **prod** 配置连到测试库 → 二次升级 + 流程加固；**Case C** **`enterprise-messaging`** 头像目录上传权限过松 → 被传可执行文件、服务器中毒、备份恢复与加固（见下）。

**Case A — Chinese herbal（标注估时）**  
**Chinese herbal** project — I **guessed two weeks** for **labels**; real work was more like **six** (messy photos). I **said so early**, **reset** the plan, **pilot** a small batch first. **Lesson**: **pilot before you trust** the estimate.

**Case B — App release（测试配置打进正式包）**  
We shipped an **app upgrade** but I left **test settings** on — build still pointed at the **test database** and **test APIs**. Users saw **wrong data**. We had to **ship again** to fix it.

Our team was **small** and we didn't have **dedicated QA** yet, so the release checklist was **weak**.

After that I changed how we work: **split configs** for dev/test/prod, **multi-round** checks with **more than one person**, and **test every build** even for small changes. We also pushed **more automation** over time to cut **human mistakes** — it wasn't **fully** automated at first, but it got **much safer**.

Since then I've treated **every release path** the same way — **database** changes, **mobile** builds, and **web** deploys — same care, same checks, no "this one is small so we can skip."

**Case C — Enterprise IM（头像上传目录 → 入侵）**  
**Enterprise messaging** — user **avatars** lived on a **Windows** **file server**. **Upload** rules were **too loose**: someone got **executables** into the **avatar** folder, the box was **compromised**, and we **lost data** we couldn't trust on that host.

We **rebuilt** the environment and **restored** from **backups**. After that the team took **security** seriously: **tighter permissions**, **antivirus** on servers, and we **moved** those **files** to **cloud** storage with **stricter** controls.

**Lesson**: **any** user-facing **upload** path is an **attack** surface — **least privilege**, **validate file type**, **never** mix **upload** dirs with **execution**, and **assume** you'll need **clean** **restore** paths.

<a id="oral-05"></a>
### ⑤ Under pressure

**提示（STAR）**：二选一。**Case A** **Smart Factory** 发布窗口；**Case B** **`enterprise-messaging`（企业即时通讯）** 早期**单人安卓**、几周原型上线、爆 bug、**日更**清优先级 + **产品**帮对接用户。

**Case A — Smart Factory（发布窗）**  
**Smart Factory** before release — **shop floor** doesn't wait. I split it: **triage**, **fix**, **verify**, **watch**. Pull the **owner** of the broken layer, **short** updates. We got it **out** without **breaking** the line. **Shrink unknowns fast** — that's how I handle heat.

**Case B — Enterprise IM（单人原型 + 上线救火）**  
Early on the **enterprise instant messaging** app — I was the **only Android dev**. We had **a few weeks** to build a **prototype**, test it, and **go live**.

After launch we hit **a lot of bugs**, and I was still the **only one** fixing them. Pressure was real — **users** wanted fixes fast, and I also had to **keep shipping**.

So I worked in a tight loop: every day I **listed** issues, **ranked** them by **priority**, fixed **high** items first, **shipped a build** every day, then **tested** again. Some fixes created **new** bugs — I kept **re-prioritizing** and focused on what hurt users most until things got **stable**.

I wasn't alone on the **people** side — **product / design** helped **explain** to users **why** things broke, **how long** fixes take, and they aligned **priority** and **dates**. They also shared **what we shipped each day** and **what we fixed**.

**Lesson**: under pressure, **visible order** + **daily rhythm** beats panic; **cross-team** user comms is part of the fix, not extra work.

<a id="oral-06"></a>
### ⑥ Prioritize quickly

**提示（STAR）**：二选一。**Case A** 产线问题 + PM 要功能；**Case B** 无对标、**下车间**澄清模糊需求、**快原型**迭代、大版本演进（压力 + 交付后仍可能改向）。

**Case A — 产线 vs 里程碑**  
**Smart Factory** — **line** issues, **PM** wants features. I fix what **hurts operators** first, then what's **on the milestone**, and I'm **honest** about dates on the rest. **Clear order** beats a **pretty** plan nobody follows.

**Case B — 下车间 + 模糊需求 + 原型迭代**  
**Smart Factory** had **no product we could copy** — we went **into the workshops**, watched **how people really worked**, and turned **vague** asks into plans we could **negotiate** with the team: **what** to build first, **how long** a slice could take.

We had to **ship prototypes fast**, then **keep changing** them as understanding improved. Requirements stayed **fuzzy** for a long time — people felt something was wrong but couldn't spell the **exact** flow — so we **validated on real screens**, not only in meetings. **Pressure** was on the **whole** team. Even after **first delivery**, users sometimes **weren't fully on board**; we needed **bigger** follow-on releases — **second**, **third** major versions — **adding** what stuck and **trimming** what didn't.

**Lesson**: when nobody has a crisp spec, **prototype + tight feedback** sets the real priority list; **big** replans aren't shame — they're how **shop-floor** software matures.

<a id="oral-07"></a>
### ⑦ Process improvement

**提示（STAR）**：（S）多厂上线步骤乱；（A）**Spring** 容器、**Jenkins**、清单、文档；（R）部署更稳、少踩坑。

Every **factory** had **long manual** deploy steps. I pushed **Spring** in **containers**, **Jenkins** for repeat work, **checklists** that matched reality, **docs** so new people weren't **chasing** chat. **Boring** — but it **worked**.

<a id="oral-08"></a>
### ⑧ Tough feedback

**提示（STAR）**：（S）**Smart Factory**；（T）经理说架构没写清；（A）**ADR** + 短 **onboarding** 笔记；（R）新人更快、问题更少。

Manager said my **big decisions** weren't **written** enough — next hire would get **lost**. Fair. I added **light ADRs** and **short** onboarding notes — **why**, not **novels**. **Onboarding** sped up. I should've started earlier.

<a id="oral-09"></a>
### ⑨ Adapted to change

**提示（STAR）**：（S）**ChatClothes** 中途约束变紧；（A）**重测**、**LLM** 本地、砍范围；（R）**honours** 稳住。

Thesis mid-way — **offline** and **speed** became **hard** rules. Numbers didn't support the **old** design. I **re-measured**, **LLM** **local**, **cut** scope where needed. Finished **strong** with **honours**. **Measure, then change your mind**.

<a id="oral-10"></a>
### ⑩ Why should we hire you?

**提示（STAR）**：（T）为什么选我；（A）**十年**交付 + 最近 **AI**；（R）奥克兰 + **full-time** + 愿意扛事。

You get **~ten years** shipping **mobile**, **backends**, and the **messy** middle — plus recent **applied AI** where it still has to **run** for users. I'm in **Auckland**, **full-time** **OK**, flexible on **Kotlin** / **Spring** / **new** AI bits. Point me at a **real user problem** — I'll **push** it **over the line** with the team.

---

<a id="section-part-b"></a>
## B. 题型与 STAR

<a id="section-1-topics"></a>
### B1. 高频分类题库（英文题干 + 中文提示）

> **速查**：**嘴上念** → [口语专页](#section-oral-only)；**嘴里关键词** → [B2 STAR](#section-2-star-brief)；**书面辞典（记得改口）** → [C 节](#section-5-scripts)。

<a id="b1-01"></a>
### 1) 自我认知与动机
- Tell me about yourself.（**见 [A ①](#oral-01)**：**30 秒 + 1 分钟**两档；事实对齐 `kb/profile.yaml`）
- What are your strengths and weaknesses?（优劣势各 1 个 + 证据 / 改进）
- Why are you looking for a new opportunity?（与 **Q32** 叙事一致：学业阶段结束 → 全职交付）
- Why do you want to join this company?（替换公司名 / 产品 / 栈，见 **Q29**）

<a id="b1-02"></a>
### 2) 团队协作与冲突处理
- Tell me about a conflict with a teammate and how you resolved it.（Enterprise Messaging 评审敏感 → 私下 + 结对）
- Describe a disagreement with your manager.（Smart Factory 上线前范围：数据 + 分期试点）
- Tell me about a time you had to collaborate cross-functionally.（接口契约 + 集成 Demo，见 **Q12**）

<a id="b1-03"></a>
### 3) 压力管理与优先级
- Tell me about a time you worked under pressure.（产线关键路径发布窗口）
- How do you prioritize when everything feels urgent?（影响 × 风险 × 透明沟通，见 **Q8** / **Q36**）
- Tell me about a time you had multiple deadlines.（可与上题或 Smart Factory 排优先合并准备）

<a id="b1-04"></a>
### 4) 失败与复盘
- Tell me about a time you failed.（中草药标注周期低估 → 小样试点；安全/基础设施教训见 **`enterprise-messaging`** [A ④ Case C](#oral-04)）
- Tell me about a time you missed a deadline.（同上故事，见 **Q22**）
- Describe a production issue you handled.（电子秤采集 / 发布窗口 triage，用 Smart Factory；安全向可选 **`enterprise-messaging`** 头像上传入侵与恢复，见 [A ④ Case C](#oral-04)）

<a id="b1-05"></a>
### 5) 复杂问题解决与技术判断
- Tell me about a complex technical problem you solved.（ChatClothes 剖延迟 + 本地 LLM + YOLO12n-LC）
- Tell me about a difficult decision you made.（范围 / 技术路径取舍，可接 ChatClothes 或产线优先）
- Describe a trade-off you had to make (speed vs quality, etc.).（速度 vs 可观测性 / 范围 vs 信任，用 Smart Factory 分期上线）

<a id="b1-06"></a>
### 6) 主动性与影响力
- Tell me about a time you took initiative.（论文交付物超出要求：部署文档 + API 说明，见 **Q7**）
- Describe a process improvement you drove.（容器化 + Jenkins + checklist）
- Tell me about a time you influenced without authority.（用数据推动分期试点，与经理分歧题同源）

<a id="b1-07"></a>
### 7) 反馈与成长
- Describe a time you received critical feedback.（ADR / onboarding 文档习惯）
- Tell me about a time you gave difficult feedback.（Junior 文档反馈 + 结对，见 **Q21**）
- What did you learn from your biggest mistake?（标注估算 → 先 pilot，与失败题同源）
- How do you assure code quality in your team?（Q43：Smart Factory 门禁 + CI + 回滚；Enterprise Messaging 高并发）
- How do you support and track a junior developer's progress?（Q45：30/60/90 天 + 结对 + 周 1:1）

<a id="b1-08"></a>
### 8) 适应变化
- Tell me about a time requirements changed suddenly.（ChatClothes 约束变化 → 可测再改）
- Describe a major change at work and how you adapted.（同上或读硕士阶段转型）
- Tell me about a time you had to learn a new technology quickly.（扩散模型 / LoRA，见 **Q14**）
- Describe the project workflow in your previous team.（Q44：Smart Factory 双周 Sprint + 接口契约 + 集成 Demo）

<a id="b1-09"></a>
### 9) 客户导向
- Describe a difficult customer/stakeholder situation.（范围拉扯 → 数据 + 试点）
- Tell me about a time you managed unclear requirements.（先澄清指标与「完成定义」，见 **Q30**）
- How do you handle conflicting stakeholder expectations?（透明优先级 + 书面契约 / ADR）

---

<a id="section-2-star-brief"></a>
### B2. STAR 备忘（关键词 · 与 [口语专页](#section-oral-only) ①–⑩ 对应）

> **编号说明**：本节 **1)–10)** 与 **[C 节](#section-5-scripts)** 里的 **Q1–Q45** 不是同一套编号；「Qxx」一律指 C 节逐题编号。  
> **怎么用**：下面每条是**嘴里关键词**；完整英文口语在 **[A 节](#section-oral-only)** 对应条。**C 节**长句别直接念，先改口。

<a id="b2-01"></a>
### 1) Tell me about yourself.

**张嘴念** → **[A ①](#oral-01)**（**30 秒 + 1 分钟**两档）。  
**嘴里关键词**：Auckland；Android + Java backend + front if needed + full-stack；AUT + **First Class Honours** + applied AI **能跑**；~10y 产线；**PSW full-time**；想干 **AI / mobile / Java** 混合活。

---

<a id="b2-02"></a>
### 2) Tell me about a complex technical problem you solved.

**口语 →** [专页 ②](#oral-02)  
**STAR — ChatClothes**：慢 + 离线；profile；LLM 路径瓶颈 → 本地；vision 收束分类；结果可演示 + honours。**Reflection：**先测再优化。  
*备选：Smart Factory 秤采集 — listener / watchdog / 重连 / 池化。*

---

<a id="b2-03"></a>
### 3) Tell me about a time you had a conflict with a teammate.

**口语 →** [专页 ③](#oral-03)  
**STAR — Enterprise Messaging**：评审抵触 → 1:1；过往公开批评伤信任 → 私下具体反馈 + 短结对；review 恢复。**Reflection：**反馈 = 流程 + 语气。

---

<a id="b2-04"></a>
### 4) Tell me about a time you failed.

**口语 →** [专页 ④](#oral-04)  
**STAR — Herbal CV**：标注估 2w → 实 6w；赶工标签脏 → 首训差；认栽、改期、pilot 50–100 再估。**Reflection：**数据活先验证工作流。  
**STAR — Release（可选）**：测试配置未切 prod → 连测试库/API → 数据异常 → 二次发版；小团队无专职测试 → 多环境配置 + 多人多轮验证 + 逐步自动化。**Reflection：**发版靠流程和检查清单，不靠记忆。  
**STAR — Security（可选，`enterprise-messaging`）**：Windows 服务器存用户头像；上传权限/校验不足，头像目录被写入可执行文件致服务器中毒与数据不可用；备份恢复 + 重建部署；事后强化权限、部署防毒，并将文件迁移至云端与更严管控。**Reflection：**上传即攻击面，最小权限 + 类型校验 + 与执行环境隔离；备份与可重建流程是底线。

---

<a id="b2-05"></a>
### 5) Tell me about a time you worked under pressure.

**口语 →** [专页 ⑤](#oral-05)  
**STAR — Smart Factory 发布窗**：关键路径；triage→fix→verify→watch；拉对人；短更新；上线未砸线。**Reflection：**先减不确定。  
**STAR — `enterprise-messaging`（早期单人安卓，可选）**：企业即时通讯客户端；几周原型→上线→bug 洪峰；每日列单、优先级、日更包、测试收敛；产品侧对用户解释与排期、日更说明。**Reflection：**高压靠节奏 + 对外透明，不靠一个人硬扛话术。

---

<a id="b2-06"></a>
### 6) Tell me about a time you had to prioritize quickly.

**口语 →** [专页 ⑥](#oral-06)  
**STAR — Smart Factory（产线窗）**：产线 vs 里程碑 vs 维护；先产线影响 → 再里程碑；其余标日期透明。**Reflection：**可见顺序 > 全是 P0。可接 **high uptime** 口径若追问。  
**STAR — Smart Factory（模糊需求，可选）**：无对标、下车间理解工人/工厂真实痛点；与团队对齐开发节奏与任务切分；快原型 → 反复确认 → 需求逐步精确；首版上线后可能仍需大版本调整；多轮大版本边加边减功能。**Reflection：**模糊需求时优先级由「验证假设」驱动，而非一开始的文档。

---

<a id="b2-07"></a>
### 7) Tell me about a process improvement you drove.

**口语 →** [专页 ⑦](#oral-07)  
**STAR**：多厂部署手顺乱；Spring 容器 + Jenkins + checklist + 文档；rollout 更可预期。**Reflection：**自动化与文档一起上。

---

<a id="b2-08"></a>
### 8) Describe a time you received tough feedback.

**口语 →** [专页 ⑧](#oral-08)  
**STAR — Smart Factory**：经理点架构未写清；ADR + onboarding；默认「写完再收工」。**Reflection：**文档 = 长期功能。

---

<a id="b2-09"></a>
### 9) Tell me about a time you adapted to change.

**口语 →** [专页 ⑨](#oral-09)  
**STAR — ChatClothes**：中程约束变；重测；LLM 本地化 + 控 scope；honours + 提前节奏。**Reflection：**研究也按工程习惯 instrument。

---

<a id="b2-10"></a>
### 10) Why should we hire you?

**口语 →** [专页 ⑩](#oral-10)  
**STAR 备忘**：久经生产（Android / Java / 集成）；applied AI 能落地；Auckland + full-time；不挑栈、跟团队把事推上线。追问可补 **NDK / Spring / 论文** 等专名。

---

<a id="section-toolbox"></a>
## D. 工具箱（模板 · 注意 · 练习法 · 句型）

<a id="section-3-templates"></a>
### D1. 面试回答速用模板

### STAR 模板
- **Situation:** 背景是什么，为什么重要
- **Task:** 你负责达成什么目标
- **Action:** 你做了哪 2-3 个关键动作
- **Result:** 最终结果（尽量量化）+ 学到什么

### 常用英文句式
- The context was that ...
- My responsibility was to ...
- I took three actions: first ..., second ..., third ...
- As a result, we ...
- What I learned was ...

### 30 / 60 / 120 秒分层模板（临场提速）
- **30 秒版（电梯版）**：`背景一句 + 关键动作一句 + 结果一句`
- **60 秒版（默认版）**：`Situation 1句 + Task 1句 + Action 2句 + Result/Reflection 1句`
- **120 秒版（深挖版）**：在 60 秒版基础上补 `权衡/指标/追问点`（如 hardest part、specific role、next time）
- **口语感**：允许一两句「跑题式」连接（*long story short*, *anyway*），避免排比三件套句句对称 —— 详见 [口语专页](#section-oral-only) 文首说明。

### 面试前 10 分钟检查清单（Leo 专用）
- 主故事是否覆盖 5 类：复杂技术、冲突、失败、压力、主动性
- 每个故事是否有 1 个可核验指标（10+ factories / high uptime（关键流程）/ 5,000 DAU / sub-200ms / First Class Honours）
- “Why this company” 是否替换了公司名、产品名、技术栈（避免模板味）
- Q32 转职原因是否保持一致：`2026-02 完成 MCIS + 回到全职工程交付`
- 每题结尾是否有一句 Reflection（我学到什么 / 下次如何做）
- 失败题是否说明「如何防止再犯」（例如 pilot、门禁、可观测性），而不只讲一次事故经过

---

<a id="section-4-notes"></a>
### D2. 使用注意事项（Leo 版）

- 数字与项目名以 KB 为准：**10+ factories**、**high uptime**（smart-factory，关键流程；口语常提 99.9% 系 smart-power 数据准确率）、**5,000 DAU**、**sub-200ms**、**First Class Honours**、**February 2026** 毕业等；不要临场夸大。
- 每个主题准备 **1 个主故事 + 1 个备选**（可与 [C 节 Q 速览表](#section-5-scripts) 对照）；Action 写清“你具体做了什么”，少用泛化的 *we*。
- 语气：不甩锅，强调行动、衡量与复盘；开发者岗避免过度“管理团队”表述，用 **协调、接口契约、交付所有权** 更准确。
- 远程 / 混合岗位：补充异步沟通习惯、文档化决策、时区友好更新（可与 Smart Factory 多现场 rollout 类比）。

---

<a id="section-6-methods"></a>
### D3. 练习与方法论（STAR(R)、故事库、Mock）
> 资源来源：`resource.txt` 的链接
> - `techinterviewhandbook.org/behavioral-interview/`：STAR(R)、关键故事组织、Big Three、Mock 等
> - `seek.co.nz/...common-interview-questions-and-how-to-answer-them`：常见题回答结构与 avoid/can-do 要点

<a id="d3-01"></a>
### 1) 用 STAR(R)：在 Result 后加一句 Reflection
- 你已经用了 STAR；再补一层 `Reflection`：一句“我学到了什么/下次会怎么做”，让面试官看到成长和可迁移的行为。

<a id="d3-02"></a>
### 2) 不要为每题单独背：先准备 3–5 个“关键故事库”
- 从你的简历/项目里挑 3–5 个高影响、高复杂度、你参与度高的项目（例如：ChatClothes、Smart Factory、Enterprise Messaging、失败/复盘类项目）。
- 为每个关键项目整理一份 STAR(R) 故事后，面试时只需要把它“映射”到问题上，而不是为每个问题重写一套叙事。
- 重点看你在每个故事里的“可复用行为”（repeatable behaviors），而不是你做过的具体项目名称。

<a id="d3-03"></a>
### 3) Big Three：优先把这三类题准备到“自然输出”
- `Tell me about yourself`：用 **Present → Recent → Past → Why here**；口头稿见 **[口语专页 ①](#oral-01)**，STAR 备忘见 **B2**；少堆数字和模型名，项目与指标留给追问。
- `Favorite / most impactful project`：选一个“影响 + 你的深度参与 + 你做的关键动作”的项目。
- `Resolved a conflict`：准备至少 1 个冲突故事，Action 要讲清楚你如何澄清、如何对齐、如何让协作继续推进。

<a id="d3-04"></a>
### 4) 日常练习策略：用“问题-追问”而不是“背题-复述”
- 练习时每答完一题，主动补一句可能的追问，例如：
  - `What was the hardest part?`
  - `How did you measure success?`
  - `What would you do differently next time?`
  - `What was your specific role?`
- 目标不是把追问也背出来，而是让你的故事天然支持它们。

<a id="d3-05"></a>
### 5) SEEK 的常见题“可用模板”（把结果变得更像真人回答）
- Strength：选“3 个不同维度但与岗位相关”的优势，每个优势都要落到一个具体证据/经历。
- Weakness：选“真实但不致命”的短板，并说清你正在如何改进；避免陈词滥调（例如“我太完美主义”）。
- Motivation：动机要和岗位/团队价值对齐，用 1 个具体例子支撑。
- Challenge / stress / prioritization：尽量讲清楚你怎么拆解问题、怎么沟通、怎么保护质量与进度。

<a id="d3-06"></a>
### 6) 模拟面试与“发现缺口”
- 做一次 mock behavioral interview：让别人用追问逼你暴露“叙事不够清楚/指标不够明确/你的 Action 不够具体”等缺口。
- 然后回到你的关键故事库，补 Action 的细节、补 Reflection、再练一轮。

---

<a id="section-7-phrases"></a>
### D4. IT 口语句型库（Behavioral 的 Action 部分）
> 资料来源：`interview_qa/IT常见面试问题` + `interview_qa/IT行业英语_42课时_QA`

<a id="d4-01"></a>
### 1) 会议沟通 / 项目更新（Meeting & Project Status）
- `Hey, I just received the meeting invitation. What about the agenda?`
- `Let's quickly go through the project progress. Currently, this task is 80% complete, but we've hit a roadblock with the database migration.`
- `I'm worried about the long-term maintainability cost of this technical solution.`
- `Additionally, we need to evaluate potential performance bottlenecks this new solution might cause to the existing system.`
- `This architecture may introduce new security risks, so we need to involve the security team in advance.`
- `Let’s wrap up the discussion here. Now I’ll quickly demonstrate the core workflow of the new feature.`
- `At the end of the meeting, I’ll quickly summarize and confirm the action items. For the next phase, X and I will be responsible for Y.`
- `I’ll send out the meeting minutes after this session. Please pay attention to your follow-up items and deadlines.`

<a id="d4-02"></a>
### 2) 研发协作 / 调试与定位（Code Review & Debugging）
- `I've got something to talk to you about the code you submitted. I reviewed it and left comments on code style and exception handling.`
- `After debugging, I found that the NPE was just a symptom. The root cause is still under investigation.`
- `Anyway, this bug is critical and should be fixed with priority, otherwise users cannot log in.`
- `The logic here is quite complex. Are you free this afternoon? We could do some pair programming to figure it out.`
- `To completely decouple these two core services, could we refactor by introducing a message queue?`
- `If we adopt the refactoring plan, we’ll need to align with the SRE team to assess whether we should apply for more computing resources.`
- `This solution also depends on a third-party service to provide a new API for pulling user profiles.`
- `I’ll go analyze the relevant application logs to identify the main performance bottleneck.`

<a id="d4-03"></a>
### 3) 敏捷与交付管理（Agile / Delivery / Prioritization）
- `At the last sprint planning meeting, we estimated this user story as 8 story points because it’s quite complex.`
- `I finished the refactoring of the front-end components. Today I plan to write unit tests for it, and I’ll sync progress in tomorrow’s daily standup.`
- `Considering the potential technical risks, we’d better reserve some buffer time in the schedule.`
- `The product manager just raised a change request. We need to confirm whether this must be included in the next release.`
- `We have two urgent tasks competing for backend resources right now. We need to hold a meeting to decide which one has higher priority.`
- `Taking testing and deployment into account, the earliest we can deliver this feature is by next weekend.`
- `Later we’ll have a sprint retrospective meeting to discuss resource conflicts and frequent change requests, and how we can improve.`

<a id="d4-04"></a>
### 4) 跨团队与管理层沟通（Cross-team / Reporting）
- `Hello everyone, welcome to the kick-off meeting. Let’s start with a quick round of introductions.`
- `I’ve already broken down the tasks. After this meeting, I’ll assign them to the offshore development team in India via Jira.`
- `Given the time difference, we’ll schedule the daily stand-up during my evening, which is your morning.`
- `When communicating with non-technical colleagues, we need to use plain language to explain why certain features are not feasible for now due to technical constraints.`
- `When reporting to management, we should focus on the business value and expected return of this technical path.`

<a id="d4-05"></a>
### 5) 故障应急 / 生产支持（Incident Response）
- `Emergency! Our primary database is down, causing a large-scale service outage. We need to activate the emergency plan immediately.`
- `Our support engineers suggested that we immediately roll back the production environment to the last stable version.`
- `I’ve created a P0 incident in the ticketing system, and I’ll keep updating the latest progress and relevant log files in real time.`
- `Meanwhile, this data access issue needs to be communicated to the information security team immediately.`
- `During deployment on the cloud platform, we encountered a configuration issue. We need to contact the cloud service provider’s technical support right away.`

<a id="d4-06"></a>
### 6) 如何把这些句型用到 Behavioral answers
- 在 `Action` 里用它们把你的“执行行为”说清楚：你做了什么 + 你如何沟通对齐 + 你如何控制风险（roadblock / security risks / performance bottleneck / rollback plan / escalation）。
- 在每题结尾加一句 `Reflection`：例如 `What I learned was that early alignment on risk and communication reduces late surprises.` 或 `I improved my estimation process by validating assumptions with a pilot first.`

---

---

<a id="section-5-scripts"></a>
## C. 逐题英文稿（Q1–Q45 · **口语版**）
> 与 **[第一部分 · 规则](#section-doc-about)** 一致：**短句、常用词、STAR 心里过**；每题 **一行中文提示（关键词）** + **一版英文**。事实只来自 KB。

### 临场（极简）
- 没听清 → **clarify**。一题 **~60–120s**：**Action** 多一句。不会 → 说**怎么查、第一步干啥**。

### 常见追问
- “Hardest part?” / “How measured?” / “Differently?” / “Your role?”

### 本节怎么读
- **速览表**见下；**Q1–Q45** ≠ **B2** 编号；与 **A** 重叠的题 **练熟一边**即可。

### Q1–Q42 速览（主故事标签；Q43–Q45 无表内归类，见逐题正文）

| Q | 主题 | 主故事 / 关键词 |
|---|------|-----------------|
| 1–2 | 优势 / 劣势 | 产研桥接 + ChatClothes；讲解过深 → 分层说明 + ADR |
| 3 | 挑战项目 | ChatClothes **或** Smart Factory 电子秤 |
| 4, 22, 38 | 失败 / 延期 / 做不完 | Chinese Herbal 标注低估 → pilot |
| 5, 27, 33 | 与上级或团队分歧 | Smart Factory 分期上线 + 数据 |
| 6, 24, 42 | 难合作 / 冲突 | Enterprise Messaging 评审 → 私下 + 结对 |
| 7 | Above and beyond | ChatClothes 文档与可复现交付 |
| 8, 34, 36, 40 | 优先级 / 多解 | Smart Factory 影响 × 风险 |
| 9 | 压力 | 里程碑 + 可控动作 + 恢复习惯 |
| 10–11 | 工作风格 / 动机 | 证据驱动；真实业务影响 |
| 12, 20 | 团队 / 主导协调 | 接口契约 + 集成 Demo；弱化纯管理 |
| 13, 21 | 收反馈 / 给反馈 | ADR；Junior 文档 + 结对 |
| 14, 25, 41 | 快速学习 / 走出舒适区 / 新学 | 扩散模型 + LoRA；可测迭代 |
| 15–16 | Agile / Code review | 六年 Sprint；先理解再反驳 |
| 17, 37 | 骄傲成就 | Enterprise Messaging NDK |
| 18–19, 39 | 风险决策 / 不会答 / 全新任务 | 周五部署谨慎；诚实 + 澄清 |
| 23 | 重大变化 | ChatClothes 约束转向 |
| 26 | DEI 产品设计 | 诚实范围 + 可测包容标准 |
| 28, 35 | 持续学习 | 论文式深读 + 小实验 |
| 29–32 | Why company / 转职 | 替换占位符；**2026-02 MCIS 完成** 与 Q32 一致 |
| 30 | 模糊需求 / 系统设计 | 澄清指标 + 轻量原型 |
| 31 | 最大技术挑战 | ChatClothes 延迟剖解 |
| 43 | 代码质量 | Smart Factory 门禁 + CI + 回滚；Enterprise Messaging 高并发 |
| 44 | 团队工作流 | Smart Factory 双周 Sprint + 接口契约 + 集成 Demo |
| 45 | 辅导 Junior | Smart Factory 30/60/90 天 + 结对 + 周 1:1 |

（本节脚本共 **Q45** 题。）

<a id="q-01"></a>
### 1) What is your greatest strength?
**提示（STAR）**：（A/R）产研桥接；（证据）**ChatClothes** **Pi 5** + **Ollama** + **LoRA** + **~four months** 系统交付 + 论文；**~十年**产线习惯。
**Script（口语）**
> I link **lab ideas** to **real apps**. Proof: **ChatClothes** — **LoRA**, **Ollama** local LLM, **Raspberry Pi 5**, **~four months** on the system build, then thesis — **submitted six months early**, **First Class Honours**.
> **~Ten years** in real products — I care if it **runs**, not only demos.

<a id="q-02"></a>
### 2) What is your greatest weakness?
**提示（STAR）**：（真弱点）讲太细；（改）先 **大图** 再代码；（证据）**Smart Factory** 带人 + **ADR**。
**Script（口语）**
> I sometimes go **too deep** when I explain — juniors need the **big picture** first. On **Smart Factory** I learned to **layer**: **what/why** first, code when they ask. **Short ADRs** help me stay at the right level. I'm **better** than I used to be.

<a id="q-03"></a>
### 3) Tell me about a challenging project and how you handled it.
**提示（STAR）**：**Option A ChatClothes**（scope + **profile** + 本地 **LLM** + **YOLO12n-LC** + **提前交**）；**Option B Smart Factory 秤**（listener / watchdog / 重连）。
**Option A — ChatClothes**
**Script（口语）**
> **ChatClothes** thesis — **Pi 5**, solo, fixed time. **Profiling** showed **cloud LLM** was slow — I used **Ollama** local. Garment side: **YOLO12n-LC** instead of heavy detection. **~Four months** build, **two** thesis writing, **six months early**, **First Class Honours**.
**Option B — Smart Factory**
**Script（口语）**
> **Electronic scales** kept **dropping** weight data. I treated it as **reliability**: **persistent listener**, **watchdog**, **reconnect**, **pooling**. Data stayed, we could **debug** the next break.

<a id="q-04"></a>
### 4) Tell me about a time you failed or made a mistake.
**提示（STAR）**：**Option A** 标注估错 + **pilot**；**Option B** 发版测试配置未切 prod → 二次发版 + 流程加固；**Option C** 安全：`enterprise-messaging` 头像上传目录被利用 → 备份恢复与加固（见 [A ④ Case C](#oral-04)）。
**Option A — Herbal**
**Script（口语）**
> **Chinese herbal CV** — I said **two weeks** for labels; needed **~six** (messy photos). I **told people early**, **reset** the plan, **pilot** small sets first. Now I always **pilot** on **data** work.
**Option B — Release**
**Script（口语）**
> I shipped an **upgrade** but left **test config** in the build — it still hit the **test DB** and **test APIs**. Users saw **bad data**, so we **released again**. We were a **small team** without **dedicated QA**. After that: **split env configs**, **multi-person** checks, **test every build**, and **more automation** over time. **Lesson**: releases need **checklists**, not **memory**.
> Since then I'm **strict** on **any** update — **DB**, **app**, or **web** — same bar, no "tiny change, skip checks."
**Option C — Avatar upload security（可选）**
**Script（口语）**
> **Enterprise IM** — **avatars** on a **Windows** server. **Upload** was **too open**; someone dropped **executables** in the **avatar** folder and the machine got **owned**. We **lost** trusted state there — **rebuilt**, **restored** from **backup**. After that: **lock down** permissions, **AV** on hosts, **validate** uploads, and we **moved** files to **cloud** with **tighter** rules. **Lesson**: **upload** == **attack** **surface**.

<a id="q-05"></a>
### 5) Tell me about a time you disagreed with your manager or a decision.
**提示（STAR）**：**Smart Factory** 先加功能 vs 先上线；（A）影响表 + **分期** + **试点**；（R）采纳、上线稳。
**Script（口语）**
> **Smart Factory** — PM wanted **more features** before first launch; I wanted a **tight core** — factories **trust** stable software. I **mapped impact**, pushed **phased** rollout: **core**, **pilots**, **~sixty days**, then add from **real** feedback. They agreed; pilots **worked**. **Data**, not ego.

<a id="q-06"></a>
### 6) Tell me about a time you worked with a difficult person.
**提示（STAR）**：**Enterprise Messaging**；**1:1** + **私下** review + **结对**。
**Script（口语）**
> **Enterprise Messaging** — teammate **avoided** review after **public** criticism elsewhere. I went **1:1**, then **private**, **specific** notes, short **pairing**. Reviews and **releases** got **healthy** again.

<a id="q-07"></a>
### 7) Tell me about a time you went above and beyond.
**提示（STAR）**：**ChatClothes** 额外 **部署文档 / API / 手册**；（R）导师认可 + **提前交**。
**Script（口语）**
> **ChatClothes** — school asked demo + thesis; I added **deploy docs**, **API** spec, **user manual** so others could **run** it alone. Supervisor **praised** the docs. I **submitted six months early** — writing forced **clear** design choices.

<a id="q-08"></a>
### 8) How do you prioritize when you have multiple deadlines?
**提示（STAR）**：**影响 × 风险**；**Smart Factory** **产线** 优先；需求模糊时 **下车间 + 快原型** 定下一刀切什么（见 [A ⑥ Case B](#oral-06)）；早说 **排序变化**。
**Script（口语）**
> I sort by **impact** and **risk**, not loudest voice. **Smart Factory** — **production** issues before **nice-to-have** features when users are **on the line**. Then **milestone** work. I **say early** when order **changes**. We kept **uptime** and still **shipped**.

<a id="q-09"></a>
### 9) How do you handle stress and pressure?
**提示（STAR）**：**习惯**：里程碑 + 范围 + 节奏；**故事（可选）**：`enterprise-messaging` 早期单人安卓日更救火，见 [A ⑤ Case B](#oral-05)。
**Script（口语）**
> I **cut unknowns early** — **milestones**, **check-ins**. Under heat: **smaller scope**, **stable core** first, then grow. **Routine** and **exercise** to reset. **ChatClothes** was tight — **early plan** helped me **finish ahead**.
> When it was really hot — like **solo Android** on our **enterprise IM** app after a fast launch with **many bugs** — I used a **daily** list, **priority** order, **ship a build** every day, and let **product** help users with **honest** timelines. **Rhythm + clarity** beats panic.

<a id="q-10"></a>
### 10) How would you describe your work style?
**提示（STAR）**：先模型再下钻；**测/原型**；**review** 友好。
**Script（口语）**
> **Think in systems**, then go **deep** where it matters. I **measure** or **prototype** instead of **debating guesses**. **Pairing** and **review** save **rework**. I also **fix the process** each round.

<a id="q-11"></a>
### 11) What motivates you at work?
**提示（STAR）**：真问题 + **长期能跑**；**Smart Factory** / **ChatClothes**。
**Script（口语）**
> **Real users**, software that **keeps working**. **Smart Factory** — people on the **floor** felt the win. **ChatClothes** — hard **AI** under **real** limits. I like **long-lived** systems.

<a id="q-12"></a>
### 12) Tell me about a time you worked effectively in a team.
**提示（STAR）**：**6 人**跨职能；**接口文档 + 24h**；**周 demo**；**10+ 厂**。
**Script（口语）**
> **Smart Factory** — **six** people: backend, frontend, **Android** (me early), **IoT**, QA. We used a **shared API contract** + **24-hour** review before breaks. **Weekly demos** with **running** code. **~Six years**, **10+ factories** — **clear interfaces** and **rhythm**.

<a id="q-13"></a>
### 13) Tell me about feedback you received and how you acted on it.
**提示（STAR）**：经理要 **手写架构决策**；（A）**ADR** + **onboarding**；（R）新人更快。
**Script（口语）**
> Manager said big **design choices** weren't **written** for **handover**. I added **light ADRs** and a **short onboarding** guide. **Ramp** got faster; fewer **repeat** questions. Docs became my **habit**.

<a id="q-14"></a>
### 14) Describe a time you had to learn something quickly.
**提示（STAR）**：**ChatClothes** **扩散/ OOTDiffusion**；**论文→跑通→LoRA**；**~六周**实验。
**Script（口语）**
> **ChatClothes** — **diffusion** / **OOTDiffusion** was new. **~Two months** target to **fine-tune**. Path: **paper → stack → run code → trace** what matters. **~Six weeks** I was doing **LoRA** runs — **PyTorch** / **HF** I already knew.

<a id="q-15"></a>
### 15) Are you comfortable working in an Agile team?
**提示（STAR）**：**Smart Factory** **双周 Sprint** **六年**；价值在 **demo**。
**Script（口语）**
> Yes. **Smart Factory** — **two-week sprints** for **~six years**: standup, plan, retro, sizing. Best part: **demo** shows **real** software each sprint — **honest** progress bar.

<a id="q-16"></a>
### 16) How do you handle code review feedback?
**提示（STAR）**：先听 **why**；不人身攻击；给反馈要 **具体**。
**Script（口语）**
> I **pause** and **ask why** — often they caught a real issue. If I still disagree, I **explain trade-offs**, not ego. I don't **ignore** comments or take them **personal**. When I **give** feedback: **on the code**, **specific**, **why**.

<a id="q-17"></a>
### 17) Tell me something you built that you’re genuinely proud of.
**提示（STAR）**：**Enterprise Messaging** **NDK**；**sub-200ms**；**5k DAU**；**10+ 年**还在跑。
**Script（口语）**
> **Enterprise Messaging** **native** path — **C** **TCP/UDP**, **JNI**, custom protocol. Needed **sub-200ms** at **~5k DAU**; **Java** alone couldn't hold it. It's been in **prod 10+ years**. **Long life** is what I'm proud of.

<a id="q-18"></a>
### 18) If you were the last member of the team in the office on a Friday afternoon and the product owner asks you to deploy a change to production, what would you do?
**提示（STAR）**：周五 → **慢**；验范围/流水线/**回滚**；不行 → **升级**下一窗口。
**Script（口语）**
> **Friday** deploy — I **slow down**. Check **scope**, **tests**, **rollback**, **release** notes. If I **can't** verify — I **escalate** and aim for **next window**. If we ship — I **watch** logs and stay **ready to roll back**. **No guess clicks**.

<a id="q-19"></a>
### 19) How would you respond if you don’t know the answer to a question?
**提示（STAR）**：不装懂；**澄清**；说会什么 + **怎么查** + **可跟进**。
**Script（口语）**
> I **won't fake** it. I **clarify** what you need, say what I **know**, and if I lack a fact I say **how** I'd check — **docs**, **code**, **incidents** — and **follow up** after.

<a id="q-20"></a>
### 20) Describe a time when you led a team. What was the outcome?
**提示（STAR）**：（弱化纯管理）**技术协调**；**Smart Factory** **接口契约** + **周 demo**；**10+ 厂**。
**Script（口语）**
> I see it as **tech leadership**, not just **manager**. **Smart Factory** — **six** of us, **10+ factories** over years. **Integration** was the risk — I pushed **clear API contracts**, **short** review before breaks, **weekly** **integrated** demos. We **shipped** with **strong uptime** and **repeatable** rollouts.

<a id="q-21"></a>
### 21) Describe a time when you had to give someone difficult feedback. How did you handle it?
**提示（STAR）**：Junior **文档**薄；（A）先夸 + **具体**标准 + **结对**；（R）评审顺了。
**Script（口语）**
> Juniors — code OK, **docs** weak. I started with **what worked**, then **clear cost** for the next person. Gave a **small template**, **paired** once. Over time **reviews** got easier.

<a id="q-22"></a>
### 22) Tell me about a time when you missed a deadline. What happened, and how did you handle it?
**提示（STAR）**：同 **Q4** 中草药标注；**早沟通** + **pilot**。
**Script（口语）**
> **Herbal CV** — labels took **~six weeks**, not **two**. I **owned** it, **reset** dates, **piloted** throughput. **Honest early** beats **silent slip**.

<a id="q-23"></a>
### 23) Tell me about a time when you had to deal with a significant change at work. How did you adapt to this change?
**提示（STAR）**：**ChatClothes** 约束变；（A）**重测** + **LLM** 本地 + 控范围；（R）全链路可跑。
**Script（口语）**
> **ChatClothes** — **offline** + **speed** became hard rules. I **re-measured**, moved **LLM** **local**, **cut** scope where needed, **shipped** a full **pipeline** that fit the box.

<a id="q-24"></a>
### 24) Describe a time when there was a conflict within your team. How did you help resolve it? Did you do anything to prevent it in the future?
**提示（STAR）**：同 **Q6** **Enterprise Messaging**；**私下** + **具体** + **预防**：反馈方式。
**Script（口语）**
> **Enterprise Messaging** — review felt **personal** to one person. **1:1**, **private** feedback, **pairing**. Later I kept feedback **specific** and **kind** — **review** as **help**, not **attack**.

<a id="q-25"></a>
### 25) Describe a time when you went out of your comfort zone. Why did you do it? What lessons did you learn from the experience?
**提示（STAR）**：**ChatClothes** 快速学 **diffusion**；**跑代码 + 论文**；**迭代**。
**Script（口语）**
> **ChatClothes** — I had to learn **diffusion** fast. **Paper** + **run inference** + **trace** code — don't read forever before **touching** the repo. **Lesson**: **theory + small experiments** beat **pure reading**.

<a id="q-26"></a>
### 26) How would you design/test a product to make sure its diverse/inclusive to all users?
**提示（STAR）**：诚实没包办过 **D&I 项目**；**可测**标准（**a11y**、语言、弱网）+ 用户样本 + 早测。
**Script（口语）**
> I haven't owned a full **D&I** program — as an engineer I'd set **clear**, **testable** goals: **accessibility**, **plain** language, **low** bandwidth. **Talk to diverse users**, test **contrast** / **font** / **screen reader** **early**, **loop** until it passes.

<a id="q-27"></a>
### 27) Tell me about a time you disagreed with a colleague. How did you handle the situation?
**提示（STAR）**：同 **Q5** **Smart Factory** **分期**。
**Script（口语）**
> **Smart Factory** — I wanted **stable core** first; others wanted **more features** before launch. I used **data**, proposed **phased** rollout and **pilots**. Team agreed; **real** feedback guided the next steps.

<a id="q-28"></a>
### 28) How do you stay up-to-date with the latest technological advancements?
**提示（STAR）**：**读 + 小实验**；**论文/官方仓库**；笔记。
**Script（口语）**
> **Read** serious sources, then **build tiny** proofs — that's how I went **ML → diffusion / LoRA**. I **prototype** instead of only **bookmarking**. Short **notes** so it **sticks**.

<a id="q-29"></a>
### 29) Why are you interested in working at [company name]?
**提示（STAR）**：换 **[Company]**、**[why fill]**；对齐 **Android/后端/AI**；**ChatClothes + Smart Factory** 证据。
**Script（口语）**
> I'm interested in **[Company]** because **[product / team / stack — fill]**. It matches how I ship — **mobile**, **Java** backend, **applied AI**. **ChatClothes** and **Smart Factory** show I care about **real** delivery.

<a id="q-30"></a>
### 30) Assume you are given a task to design a system. How would you do it? How would you resolve ambiguity?
**提示（STAR）**：问清 **目标/约束**；**画架构**；**spike** 模糊点；**写**大决策；模糊需求时 **下车间/用户** + **快原型** 验证（见 **A ⑥ Case B**）。
**Script（口语）**
> I **ask** until **goals** and **constraints** are clear — put **unknowns** on the table. Sketch **architecture** and **interfaces**, **spike** if two paths are fuzzy. **Document** big calls, **iterate** with **feedback** and **numbers**. When users only have a **fuzzy** picture, I **go to the floor**, **prototype fast**, and **tighten** requirements from **what they actually do**.

<a id="q-31"></a>
### 31) What is the biggest technical challenge you have worked on?
**提示（STAR）**：**ChatClothes** **端到端延迟** + 离线；（A）**profile** → **LLM** 本地 + **YOLO12n-LC**；（R）可演示 + **早交论文**。
**Script（口语）**
> **ChatClothes** — make the **whole** path **fast** on **small** hardware **offline**. I thought **diffusion** was the problem — **profiling** showed **LLM** **cloud** trips were. I went **local LLM**, lighter **vision** (**YOLO12n-LC**). **System worked**; thesis **handed in early**.

<a id="q-32"></a>
### 32) Why do you want to change your current company?
**提示（STAR）**：（与 `kb/profile.yaml`）**2026-02** **AUT MCIS** **First Class**；**PSWV**；学业结束 → 要 **全职交付**。
**Script（口语）**
> I finished **MCIS** at **Auckland University of Technology** in **Feb 2026**, **First Class Honours** — **ChatClothes** is my main **AI** piece. I'm in **Auckland** with **full-time** rights (**PSWV**). I want **full-time engineering** again — **Android** / **backend** / **applied AI** — moving from **study** back to **shipping** on purpose.

<a id="q-33"></a>
### 33) Tell me about a time when you had a different opinion than the rest of the team. How did you handle it?
**提示（STAR）**：同 **Q5** **分期上线** + **试点**。
**Script（口语）**
> **Smart Factory** — I wanted **small stable** first launch; others wanted **more features**. I argued **trust** on the **floor** beats **half-broken** breadth. We used **data**, **phased** rollout, **pilots**. Team aligned; **users** guided what came next.

<a id="q-34"></a>
### 34) Tell me about a time when you were faced with a problem that had a number of possible solutions. What was the problem and how did you determine the course of action? What was the outcome of that choice?
**提示（STAR）**：**产线** vs **里程碑**；（A）**影响×风险**排序；（R）**uptime** + 计划仍推进。
**Script（口语）**
> **Smart Factory** — **live** issues vs **feature** deadlines. I ranked by **risk** and **impact** — **fix production** first, then **milestone** work. **Told** people when order **shifted**. **Uptime** held; roadmap **moved**.

<a id="q-35"></a>
### 35) What do you do to enhance your technical knowledge apart from your project work?
**提示（STAR）**：**读 + 小原型**；短笔记。
**Script（口语）**
> I **read**, then **build small** demos — thesis was **read → try → ship**. I keep **short notes** on what **worked** so I don't **forget**.

<a id="q-36"></a>
### 36) How do you prioritize your workload? What do you do when your work feels like it's just too much to get done?
**提示（STAR）**：**影响+风险**；**切块**；**早说**；必要时 **砍范围**保核心。
**Script（口语）**
> **Too much** work — I sort **impact** and **risk**, break into **chunks**, **say early** if dates move. If needed I **cut** scope to save the **must-have**, then **grow** back when **stable**.

<a id="q-37"></a>
### 37) What’s the Number One Accomplishment You’re Most Proud Of?
**提示（STAR）**：同 **Q17** **NDK** 消息；**sub-200ms**；**5k DAU**；**长寿**系统。
**Script（口语）**
> **Enterprise Messaging** **NDK** stack — **sub-200ms**, **~5k DAU**, **C** sockets + **JNI**, still **running 10+ years** in prod. **Shipping** is easy; **surviving** load is the win.

<a id="q-38"></a>
### 38) Tell me about a time when you had an excessive amount of work and you knew you could not meet the deadline. How did you manage then?
**提示（STAR）**：同 **Q4/Q22** 标注；**拥有延误** + **pilot** + 新计划。
**Script（口语）**
> **Herbal** labels — timeline **wasn't real**. I **owned** it, **new** schedule, **pilot** to know **speed** and **error rate**. **Cleaner** data, **better** next estimate.

<a id="q-39"></a>
### 39) What will be your course of action if you are assigned some task which you don’t know at all?
**提示（STAR）**：**澄清 → 学 → 小交付**；保持同步。
**Script（口语）**
> **Clarify** scope, learn from **good** sources, **tiny** **shippable** slice, **test** it, **update** stakeholders while I learn. No **silent** drift.

<a id="q-40"></a>
### 40) Describe a time when you had to work simultaneously on both high-priority urgent projects as well as long-term projects. How did you go about handling both?
**提示（STAR）**：**Smart Factory** **火** + **路线图**；（A）先 **产线** 再 **里程碑**；（R）稳 + 仍交付。
**Script（口语）**
> **Smart Factory** — **urgent** **prod** and **long** roadmap together. **Prod** first where users **depend**, then **milestone** tasks. **Clear** dates, **small** tasks — **ops** stable, features still **moved**.

<a id="q-41"></a>
### 41) What is something new that you’ve learned recently?
**提示（STAR）**：**AI** 在 **弱硬件/离线** 下要 **profile 全链路**。
**Script（口语）**
> Going **deeper** on **AI** under **tight** **latency** and **offline** — **profile** the **whole** path, not only the **model**. I use that for **research** and **prod** bugs now.

<a id="q-42"></a>
### 42) Tell me about a time when you had a hard time working with someone in your team. How did you handle it?
**提示（STAR）**：同 **Q6/Q24**。
**Script（口语）**
> **Enterprise Messaging** — someone **froze** on **review**. **Private** talk, **gentle** **specific** notes, **pair** a bit. **Quality** and **mood** improved; **same playbook** as conflict question.

<a id="q-43"></a>
### 43) How do you assure code quality in your team?
**提示（STAR）**：**防**（规范+**CI**+**review**）/**抓**（测+**集成 demo**）/**救**（监控+**回滚**+复盘）。
**Script（口语）**
> **Prevent**: standards, **CI**, **mandatory** review. **Catch**: tests + **weekly integrated** demos (**Smart Factory**). **Recover**: **monitoring**, **rollback**, **postmortem**. That mix kept **uptime** across **sites**.

<a id="q-44"></a>
### 44) Describe the project workflow in your previous team.
**提示（STAR）**：**双周 Sprint** **六年**；**demo**；**接口契约**。
**Script（口语）**
> **Smart Factory** — **two-week sprints** **~six years**: plan, standup, review, retro. Every sprint **demo** with **real** software. **Shared API contracts** before **breaking** changes — **mobile**, **backend**, **IoT** stayed aligned.

<a id="q-45"></a>
### 45) How do you support and track a junior developer's progress?
**提示（STAR）**：**30/60/90**；**结对**+**review**当教练；**周 1:1**；看 **质量/独立交付** 非只看工单数。
**Script（口语）**
> **30/60/90** goals with **clear** tasks. **Pair** and use **review** as **coaching**; **weekly 1:1** for blockers. I watch **quality** and **shipping**, not only **ticket** count. **Light checklist** for **self-check**.

---

<a id="section-appendix"></a>
<a id="section-personal-drafts"></a>
## 附录 · 个人素材

### 个人素材补全（草稿 · 与工程事实对齐）

> **用途**：你往这里贴**新故事、新指标、新复盘**；整理满意后，再同步到 [口语专页](#section-oral-only)、[B2 STAR 备忘](#section-2-star-brief)、[C 逐题英文稿](#section-5-scripts)，并与该节 Q 速览里的主故事标签保持一致。  
> **硬约束**：数字、职责、时间线只能来自已有 YAML（`kb/*.yaml`、`projects/*/facts.yaml`）。缺事实就写 `MISSING_INFO`，不要先写进正式口语稿。  
> **和 AI 协作**：粘贴素材时带上 **项目 id**（如 `chatclothes`、`smart-factory`）和「想覆盖的面试题类型」，便于把草稿合并进全篇且不越界编造。

### 单条故事模板（复制填空）

```
【项目 id】projects/__________/facts.yaml（或 kb 条目）
【适用题型】如：冲突 / 失败 / 压力 / 技术深度 / 主动性 …
【STAR-R 草稿】
- Situation:
- Task:
- Action:（动词开头，写你具体做了什么；可中英混记要点）
- Result:（尽量可核对；无出处则标 MISSING_INFO）
- Reflection:（一句可迁移的行为改变）
【追问预案】What was hardest? / How measured? / What differently? / Your role?
【合并状态】□ 已进口语 □ 已进 STAR □ 已进 Q__ 脚本 □ 已更新故事映射
```

### 素材收件箱（按时间追加；以下为占位，可删）

- （在此逐条追加你的草稿，或新建 `interview_qa/behavioral_drafts_YYYY-MM-DD.md` 只存长文，本页只保留链接一行。）
- 【2026-05-05 新增】`enterprise-messaging` / Android 稳定性与崩溃治理（可用于：复杂技术问题、故障处理、质量保障、学习成长）
  - Situation: 即时通讯 App 有阶段性崩溃；早期没有成熟第三方崩溃 SDK，用户手动上传日志效率低、覆盖差。
  - Task: 在不依赖用户手工操作的前提下，自动采集崩溃信息并回传平台；同时降低图片相关 OOM 崩溃。
  - Action: 早期自研崩溃捕获与自动上报机制（崩溃后自动收集并上传）；后续逐步接入成熟方案。针对 OOM，补齐图片加载库能力与内存控制策略，避免大图直接压爆内存。
  - Result: 崩溃问题可被更快定位，线上排障效率提升；图片类内存溢出问题明显收敛（量化指标待补：`MISSING_INFO`）。
  - Reflection: 稳定性要前置建设：日志链路自动化 + 内存边界管理，比事后让用户“复现并上传”更可靠。
  - 用户追问场景（常见对比）：用户会问“为什么微信能长期后台存活，你们不行？”
    - 回答要点：主流大体量 App 常被厂商策略优待（内置白名单/更高保活策略），中小体量 App 通常不在该范围。
    - 可执行动作：我们提供用户侧引导（手动加入电池白名单、后台运行权限、通知权限、桌面 widget 等）来提高存活优先级。
    - 沟通口径：耐心解释“不是不做，而是系统策略边界不同”；承诺我们会持续优化“被杀后快速恢复 + 消息重同步”。
- 【2026-05-05 新增】`MISSING_INFO(project_id)` / 勒索病毒与灾难恢复沟通（可用于：危机处理、决策取舍、客户沟通、数据恢复）
  - Situation: 服务器遭遇勒索病毒，数据库与图片文件受影响；部分数据在云数据库，部分在自建环境，头像文件出现不可读，存在用户数据丢失风险。
  - Task: 在不支付赎金的前提下尽可能恢复业务与数据，并同步处理“谁承担恢复成本、如何对外沟通”的决策压力。
  - Action: 明确不把“支付赎金”作为主方案；优先走备份与恢复链路。数据库侧采用日志恢复（而非直接回滚到旧库）以尽量减少数据损失；文件侧通过备份恢复可恢复资产。并行准备对用户的事实说明：当前影响范围、恢复路径、预计时间、剩余风险。
  - Result: 在高压下推进可验证恢复路径，并把技术恢复与客户沟通同步推进；最终恢复程度与损失范围待补：`MISSING_INFO`。
  - Reflection: 灾难场景里，技术动作和沟通动作必须并行；“不确定性透明化 + 可执行恢复计划”比承诺不确定结果更重要。
- 【2026-05-05 新增】`MISSING_INFO(project_id)` / 团队技术选型分歧（可用于：Conflict / 决策 / 影响力）
  - Situation: 新项目立项期，团队对技术栈有分歧；资深同事偏向熟悉的旧栈（如 C# / C++），而项目需求与长期方向更偏向新技术方案。
  - Task: 在保证可交付与风险可控的前提下，达成团队共识，而不是陷入“个人偏好之争”。
  - Action: 拉齐 PM、TL、相关同事做联合评估：时间成本、交付风险、可维护性、团队学习成本、与项目方向匹配度；将讨论从“谁熟悉什么”改为“项目现在和未来最合适什么”。
  - Result: 形成共识技术方案，减少争执，推进节奏恢复（具体项目名与量化结果待补：`MISSING_INFO`）。
  - Reflection: 技术选型冲突本质是决策框架问题；透明评估标准比个人资历更能建立信任。
- 【2026-05-05 新增】`MISSING_INFO(project_id)` / 跨部门需求冲突与折中上线（可用于：Conflict / Stakeholder Management / Prioritization）
  - Situation: 产品侧提出“竞品有、我们也要马上上”的需求，时间紧，技术实现复杂，存在稳定性与交付风险。
  - Task: 在不破坏协作关系的前提下，避免不现实承诺，推动形成可落地方案并按时上线可用价值。
  - Action: 用非技术语言讲清技术边界与实现成本；给出分级选项（MVP 先上 / 分期上线 / 完整版本后置），并与产品、TL、PM对齐时间、质量与用户影响三方取舍。
  - Result: 从“为什么做不到”转为“先做什么最值”，形成双方可承诺的路线并保持交付节奏（项目名与量化结果待补：`MISSING_INFO`）。
  - Reflection: 跨部门冲突核心不是对错，而是把隐性工程成本显性化，并给出可执行折中路径。
- 【2026-05-05 新增】`smart-factory` / 真实需求甄别失败与复盘（可用于：失败复盘 / 产品协作 / 用户导向 / 冲突）
  - Situation: 工厂项目中，团队（含 PM、产品、开发）希望提升工人效率，设计了“单件衣服部件编码 + 扫码拼接 + 逐件流转”的功能。
  - Task: 通过数字化拆解与逐件追踪，减少堆积、提高节拍，并推动工序更顺滑地流转。
  - Action: 功能按“用户视角”推进并上线，但上线后持续观察真实使用行为与采用率。
  - Result: 使用率不高，工人仍主要沿用“同款批量匹配、整批流转”的旧流程；说明“看起来合理”的需求不等于“现场高频真实需求”（量化采用率待补：`MISSING_INFO`）。
  - Reflection: 产品、开发都要做需求甄别与现场验证；应先用小范围试点/可用性验证，避免把理想流程直接全量产品化。
  - 补充原则：一线工人常按“本工位最方便”提需求，但系统设计要看**端到端流程最优**；“提出需求”不等于“必须实现”，需评估对上游/下游、节拍与整体吞吐的影响。
  - Suggested line (EN): "Workers often ask for what is easiest at their station, but we must optimize the end-to-end flow. A request is important input, not an automatic must-build item."
- 【2026-05-05 新增】`cross-project` / 分歧无法调和时的执行原则（可用于：Conflict / Stakeholder / Leadership）
  - Principle: 当团队充分讨论后仍无法达成一致，执行层遵循“最终决策责任人”（decision owner）的结论，而不是开发者个人偏好。
  - Execution posture: 即使个人观点不同，仍负责把方案执行好，并提前暴露风险、持续反馈执行结果。
  - Suggested line (EN): "When we can’t fully align, we follow the final decision owner, not individual developer preference. My job then is to execute well and surface risks early."
- 【2026-05-08 新增】`enterprise-messaging` / 发版失误：测试配置未切生产（可用于：Failure / 流程改进 / 质量保障）
  - Situation: APP 升级发版；构建仍使用测试侧配置（测试库、测试接口），因发布前未将配置从测试切换为正式。
  - Task: 用户侧发现数据/行为异常后，需尽快纠正并重新发布可用版本。
  - Action: 紧急二次升级切换为正式环境配置；事后拆分多环境配置文件、加强发布前多人多轮验证；逐步引入更多自动化以减少人为漏操作（当时尚未完全自动化）。
  - Result: 问题通过二次发版收敛；团队发布纪律与检查机制加强（具体影响范围、时长待补：`MISSING_INFO`）。
  - Reflection: 发版不能依赖“记得改一处配置”；要靠环境隔离、清单与自动化兜底。此后对各类更新一律同等认真：**数据库**、**APP**、**网页**发布均按同一套纪律执行，不因“改动小”而省略验证。
- 【2026-05-09 新增】`smart-factory` / 下车间 + 无对标 + 模糊需求下的优先级（可用于：Prioritization / Ambiguity / Stakeholder / 产品迭代）
  - Situation: 智能工厂类项目缺乏可直接对标的产品；需深入车间了解工人与工厂侧诉求；用户侧往往只有模糊目标，需求高度不确定；团队需在强时间压力下快速出可用原型并持续调整。
  - Task: 在信息不完整的情况下，与团队商议制定可执行的开发周期与任务切分；通过迭代把「模糊要求」逐步变成可交付、可验证的范围。
  - Action: 下车间观察与访谈，把现场流程与痛点具象化；优先落地可演示原型，用原型与用户反复确认；根据反馈调整优先级与版本范围；首版交付后如未获充分认可，则推动更大范围的需求重梳与后续大版本演进（功能随真实使用增加或精简）。
  - Result: 经多轮大版本迭代，产品方向随现场验证逐步收敛（具体版本数、周期、量化指标待补：`MISSING_INFO`）。
  - Reflection: 无对标、强模糊场景下，「快原型 + 短周期验证」比长文档更能定义真实优先级；大版本调整是常态而非失败，关键是团队对外透明、对内可执行。
  - Suggested line (EN): "We had no reference product — we earned priorities on the shop floor: fast prototypes, tight feedback loops, and honest replans when the first release still didn’t match what people actually needed."
- 【2026-05-08 新增】`enterprise-messaging` / 早期单人安卓：企业即时通讯客户端，原型窗口上线后高压修 bug（可用于：Under pressure / Prioritization / Stakeholder）
  - Situation: 企业即时通讯（IM）产品极早期，团队侧 Android 开发仅一人；需在约数周内完成原型、测试并上线。
  - Task: 上线后集中暴露大量缺陷，需在用户期望与修复/发版进度之间承压推进。
  - Action: 每日整理缺陷清单并按优先级排序；优先修复高优先级问题；尽量每日发布一版供验证，迭代收敛；与产品/设计协作，由其对用户解释原因、修复预期、优先级与计划日期，并同步每日变更与已解决问题（修复可能引入新问题，持续重排优先级直至稳定）。
  - Result: 缺陷逐步收敛，产品趋于稳定（具体周数、发版次数等量化待补：`MISSING_INFO`）。
  - Reflection: 高压下靠「可见优先级 + 固定发版节奏 + 跨职能对用户透明」；单靠开发扛沟通会放大压力。
- 【2026-05-09 新增】`enterprise-messaging` / 头像存储上传权限疏漏致入侵与恢复（可用于：Security / Production incident / Failure / 从教训到流程改进）
  - Situation: 企业即时通讯的用户头像存放在 Windows 文件服务器上；文件上传相关权限与校验不足，攻击者利用后在头像目录写入可执行文件，导致服务器中毒；出现数据丢失或数据不可信，业务需从干净基线恢复。
  - Task: 控制影响、恢复可用服务与用户数据，并在事后降低同类风险。
  - Action: 重新部署环境；以备份数据恢复可恢复部分；团队强化安全意识，部署防病毒软件，收紧目录与上传权限；后续将头像/用户文件整体迁移至云端对象存储等托管服务，配合更严格的访问与上传策略。
  - Result: 服务从备份与重建路径恢复；文件存储架构向云端与更强管控演进（具体停机时长、影响用户数待补：`MISSING_INFO`）。
  - Reflection: 用户上传路径必须按攻击面设计：最小权限、内容类型与白名单、上传目录与可执行环境隔离；备份与可重建演练不是“可选项”。若与「勒索病毒/灾难恢复」条目在事实层面为同一事件链，口试时可合并为一条叙事；若确认为独立事件则分开讲。
  - Suggested line (EN): "We treated avatar uploads like a product feature — but the server treated that folder like a trusted path. Tight ACLs, validation, and moving blobs to cloud storage with least-privilege access became non-negotiable after we paid the restore tax once."
