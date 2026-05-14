# Behavioral Interview — Leo Zhang

## 目录（概要）

| Part | 内容 | 跳转 |
|----|------|------|
| Part 1 | **Core Behavioral Answers**：10 个最高频主答，先看这个 | [→](#section-oral-only) |
| Part 2 | **Project Story Bank**：按项目归类的故事仓库 + B1/B2 分类索引 | [→](#section-part-b) |
| Part 3 | **Question Script Bank**：Q1–Q45 全文脚本 + 深挖细节 | [→](#section-5-scripts) |
| Part 4 | **Quick Review & Appendix**：工具、速查、素材草稿与收件箱 | [→](#section-toolbox) / [→](#section-appendix) |

> 细粒度锚点（如 `oral-01`、`b1-03`、`q-12`、`d3-04`）在**正文各小节标题上方**；需要时搜索 `id="q-12"` 或先打开对应 Part 再按 `### 12)` 等标题浏览。

---

<a id="section-doc-about"></a>
## Part 1 — Core Behavioral Answers

This is the main speaking path. Use Part 1 first, then jump to the story bank, deep-dive scripts, or quick review only when you need more detail.

本文件是 **Behavioral 面试**用：**Part 1** 放 10 个最高频主答，**Part 2** 放故事库，**Part 3** 放 Q1–Q45 全文脚本/深挖，**Part 4** 放速查/工具。

### 规则（可在此往下加你自己的）

- **先想为什么问**，再答到点上（别只堆经历）。
- **事实**：数字与经历只来自 `kb/*.yaml`、`projects/*/facts.yaml`；我会在对话中提到新的事实，要持久化到项目中。
- **口语**：短句、好念；**常用词**优先；**A** 主练，**C** 当辞典；临场改口，别背稿腔。
- **篇幅**：**①、⑩** 备 **30 秒 + 1 分钟** 两档；**②—⑨** 与 **C 节**每题 **一版**口稿即可，长短临场伸缩。
- **STAR**：心里过 **S→T→A→R**；正文里用 **一行中文提示（关键词）** 帮你对齐，英文口稿保持简洁。
- **改结构**：尽量别删 `oral-*` / `q-*` / `section-*` 锚点。


---
<a id="section-oral-only"></a>
### A. 临场开口

> **版面**：**①、⑩** = **30 秒 + 1 分钟**；**②—⑨** = **每题一版**。下方 **提示（STAR）** 为中文关键词，英文为口稿。

<a id="oral-01"></a>
### ① Tell me about yourself

**Key idea:** 先年限和方向，再 AUT / ChatClothes / 现在能做什么。

#### 30 秒版（约 30s）

Hi, I'm **Leo Zhang**, a software engineer based in **Auckland** with around **thirteen years** of experience across **Android**, **Java backend**, **full-stack** development, and **applied AI**.

Most of my work has been in real production environments, including **Smart Factory** systems for manufacturing sites and an **Enterprise Messaging** platform with real-time communication and large-scale mobile/backend integration.

I recently completed my **Master of Computer and Information Sciences** at **AUT** with **First Class Honours**. My thesis, **ChatClothes**, focused on lightweight offline AI using local **LLMs** and **LoRA** models.

I'm now looking for a role where I can combine strong engineering delivery with full-stack and AI-focused work in New Zealand.

#### 1 分钟版（约 60–90s）

Hi, I'm **Leo Zhang**, a software engineer based in **Auckland**. I have around **thirteen years** of experience across **Android** development, **Java backend** systems, **full-stack** engineering, and more recently **applied AI** projects.

A big part of my background comes from **enterprise and industrial systems**. I worked on **Smart Factory** platforms used across manufacturing sites, involving shop-floor workflows, hardware integration, backend services, web systems, rollout coordination, and operational support. I also worked on an **Enterprise Messaging** platform focused on real-time communication, Android background reliability, and large-scale mobile/backend integration.

Over the years, I've worked across multiple layers of systems — mobile clients, backend services, web platforms, deployment workflows, and production support — especially in environments where stability and real operational constraints mattered a lot.

More recently, I completed my **Master of Computer and Information Sciences** at **AUT** with **First Class Honours**, focused on applied AI. My thesis project, **ChatClothes**, explored lightweight offline AI deployment using local **LLMs**, **LoRA** optimization, and constrained hardware environments.

Overall, I enjoy building practical systems end-to-end and solving messy real-world engineering problems. I'm now looking for a role where I can continue combining software engineering, full-stack delivery, and applied AI work here in New Zealand.

<a id="oral-02"></a>
### ② Complex technical problem

**Key idea:** 讲 Android 后台收消息，强调多层保活和主通道/备用通道。

One complex problem I worked on was **real-time messaging** on Android.

The challenge was that Android aggressively kills background processes to save battery, especially on some OEM systems like Xiaomi or Huawei. But for an enterprise messaging app, users still expect messages to arrive reliably and quickly.

So the problem wasn't just "send a message." It was really about background survival, reconnect reliability, and balancing real-time performance against battery usage.

We used a layered approach.

For the main messaging path, we used **Easemob** for core IM delivery. Then we added **JPush** as a secondary push channel for notification-style wake-ups, so we weren't depending on only one mechanism when Android became aggressive about background restrictions.

On the client side, we also optimized heartbeat and reconnect strategy, handled fast session recovery after process death, and added state reconciliation between local cache and server state to reduce message inconsistency issues.

Another difficult part was **Android fragmentation**. Different OEM ROMs behaved differently, and some bugs only appeared on real user devices — not in emulators. So we had to balance release speed, test coverage, and device cost realistically. We focused on strong mainstream device coverage first, then reproduced edge cases on exact hardware when important issues came in.

The result was much better background message reliability and fewer missed-message complaints.

What I learned is that on Android, reliability usually doesn't come from one trick — it comes from **multiple layers** working together.

**（延展）Enterprise IM — Android OEM / version fragmentation**  
Another messy side wasn't only **logic** — it was **where** the app ran. **Enterprise IM** still hits a **consumer-style Android long tail**: many OS levels, and in China **Xiaomi**, **Huawei**, **OPPO** ROMs change behavior again.

We focused routine QA on **mainstream** devices and versions — roughly down to **Android 7 or 8** as our lab floor; older phones we usually didn't keep. Brand-new OS drops sometimes lagged because we didn't own the hardware yet.

Users still reported bugs we couldn't replay on an emulator with the same API level — **vendor layers matter**. When we were stuck, we **bought a target phone**, or worked with the user **remotely / on-site** to see their real settings.

A lot of issues only **showed up in real user environments** — permissions, power policies, OEM tweaks we didn't mirror in the lab. The **usage surface** is too wide to **pre-catch** every **small** defect without paying **huge** time, people, and **device** money.

So we **balanced** three things: **release clock**, **how deep we test**, and **what hardware we can afford** to keep in-house. **Perfect** pre-release coverage wasn't the goal — **good** mainstream gates plus **fast** **narrow** follow-up when **signals** were **strong** was.

Ideally you'd run a **full matrix** before every ship — reality is **cycle time** and **cost**. We shipped on strong mainstream coverage, then closed repro on the **exact device path** when tickets came in.

<a id="oral-enterprise-files"></a>
### （补充）Enterprise IM — 自建文件平台（FastDFS）

**Key idea:** 单机文件扛不住时，讲 FastDFS、自建分层和权限控制。

Early on, almost everything lived on **one file server**. As usage grew, it wasn't just "a few uploads" — **chat attachments** piled up, and other modules needed files too: **contracts**, **design drawings**, things you don't want to lose or leak.

We couldn't keep **all** of that on a single box forever. At the same time, **privacy / data control** mattered for the customer, so we didn't want to push **all** enterprise documents to a **public cloud file service** as the default answer.

So we built a **self-hosted** style file layer around **FastDFS** (an open-source distributed file system). The idea was **scale-out storage**, **redundancy**, and a **single document backbone** that **User**, **Messaging**, and **workflow-style** subsystems could all call into — not three different ad-hoc upload folders.

Operationally, that forced real engineering work: how files are **sharded**, how we think about **backup and restore**, and how **access control** stays consistent when many features touch the same files. It wasn't "install and forget" — it was **capacity + reliability + security** together.

*(Layering note for interviews: later, after a serious incident on a **Windows avatar upload path**, we tightened controls and moved some **user-facing blobs** to **cloud object storage**. That's a different slice of the same product — the **business document** story here is still **on-prem / self-managed** **FastDFS** for the heavy volume.)*

<a id="oral-03"></a>
### ③ Conflict with a teammate

**Key idea:** 先讲 1:1 和反馈方式怎么改，而不是对错。

One time I worked with a difficult teammate was during an Enterprise Messaging project where code reviews had become increasingly tense.

At first, it looked like a technical disagreement problem because the teammate often reacted defensively to review comments and avoided review discussions altogether.

Instead of continuing the conflict publicly, I spoke with them privately one-on-one. During that conversation, I realized the real issue wasn’t technical ability — it was that they had previous bad experiences with public criticism, so review comments felt personal very quickly.

After that, I changed how I worked with them. I kept feedback more private, focused comments on the code and engineering impact instead of wording things too directly, and for more complicated areas we used short pairing sessions instead of long review threads.

Over time, the communication became much healthier. Reviews moved faster, collaboration improved, and the release process became more stable again.

After that, I became much more careful about how review feedback is delivered, especially in larger teams, and focused more on building trust before pushing for deep technical changes.

**Case B（可选：技术选型分歧）**
**Key idea:** 讲技术选型时的约束、风险和团队共识。

In another project, we had a disagreement about technical direction.

One teammate had deep experience with older tools like **Delphi** and preferred staying with a familiar stack for stability and delivery speed. I was leaning toward using more modern components because I thought long-term maintenance and integration would be easier.

Instead of turning it into a personal argument, we discussed the trade-offs openly with the team — delivery risk, maintainability, existing system constraints, and who would support the system later.

In the end, we chose a more practical middle ground. Some legacy parts stayed because replacing them immediately would add too much risk, while newer components were introduced gradually around them.

Even when the final decision wasn't exactly my preferred direction, I still focused on making the delivery successful and reducing future risk through documentation and cleaner interfaces.

Since then, I focus more on showing the real operational impact and risk of different options, rather than just arguing which technology is technically "better."

**（更贴近你经历的展开）**：**Delphi vs 团队主流栈**、**入口地磅/称重联动**（超重预警、抬杆/报警）、**负责人拍板后仍专业执行 + 文档降风险** → 详见 **[Q42 Option B](#q-42)**（事实未入库前口试勿编客户/项目正式名）。

**Case C（可选：跨部门沟通冲突）**
**Key idea:** 讲清边界和折中，不要硬答“能”。

In cross-team work, product teams sometimes ask for features that look simple from user view, but are expensive or risky to build, and still want them live very fast.

When that happens, I don't just say "no." I explain the technical reason in plain language, show the real cost and risk, and offer options: **MVP now**, full version later, or phased rollout.

We compare trade-offs together — time, quality, and user impact — and pick a plan both sides can commit to.

That way, we avoid fake promises, still ship something useful on time, and keep trust between product and engineering.

<a id="oral-04"></a>
### ④ Failure

**Key idea:** 选一个真失误，讲修复和防再犯。

**Case A — Chinese herbal labeling（备用 · 估时 / 延期 / 模糊需求）**  
**Key idea:** **stakes 相对小**，不适合压过「最大失败」主叙事；**missed deadline / estimation / ambiguity** 追问时用。  
**Tension:** underestimated how messy real-world images would be. **Action:** raised the slip early, reset the plan, piloted small batches first. **Lesson:** validate throughput on real samples before committing to a hard estimate.

**Case B — App release（测试配置打进正式包 · 主答同源）**  
**Key idea:** 与 **[Q4 Option B](#q-04)** 同一叙事 — **accountability** + **流程薄弱（人手/记忆）** + **加固** + **小改动也不跳过守门**。

One mistake I made earlier in my career happened during an application release.

I shipped an upgrade where the build was still pointing to test environment configurations instead of the production APIs and database. As a result, users started seeing incorrect data after the release, and we had to prepare and ship a corrected version quickly.

At that time, we were still a relatively small team without a very mature QA or release process, and too much of the release validation depended on manual checking and individual memory.

I took responsibility for the mistake, and afterward we improved the release process significantly. We separated development, testing, and production configurations more clearly, added multi-person verification before releases, and gradually introduced more automation into the deployment and validation flow.

Since then, I've been much more disciplined about release management, even for small updates. That experience taught me that reliable delivery processes need systems and checklists, not assumptions that someone will remember every step manually.

**Case C — Enterprise IM（用户上传路径 · 可选 · 安全岗再默认主答）**  
**Key idea:** 事实强但**话题易跑偏**；非 **security / infra / IR** 岗**勿默认主答**；若讲，**弱化 drama**，强调**边界与流程学习**（与 [Q4 Option C](#q-04) 同源）。

An earlier security-related mistake involved a user upload path in an enterprise messaging system.

At the time, avatar uploads were hosted on a Windows-based file server, and the upload controls were not strict enough. That created a security exposure which eventually forced us to rebuild and restore the environment from backups.

After that incident, we tightened permissions, improved upload validation, added stronger host protections, and later moved some user-facing storage paths into more controlled cloud storage environments.

The experience made me much more aware that user upload functionality should always be treated as part of the system's security boundary, not just as a simple file feature.

<a id="oral-05"></a>
### ⑤ Under pressure

**Key idea:** 先说压力来源，再说你怎么稳住节奏。

**Case A — Smart Factory（发布窗）**  
**Smart Factory** before release — **shop floor** doesn't wait. I split it: **triage**, **fix**, **verify**, **watch**. Pull the **owner** of the broken layer, **short** updates. We got it **out** without **breaking** the line. **Shrink unknowns fast** — that's how I handle heat.

**Case B — Enterprise IM（单人 Android + 上线后救火 · 与 [Q9](#q-09) 主答同源）**  
When I'm under pressure, I usually try to reduce uncertainty as early as possible instead of reacting emotionally to the situation.

One example was during the early release period of an Enterprise Messaging app where I was the only Android developer at the time. We launched quickly, but after release a large number of bugs and user issues started coming in at the same time.

Instead of trying to solve everything at once, I worked in a very structured rhythm. Every day I reviewed the incoming issues, prioritized them by user impact, focused on stabilizing the highest-risk problems first, and released updated builds continuously instead of waiting for one huge fix.

At the same time, product and support teams helped communicate realistic timelines to users so expectations stayed clear while engineering focused on recovery.

That experience taught me that under pressure, staying calm and maintaining a clear execution rhythm is usually much more effective than trying to react to every issue emotionally or all at once.

**Case C — Air-gapped site（造币印纸厂 / 备用 · follow-up）**  
**Key idea:** **memorable**、**unusual**，但信息量大 — **勿与 Case B 叠成长段**；**压缩骨架**见 **[Q9](#q-09) Option B**。

> **Tension:** **high-security** **offline** site — **costly** **access**, **no** normal **deploy–patch–retry** loop.  
> **Action:** **offline** packages, **heavy** **prep**, **small** **checkpoints** per visit, **honest** timelines when **process** was the bottleneck.  
> **Reflection:** pressure can be **managing friction and expectations**, not **only coding faster**.

<a id="oral-06"></a>
### ⑥ Prioritize quickly

**Key idea:** 用 impact / risk / dependency 排序，再早沟通。

**Case A — 产线 vs 里程碑**  
**Smart Factory** — **line** issues, **PM** wants features. I fix what **hurts operators** first, then what's **on the milestone**, and I'm **honest** about dates on the rest. **Clear order** beats a **pretty** plan nobody follows.

**首版范围分歧（与 [Q5](#q-05) 同源）** — **产品侧**想首版更「满」；**工程/现场**侧担心 **rollout risk**（流水线未充分验证）。**分歧点**是 **timing / operational risk**，不是人身对立；用 **trade-off 可见化 + 分期试点** 对齐。**完整口播**见 **[Q5](#q-05)**。

**Case B — 下车间 + 模糊需求 + 原型迭代**  
In **Smart Factory** projects, one challenge was that requirements were often unclear at the beginning.

Operators knew parts of the workflow were painful, but they usually couldn't describe the exact solution in technical terms. So instead of relying only on meetings or documents, we went into the workshops, watched how people actually worked, and built prototypes very quickly.

The prototypes helped users react to something concrete, which gave us much better feedback than abstract discussions. Over time, the product evolved through several major iterations — some features expanded, others were removed completely after real usage feedback.

In operational software, I've seen that prototypes and real usage feedback are usually more valuable than trying to perfect the spec too early.

**Case C — Many projects at once（外部 + 自营）**  
At one point, I was handling several projects at the same time — not just one backlog.

Some projects were external customer work, like **Smart Factory** systems and **enterprise messaging** platforms. At the same time, we also had internal product work, including smart locker systems and other internet-facing projects.

The biggest challenge was that everything always looked urgent from somebody's perspective. I couldn't treat every request as P0, or nothing would actually move forward.

So I built a very visible prioritization habit for myself.

Each day, I looked at three things first:

which release or customer deadline was closest,
which technical blocker was currently slowing the team down the most,
and which tasks could safely move a little without damaging trust.

I focused on impact and delivery risk first, instead of just whoever messaged me most recently.

Another important part was escalating early. If I saw that something would not realistically fit into one person's capacity, I raised it early — borrowing help from another developer, pairing on difficult issues, or splitting ownership more clearly instead of silently carrying the overload.

That approach helped us keep multiple projects moving without constantly falling into chaos or fake urgency.

I've come to realize that prioritization isn't just about sorting tasks — it's also about expectation management and knowing when to ask for help early.

<a id="oral-07"></a>
### ⑦ Process improvement

**Key idea:** 从手工到自动化，讲为什么更稳。

One process improvement I helped drive was moving our deployment workflow from mostly manual releases to a more automated CI/CD setup.

At the beginning, deployments were handled manually — copying builds, syncing files, updating services by hand. That worked when projects were smaller, but **Smart Factory** eventually expanded to many sites, and the operational risk started scaling with it. Small mistakes during deployment could easily turn into rollback work or production issues.

So we introduced **Jenkins** integrated with **GitLab** to standardize build and deployment pipelines.

The setup itself took time — configuring repositories, agents, credentials, deployment steps, and getting the first stable pipeline running — but once the flow became reliable, releases became much more predictable.

We first rolled it out on the **Smart Factory** project, then gradually moved other projects onto the same workflow so the team wasn't maintaining different deployment habits everywhere.

We also combined that with **containerized Spring services**, lightweight deployment checklists, and short internal docs so onboarding and releases depended less on tribal knowledge.

The biggest improvement wasn't just speed — it was consistency. Releases became easier to repeat, easier to recover, and much less dependent on individual memory.

<a id="oral-08"></a>
### ⑧ Tough feedback

**Key idea:** 先承认反馈合理，再讲你怎么改。

**Case A — Manager（文档习惯）**  
One piece of tough feedback I received came from a manager during a long-running project.

He pointed out that I sometimes kept too much technical context in my head instead of documenting it clearly enough for the team. As the work involved more people, that made onboarding and long-term maintenance harder — newer team members often had to come back and ask why certain technical decisions had been made.

Honestly, the feedback was fair. At that time, I was very focused on delivery speed and solving problems quickly, so I treated documentation as secondary unless it became a blocker for the team.

After that conversation, I changed how I worked. I started writing lightweight decision notes for larger technical choices — not huge documents, just enough to explain the reasoning, trade-offs, and important considerations behind the decision.

I also added short onboarding notes for systems or modules that new developers frequently found confusing.

Over time, onboarding became smoother, repeated questions decreased, and technical discussions became easier because more context was already written down.

That feedback changed how I think about engineering communication. I still try to keep documentation practical instead of excessive — but now if a decision will affect maintainability, onboarding, or future development work, I make sure the important context is written down and easier for the team to follow.

**Case B — Many user voices（原型 + 单一决策人）**  
In some **Smart Factory** and smart locker projects, one challenge was that different stakeholders wanted different things, but nobody had a fully clear picture of the workflow.

At first, we spent a lot of time discussing requirements in meetings, but many operators and managers couldn't easily follow technical explanations or abstract plans. That often led to **conflicting directions, repeated requirement changes, and potential rewrite risk** for the engineering team.

What worked much better was building quick prototypes and putting them in front of real users. Once people could interact with something concrete, feedback became much more practical and decisions became faster.

We also realized we needed a clearer ownership structure. Instead of treating every conversation as a requirement change, we aligned with one primary customer-side decision maker who could prioritize requests and define what "done" actually meant.

That reduced **scope churn, avoided constant rework**, and gave the engineering team a much more stable delivery target.

<a id="oral-09"></a>
### ⑨ Adapted to change

**Key idea:** 讲约束变了，你也跟着改方案。

**Case A — ChatClothes**  
During my **ChatClothes** thesis project, I had to adapt the design quite significantly halfway through development.

Originally, some parts of the pipeline depended more heavily on cloud-side processing. But as the project evolved, **offline capability and response speed became hard requirements** because I wanted the system to run on lightweight hardware like **Raspberry Pi** devices.

Once I started measuring real performance numbers, it became clear that the original approach wouldn't meet those constraints reliably.

So instead of forcing the original design to work, I stepped back and re-evaluated the system architecture. I moved more of the AI pipeline **locally** using **lightweight LLM deployment** and **LoRA-based optimization**, reduced parts of the scope that weren't essential, and focused more on **practical responsiveness** than theoretical completeness.

That shift changed both the technical direction and the project priorities, but it allowed the final system to run **offline** with much better performance on limited hardware.

In the end, the project finished successfully with **First Class Honours**.

What I learned is that **adapting to change sometimes means letting go of your original design** instead of trying to defend it. Real measurements matter more than attachment to an early idea.

**Case B — Enterprise IM（约束变了，系统跟时代一起改）**  
Another example was our long-running enterprise messaging platform.

Over the years, the **constraints changed completely**. What started as a standalone messaging product gradually evolved into a larger internal **platform** with **shared identity**, **file services**, **permissions**, and **multiple business modules** connected together.

That forced us to continuously adapt the architecture.

For example, early on we tried maintaining more **low-level messaging infrastructure** ourselves, including C++ server components. But as scale and operational pressure increased, **stability became harder to maintain**. Eventually we moved core messaging capabilities onto **Easemob** while focusing our own engineering effort higher up the stack — **permissions**, **workflows**, **user systems**, and **platform integration**.

We also evolved file storage from a **single server** into a **distributed FastDFS-based system** as attachments and business documents grew over time.

At the same time, the **team process evolved** too — more automation, better collaboration tools, clearer approval flows, and more structured project coordination as the organization became larger.

I’ve realized that **good systems are rarely static**. As scale, cost, and operational reality change, I’ve learned to evolve the architecture and process along with them.

**口试边界（与 [Q23](#q-23) 对齐）**：**显著变化**题优先用 **Q23 主答** 抓 **「从独立 IM 到共享基础设施」** 一条主线；**厂商/组件细节** 追问再展开或见 `projects/enterprise-messaging/facts.yaml`，避免 **conference-talk** 式信息过载。

<a id="oral-10"></a>
### ⑩ Why should we hire you?

**Key idea:** 先说你能交付什么，再说为什么对岗。

#### 30 秒版（约 30s）

You should hire me because I'm comfortable taking **complex real-world problems** and turning them into **reliable software delivery**.

I've spent about **thirteen years** across **Android**, **Java backend** systems, and **full-stack** product work, mainly in **production-heavy environments** like **enterprise messaging** and **Smart Factory** platforms.

More recently, I completed my **Master's at AUT** with **First Class Honours**, focused on **applied AI** and **lightweight offline deployment**.

I'm based in **Auckland** with **full-time work rights**, and I'm looking for a role where I can contribute **strong engineering execution**, **practical problem-solving**, and **AI-focused development**.

#### 1 分钟版（约 60–75s）

I think I'm a strong fit because my background combines **software engineering**, **real-world delivery**, and **applied AI**.

Over the past **thirteen years**, I've worked across **Android**, **Java backend** systems, **integration work**, and **full-stack delivery** — mostly in environments where **reliability**, **rollout**, and **operational reality** mattered just as much as writing features.

For example, I've worked on **enterprise messaging** systems with **real-time communication** challenges, **Smart Factory** platforms involving **devices** and **multi-site deployment**, and more recently **AI-focused** systems during my **Master's at AUT**.

My thesis project, **ChatClothes**, focused on **running AI efficiently on lightweight hardware with offline support**. That project reflects how I usually work: **measure constraints early**, **adapt the design when needed**, and focus on **practical usability** instead of unnecessary complexity.

I'm also comfortable working across different parts of a system — **client**, **backend**, **deployment**, and **operational processes** — which helps when projects become messy or requirements change over time.

I'm based in **Auckland** with **full-time work rights**, and I'm looking for a team where I can contribute **strong engineering execution**, **reliability**, and **practical problem-solving**.

#### 精简一句版（收尾用）

> I enjoy working on **difficult real-world problems** and helping turn them into **stable products** people can actually use.

<a id="oral-creative"></a>
### （补充）Creative idea — Smart Factory（电子秤串口 → WebSocket → 网页自动填重）

**Key idea:** 讲串口秤到 WebSocket 的减负思路。**与 [Q7 Option B](#q-07)** 压缩骨架同源；题干若是 **above and beyond**，主答仍用 **Q7 Option A（ChatClothes 文档）**。

**Script（口语）**  
One small but creative improvement I worked on was in a **Smart Factory** system for recording fabric weight.

Originally, operators had to place fabric on a scale, read the number manually, then type it into a web form. It sounds simple, but on a busy production line it created a **lot of friction** — slower workflow, typing mistakes, and operators constantly stopping what they were doing just to enter numbers.

I checked the hardware and found the scale could output weight data through a **serial connection**.

So on the Windows PC beside the scale, I built a **lightweight local service** that listened to the COM port, cleaned up the incoming data, and exposed it through a small **WebSocket server**. The browser page connected to it directly and automatically filled the current weight into the **active input field**.

After that, operators could just keep weighing and moving materials without manually retyping values every time.

The improvement itself was **technically small**, but it removed a lot of **repetitive friction** from the workflow and **reduced input errors** on the production line.

I like that kind of engineering work — connecting **real-world operations** with software in a way that makes **daily work smoother** for users.

---

<a id="section-part-b"></a>
## Part 2 — Story Bank & Question Index

This section is the reusable story bank and question-family index. Use it to avoid rewriting the same story in multiple places.

This section keeps the project-level stories and the question-family index, so the same example doesn't need to be rewritten in multiple places.

<a id="section-1-topics"></a>
### B1. 高频分类题库（英文题干 + 中文提示）

> **速查**：**嘴上念** → [口语专页](#section-oral-only)；**嘴里关键词** → [B2 STAR](#section-2-star-brief)；**书面辞典（记得改口）** → [C 节](#section-5-scripts)。  
> **B1 跳转**：**B1-01** 动机专页 [oral-b1-01](#oral-b1-01)；**B1-02～B1-09** 各题干见小节内 **→ 口稿** 链接；**仅下列为题干补稿**（C 节无对等 Q 或需单独成段）→ [oral-b1-05-supplement](#oral-b1-05-supplement) · [oral-b1-06-influence](#oral-b1-06-influence)。

<a id="b1-01"></a>
### 1) 自我认知与动机
- Tell me about yourself.（**见 [A ①](#oral-01)**：**30 秒 + 1 分钟**两档；事实对齐 `kb/profile.yaml`）
- What are your strengths and weaknesses?（**见 [B1-01 口语专页 · 优劣势](#oral-b1-01-sw)**；速答版另见 [Q1](#q-01) · [Q2](#q-02)）
- Why are you looking for a new opportunity?（**见 [B1-01 口语专页 · 换机会](#oral-b1-01-why-move)** = **Q32**）
- Why do you want to join this company?（**见 [B1-01 口语专页 · 投公司](#oral-b1-01-why-company)** = **Q29** 模板；**[业务 + 岗位 JD 对齐备忘](#oral-b1-01-why-company-research)**）

<a id="oral-b1-01"></a>
#### B1-01 口语专页（动机类 · 与 `kb/profile.yaml` 对齐）

<a id="oral-b1-01-sw"></a>
**What are your strengths and weaknesses?**

**提示**：优势 1 + **证据**；劣势 1 + **可改进动作**（忌假弱点「我太完美」）。劣势用 **经理反馈 → lightweight decision notes / onboarding** 有真实故事（见 [A ⑧ Case A](#oral-08)）。

**Script（约 45–60s）**

> **Strength** — I **ship across layers**. About **thirteen years** I've taken **Android**, **Java** **backends**, and **integration** work from **idea** to **production** — **Enterprise Messaging** at **real** **user** **scale**, **Smart Factory** on the **shop** **floor** with **devices** and **long** **rollouts**. I'm **comfortable** **owning** the **messy** **middle** between **hardware**, **APIs**, and **clients**.
>
> I also **measure before I argue**. On **ChatClothes** I **profiled** the **pipeline**, found the **real** **bottleneck**, and **moved** **work** **local** so the **thesis** **system** **ran** **offline** on **small** **hardware** — that’s how I like to work: **evidence**, then **change** the **design**.
>
> **Weakness** — earlier I sometimes **kept too much technical context in my head** instead of **documenting clearly enough for the team**. As projects **grew** and **more people** joined, **onboarding** and **long-term maintenance** got harder. A **manager** said so **directly**; I **agreed**. I **changed** with **lightweight decision notes** on **bigger** technical choices (**reasoning**, **trade-offs**) plus **short onboarding notes** where **new** people **got lost**. I still keep docs **practical**, not **excessive** — but if a decision touches **maintainability**, **onboarding**, or **future** work, I **write down** what the **team** needs to **follow**.

---

<a id="oral-b1-01-why-move"></a>
**Why are you looking for a new opportunity?**（同 **Q32**）

**提示**（已对齐你的说法）：**主因是家庭** — 从 **中国** **迁居** **新西兰**，希望 **重新开始一种生活**；因此 **离开原来的公司**（地理与人生规划，**非绩效或与人闹翻**）。**来纽之后**：**2026-02** 完成 **AUT MCIS** **First Class**（**ChatClothes**）；现求 **Auckland** **稳定全职** 工程岗。**对前职**：仍 **认可原工作与技能积累**，下一份希望 **延续 Android / Java 后端 / 企业与工业交付 / applied AI** 等同一套能力；**不贬原雇主**。**PSWV** 全职权利（与 `kb/profile.yaml` 一致）。

**Script（口语）** → 见 **[Q32](#q-32)** 正文（展开版 + 极简）。

---

<a id="oral-b1-01-why-company"></a>
**Why do you want to join this company?**（同 **Q29** 骨架）

**提示（中文要点 · 已对齐你的说法）**：① **管理理念 / 工作环境** — 更偏信任、专业自主与工程文化；② **想做「真产品」** — 用户或一线能直接感到价值（**Smart Factory** 提产减负、**smart-power** 实时监控与数据可见）；③ **投 Air NZ** — 航司规模下，**旅客端数字体验与可靠运营** 能把技术价值放大到更多人（不写未核实的内部系统名，避免臆测）。**面试前**务必做 **[业务 + 岗位 JD 对齐](#oral-b1-01-why-company-research)**，把动机钉到**具体 JD 原词**上。

**Script — Air New Zealand（约 30s）**

> I'm interested in **Air New Zealand** because it's a **real product** at **national scale** — **millions** of **travelers** depend on **reliable** **operations** and **clear** **digital** **touchpoints**. I like workplaces that **trust** engineers with **ownership** and **adult** **judgment** — that's the kind of **culture** I want next.
>
> My background matches that **style** of work: **Smart Factory** — I could **see** **capacity** and **operator** **load** **improve** on the **floor**; **smart-power** — **live** **telemetry**, **dashboards**, and **fast** **alarms** so **sites** **feel** the **benefit** of the **system**; plus **enterprise** **messaging** at **real** **user** **scale**. I want to **ship** **end-to-end** **quality** where **customers** **notice** the **difference** — not **only** internal tools.

**Script — Air New Zealand（约 60s，在 30s 上略展开）**

> I'm interested in **Air New Zealand** for two honest reasons: **culture** and **impact**.
>
> On **culture**, I'm looking for a **professional** environment that **defaults** to **trust** — **clear** **goals**, **space** to **own** **decisions**, and **less** **theatre** than **pure** **face-time**. That's what people mean when they say **"more freedom"** in a **good** way — not **chaos**, but **mature** **autonomy**.
>
> On **impact**, I care about **products** **people** **touch**. An airline is **exactly** that — **booking**, **day-of-travel**, **disruption** handling, **safety** and **ops** **systems** — **high** **stakes**, **high** **visibility**. I've spent years shipping **software** where **outcomes** are **measurable**: **Smart Factory** where we **raised** **efficiency** and **reduced** **manual** **pain** for **workers**; **smart-power** where **operators** could **see** **live** **power** **data** and **get** **alarms** **fast**; **enterprise messaging** for **thousands** of **daily** **users**. I want the **next** chapter to be **that** same **pattern** — **quality** **engineering** **with** **clear** **human** **value** — at **Air** **New** **Zealand's** **scale**.

**Script — 备选公司名「Hotter」（若你指其他品牌，请把公司全名改成正式英文）**

> I'm interested in **[Hotter — replace with exact legal name]** for the **same** **core** **reasons**: a **product** **culture** I can **learn** from, and **work** that **helps** **real** **people** **feel** **the** **tech**. I've already **proven** I care about **measurable** **outcomes** — **Smart Factory**, **smart-power**, **large-scale** **mobile** **and** **backend** **delivery** — and I want to **bring** that **mindset** to a **team** here in **New Zealand**.

**Script（通用模板 · 其他公司仍用方括号）**

> I'm interested in **[Company]** because **[one concrete product or problem they own — fill]**. That's close to what I've already shipped — **[e.g. real-time mobile + backend / factory + IoT / on-device AI — pick one line from ChatClothes, Enterprise Messaging, or Smart Factory]**. I want **[team size / domain / stack — fill]** where I can **own** **end-to-end** pieces and keep **quality** **high** in **production**.

**极简一句（背这个也行）**

> I'm interested in **Air New Zealand** — **national-scale** **travel** **products** plus a **trust-based** **engineering** **culture**. My **Smart Factory** / **smart-power** / **enterprise** **messaging** **track** **record** is all about **real** **users** **feeling** the **win**.

<a id="oral-b1-01-why-company-research"></a>
**投公司前：公司业务 + 岗位需求（结构化备忘）**

**目的**：把「为什么选你们」从**泛泛文化/真产品**，升级成**我读了你做什么生意 + 这个职位要什么 + 我哪几条经历一一对应**。口试时最稳的是**复述对方 JD 里的 must-have**，再接你的项目证据（避免编造内部架构）。

#### A) 公司业务（Air New Zealand · 公开信息层）

| 维度 | 你应能说清什么（不求背数字） | 信息从哪来 |
| --- | --- | --- |
| **客户与产品形态** | 客运为主、国际国内网络；旅客触点含 **App / Web**、行程与自助服务；**出行日**体验对延迟、清晰度、稳定性敏感 | 官网、新闻稿、年报/IR 摘要 |
| **数字化在生意里的位置** | 数字渠道是**产品的一部分**（不仅是 IT）；运营侧强调**可靠、合规、伙伴对接** | 招聘站 **[Digital 职业路径](https://careers.airnewzealand.co.nz/belong-here/career-options/digital)** |
| **工程「痛点类型」**（概括） | 高并发读路径、离线/弱网、身份与支付周边、**中断/改签**类流程、观测与发布纪律 | 结合 JD + 你对航旅产品的常识；**勿断言**未公开的内部系统名 |

#### B) 岗位角色需求（JD → 口播映射表）

1. **拆 JD**：`Must-have` / `Nice-to-have` 分行；若有 leadership，加 `people / roadmap / stakeholders`。
2. **做三列表**（打印一页带进面试前复习）：`JD 原词` | `对方要的行为/产出` | `你的证据（项目 + 动词 + 结果，事实来自 KB）`。
3. **常见移动/全栈 JD 技能簇**（来自公开市场岗位描述**归纳**，**以你投递的那一份为准**）：生产级 **Android（Kotlin / Jetpack / Compose）** 或 iOS；**REST / 现代客户端架构**；部分岗位写 **BFF、AWS、CI/CD**、与后端协作。你口述时用 **your posting mentions …** 引用具体词。
4. **项目占位对齐**（按 JD 勾选改写）：规模化移动端与集成 → **enterprise-messaging**；实时数据与告警/可观测 → **smart-power**；一线业务澄清与分期交付 → **Smart Factory**；端侧 AI / 论文级证据 → **ChatClothes**。

#### C) 英文备用（「你了解我们公司业务吗？」）

> Air New Zealand is a **full-service airline** where **digital is part of the customer product** — **travelers** feel **latency**, **clarity**, and **reliability** on **day-of-travel**. I **won't guess** your **internal architecture**, but I've read **your public careers material** **[and / or] this job description** — it emphasizes **[paste 2–3 exact phrases from the JD]**, which is how I've already shipped work on **Smart Factory**, **smart-power**, and **large-scale mobile**, with **measurable outcomes**.

#### D) 备选雇主（Hotter / 其他）

同一套流程：**官网产品/关于我们 + 该职位 JD** → 用一句话说清 **客户是谁、卖什么、技术扮演什么角色**，再走 **B)** 三列表。公司名未定时不要写死业务细节。

（与 **Q29** 一致；完整题干跳转 **[Q29](#q-29)**。）

<a id="b1-02"></a>
### 2) 团队协作与冲突处理
- **Tell me about a conflict with a teammate and how you resolved it.** → **口稿**：[A ③ 冲突与评审](#oral-03) · [Q6](#q-06) · [Q24](#q-24) · [Q42](#q-42)（**Option B** 技术栈/协作：**Delphi** vs **团队主流栈**）
- **Describe a disagreement with your manager.** → **口稿**：[Q5](#q-05)（**主：明确 disagree + timing/ops risk**）· [Q33](#q-33)（团队 rollout 张力 + 试点 + 产线反馈）· 语境 [A ⑥ 产线 vs 里程碑](#oral-06)
- **Tell me about a time you had to collaborate cross-functionally.** → **口稿**：[Q12](#q-12) · [Q20](#q-20)（接口契约 + 周 demo + 多端对齐）

<a id="b1-03"></a>
### 3) 压力管理与优先级
- **Tell me about a time you worked under pressure.** → **口稿**：[Q9](#q-09) **主：Enterprise IM**；**备：Air-gapped** 骨架 · [A ⑤ Under pressure](#oral-05)
- **How do you prioritize when everything feels urgent?** → **口稿**：[A ⑥ Prioritize](#oral-06)（含多线并行 Case C）· [Q8](#q-08) · [Q36](#q-36)
- **Tell me about a time you had multiple deadlines.** → **口稿**：[A ⑥ Case C 多项目并行](#oral-06) · [Q8](#q-08)
- **Urgent work + long-term projects at the same time（紧急与长线并行）** → **口稿**：[Q40](#q-40)（**Smart Factory**：**产线打断计划** vs **只救火则路线图烂尾**；**有意分开**、**可见性**；**双线不同速**）
- **Excessive workload / at risk of missing deadline（工作量过大）** → **口稿**：[Q38](#q-38)（**绘本**：同事离职接手 → **计划与现实脱节** → **早与主管再平衡**；**借还书客户端** vs **柜端/锁/传感器/现场集成**）；估错类备选 **[Q22](#q-22)**

<a id="b1-04"></a>
### 4) 失败与复盘
- **Tell me about a time you failed.** → **口稿**：[A ④ Failure](#oral-04) · [Q4](#q-04)
- **Tell me about a time you missed a deadline.** → **口稿**：[Q22](#q-22)（同中草药标注故事）
- **Describe a production issue you handled.** → **口稿**：[A ⑤ Case A 产线发布窗 triage](#oral-05) · [创意 · 电子秤](#oral-creative)（设备/网页链路）· 安全向 [A ④ Case C 头像入侵](#oral-04)

<a id="b1-05"></a>
### 5) 复杂问题解决与技术判断
- **Tell me about a challenging project and how you handled it.** → **口稿**：[Q3](#q-03)（**主 ChatClothes**；**备 Smart Factory 秤/集成** 作 *another example* / 硬件不稳追问）
- **Tell me about a complex technical problem you solved.** → **口稿**：[A ② Complex technical](#oral-02)（含 Android OEM 延展）· [oral-enterprise-files](#oral-enterprise-files)（FastDFS）· [Q31](#q-31)
- **Tell me about a difficult decision you made.** → **口稿**：[B1-05 补稿 · Difficult decision](#oral-b1-05-decision) · 可并讲 [A ⑨ Case B 架构演进](#oral-09)（Easemob / FastDFS 等）· [oral-enterprise-files](#oral-enterprise-files)
- **Describe a trade-off you had to make (speed vs quality, etc.).** → **口稿**：[B1-05 补稿 · Trade-off](#oral-b1-05-tradeoff) · [Q34](#q-34)（Smart Factory：**云端抬规格+读写分流**换时间 vs 成本；另：**产线 vs 里程碑**）· [A ② 延展 OEM 矩阵 vs 发版](#oral-02) · [oral-enterprise-files](#oral-enterprise-files)（自建文件 vs 公有云）

<a id="b1-06"></a>
### 6) 主动性与影响力
- **Tell me about a time you took initiative.** → **口稿**：[Q7](#q-07) **Option B**（**Smart Factory 秤** 压缩骨架）· [创意 · 电子秤](#oral-creative)（展开）；**above and beyond** 题干 → **Q7 Option A 主：ChatClothes**
- **Describe a process improvement you drove.** → **口稿**：[A ⑦ Process improvement](#oral-07) · [Q44](#q-44)（含 CI/CD 叙事）
- **Tell me about a time you influenced without authority.** → **口稿**：[B1-06 补稿](#oral-b1-06-influence)（**问法 = influence**）· 与 **[Q5](#q-05)** 同源 **Smart Factory** 分期故事；**若题干是 disagree with manager** → 用 **Q5**（开头要点出 **disagreement**）· [Q33](#q-33)（团队 rollout + 场景先入、少「原则独白」）

<a id="b1-07"></a>
### 7) 反馈与成长
- **Describe a time you received critical feedback.** → **口稿**：[A ⑧ Tough feedback](#oral-08)（Case A 经理 ADR；Case B 原型 + 拍板人）· [Q13](#q-13)
- **Tell me about a time you gave difficult feedback.** → **口稿**：[Q21](#q-21)
- **What did you learn from your biggest mistake?** → **口稿**：[Q4](#q-04) **主：发版配置**；**备：中草药 pilot**（估时/延期）· [A ④](#oral-04)
- **How do you assure code quality in your team?** → **口稿**：[Q43](#q-43)（**主：融合推荐版**；手册级细节 **追问再展开**）
- **How do you support and track a junior developer's progress?** → **口稿**：[Q45](#q-45)（**主：Smart Factory 融合推荐版** — **交付赋能**；**文档/难反馈**深挖 → **[Q21](#q-21)** / **[Q13](#q-13)**）

<a id="b1-08"></a>
### 8) 适应变化
- **Tell me about a time requirements changed suddenly.** → **口稿**：[A ⑨ Adapted to change](#oral-09)（Case A ChatClothes；Case B Enterprise IM）· [Q23](#q-23)
- **Describe a major change at work and how you adapted.** → **口稿**：[A ⑨](#oral-09) · [Q23](#q-23)
- **Tell me about a time you had to learn a new technology quickly.** → **口稿**：[Q14](#q-14) · [Q25](#q-25)（舒适区外快速学习）· **最近学什么**见 **[Q41](#q-41)**（**实践 AI 工程 + ChatClothes 全链路 profiling**）· 完全不会的任务见 **[Q39](#q-39)**（GitHub/文档 + **中草药平台** YOLO 基线 → 平台化）
- **Describe the project workflow in your previous team.** → **口稿**：[Q44](#q-44) · [A ⑦](#oral-07) · 组织演进 [A ⑨ Case B](#oral-09)（飞书/审批等一句带过）

<a id="b1-09"></a>
### 9) 客户导向
- **Describe a difficult customer/stakeholder situation.** → **口稿**：[A ⑧ Case B](#oral-08)（原型 + 客户方唯一决策人）
- **Tell me about a time you managed unclear requirements.** → **口稿**：[Q30](#q-30) · [A ⑧ Case B](#oral-08)（下车间/原型对齐）
- **How do you handle conflicting stakeholder expectations?** → **口稿**：[A ⑧ Case B](#oral-08) · [Q30](#q-30)

<a id="oral-b1-05-supplement"></a>
#### B1-05 补稿（C 节无独立 Q 号的两题）

<a id="oral-b1-05-decision"></a>
**Tell me about a difficult decision you made.**

**提示（STAR）**：（T）自建消息基础设施 vs 稳定性；（A）评估 **C++** 自建长期缺陷成本 vs **环信 Easemob** 厂商依赖；（R）核心 IM 迁环信 + **极光 JPush** 通知备用 + 自研上移到平台子系统。

**Script（约 45–60s）**

> One difficult technical decision we made was around the **messaging infrastructure** in an enterprise IM platform.
>
> Originally, we **maintained more of the low-level messaging stack ourselves**, including some C++ server-side components. Over time, the **operational cost became harder** to justify. **Stability issues kept reappearing**, **maintenance effort stayed high**, and too much engineering time was being spent **solving infrastructure problems** repeatedly instead of improving **product capabilities**.
>
> At that point, we had to decide whether to continue investing heavily in our own messaging infrastructure or **move core messaging capabilities onto Easemob**.
>
> Moving to Easemob wasn't a perfect decision either. It introduced **vendor dependency** and **integration overhead**, and **giving up direct control** over part of the stack was uncomfortable at first.
>
> But after evaluating the trade-offs, we decided the **operational stability** and **mature messaging capabilities** were worth it. We also kept **JPush** as a **secondary notification path** for wake-up and alert-style traffic.
>
> That decision also changed where our **engineering effort** went. Instead of continuously rebuilding messaging infrastructure, the team **focused more on higher-level platform capabilities** like **permissions**, **workflows**, **file systems**, and **integration services**.
>
> In the long run, the system became **more stable** and the engineering team could spend more time **building business value** instead of repeatedly fighting infrastructure reliability problems.
>
> That experience taught me that difficult engineering decisions are often less about "Can we build it ourselves?" and more about **where engineering effort creates the most value over time**.

<a id="oral-b1-05-tradeoff"></a>
**Describe a trade-off you had to make (speed vs quality, etc.).**

**提示（STAR）**：（T）Android 全矩阵测试 vs 发版节奏；（A）主流守门 + 强信号真机；（R）可发布节奏 + 疑难工单收敛。

**Script（约 45–60s）**

> One trade-off we had to make in an **enterprise Android messaging product** was balancing **release speed**, **test coverage**, and the **reality of device fragmentation**.
>
> In **theory**, the ideal approach would be **full testing coverage** across many Android versions, manufacturers, and ROM customizations. But in **practice**, that wasn't realistic from either a **time** or **hardware-cost** perspective.
>
> So instead of trying to test every possible device combination equally, we **focused first on strong coverage** for **mainstream Android versions** and the most **common production devices** in our test lab.
>
> For less common or harder-to-reproduce issues, we used a **more targeted approach**. If a bug report showed **strong signals** — for example repeated failures on a specific device or ROM — we would invest deeper: **buy the device** if needed, **work directly with the user**, or **reproduce the issue remotely** on the exact hardware path.
>
> The trade-off was accepting that we **couldn't guarantee perfect pre-release coverage everywhere**, while making sure our **release cadence and overall quality stayed practical and sustainable**.
>
> That approach helped us keep **shipping reliably** while still narrowing down difficult device-specific issues when they genuinely mattered.
>
> The experience taught me that engineering trade-offs are often about **focusing effort where risk and impact are highest** instead of pretending unlimited coverage is possible.

<a id="oral-b1-06-influence"></a>
#### B1-06 补稿：Influence without authority

**Tell me about a time you influenced without authority.**

**与 [Q5](#q-05) 的关系**：同一 **Smart Factory** 首版分期 / 试点故事；**Q5** 面向 **disagreed with manager or a decision**（开场就要让人听到 **disagreement**）；**本题**面向 **无正式职权仍推动决策** — 可用下方短稿，或 **改口** 把 Q5 主答里的 **"disagreed" framing** 换成 **"wasn't the final decision maker, but needed to steer risk"**。

**提示（STAR）**：（S）Smart Factory 首版上线前 PM 要加功能；（T）无拍板权但要推动风险可控；（A）影响表 + 分期 + 试点数据；（R）团队采纳、先稳后扩。

**Script（约 45s）**

> I wasn't the **PM** — but **launch** **risk** was **on** **everyone**. On **Smart Factory**, **PM** wanted **more** **features** **before** **first** **release**; I wanted a **small** **stable** **core** because **factories** **punish** **half-broken** **software**. I didn't **pull** **rank** — I **wrote** down **impact**: **what** **breaks** **the** **line**, **what** can **wait**, and **what** a **phased** **pilot** **buys** us in **~sixty** **days**. We **aligned** on **core** **first**, **pilots**, then **grow** from **real** **floor** **feedback**. **Lesson**: **influence** without **authority** is **data** + **options** people can **say** **yes** to — not **louder** **opinions**.

---

<a id="section-2-star-brief"></a>
### B2. STAR 备忘（关键词 · 与 [口语专页](#section-oral-only) ①–⑩ 对应）

> **编号说明**：本节 **1)–10)** 与 **[C 节](#section-5-scripts)** 里的 **Q1–Q45** 不是同一套编号；「Qxx」一律指 C 节逐题编号。  
> **怎么用**：下面每条是**嘴里关键词**；完整英文口语在 **[A 节](#section-oral-only)** 对应条。**C 节**长句别直接念，先改口。

<a id="b2-01"></a>
### 1) Tell me about yourself.

**核心画像**：Messy real-world systems → reliable delivery

**Trigger**：Auckland / AUT First Class Honours / Android + backend + AI / Enterprise IM / Smart Factory / ChatClothes / production + operational reality / full-time rights

**收尾**：practical AI + engineering delivery

---

<a id="b2-02"></a>
### 2) Tell me about a complex technical problem you solved.

**核心冲突**：Android 后台保活 vs 系统杀进程；离线 + 轻量 vs AI 性能

**关键动作**：分层方案（Easemob 主通道 + JPush 备用）+ 心跳调优 + 状态同步；本地 LLM + LoRA 优化；主流机守门 + 反馈驱动真机

**职业人格**：reliability comes from layers, not one trick

---

<a id="b2-03"></a>
### 3) Tell me about a time you had a conflict with a teammate.

**核心冲突**：评审抵触 feeling personal

**关键动作**：1:1 私聊 + 具体反馈 + 短结对

**职业人格**：fix communication style, not just code

---

<a id="b2-04"></a>
### 4) Tell me about a time you failed.

**核心冲突**：test config shipped to prod

**关键动作**：认错 + **env separation** + **multi-person** checks + **渐进自动化** + **小更新**也走同一套验证（系统与清单，不靠记忆）

**职业人格**：systemic fixes over blame

---

<a id="b2-05"></a>
### 5) Tell me about a time you worked under pressure.

**核心冲突**：**主**：Enterprise IM **post-launch** bug flood（solo Android）；**备**：air-gapped **access / process** friction

**关键动作**：**reduce uncertainty early** + **structured daily rhythm** + **impact-first triage** + **continuous small releases** + **product/support** **clear expectations** / 离线：**prep + checkpoints + honest timelines**

**职业人格**：**calm operational engineer** — interviewer 应听到 **organized under pressure**，不是 **故事数量**

---

<a id="b2-06"></a>
### 6) Tell me about a time you had to prioritize quickly.

**核心冲突**：everything looks urgent / ambiguous requirements / multi-project overlap

**关键动作**：impact × **operational risk** × **dependency** / **early comms**（expectations）/ **practical triage**（deadlines, blockers, what can slip safely）/ **escalate or coordinate** before you become the **bottleneck**

**职业人格**：operationally grounded — **stable systems** + **sustainable** delivery pace

---

<a id="b2-07"></a>
### 7) Tell me about a process improvement you drove.

**核心冲突**：manual releases don't scale with multi-site rollout

**关键动作**：Jenkins + GitLab CI/CD + pilot first + team-wide migration

**职业人格**：less dependent on individual memory

---

<a id="b2-08"></a>
### 8) Describe a time you received tough feedback.

**核心冲突**：big decisions lived in my head / stakeholder chaos

**关键动作**：lightweight ADR + onboarding notes / prototype + single decision owner

**职业人格**：documentation = long-term feature / noise isn't a requirements doc

---

<a id="b2-09"></a>
### 9) Tell me about a time you adapted to change.

**核心冲突**：constraints changed (offline / hardware) / operational cost too high

**关键动作**：measure → re-evaluate design / stop rebuilding commodity infra

**职业人格**：good systems are rarely static

---

<a id="b2-10"></a>
### 10) Why should we hire you?

**核心画像**：I stabilize messy real-world systems

**Trigger**：10y production / Android + backend + AI / Enterprise IM + Smart Factory + ChatClothes / operational reality / full-time rights

**收尾**：I enjoy working on difficult real-world problems and helping turn them into stable products people can actually use

---

<a id="section-5-scripts"></a>
## Part 3 — Question Script Bank

This section keeps the longer Q1–Q45 scripts and deeper notes. It is still answer material, but it is not the first thing you scan before the interview.

> 与 **[第一部分 · 规则](#section-doc-about)** 一致：**短句、常用词、STAR 心里过**；每题尽量保持 **一行中文提示 + 一版英文主答**；**Q29–Q45** 已附 **追问 + 短答要点**。事实只来自 KB。

### 临场（极简）
- 没听清 → **clarify**。一题 **~60–120s**：**Action** 多一句。不会 → 说**怎么查、第一步干啥**。

### 常见追问（怎么用本节里的「追问」块）
- 面试官常在主答后追问 **细节 / 数字 / 你的角色 / 若重来 / 与团队分歧**；下面 **Q29–Q45** 在正文末附有 **「追问」+「短答要点」**，临场可只记 **要点** 不必背长段。
- 英文高频句式：**What was the hardest part?** / **How did you measure success?** / **What would you do differently?** / **What was your specific role?** / **Tell me more about the trade-off.**

### 本节怎么读
- **速览表**见下；**Q1–Q45** ≠ **B2** 编号；与 **A** 重叠的题 **练熟一边**即可。
- **追问**：**Q29–Q45** 每题末已列；**Q1–Q28** 可复用本节开头的追问句式 + 你最熟的主故事自补。

### Q1–Q45 速览（主故事标签）

| Q | 主题 | 主故事 / 关键词 |
|---|------|-----------------|
| 1–2 | 优势 / 劣势 | 产研桥接 + ChatClothes；讲解过深 → 分层说明 + ADR |
| 3 | 挑战项目 | **主：ChatClothes**（复杂度 + 约束 + ownership）；**备：Smart Factory 秤/集成**（追问 *another example* / 硬件不稳 / 可靠性） |
| 4, 22, 38 | 失败 / 延期 / 做不完 | **Q4 主：发版测试配置进 prod**（责任 + 流程 + 防再犯）；**Q38** 绘本 — **离职接手 + 早再平衡 + 按上下文分工**（见正文）；**Q4/Q22 备：中草药标注** → **pilot**（估时/延期） |
| 5, 27, 33 | 分歧 | **Q5**：**disagree with manager/decision** — **Smart Factory**（**timing + operational risk** vs 首版加功能）；**Q27** 同事；**Q33** 团队 **rollout** 策略分歧 + **试点/产线反馈** 纠偏（同源故事，问法不同） |
| 6, 24, 42 | 难合作 / 冲突 | **Q42**：**Option A** Enterprise IM 评审冻结；**Option B** **Delphi vs 团队栈**（地磅/入口称重联动，**口述待入库 facts**） |
| 7 | Above and beyond | **主：ChatClothes**（**非评分硬性要求**的部署/API/用户文档 + **可复现** + 导师认可 + **约提前六个月**）；**备：Smart Factory 秤** → **initiative / creative / process**（见 Q7 Option B） |
| 8, 34, 36, 40 | 优先级 / 多解 | **Q8**：**impact + operational risk + dependency**；**沟通/期望**；**多线 triage**；**早升级**防 **silent bottleneck**。**Q40**：**产线 vs 路线图** — **救火与长线都要动**、**可见性**、**迭代中系统仍在线**（见正文）。**Q34** Smart Factory 多解取舍。**Q36**：排序 + 过载 — **经验句先行**、**反默默硬扛**、**小团队灵活**（见正文） |
| 9 | 压力 | **主：Enterprise IM**（减不确定 + **structured rhythm** + **continuous builds** + **期望清晰**）；**备：banknote air-gapped** 压缩骨架（**Q9 Option B**） |
| 10–11 | 工作风格 / 动机 | **Q11**：**运营真实问题** + **长期可靠** + **现场可感知** + **ChatClothes = 约束下 AI**；**long-lived > demo** |
| 12, 20 | 团队 / 主导协调 | 接口契约 + 集成 Demo；弱化纯管理 |
| 13, 21 | 收反馈 / 给反馈 | **Q13** ADR/onboarding（收反馈）；**Q21** 给 **Junior 难反馈**：**先肯定技术** → **工程后果（接手成本/评审/风险）** → **模板 + 结对示例** → **具体可执行、非人身** |
| 14, 25, 41 | 快速学习 / 走出舒适区 / 新学 | **Q41**：**实践 AI 工程**（**AUT + ChatClothes**）— **全链路 profiling**、**瓶颈常非推理**；**日常开发里 LLM 工具**；**demo vs 产线** 收束为 **个人接触面**。**Q14**：**ChatClothes** — **paper→run→trace→LoRA**（**~two months** 目标、**~six weeks** 可迭代）；**Q25** 舒适区外 |
| 15–16 | Agile / Code review | **Q15** Sprint + **demo**；**Q16**：**review = 协作解题**、**先问 why**、**trade-off 讨论**、**对事不对人**、**给出反馈具体** |
| 17, 37 | 骄傲成就 | **Smart Factory** 主答 + **Enterprise IM NDK** 备选（见 Q17/Q37） |
| 18–19, 39 | 风险决策 / 不会答 / 全新任务 | **Q18**：周五 prod — **先降速**、**范围/验证/回滚/监控/发布说明**、不行则 **升级或下一窗口**；真紧急则 **盯日志 + 回滚在手**。**Q19**：**不装懂** → **澄清** → **边界 + 查证路径** → **透明** → **重要则 follow up**。**Q39** 完全不会的任务 |
| 23 | 重大变化 | **主：`enterprise-messaging` 演进**（平台化 + FastDFS + Easemob + 组织流程 + 角色扩展；**一条主线**）；**备：ChatClothes** 约束变（骨架） |
| 26 | DEI 产品设计 | **Q26**：**不装 D&I 专家**；**工程可测** — **a11y / 语言 / 弱网/弱机** + **早测迭代** + **真实多样用户反馈**；包容 = **更广人群可用的可靠软件** |
| 28, 35 | 持续学习 | **Q28**：**读 + 小实验/POC** + **trace 行为** + **轻笔记**；**ChatClothes** 例（diffusion/LoRA/本地部署）。**Q35**：业余跟进 + **产线侧真实用法** 过滤 + **Android 平台漂移**；**Q41** **实践 AI / profiling / 部署现实**（见正文） |
| 29–32 | Why company / 转职 | **Q29** Air NZ + [业务/JD](#oral-b1-01-why-company-research)；Hotter 备选需确认公司名；**Q32** **主因家庭**（**中国→纽**、新生活）→ **离原公司**；**MCIS 2026-02** + **稳定全职** + **延续技能**（[oral-b1-01-why-move](#oral-b1-01-why-move)） |
| 30 | 模糊需求 / 系统设计 | **Q30**：**workflow + 约束** 先于 **架构 buzzword**；**下车间观察**；**拆成可验证小块**；**原型**；**假设显性化**（**ADR / spike**）；**分期**；**运营侧验证** |
| 31 | 最大技术挑战 | ChatClothes 延迟剖解 |
| 43 | 代码 quality | **主：Q43 融合稿** — **减少上线前可避免的不稳定**；**Smart Factory** **真机集成 demo**；**Enterprise IM** **配置事故 → 环境/校验/自动化**；**工具≠质量**。**深挖**再拆：GitLab+Jenkins、Easemob、静态扫描/MR — 见 Q43「追问时再展开」与 **Q44** |
| 44 | 团队 workflow | **Option A** Smart Factory：**双周 Sprint** + **接口契约** + **周 demo** + **GitLab/Jenkins** 试点推广（[A ⑦](#oral-07)）。**Option B** **`enterprise-messaging`**：平台化演进节奏 + **飞书/文档/审批/预算** + **渐进自动化**；早期 **数周原型→上线救火** 与 **产品/设计对用户透明**（见 `facts.yaml` / [A ⑨ Case B](#oral-09)） |
| 45 | Mentor Junior | **Q45 主：融合稿** — **delivery enablement**（小切片、早集成、可见进度）；**check-in**：**试了什么 / 卡哪 / 不抢键盘**；**review** 讲 **维护成本与集成风险**（**beyond compiler happy**）；**轻分享**看 **trade-off**。**深挖**：站会/看板/30·60·90 → **追问再答**。**文档线** → **Q21+Q13** |

（本节脚本共 **Q45** 题。）

<a id="q-01"></a>
### 1) What is your greatest strength?
**提示（STAR）**：产研桥接 + 实战年限 + 证据驱动（ChatClothes profile 证据）。


<a id="q-02"></a>
### 2) What is your greatest weakness?
**提示（STAR）**：别说假弱点；用 **规模上来后上下文多在个人脑子里 → 团队接手与维护变难**，**经理直接点出 → 认同 → lightweight decision notes + onboarding**；收尾落到 **可维护性、接手、后续开发**（与 [A ⑧ Case A](#oral-08) 同源）。

**Script（口语）**
> One weakness I had earlier in my career was that I sometimes kept too much technical context in my head instead of documenting it clearly enough for the team.
>
> As projects became larger and involved more people, that made onboarding and long-term maintenance harder because newer team members often had to come back and ask why certain technical decisions had been made.
>
> A manager pointed that out to me directly, and I agreed with the feedback.
>
> After that, I changed how I worked. I started writing lightweight decision notes for larger technical choices — not huge documents, just enough to explain the reasoning, trade-offs, and important considerations behind the decision.
>
> I also added short onboarding notes for systems or modules that new developers frequently found confusing.
>
> I still try to keep documentation practical instead of excessive, but now if a decision will affect maintainability, onboarding, or future development work, I make sure the important context is written down and easier for the team to follow.

**临场（念法）**：内容已经够完整；口试不必 **句句齐整** — 可 **缩句**、**停顿**、偶尔只答 **其中两三句**，更像对话而非背稿。

<a id="q-03"></a>
### 3) Tell me about a challenging project and how you handled it.
**提示（STAR）**：**主答 ChatClothes** — **张力**：初版架构**纸面可行**，**真机 profile** 后 **延迟 + 硬件边界**（含 **LLM / vision**）变成硬约束；**动作**：**不硬扛原设计扩 scale**，按**实测瓶颈**改架构（如 **本地 Ollama**、**vision 路径减负**）；**ownership**：课题**自驱**、**固定**学位截止、**范围**同时盖住 AI / 集成 / 部署；**结果**：系统交付、**约提前六个月**交论文、**First Class Honours**；**反思**：**先测再改**、少猜。主答里**不必早抛**具体小模型全名（技术细节追问见 **[Q31](#q-31)** / `projects/chatclothes/facts.yaml`）。**备用 Option B** — **Smart Factory 秤/串口链路**：更像 **可靠性 + 集成 + 主动性**；适合 **「再来一例 / 不稳定硬件 / 产线侧集成」** 类 follow-up，**不抢**主答的「大挑战」叙事。

**Option A — ChatClothes（主答）**
**Script（口语）**
> One challenging project I worked on was my master's thesis project, ChatClothes.
>
> The goal was to build a lightweight virtual try-on system that could still run offline on constrained hardware, including Raspberry Pi-class devices. The challenge was that the original architecture looked fine on paper, but once I profiled the real pipeline, the latency and hardware limits became a serious problem — especially around the LLM and vision processing parts.
>
> Instead of forcing the original design to scale, I reworked parts of the architecture around the actual bottlenecks. I moved the LLM pipeline to a local Ollama-based setup and simplified parts of the vision workflow so the system stayed practical on smaller hardware.
>
> The project was largely self-driven, with fixed academic deadlines and a relatively large technical scope covering AI, backend integration, and deployment constraints at the same time.
>
> In the end, I completed the system successfully, finished the thesis about six months early, and graduated with First Class Honours.
>
> What I learned from that project is that difficult engineering work usually becomes manageable once you stop guessing and start measuring the real bottlenecks first.

**临场（念法）**：少 **project → tech list → result** 的简历腔；口播抓住 **「难在哪 → 我怎么重新框问题 → 怎么落地」**；可**停顿**、**删半段**，不必一次念满。

**Option B — Smart Factory scale integration（备用 · follow-up）**

**Key idea:** **可靠性 / 集成 / 流程改进**；对方问 *Tell me another example*、*hardware kept dropping data*、*unreliable devices on the floor* 时用（展开链路仍见 [创意 · 电子秤](#oral-creative)）。

**Script（口语 · 压缩骨架）**
> **Tension:** weight readings from the **scales** dropped **unpredictably** in the capture path — felt like flaky hardware, but users still needed **stable** data on the line.  
> **Action:** I treated it as **reliability engineering** — **persistent listener**, **watchdog**, **reconnect**, **pooling** so we didn't lose the stream.  
> **Result:** **stable collection** and **reproducible traces** when something broke again.  
> **Reflection:** an unstable **device link** isn't a **one-off bug** — it needs the same **discipline** as any other **production** surface.

<a id="q-04"></a>
### 4) Tell me about a time you failed or made a mistake.
**提示（STAR）**：**主答 Option B 发版配置** — **张力**：小团队、**验证过度依赖人手与记忆**；**动作**：认错 + **快修二次发版** + **环境隔离 / 多人校验 / 渐进自动化**；**反思**：可靠发布靠 **系统与清单**，不靠「有人会记得」。**临场**：少叠方法论标题，**一段事故 + 一段改进** 即可。**Option A 中草药标注** — **估时 / 延期 / 模糊样本** 类题作 **备答**（stakes 偏小，不作「最大失败」默认主叙事）。**Option C 头像上传安全** — **很强但易追问 breach**；**仅 security / infra / IR 向岗位**可作主答，否则 **默认不讲或极短带过**，口径见下（弱化戏剧化，强调 **upload path = security boundary**）。

**Option B — Release config mistake（主答）**
**Script（口语）**
> One mistake I made earlier in my career happened during an application release.
>
> I shipped an upgrade where the build was still pointing to test environment configurations instead of the production APIs and database. As a result, users started seeing incorrect data after the release, and we had to prepare and ship a corrected version quickly.
>
> At that time, we were still a relatively small team without a very mature QA or release process, and too much of the release validation depended on manual checking and individual memory.
>
> I took responsibility for the mistake, and afterward we improved the release process significantly. We separated development, testing, and production configurations more clearly, added multi-person verification before releases, and gradually introduced more automation into the deployment and validation flow.
>
> Since then, I've been much more disciplined about release management, even for small updates. That experience taught me that reliable delivery processes need systems and checklists, not assumptions that someone will remember every step manually.

**临场（念法）**： spirit 仍是「**清单与系统，而不是靠记忆**」；口播不必 slogan 化，**最后一句**可再缩短半句。

**Option A — Herbal labeling（备用 · 估时 / 延期 / ambiguity）**

**Key idea:** 好 **learning story**，**impact stakes** 小于发版事故 → 适合 **missed deadline / estimation** 题干，不作 **greatest failure** 默认主答。

**Script（口语 · 压缩骨架）**
> **Tension:** I **underestimated** how **messy** real-world **images** would be for labeling — my **two-week** guess was **wrong**.  
> **Action:** I **raised** it **early**, **reset** the plan, and **piloted** **small batches** first to learn real **throughput**.  
> **Lesson:** **validate** on **real samples** before you **lock** a **hard** estimate.

**Option C — Avatar upload path / security（可选 · 慎作主答）**

**Key idea:** 仅 **security / platform / incident** 角色或对方**明确深挖安全**时展开；否则易被拽进 **breach 细节** 而弱化 **你的成长**。口径：**professional**，**不讲**「机器被黑」类论坛感措辞。

**Script（口语）**
> An earlier security-related mistake involved a user upload path in an enterprise messaging system.
>
> At the time, avatar uploads were hosted on a Windows-based file server, and the upload controls were not strict enough. That created a security exposure which eventually forced us to rebuild and restore the environment from backups.
>
> After that incident, we tightened permissions, improved upload validation, added stronger host protections, and later moved some user-facing storage paths into more controlled cloud storage environments.
>
> The experience made me much more aware that user upload functionality should always be treated as part of the system's security boundary, not just as a simple file feature.

<a id="q-05"></a>
### 5) Tell me about a time you disagreed with your manager or a decision.
**提示（STAR）**：题干是 **disagreed with manager or a decision** — 前两句就要让人听到 **disagreement**（**首版范围/节奏**：产品要 **更强首交付**，你从 **工程 + 现场运维** 判断 **rollout risk** 过高）。**张力**是 **timing / operational risk**，不是「反对功能本身」（用 **I wasn't against the features themselves** 类句子 **去 ego**）。**做法**：**trade-offs 可见化** + **分期试点** + **现场反馈**，把讨论从主观立场拉到 **证据与共同结果**。**收尾**：主反思句偏完整时略像备稿 → 见下 **临场** 可改更短、更对话。

**Script（口语）**
> One time I disagreed with a rollout decision was during an early Smart Factory deployment.
>
> Before the first release, the product side wanted to include additional functionality because they felt it would create a stronger first delivery. From the engineering and operational side, I was concerned that the rollout risk was becoming too high because some workflows still hadn't been validated properly on the production floor.
>
> I wasn't against the features themselves — the disagreement was really about timing and operational risk.
>
> Instead of turning it into a subjective debate, I focused on making the trade-offs visible. I broke the discussion down into practical impact: which functionality was essential for a stable first rollout, which features could safely move into a later phase, and how a smaller pilot deployment could give us real operator feedback while reducing the risk of disruption.
>
> Once the discussion became more concrete and evidence-based, alignment became much easier.
>
> In the end, the team agreed to launch a smaller stable core first, validate it with real users on the production floor, and then expand functionality in later phases based on actual operational feedback.
>
> That experience reinforced for me that professional disagreement works best when the conversation stays focused on risk, trade-offs, and shared outcomes instead of personal opinions.

**临场（念法）**：若最后一段嫌「总结稿」感，**二选一**即可：**保留**上面 **reinforced… shared outcomes**；**或**改短为更对话的一句，例如：**After that rollout, I became even more careful about first-release scope whenever the environment is operational and unforgiving.** 不必两句叠念。

<a id="q-06"></a>
### 6) Tell me about a time you worked with a difficult person.
**提示（STAR）**：**主**：**Enterprise Messaging**（与 **[Q42 Option A](#q-42)** 同源）；**1:1** + **私下** review + **结对**。**备选**：**技术栈/可维护性分歧** → **[Q42 Option B](#q-42)**。
**Script（口语）**
> **Enterprise Messaging** — teammate **avoided** review after **public** criticism elsewhere. I went **1:1**, then **private**, **specific** notes, short **pairing**. Reviews and **releases** got **healthy** again.

<a id="q-07"></a>
### 7) Tell me about a time you went above and beyond.
**提示（STAR）**：**主答 ChatClothes** — 题干考 **ownership / initiative / 超出最低交付**，不是 **加班 hero**。**张力**：正式要求主要是 **研究 + demo + 论文**；你意识到 **没有部署与运行级文档** 别人很难 **独立复现或接手**。**动作**：**额外**写 **deployment guides、API documentation、user instructions**（**not formally required for grading**）。**结果**：导师肯定文档与整体组织 + **约提前六个月**提交。**反思**：功能只是工作的一部分 — **可理解、可维护、给他人可用** 同样重要。**Option B 电子秤** — 更像 **initiative / creative / workflow / customer focus**；作 **第二故事库** 与 **[创意 · 电子秤](#oral-creative)** 对齐，**不抢**本题「above minimum thesis bar」的主叙事。

**Option A — ChatClothes（主答）**
**Script（口语）**
> One example of going above and beyond was during my ChatClothes thesis project at AUT.
>
> The original requirement was mainly to deliver the research, the system demo, and the thesis itself. But while building the project, I realized that without proper deployment and operational documentation, the system would be difficult for other people to run or extend independently later.
>
> So beyond the core implementation, I also created deployment guides, API documentation, and user instructions to make the system easier to reproduce and maintain.
>
> That extra work wasn't formally required for grading, but I felt it was important because the project involved multiple components across AI models, backend services, and deployment constraints.
>
> My supervisor specifically praised the clarity of the documentation and the overall organization of the project, and I ended up completing and submitting the thesis about six months earlier than the expected schedule.
>
> The experience reinforced something I value in engineering work: delivering the feature itself is only part of the job — making the system understandable and usable for other people matters too.

**临场（念法）**：最后一段若嫌 **keynote 收尾**感，**二选一**：保留 **reinforced… matters too**；**或**改短为更对话，例如：**After that project, I became even more careful about making systems easier for the next person to use or maintain.**

**Option B — Smart Factory workflow optimization（备用 · initiative / creative / process improvement）**

**Key idea:** 强故事，但本题问 **above and beyond** 时 **让 ChatClothes 主答**；对方问 **initiative、creative idea、customer focus、floor friction** 时用本段或 [创意 · 电子秤](#oral-creative)。

**Script（口语 · 压缩骨架）**
> **Tension:** operators kept **re-typing** **scale** **readings** into a **web** **form** — small step, **high** **repetition**, easy **errors** on a **busy** **line**.  
> **Action:** **serial** listener on the **Windows** PC beside the scale, **local** **WebSocket** server, **browser** client **auto-filled** the **focused** **input** with the **live** **weight**.  
> **Result:** **less** **manual** **work**, **fewer** **mistakes**, **smoother** **hands** on the **floor**.  
> **Reflection:** **small** **operational** **friction** **compounds** **fast** in **production** environments — sometimes the **best** **win** is **removing** **dumb** **copy-paste** **work**.

<a id="q-08"></a>
### 8) How do you prioritize when you have multiple deadlines?
**提示（STAR）**：**不要**答成工具清单（Jira 四象限口号）。**排序逻辑**：**impact** + **operational risk** + **dependency** — **不是谁声音大**。**例（Smart Factory）**：**产线/操作者**直接受影响 → **立刻高于**低影响功能；再 **里程碑关键路径**；再 **低优先级改进**。**沟通**：优先级因 **线上问题/阻塞** 变了 → **早说**，让 **expectation** 现实，别最后吓人。**多线并行**：把事拆成 **最近截止 / 未解阻塞 / 依赖 / 可延后且不制造运维风险** 几块。**升级成熟**：发现自己 **不能高效单点解开** → **早升级或协调**、**厘清 ownership**、**别把瓶颈闷在自己身上**（**silently becoming the bottleneck**）。收尾 **sustainable pace** 一句即可，**忌**叠多层「领导力文章」式总结 — 见 **临场**。

**Script（口语）**
> When I have multiple deadlines, I usually prioritize based on impact, operational risk, and dependency — not simply whoever is shouting the loudest.
>
> For example, in Smart Factory projects, if something was affecting production-floor workflows or operators directly, that would immediately take priority over lower-impact feature work. After that, I would focus on milestone-critical delivery items and then lower-priority improvements.
>
> A big part of prioritization for me is also communication. If priorities changed because of a production issue or a blocker, I tried to communicate that early so expectations stayed realistic instead of surprising people later.
>
> There were also periods where I was supporting several projects at the same time — factory systems, enterprise messaging work, and some internal product development. In those situations, I would break things down very practically: nearest deadlines, unresolved blockers, dependencies, and what work could safely move later without creating operational problems.
>
> If I realized I couldn't unblock something efficiently alone, I preferred escalating or coordinating early instead of silently becoming the bottleneck myself.
>
> That approach helped us keep important systems stable while still moving long-term delivery forward at a sustainable pace.

**临场（念法）**： credibility 已够 — **少一句 abstract lesson** 也行（例如 **只念到 escalate 那句就停**）；多留 **半拍** 在 Smart Factory 例与 **多项目** 段之间，听起来更像聊天。与 **[A ⑥ Case C](#oral-06)** 可交叉练，不必两处长段完全重复。

<a id="q-09"></a>
### 9) How do you handle stress and pressure?
**提示（STAR）**：考 **情绪稳定 + 排序 + 沟通 + 可持续执行**，不是 **比惨**。**主答**：`enterprise-messaging` **早期单人 Android** — **上线后** **issue 洪峰**；**做法**：**先减不确定**、**结构化日节律**、**按 impact 稳高危**、**连续发小版本**、**产品/支持**帮用户 **对齐期望**。**忌**：一题里 **三段长篇回忆录**（**banknote**、**ChatClothes** 整段叠念）。**Air-gapped banknote mill** → **追问 / second example** 用下方 **Option B 骨架**（见 [A ⑤ Case C](#oral-05) 语境）。**ChatClothes** 的强项在 **profiling / scope / architecture**（**[Q3](#q-03)**、**[Q31](#q-31)**；**显著变化**备答见 **[Q23](#q-23) Option A**），**本题不必**再用「**提前交**」一笔带过当压力主证据。

**主答 — Enterprise IM（单人 Android + 上线后救火）**
**Script（口语）**
> When I'm under pressure, I usually try to reduce uncertainty as early as possible instead of reacting emotionally to the situation.
>
> One example was during the early release period of an Enterprise Messaging app where I was the only Android developer at the time. We launched quickly, but after release a large number of bugs and user issues started coming in at the same time.
>
> Instead of trying to solve everything at once, I worked in a very structured rhythm. Every day I reviewed the incoming issues, prioritized them by user impact, focused on stabilizing the highest-risk problems first, and released updated builds continuously instead of waiting for one huge fix.
>
> At the same time, product and support teams helped communicate realistic timelines to users so expectations stayed clear while engineering focused on recovery.
>
> That experience taught me that under pressure, staying calm and maintaining a clear execution rhythm is usually much more effective than trying to react to every issue emotionally or all at once.

**临场（念法）**： spirit 仍是 **rhythm + clarity beats panic**，**口播别 slogan 化**；主答 **到 recovery 句可停**，**不必**叠念 **banknote**。**追问**「**还有别的压力吗**」→ 再 **Option B 压缩骨架**。

**Option B — Air-gapped deployment（备用 · follow-up / unusual environment）**

**Key idea:** **memorable** 但 **heavy**；**勿**与主答 **串成长篇**。

**Script（口语 · 压缩骨架）**
> **Tension:** **high-security** **offline** customer site — **costly** **access**, **no** normal **deploy–patch–retry** loop, **long** approval cycles.  
> **Action:** **offline** packages, **heavy** **prep** before each visit, **small** **checkpoints**, **reset** timelines with PM/customer when **process** not code was the bottleneck.  
> **Reflection:** sometimes pressure is **managing process friction and expectations**, not **only coding faster**.

<a id="q-10"></a>
### 10) How would you describe your work style?
**提示（STAR）**：**systems first** → **operational picture** → **evidence before opinion** → **collaborative** → **process improvement**。

**Script（口语）**
> I'd describe my work style as **practical, systems-focused, and collaborative**.
>
> I usually try to **understand the bigger operational picture first** — how different parts connect, where the real constraints are, and what actually creates risk for users or the business — then I go deeper into the technical details where they matter most.
>
> When solving problems, I **prefer measuring or prototyping early** instead of spending too much time debating assumptions. In a lot of projects, **real usage or profiling data changes the direction** much faster than opinions do.
>
> I also value **collaborative engineering habits** — short feedback loops, code reviews, pairing when needed, and **making systems easier for the next person** to understand instead of relying too much on tribal knowledge.
>
> And after each release or project cycle, I usually **look for ways to improve the process a little** — whether that's documentation, deployment flow, testing, or communication — so the **team becomes more stable over time** instead of repeatedly fighting the same problems.

<a id="q-11"></a>
### 11) What motivates you at work?
**提示（STAR）**：**不要**答成 **钱/职级/new challenges 空话/泛泛热爱编码**。**能量来源**：**真实运营问题** + **软件长期可靠**（**long-lived systems**）；**环境**：能 **看到** 系统是否在帮人（**Smart Factory 一线**）；**技术兴奋点**：**难**但要 **接真实约束**（**ChatClothes**：不是为 AI 而 AI，而是 **离线 + 硬件边界下能跑**）。**人设**：**practical systems engineer**，不是 hype。**忌**：只有 **keynote bullet** 无场景 — 下面口稿要有 **一两句可画面化** 的例。

**Script（口语）**
> What motivates me most is building software that solves real operational problems and continues working reliably over time.
>
> For example, in Smart Factory projects, I liked seeing how software could directly reduce manual work or improve workflows for operators on the production floor. You could actually see whether the system was helping people or not.
>
> I'm also motivated by technically difficult problems when they connect to practical use cases. In my ChatClothes project, the interesting part for me wasn't only the AI itself — it was figuring out how to make AI run under real hardware and offline constraints instead of only working in ideal lab conditions.
>
> In general, I enjoy long-lived systems more than short demos. I like work where engineering decisions still matter months or years later because real users depend on the system every day.

**临场（念法）**：最后一句若嫌 **interview-polished**，**二选一**：保留 **…depend on the system every day**；**或**改更口语：**I enjoy work where the software keeps mattering after launch, not just during the demo.** 不必两句叠念。

<a id="q-12"></a>
### 12) Tell me about a time you worked effectively in a team.
**提示（STAR）**：**跨职能 6 人** → **coordination cost** → **lightweight 结构** → **clear interfaces + steady rhythm** → **10+ 厂多年交付**。

**Script（口语）**
> One example of effective teamwork was during a long-running **Smart Factory** project involving around **six people** across **backend, frontend, Android, IoT integration, and QA**.
>
> Because the system touched both **software and factory hardware workflows**, **coordination problems could quickly slow everyone down** if interfaces or responsibilities were unclear.
>
> To keep the collaboration stable, we introduced a few **lightweight but consistent working habits**. We used **shared API contracts** between teams, required interface changes to be **reviewed before breaking** existing integrations, and held **weekly demos using running code** instead of only status updates or slides.
>
> That helped **problems surface earlier** and kept everyone aligned on what was actually working in production-like environments.
>
> The project eventually **rolled out across more than ten factory sites over several years**, and I think a big reason the collaboration worked well was that the team focused on **clear interfaces, predictable communication, and steady delivery rhythm** instead of relying on constant firefighting.

<a id="q-13"></a>
### 13) Tell me about feedback you received and how you acted on it.
**提示（STAR）**：**经理反馈** → **shared context 缺失** → **delivery speed vs onboarding** → **lightweight ADR + onboarding guide** → **ramp 更顺 + 重复问题减少**。

**Script（口语）**
> One piece of feedback that really stayed with me came from a **manager during a larger long-running project**.
>
> He pointed out that some **important architectural and technical decisions** were **living too much in my head or scattered across chats**, which made **onboarding and handover harder** for newer team members.
>
> I thought the feedback was fair. At that stage, I was very focused on **delivery speed** and solving problems quickly, so I sometimes **underestimated how important shared context becomes** as projects grow.
>
> After that, I changed how I worked. I started writing **lightweight ADR-style notes** for larger technical decisions — not huge documentation, just enough to explain the **reasoning, trade-offs, and important constraints** behind the choice.
>
> I also added **short onboarding guides** for systems or modules that newer developers regularly found confusing.
>
> Over time, **onboarding became smoother**, **repeated questions dropped**, and **technical discussions became easier** because more context was already documented and shared.
>
> After that, I became much more careful about making important decisions **easier for the next person to understand** — good documentation isn't about writing more, it's about **reducing future confusion**.

<a id="q-14"></a>
### 14) Describe a time you had to learn something quickly.
**提示（STAR）**：**情境**：**ChatClothes** 管线需 **扩散 / OOTDiffusion** 与 **LoRA 微调**（见 `projects/chatclothes/facts.yaml`）。**张力**：领域新、**里程碑紧**（自述约 **~two months** 内要跑出可信 **fine-tune** 闭环）。**做法**：**论文 + 官方栈 → 先跑通推理 → trace 耗时/显存/训练热点** → **小步 LoRA 实验**（约 **~six weeks** 进入可迭代跑法）；**PyTorch / Hugging Face** 为可迁移基础。**收束**：快速学习 = **早跑代码、用测量缩小该读什么**，不是纯堆文献。**临场**：追问再展开 **DressCode / VITON-HD** 或指标；口试忌 **名词连读** 无停顿。

**Script（口语）**
> A clear example was during my **ChatClothes** thesis work at **AUT**, where part of the pipeline depended on **diffusion-based virtual try-on** and I needed to get **LoRA fine-tuning for OOTDiffusion** working on a tight timeline.
>
> That corner of **diffusion** and **OOTDiffusion** was genuinely new to me — I couldn't just pattern-match from older projects. I gave myself about **two months** to reach a credible **fine-tuning** loop for the next thesis milestone.
>
> Instead of reading for weeks in isolation, I used a very practical loop: **paper → stack → run inference → trace** where time and memory actually went. Once the pipeline moved, I focused experiments on what really changed outputs — not every hyper-parameter at once.
>
> Within about **six weeks** I was running **LoRA** training experiments I could iterate on. What transferred quickly was tooling I already knew — **PyTorch** and **Hugging Face** — but the new part was learning how **LoRA** interacted with **OOTDiffusion** without destabilizing generation quality.
>
> What stuck with me is that **fast learning** wasn't memorizing the literature first — it was **shrinking unknowns early** by getting **runnable code** in front of me and letting **measurements** tell me what to study next.

**临场（念法）**：**OOTDiffusion / LoRA** 可念慢一点；**最后一段**若嫌「方法论收尾」感，**可删**，停在 **six weeks… iterate** 也行。

<a id="q-15"></a>
### 15) Are you comfortable working in an Agile team?
**提示（STAR）**：**双周 Sprint 六年** → **反馈循环短** → **working software > status reports** → **用户看到真系统后需求演进** → **demo 验证方向**。

**Script（口语）**
> Yes, I'm comfortable working in Agile environments.
>
> In **Smart Factory** projects, we worked in roughly **two-week sprint cycles** for **several years**. We used the usual Agile practices — **sprint planning, standups, retrospectives, backlog prioritization, and estimation** — but what mattered most for us was **keeping feedback loops short** and making progress visible early.
>
> Because the projects involved **real factory workflows and hardware integration**, **requirements often evolved once users saw the system running in practice**. So **regular demos with working software** became much more valuable than long discussions or status reports.
>
> That helped the **team adjust priorities earlier**, **catch misunderstandings faster**, and **keep engineering aligned** with what operators actually needed on the production floor.
>
> For me, the most useful part of Agile is not the ceremony itself — it's the ability to **continuously validate direction with real users and working systems** instead of waiting until the very end.

<a id="q-16"></a>
### 16) How do you handle code review feedback?
**提示（STAR）**：**不要**答成「我全盘接受」或 **ego 防御**。**收反馈**：**review 是工程机制** → **先理解 comment 背后的 risk/context** → 仍有分歧则 **讲约束与 trade-off**，**不对人**。**给反馈**：**具体**、**落在代码与工程影响**、**说明为何以后会变成问题**。**心理安全**：目标是 **一起把系统变好**，不是 **谁赢辩论**。**临场**：最后一句若嫌 **management tone**，改用更短口语（见下）。

**Script（口语）**
> I usually treat code review as part of collaborative problem solving, not as personal criticism.
>
> When I receive review feedback, my first step is usually to understand the reasoning behind the comment, because many good review comments come from context or risks I may not have fully considered myself.
>
> If I still see the problem differently, I try to explain the trade-offs or constraints behind my approach instead of turning it into an ego discussion about who is "right."
>
> I also try not to ignore comments or react emotionally to them. In most cases, even when I disagree initially, the discussion improves the final result somewhere.
>
> When I give feedback to other developers, I try to keep it specific, focused on the code and engineering impact, and clear about why something may become a problem later instead of making comments feel personal.
>
> I think healthy code review culture works best when people feel they are improving the system together, not defending themselves from criticism.

**临场（念法）**：**最后一段**若嫌 **polished / 领导力腔**，**二选一**：保留 **healthy code review culture…**；**或**改更对话：**I've found reviews usually go much better when people feel the goal is improving the system, not defending their own code.** 不必两句叠念。

<a id="q-17"></a>
### 17) Tell me something you built that you're genuinely proud of.
**提示（STAR）**：**主答 Smart Factory** → **不只是软件 demo** → **真生产环境 10+ 厂** → **硬件集成 + 可测量 impact** → **operators felt workflow 更顺** → **长期学习 + 持续交付**。**备用 Enterprise Messaging NDK**：**Tension-Action-Result 结构**。

**Script（口语）** — **主：Smart Factory（约 45–55s）**

> One project I'm **genuinely proud** of is the **Smart Factory** program I worked on for **several years**.
>
> It wasn't just a **software demo** — it was a **real production environment** across **more than ten manufacturing sites**, involving **factory workflows, hardware integration, shop-floor operations, and long-term rollout support**.
>
> The system connected **multiple layers together**: backend services, web platforms, Android tools for operators, and edge-side integrations with devices like **scales and RFID equipment**. One thing I liked about the project was that the software had **very visible operational impact**. Improvements were **measurable** — including **roughly thirty percent** efficiency improvement in some of the production metrics we tracked — and **operators could genuinely feel** the workflow becoming smoother.
>
> What I'm most proud of isn't only the technology itself, though. I **spent a lot of time** understanding **real factory workflows**, working **directly with operators, customers, product teams, and engineers**, and **helping coordinate delivery** across a **small cross-functional team** over a long period of time.
>
> I also **didn't start** the project already **knowing every layer** involved. A big part of the experience was **learning continuously while still delivering reliably** in production environments.
>
> For me, that's the kind of engineering work I enjoy most — **systems that people depend on every day**, where **reliability and operational reality matter as much as the code itself**.

**Script（口语）** — **备用：Enterprise Messaging NDK（约 20–25s）**

> **Enterprise Messaging native path** — **Java alone couldn't meet the latency target** (needed **sub-200ms** at **~5k DAU**). I built a **native TCP/UDP + JNI** path to handle the hot path. It's been in **production for more than ten years**. **Long life** is what I'm proud of — systems that **stay alive and useful** in real production.

<a id="q-18"></a>
### 18) If you were the last member of the team in the office on a Friday afternoon and the product owner asks you to deploy a change to production, what would you do?
**提示（STAR）**：考 **production judgment**，不是 **敢不敢点发布**。**态度**：**先降速** — 周五下午 + **support coverage 变弱**，风险阈值应更高。**核对**：影响面、**测试是否覆盖**、**回滚路径是否清楚**、**监控与 release notes** 是否就绪。**不能自信验证恢复路径** → **升级**或 **挪到下一发布窗**，避免 **无谓周五 prod 风险**。**若确属紧急且集体决定上**：**监控打开**、发版后 **紧盯日志**、**回滚步骤随手可执行**。**收束**：靠 **准备与运行纪律**，不靠 **信心或猜**。**spirit**：原有一句 **No guess clicks** 很准 — 口播若嫌 **slogan**，见 **临场** 换成更对话说法。

**Script（口语）**
> If I'm the last person in the office on a Friday afternoon and someone asks for a production deployment, my first reaction is usually to slow the situation down instead of rushing.
>
> I'd first try to understand the scope and risk of the change: what systems are affected, whether the change has already been tested properly, whether rollback steps are clear, and whether monitoring and release notes are ready.
>
> If I can't confidently verify the deployment safety or recovery path, I'd rather escalate the decision or move the release to the next deployment window instead of taking unnecessary production risk late on a Friday.
>
> If the deployment is genuinely urgent and we decide to proceed, then I'd make sure monitoring is active, logs are being watched closely after release, and rollback steps are immediately available if something goes wrong.
>
> In general, I think production releases should rely on preparation and operational discipline, not confidence or guesswork — especially at the end of the week when support coverage is limited.

**临场（念法）**：**No guess clicks** 可作 **心里锚点**；口播若嫌 **punchline 感**，**二选一**：保留上面 **guesswork / support coverage** 收尾；**或**加一句更松的：**I don't like production deployments that rely on assumptions, especially late on a Friday.** 与正文末段 **二选一** 即可，不必叠满。

<a id="q-19"></a>
### 19) How would you respond if you don’t know the answer to a question?
**提示（STAR）**：考 **未知下是否可靠**，不是 **全知**。**态度**：**不装懂**；**先澄清**题干与语境（真问题常与第一句字面略有偏差）。**做法**：说明 **已知边界**、**不确定从哪开始**、**怎么查证**（文档 / 代码路径 / **生产日志** / 复现 / 问对口的人）。**原则**：**可靠、有条理** 优于 **听起来很确定**；重要事项 **事后 follow up** 给已核实答案 — **unknown 不可怕，失联才可怕**。**临场**：若嫌 **leadership article** 腔，见下 **二选一** 替换句。

**Script（口语）**
> If I don't know the answer to something, I try not to pretend that I do.
>
> Usually my first step is to clarify the question properly, because sometimes the real problem is slightly different from the initial wording and context matters a lot.
>
> Then I'll explain what I do know, where the uncertainty starts, and how I would investigate the missing part — whether that's checking documentation, reviewing code paths, looking at production logs, reproducing the issue, or speaking with someone closer to that area.
>
> I think in engineering it's much more important to be reliable and methodical than to sound confident about things you haven't verified yet.
>
> In practice, I'm comfortable learning new systems quickly, but I prefer being transparent about what I know versus what still needs confirmation.
>
> And if it's something important, I make sure to follow up afterward with the verified answer instead of letting the question disappear.

**临场（念法）**：**“reliable and methodical…”** 一段若嫌 **polished**，**二选一**：保留；**或**改更口语：**I've found it's usually better to be clear about uncertainty than to sound confident and be wrong.** 与 **follow up** 句衔接自然即可，不必叠两句价值判断。

<a id="q-20"></a>
### 20) Describe a time when you led a team. What was the outcome?
**提示（STAR）**：**技术 leadership**（非 formal management）→ **跨职能 6 人** → **集成风险** → **API contracts** → **weekly demos** → **stable rhythm** → **10+ 厂长期 rollout**。

**Script（口语）**
> I'd describe it more as **technical leadership** than formal people management.
>
> One example was during a long-running **Smart Factory** program involving a **small cross-functional team** of around **six people** across **backend, frontend, Android, IoT integration, and QA**.
>
> Because the system **connected factory workflows, hardware devices, and multiple software layers**, **integration and coordination were the biggest risks**. If teams moved independently without enough alignment, small interface mismatches could quickly slow down delivery or create rollout problems on site.
>
> A big part of my role was **helping create a stable engineering rhythm** for the team. We introduced **clearer API contracts** between systems, **lightweight review steps** before interface changes, and **weekly demos using integrated running software** instead of isolated module updates.
>
> That helped **surface issues earlier**, **reduced integration surprises**, and **kept everyone aligned** around what was actually working end-to-end.
>
> Over several years, the system **successfully rolled out across more than ten factory sites** with **stable operation** and **repeatable deployment processes**.
>
> After a while we realized **coordination problems were usually more dangerous than the coding itself** — technical leadership is often less about directing people and more about **reducing coordination friction** so the whole team can deliver consistently together.

<a id="q-21"></a>
### 21) Describe a time when you had to give someone difficult feedback. How did you handle it?
**提示（STAR）**：**不要**答成 **粗暴指责 / 压权威 / 单纯「你做错了」**。**情境**：**Junior** 实现 **技术尚可**，**文档与交接** 薄 → **评审与维护成本** 上升。**做法**：**先肯定**做得好的部分 → **把影响讲具体**（**onboarding 成本、review 变慢、后续改动风险** — **clear cost for the next person**）→ **不只指出问题**：给 **轻量模板** + **结对走一个真实例子**，让期望 **可落地**。**结果**：文档与评审节奏改善，对方也更敢讲清自己的设计取舍。**人设**：**low-ego technical coaching**。**持续机制**可并 **[Q45](#q-45)** 备选「**文档/ADR**」线、**[Q13](#q-13)**。**临场**：若嫌 **HR 式 polished 收尾**，见下 **二选一**。

**Script（口语）**
> One time I had to give difficult feedback was to a junior developer whose implementation work was generally solid, but the documentation and handover quality were making reviews and maintenance harder for the rest of the team.
>
> I didn't want the conversation to feel like criticism of their ability, so I started by acknowledging the parts they were already doing well technically.
>
> Then I explained the engineering impact more concretely — that unclear documentation increases onboarding cost, slows reviews, and makes future changes riskier for the next person working on the system.
>
> Instead of only pointing out the problem, I also tried to make improvement easier. I shared a lightweight template for documenting changes and paired with them once on a real example so the expectations felt practical instead of abstract.
>
> Over time, the quality of the documentation improved, reviews became smoother, and the developer became much more confident explaining their own design decisions as well.
>
> That experience reinforced for me that difficult feedback works much better when it's specific, actionable, and focused on helping the other person succeed rather than just pointing out flaws.

**临场（念法）**：**“reinforced for me…”** 若嫌 **interview-perfect**，**二选一**：保留；**或**改更口语：**After that, I became more careful about making feedback practical instead of only critical.** 不必两句价值判断叠念。

<a id="q-22"></a>
### 22) Tell me about a time when you missed a deadline. What happened, and how did you handle it?
**提示（STAR）**：**中草药 CV 标注项目** → **真实数据 vs 理想假设** → **数据质量差** → **早沟通** → **重设预期** → **pilot batch 测吞吐** → **更可预测**。

**Script（口语）**
> One time I missed a deadline was during a **computer vision-related labeling project** involving **Chinese herbal data**.
>
> At the beginning, I estimated the work would take about **two weeks**, but once we started processing the **real image set**, the **data quality turned out to be much messier** than expected — **inconsistent photos**, **unclear labeling boundaries**, and **much more manual cleanup** than the original estimate assumed.
>
> Pretty quickly I realized the **timeline was no longer realistic**.
>
> Instead of **staying quiet** and hoping we could somehow catch up later, I **raised the issue early**, explained why the estimate had changed, and worked with the team to **reset expectations and adjust the schedule**.
>
> I also changed how we approached the work technically and operationally. Instead of **estimating based on assumptions**, I started using **smaller pilot batches first** to **measure realistic throughput** before committing to larger delivery timelines.
>
> The final delivery took **closer to six weeks than two**, but the process afterward became **much more predictable and less risky**.
>
> After that project, I **stopped trusting early estimates** until I'd **seen real sample throughput first**.

<a id="q-23"></a>
### 23) Tell me about a time when you had to deal with a significant change at work. How did you adapt to this change?
**提示（STAR）**：考 **随约束与业务演变而调整**，不是 **十年架构演讲**。**主答**：**`enterprise-messaging` 长期演进** — 从 **独立企业 IM** → **共享身份 / 文件 / 权限 + 多子系统的平台**；技术侧 **单机文件 → FastDFS**、**自建消息底层难稳 → Easemob 平台/SDK**（细节追问见 `facts.yaml`）；组织侧 **工具/文档/审批/自动化**（**informal 沟通单独不够 scale**）；个人 **从单线开发 → 跨系统协调、交付与优先级**。**主线一句**（可先在心里念）：**The system stopped being just a chat app and became shared infrastructure.** **忌**：**JPush / 七牛 / 阿里云对标** 等名词 **一口气全倒** — 留追问。**Option A ChatClothes** — **短答 / AI 岗 / technical adaptation** 用 **backup 骨架**；**深叙事**仍可用 **[A ⑨ Case A](#oral-09)**。

**主答 — Enterprise IM evolution（简化版）**
**Script（口语）**
> One major change I had to adapt to happened during the long evolution of our Enterprise Messaging platform.
>
> When the product started, it was mainly a standalone enterprise chat system. But over time, the business needs changed significantly. The platform gradually expanded into a larger ecosystem with shared user identity, centralized file management, permissions, and multiple business subsystems built on top of the same infrastructure.
>
> That change affected both the architecture and the way the team worked.
>
> On the technical side, some earlier decisions no longer scaled well. For example, file storage outgrew a single-server model, so we moved toward a distributed FastDFS-based approach for better scalability and operational control.
>
> Messaging infrastructure also evolved. We originally maintained more low-level messaging components ourselves, but stability and maintenance costs kept growing. Eventually we moved core messaging flows onto Easemob's platform and SDK ecosystem, while our own engineering effort focused more on business logic, permissions, workflows, and shared platform services.
>
> The organization evolved too. As the number of projects and teams grew, we introduced more structured collaboration tools, documentation, approvals, and automation processes because informal communication alone stopped scaling well.
>
> Personally, my role changed a lot during that period. I started mainly focused on development work, but over time I became more involved in cross-system coordination, delivery planning, technical trade-offs, and helping manage priorities across parallel projects.
>
> What helped me adapt was staying flexible about the original design and being willing to re-evaluate assumptions as scale, operational pressure, and business needs changed over time.

**临场（念法）**：口播 **抓一条主线**（上段首句或 **chat app → shared infrastructure**）；**别**把 **Easemob/FastDFS/子系统** 再扩成第二篇长文。**AI 岗只要短答** → 可只念 **Option A** 四行骨架。

**Option A — ChatClothes（backup · concise / AI / technical adaptation）**

**Script（口语 · 压缩骨架）**
> **Tension:** **offline** + **speed** became **hard constraints** mid-project.  
> **Action:** **re-profiled** the pipeline, moved the **LLM** path **local**, and **cut** scope **strategically** where needed.  
> **Result:** a **full working offline pipeline** on **constrained hardware**.  
> **Reflection:** adaptation starts with **measurement**, not **attachment** to the **first** design.

<a id="q-24"></a>
### 24) Describe a time when there was a conflict within your team. How did you help resolve it? Did you do anything to prevent it in the future?
**提示（STAR）**：**团队内部**（工程 vs 产品 vs 运营）→ **需求漂移 + 定义不清** → **原型对齐** → **单一决策人** → **预防：ownership + prototype + requirement discipline**。

**Script（口语）**
> One conflict situation I helped resolve happened during a **Smart Factory** project where **different groups inside the team** had very different views of the workflow and priorities.
>
> **Operators** focused on usability and speed on the production floor, **managers** focused on reporting and process control, while **product and engineering teams** were trying to balance delivery timelines with changing requirements.
>
> Over time, the **team started feeling friction** because **priorities kept shifting** and **different people had different definitions** of what "done" actually meant. **Engineering risk** also increased because **requirements were changing faster** than the implementation could stabilize.
>
> What helped was moving the **discussion away from abstract debates** and toward **working prototypes and real workflow demonstrations**. Once people could **interact with actual screens** and production-style flows, feedback became **much more concrete** and misunderstandings dropped quickly.
>
> We also aligned around a **single customer-side decision maker** who could **prioritize requests** and **confirm workflow direction** instead of every conversation becoming a new requirement change.
>
> That helped **reduce scope churn**, **stabilize delivery planning**, and **improve collaboration** between engineering, product, and operational stakeholders.
>
> To help prevent similar problems later, we became much more **disciplined about defining ownership**, **validating workflows earlier with prototypes**, and **separating discussion ideas from confirmed requirements**.
>
> The real issue turned out to be **coordination and clarity problems**, not personal disagreements.

<a id="q-25"></a>
### 25) Describe a time when you went out of your comfort zone. Why did you do it? What lessons did you learn from the experience?
**提示（STAR）**：**ChatClothes** → **从 Android/后端/企业软件** → **AI diffusion/模型优化/部署约束** → **跨领域快速学习** → **理论 + 实验 + 迭代** → **小规模实验比纯理论更快**。

**Script（口语）**
> One experience that pushed me outside my comfort zone was my **ChatClothes** thesis project, where I had to move **much deeper into diffusion models and modern AI workflows** than my previous background.
>
> Before that, most of my experience was in **Android, backend systems, enterprise software, and industrial platforms**. The AI side — especially **diffusion pipelines, model optimization, and deployment constraints** — required me to **learn a very different stack** in a relatively short amount of time.
>
> What helped was **not trying to learn everything theoretically first**. I **combined reading papers with hands-on experimentation** very early: **running inference pipelines**, **tracing model code**, **profiling bottlenecks**, **modifying small components**, and gradually understanding how the system behaved in practice.
>
> I found that **small working experiments** taught me much faster than staying too long in theory-only learning.
>
> Over time, I became comfortable moving between **research ideas and practical engineering constraints**, which was important because the **final system also had to run offline on lightweight hardware** instead of only working in ideal environments.
>
> I learned much faster once I **stopped waiting to fully understand everything** before touching the code.

<a id="q-26"></a>
### 26) How would you design/test a product to make sure its diverse/inclusive to all users?
**提示（STAR）**：**不背** diversity 术语、**不装**全公司 **D&I 项目 owner**。**立场**：从 **工程 + 产品可用性** 答 — **同理心 + 意识** 落在 **可验证行为**。**做法**：**早期**定 **可测** 目标（**对比度、字号缩放、键盘导航（如适用）、读屏、清晰语言、弱网/弱机表现**）；**尽早**让 **不同背景用户** 接触系统 — 很多问题 **只有真实使用才暴露**。**流程**：开发中 **持续测**，别堆到上线前一刻。**收束**：包容设计 **不是单独「功能」**，而是 **让更多人、更多环境下可靠工作** 的软件的一部分。**临场**：若末句 **polished**，见下 **二选一**。

**Script（口语）**
> I haven't personally led a full diversity and inclusion program, so I wouldn't pretend to be an expert in that area.
>
> But from an engineering perspective, I think inclusive products become much more achievable when the goals are concrete and testable instead of only theoretical.
>
> For example, I'd look at accessibility basics early in the process — things like readable contrast, scalable font sizes, keyboard navigation where relevant, screen reader compatibility, clear language, and how the product behaves under weaker devices or lower-bandwidth environments.
>
> I also think it's important to get feedback from different kinds of users as early as possible instead of assuming one workflow fits everyone. In practice, many usability problems only become obvious once real users interact with the system.
>
> So my approach would usually be: define measurable accessibility and usability goals early, test them continuously during development instead of at the end, and keep iterating based on real feedback.
>
> I see inclusive design less as a separate feature and more as part of building software that works reliably for a wider range of people and environments.

**临场（念法）**：最后一句若嫌 **crafted**，**二选一**：保留 **…wider range of people and environments**；**或**改更口语：**I've found a lot of accessibility or usability issues only become obvious once different kinds of people actually use the product.**（与上一段 **real users** 略有重复时 **二选一** 即可。）

<a id="q-27"></a>
### 27) Tell me about a time you disagreed with a colleague. How did you handle the situation?
**提示（STAR）**：**工程分歧**（非 stakeholder 冲突）→ **Smart Factory rollout scope** → **产品想要更多功能** → **工程更关注 rollout 稳定性** → **Tension：delivery ambition vs operational risk** → **分阶段发布** → **make trade-offs visible**。

**Script（口语）**
> One disagreement I had with a colleague happened during a **Smart Factory rollout** where we had **different views on release scope and timing**.
>
> From the **product side**, there was **pressure to include more functionality** before the first deployment because everyone wanted the release to feel more complete.
>
> From the **engineering side**, I was more **concerned about rollout stability** because some workflows still hadn't been **fully validated on the production floor**.
>
> The disagreement wasn't really about the **value of the features themselves** — it was about **balancing operational risk against delivery ambition**.
>
> Instead of **arguing from personal preference**, I tried to **make the trade-offs more visible**. We **broke the discussion down** into: what functionality was **critical for the first stable rollout**, what could **safely move into later phases**, and what **operational risks were still uncertain**.
>
> We also discussed how a **smaller pilot deployment** could give us **real production feedback much earlier** instead of betting everything on one large release.
>
> Once the discussion became **more concrete and evidence-based**, alignment became much easier. We agreed on a **phased rollout approach**, stabilized the first deployment, and **expanded functionality later** based on real operator feedback.
>
> Disagreements are usually easier to resolve when the conversation focuses on **shared goals, risks, and trade-offs** instead of defending personal opinions.

<a id="q-28"></a>
### 28) How do you stay up-to-date with the latest technological advancements?
**提示（STAR）**：**不要**答成 **刷 YouTube / 泛泛追新闻 / 只收藏不练**。**习惯**：**读**（论文、**官方文档**、**靠谱博客**、**开源仓库**）— 尤其搞清 **系统底下怎么工作**，而不只 **API 表面**。**关键**：**读不够** → **小原型 / POC**、跑推理、**改一小块看行为**（与 **ChatClothes**、**[Q14](#q-14)** 一致：**hands-on validation**）。**轻笔记**留住 **trade-off**，方便回看。**人设**：**hands-on systems learner**。**临场**：若末句 **polished**，见下 **二选一**。

**Script（口语）**
> I usually stay up to date by combining reading with small hands-on experiments.
>
> I read technical papers, official documentation, engineering blogs, and open-source repositories — especially when I'm trying to understand how a system works underneath instead of only learning the surface-level API usage.
>
> But I've found that reading alone usually isn't enough for me. What helps most is building small prototypes or proof-of-concept experiments around the ideas I'm learning.
>
> That's how I moved deeper into areas like diffusion models, LoRA workflows, and local AI deployment during my ChatClothes project. I didn't try to understand everything theoretically first — I learned by running inference pipelines, tracing code paths, modifying small pieces, and seeing how the system behaved in practice.
>
> I also keep lightweight notes while learning so the important ideas and trade-offs are easier to revisit later.
>
> In general, I learn fastest when theory and experimentation happen together instead of separately.

**临场（念法）**：最后一句若嫌 **crafted**，**二选一**：保留 **theory and experimentation together**；**或**更口语：**I usually understand new technology much faster once I've actually built something small with it.**

<a id="q-29"></a>
### 29) Why are you interested in working at [company name]?
**提示（STAR）**：**主练 Air New Zealand** → **运营型数字系统**（travel systems, timing, communication, operational flow）→ **软件质量直接影响用户体验** → **engineering culture + long-term ownership** → **与 Smart Factory / enterprise messaging 经验对齐**。**投前**做 **[业务 + JD 对齐](#oral-b1-01-why-company-research)**。备选公司名 **Hotter** 见同锚点「备选」段（**请确认正式英文公司名**后替换）。其他雇主仍可用模板方括号。

**Script（口语）** — **Air New Zealand（30 秒版）**
> I'm interested in **Air New Zealand** because it's the kind of environment where **software quality directly affects real customer experience** and **operational reliability at scale**.
>
> That's very close to the work I've already done — **enterprise messaging systems**, **Smart Factory platforms**, and **operational tools** where **stability and responsiveness** mattered in **real production environments**.
>
> I also like **long-term product environments** with **strong ownership and engineering discipline**, so the role feels like a **strong fit** for both my background and the type of systems work I enjoy.

**Script（口语）** — **Air New Zealand（60 秒版）**
> I'm interested in **Air New Zealand** because it's an environment where **software quality and operational reliability directly affect real customer experience at scale**.
>
> In **travel systems**, users **immediately feel** whether the software is **clear, responsive, and reliable** — especially during **real travel situations** where **timing, communication, and operational flow** matter. I enjoy that kind of engineering environment because the **impact of good systems is very visible**.
>
> That connects closely with the kind of work I've already done. I've spent years building **enterprise messaging systems**, **Smart Factory platforms**, and **operational tools** where **reliability, responsiveness, and stable delivery** mattered in **real production environments**, not just in demos.
>
> I'm also looking for a **mature engineering culture** with **strong ownership** and **long-term product thinking**. I enjoy working on **systems that evolve over time**, where **maintainability, operational discipline, and collaboration** matter as much as feature delivery itself.
>
> I think my background fits that kind of environment well because I'm **comfortable working across multiple layers** — **client applications, backend systems, integrations, deployment workflows, and operational support** — especially in systems where **reliability and coordination become critical**.
>
> It feels like the kind of environment where my background would actually be useful.
**Script（口语）** — **备选 Hotter（公司全名请自换）**
> Same **motivation** as **Air** **New** **Zealand** — **trust-based** **culture** plus **products** **users** **feel** — but at **[Hotter — fix name]** I'd **[one line: what they build — fill after you confirm the company]**. My **proof** stays the **same**: **Smart Factory**, **smart-power**, **Android**/**Java** **delivery** under **real** **constraints**.

**追问**
- **What do you know about our business / tech?** → 用 **[oral-b1-01-why-company-research](#oral-b1-01-why-company-research)**：JD 原词 + 公开信息，**不猜**内部架构。
- **Why not stay in China / why NZ?** → **家庭**、**长期生活**、**职业连续**（与 **Q32** 一致），**不贬**原居地。
- **How do you handle on-call / travel in aviation?** → 诚实：**听 JD**；你有 **产线/现场** 与 **高可用交付** 习惯，愿按团队排班。

**短答英文（背 1 句即可）**
> I **won't** **guess** your **internals** — I've **read** **your** **posting** and **public** **materials**; my **proof** is **shipping** **measurable** **work** in **factory**, **power**, and **large-scale** **mobile**.

<a id="q-30"></a>
### 30) Assume you are given a task to design a system. How would you do it? How would you resolve ambiguity?
**提示（STAR）**：题干含 **design a system** — 不要只答成 **需求发现**；要带出 **如何结构化思考、降不确定、验证假设、让架构随现实演进**。**起点**：**真实 workflow + 运行约束**（**Smart Factory**：初期常 **ambiguous**，操作者 **痛点多但说不清「理想流程」**）。**做法**：**现场观察**（延迟、信息缺口、摩擦在哪）→ **拆成更小的可验证块**，**避免一次画完美大图** → **快原型** 让用户对 **具体界面/流程** 反应（**people react more accurately to something concrete**）→ 随反馈 **调优先级、改流程、让架构围着线上有效部分演化**。**模糊时**：**假设写清楚** — **轻量 ADR**、高风险区 **spike**、能 **分期** 就不 **一把梭**。**收束**：**快反馈 + 运营验证** 往往比 **过早死磕规格文档** 更降风险。**临场**：中间可插 **一两句现场口吻**（如 **What we noticed pretty quickly was…**），少纯 **retrospective 总结腔**。

**Script（口语）**
> When I'm asked to design a system, I usually start by understanding the real workflow and constraints before jumping directly into architecture decisions.
>
> In a lot of Smart Factory projects, the biggest challenge at the beginning wasn't technology — it was ambiguity. Operators often knew parts of the workflow were painful or inefficient, but they couldn't always describe the ideal process clearly in technical terms.
>
> So instead of relying only on requirement documents or long meetings, we spent time on the production floor observing how people actually worked, where delays happened, what information they needed most often, and where operational friction appeared in practice.
>
> From there, I usually break the problem into smaller validated pieces instead of trying to design the entire perfect system upfront. We built quick prototypes and tested workflows directly with users because people react much more accurately to something concrete than to abstract discussions.
>
> As feedback became clearer, we refined the workflows, adjusted priorities, and evolved the system architecture around what was actually working in production environments.
>
> When ambiguity exists, I also try to make assumptions visible early — lightweight ADRs for major decisions, small spikes or prototypes for risky areas, and phased rollouts where possible instead of betting everything on one large design upfront.
>
> I've found that in complex real-world systems, fast feedback loops and operational validation usually reduce risk much more effectively than trying to perfect the specification too early.

**临场（念法）**：在 **「车间观察」** 与 **「拆块原型」** 之间，可插半句现场过渡（例如 **People actually struggled with…** / **The workflow looked simple until we watched a shift**），打破纯 **architect retrospective** 节奏；**末段**若嫌满，可**省略** **I've found…** 一句。

**追问**
- **Give a concrete example.** → **Smart Factory** 下车间 + 分期试点；或 **断网厂区** 见 **A ⑤ Case C**。
- **How do you document decisions?** → **ADR / 一页架构** + 里程碑；大分叉 **spike** 再写结论。
- **What if stakeholders disagree after prototype?** → 回到 **约束与数据**；必要时 **试点范围** 缩小再量。

**短答英文**
> I start from **real workflows + constraints**, **slice** into **validated** pieces, **prototype early**, make **assumptions visible** (**light ADRs / spikes**), use **phased rollouts** when I can — **operational validation** beats **perfecting the spec** too early.

<a id="q-31"></a>
### 31) What is the biggest technical challenge you have worked on?
**提示（STAR）**：**主答 Android OEM 碎片化** → **不是单一 bug** → **真实用户环境的长尾** → **lab setup 永远小于 reality** → **分层保活策略 + 备用通道** → **trade-off: release speed vs test depth vs operational risk**。**Backup**: ChatClothes（离线 AI 延迟优化）、FastDFS（分布式文件存储）。

**Script（口语）** — **主：Android OEM 碎片化（约 45–60s）**
> One of the biggest technical challenges I worked on was **large-scale Android reliability** for an **enterprise messaging platform**.
>
> The hardest part wasn't the **messaging logic itself** — it was the **real-world Android ecosystem**. Different OEMs like **Xiaomi, Huawei, and OPPO** all **modified Android behavior differently**, especially around **background execution, battery management, notifications, and process survival**.
>
> A lot of issues **only appeared in real user environments** and couldn't always be reproduced reliably in **emulators or even on devices with the same Android API level**. **Vendor-specific ROM behavior mattered a lot**.
>
> At the same time, we had **practical constraints**. We couldn't realistically **test every device and every ROM combination** before every release without **exploding schedule, testing cost, and hardware budget**.
>
> So we had to **balance release speed, test depth, and operational risk** carefully. We focused our **main QA coverage on mainstream Android versions and high-usage devices** first, then **investigated deeper on strong production signals** — sometimes **buying target phones**, sometimes **reproducing issues directly with users** in their real environments.
>
> We also **designed the system defensively**: **layered keep-alive strategies**, **backup push channels**, **reconnect logic**, **session restore**, **message re-sync**, and **stronger state reconciliation** after reconnects.
>
> What made the challenge difficult wasn't one bug — it was dealing with a **huge long-tail environment** where **the lab setup was always smaller than reality**.
>
> That experience taught me a lot about **operational engineering trade-offs**: **perfect coverage is usually impossible at scale**, so the real skill becomes **reducing risk, prioritizing correctly, and responding quickly** when production signals appear.

**Script（口语）** — **Backup：ChatClothes（AI 延迟优化，约 20s）**
> Another hard AI challenge was making the **entire pipeline usable offline on lightweight hardware**. I originally assumed **diffusion was the main bottleneck**, but **profiling showed cloud LLM latency was actually dominating** the experience. I **moved the LLM local**, **reduced model weight** where possible, and **optimized the vision path** with a lighter YOLO pipeline. The system became **fast enough for real offline demos**, and I finished the thesis early.

**Script（口语）** — **Backup：FastDFS（分布式文件存储，约 20s）**
> Another hard challenge was **distributed file infrastructure**. **Chat attachments plus business documents** outgrew a **single-server setup**, but **privacy requirements** meant we couldn't simply move everything to **public cloud storage**. We **built around FastDFS** and had to think about **redundancy, sharding, backup, access control, and cross-system integration** as shared infrastructure, not just "upload works".

**追问**
- **Biggest mistake in that project?** → 可转 **Q4** **主：发版配置**；**安全岗**再 **Option C**；或 **剖分错了先优化 diffusion**。
- **How measured latency / DAU?** → **profiling**、日志与现场计时；DAU 来自 **运营侧指标**（与 facts 一致，勿编新数）。
- **Why not buy cloud IM earlier?** → **成本/可控/当时能力**，后迁 **Easemob** 换稳定性（**Q23**）。

**短答英文**
> I **measured** **first** — **profiling** beat **guessing**; for **scale** we **traded** **vendor** **risk** vs **self-hosting** **control** **explicitly**.

<a id="q-32"></a>
### 32) Why do you want to change your current company?
**提示（STAR）**（与 `kb/profile.yaml` 一致，并含你的叙事）：**纽面稳态**：**不抱怨上家**、**不编办公室政治**、**不虚假激情**、**不过度 personal**、**不 defensive** — 主线 **life transition + career continuity**（**地点变了，工程方向一致**）。**核心 tension**：**relocation 中断职业连续性 → 重建长期工程路径**。**事实链**：**家庭/长期生活** **中国 → 新西兰** → **离开原职、在奥克兰本地重建职业**；**AUT MCIS** **2026-02** **First Class**，**ChatClothes**（**applied AI + 实际部署约束**，**保持贴近真实工程问题而非纯学术研究**）；现求 **Auckland 全职工程**。**价值**：仍认可 **enterprise messaging / Smart Factory** 等积累，强调 **reliability, scaling, long-term maintenance with real users**，愿 **在此长期** 延续 **Android / backend / 运营型平台 / AI 工程**。**PSWV** 全职权利。

**Script（口语）** — **推荐版（约 45–60s）**
> I'm looking for a new opportunity mainly because my **life changed direction** over the last few years.
>
> I moved from **China to New Zealand for family and long-term lifestyle reasons**, so I **stepped away** from my previous role and **focused on rebuilding things locally** here in Auckland.
>
> During that period, I completed my **Master's at AUT with First Class Honours**. My thesis was very **applied** — **AI systems, offline inference, deployment constraints**, that kind of work — so I **stayed pretty close to real engineering problems** rather than purely academic research.
>
> Now that I've finished the degree, I'm looking to **move back into full-time engineering** again.
>
> The direction honestly hasn't changed that much from what I've already spent years doing — **Android, backend systems, operational platforms**, and more recently **AI-related engineering**.
>
> I still **value my previous experience** a lot, especially the **Smart Factory and enterprise messaging work**, because those projects taught me a lot about **reliability, scaling, and long-term system maintenance with real users**.
>
> At this point I'm mainly looking to **settle back into long-term engineering work here in Auckland**.

**临场（念法）**：**「commit properly to the right role and team」** 若嫌 **HR 腔**，**二选一**：保留；**或**改更自然：**I'm ready to settle back into long-term engineering work here in Auckland.**（与 **full-time work rights** 二选一叠一句即可，不必两句都满。）

**Script（极简版 · ~20–30s）**
> I moved from **China to New Zealand for family and long-term lifestyle reasons**, which meant **pausing my previous role and rebuilding my career locally**.
>
> Since then, I completed my **Master's at AUT** focused on **applied AI and practical systems work**, and now I'm looking to move back into **full-time engineering in Auckland** — continuing the same kind of **Android, backend, and operational systems** work I've already spent years building.

**追问**
- **Why this role / why leave last employer?** → 主叙事：**学业阶段结束 + 留纽家庭**；**非** 与老板不和。
- **Any gap on resume?** → **AUT** 全职读书；**ChatClothes** 为成果。
- **Salary / start date?** → **诚实** + **flexible**；工作权利 **PSWV**。

**短答英文**
> **Life direction changed** — moved to NZ for family, **rebuilt locally**, finished **Master's at AUT** (**applied AI / ChatClothes**), now returning to **full-time engineering** in **Auckland** — same direction: **Android, backend, operational systems, AI**.

<a id="q-33"></a>
### 33) Tell me about a time when you had a different opinion than the rest of the team. How did you handle it?
**提示（STAR）**（已对齐你的表述）：**本题**偏 **团队多方意见不一**；**与经理/决策直接分歧** → 以 **[Q5](#q-05)** 为准。**口试策略**：**先给场景与张立**（rollout / 首版范围 / 产线信任），**再** 带方法论 — 避免开头一长段 **management philosophy**（interviewer 还没进故事就听到「人生原则」）。**语言**：少叠 **consultant** 腔（**parallel spikes / technical paths / rails** 连打）；多 **scene feeling**：**factory floor**、**rollout noise**、**support burden**、**unexpected workflow**。**结尾**：不必 **too tidy**（「全员对齐、一切完美」）；可留 **discovery / gradual convergence / 试点后优先级被现实改写**。**金句（可选插一句）**：**trust on the floor beats half-broken scope** — **concrete**，与 **operational realism** 一致。**例证** 与 **Q5** 同源：**Smart Factory**。

**Script（口语）** — **展开版（约 60–75s）** — **推荐**

> I think disagreements are pretty normal on engineering teams. Most of the time it's not about ego — people are optimizing for different risks.
>
> One example was during the Smart Factory project. We had a disagreement around rollout strategy. Some people wanted broader functionality in the first release, while I was pushing for a smaller but very stable initial launch.
>
> My concern wasn't really the engineering difficulty. It was operational trust. These systems were being used directly on factory floors, and once users lose confidence early, it's hard to recover from that.
>
> So instead of debating endlessly, we narrowed the discussion down to a few practical questions — what could realistically be supported, what failure tolerance production teams had, and what we could safely roll out without creating operational noise.
>
> We ended up doing a phased pilot with a smaller scope first. That gave us real usage data instead of assumptions. Some of the feature requests people originally pushed for turned out to matter less than expected, while a few workflow problems we underestimated became much more important once operators started using the system day to day.
>
> After that, the discussion became much easier because we were working from production feedback instead of opinions.

**临场**：若时间紧，**第二段**可压缩为一句张力 + **一句**「**trust on the floor beats half-broken scope**」；**避免** 开场先念 **半分钟原则** 再进 **Smart Factory**。**反模式**：**compressed engineering philosophy**（原则 + tradeoff + methodology 全塞首段）→ 易像 **panel / blog**，不像 **现场工程师**。

**Script（极简 backup · ~28–35s）**

> **Smart Factory** — we disagreed on **first-release scope**: broader features vs my push for a **smaller, stable** launch. My worry was **operational trust** on the **factory floor** — **trust on the floor beats half-broken scope**. We **phased** a **pilot**, got **real usage**, and **priorities shifted**: some **requested** features **mattered less**, a few **workflow** issues **mattered more**. After that we argued from **production feedback**, not **opinions**.

**追问**
- **Were you ever wrong?** → 试点后 **有的功能不如想象中重要**、**现场 workflow 被低估** — **跟反馈改**，不必「我一开始全对」。
- **How handle strong personalities?** → 对事不对人；**书面**对齐目标。
- **What if manager overrides you?** → **执行** + **记录风险**；或转 **Q5** 经理分歧叙事。

**短答英文**
> **Rollout disagreement** on **Smart Factory** — I prioritized **operational trust** on the **floor** over **wide fragile scope**; **phased pilot** and **production feedback** replaced **debate**.

<a id="q-34"></a>
### 34) Tell me about a time when you were faced with a problem that had a number of possible solutions. What was the problem and how did you determine the course of action? What was the outcome of that choice?
**提示（STAR）**（与 `projects/smart-factory/facts.yaml` 对齐）：**核心 tension**：**immediate operational pain vs deep technical cleanup** → **阶段性方案** → **先买时间 + 再做根治** → **explicit trade-off: cost increase**。**情境**：任务表日增约 **十万级**、**半年达百万**，大量 **JOIN 查询** 变慢 → **影响现场生产使用**。**可选路径**：硬停开发做根治（打断交付节奏）；完全不动（用户不满）；阶段性抬容量换时间。**取舍**：**先迁云端托管 MySQL + 读写分流** → **保在研功能上线** → 再做 **慢查询与索引/结构** 根治 → 优化后 **回迁本地降成本**。**Backup**：**产线紧急 vs 里程碑** → **影响×风险** 排序。

**Script（口语）** — **展开版（约 65–80s）**
> In the **Smart Factory** system, we hit a **scaling problem in production**.
>
> One of the **task tables was growing very quickly** — roughly **over a hundred thousand new rows a day** — and a lot of **portal and reporting queries** depended on it. After a few months, some **screens became slow enough** that **operators on the factory floor started noticing it** during daily work.
>
> We had **a few possible directions**.
>
> **One option** was to **stop feature work** and do a **deeper database redesign** immediately. Technically that was probably the **cleanest path**, but it would have **disrupted delivery for quite a while**.
>
> **Another option** was basically to **tolerate the slowdown temporarily**, which I didn't think was realistic once **production users were already feeling the impact**.
>
> So we chose a **staged approach** instead.
>
> First, we **moved the workload onto higher-capacity cloud-hosted MySQL infrastructure** and **separated some of the read traffic** so the operational screens became responsive again. That **increased hosting cost**, but the **trade-off was explicit** — we were **buying stability and time**.
>
> Then, once the **immediate pressure was lower** and the **current feature work shipped**, we **scheduled the slower structural work** properly — **slow-query analysis, indexing cleanup, and some schema adjustments**.
>
> Later, after performance stabilized, we **moved part of the workload back on-prem** to **reduce ongoing cost** again.
>
> The main thing I took from that was that **sometimes the right decision isn't the theoretically best architecture**. It's **sequencing the fixes in a way the business and production environment can actually absorb**.

**Script（极简 backup · ~22s）** — **产线 vs 里程碑**
> **Smart Factory** — **live issues vs feature deadlines**. I ranked by **risk** and **impact** — **fix production** first, then **milestone** work. **Told** people when order **shifted**. **Uptime** held; roadmap **moved**.

**追问**
- **Exact metrics after cloud migration?** → 诚实：**响应/现场感受**改善为先；**根治**在后续慢查询窗口（**勿编**未在 facts 写的百分比）。
- **Who paid for cloud cost?** → **业务/项目**共同决策；**成本上升**是已说清的 **trade**。
- **Alternative you rejected?** → 硬停开发做重写 vs 完全不动 — 说明为何不可行。

**短答英文**
> We **bought time with capacity**, then **scheduled real SQL work** — **cost went up on purpose**, not by surprise.

<a id="q-35"></a>
### 35) What do you do to enhance your technical knowledge apart from your project work?
**提示（STAR）**（已对齐你的说法）：**人设**：**产线向工程师** 用 AI / 工具 — **不是** hype chaser、**不是** tooling influencer。**业余习惯**见 **[Q41](#q-41)**（**实践 AI 工程 + 工作流工具**，正文）；本节：**小项目** + **真实世界里人们在用什么**（release notes、blogs、**GitHub discussions**、必要时 forums）。与 **[Q28](#q-28)** 仍共享 **读 → 小原型 → 短笔记**，**勿**两题整段重念；口试 **Q35 一句带过** + **深挖交给 Q41**。**反模式**：**AI 段信息过密**（agents / Hermes / ecosystem 连打像 Twitter）；**leverage / acceleration / multiplier** 等 **tech-twitter** 词；**每句都总结成 insight**（**compressed insight density**）— 允许 **plain observation**、**无聊但真的运维细节**、**话没说完的松弛感**。

**Script（口语）** — **展开版（约 50–60s）** — **推荐**

> Outside work, I mostly learn by building small things and following what people are actually using in production.
>
> I read release notes, engineering blogs, GitHub discussions, sometimes forums if I'm digging into a specific problem. I don't try to track everything — mostly the areas connected to the kind of systems I already work on.
>
> Recently that's been a lot of **AI-related tooling** — **local models**, **offline inference**, lightweight agents for coding workflows. Partly from my thesis work, but also because I think these tools are starting to become **practical for day-to-day engineering work**.
>
> I still keep up with Android as well because the platform changes constantly, especially around device behavior, permissions, and background restrictions. If you stop paying attention for a while, things drift pretty quickly.
>
> Usually my learning loop is pretty simple. I read something, build a very small prototype around it, and keep short notes if I think it'll be useful later. That's normally enough for me to understand whether something is genuinely practical or just interesting on paper.

**临场**：**Android** 末句若你想保留旧语感，可与 **「I don't want to wake up surprised.」** **二选一**（勿两句叠满）。**AI 段**若仍嫌密，可再删 **一个** 名词堆叠（例如只留 **local models + offline inference**）。

**Script（极简 backup · ~25–32s）**

> **Outside work** — **small builds**, **release notes**, **blogs**, **GitHub threads**; **mostly** what ties to **systems I ship**. **Lately** **AI tooling** — **local models**, **lightweight agents**, **offline inference** — **partly thesis**, **partly** it's **getting practical** for **day-to-day engineering**. **Android** — **permissions**, **background**, **device behavior** **drifts** if you **look away**. **Loop**: **read** → **tiny prototype** → **short notes** → enough to tell **practical vs paper-interesting**.

**追问**
- **Name one repo or paper you read last month.** → 准备 **1 个真名**（某 **local model** 发行版 / **agent** 小工具 / **Android** release note / **GitHub discussion** 皆可）。
- **How do you avoid tutorial hell?** → **小交付** + **记笔记** + 与 **项目**挂钩。
- **Company time vs personal time?** → **边界**：业余自学；**不泄露**上家机密。

**短答英文**
> **Small builds** + **what ships in production** — **release notes**, **blogs**, **GitHub discussions**; **lately practical AI tooling** and **Android platform drift**; **read → tiny prototype → short notes** to filter **real** vs **hype**.

<a id="q-36"></a>
### 36) How do you prioritize your workload? What do you do when your work feels like it's just too much to get done?
**提示（STAR）**（已对齐你的表述）：**内核**不变：**影响**、**依赖链**、**不确定性提前**；**不把风险闷在自己手里**（**早暴露**）；团队内 **临时拉人 / 拆活 / 调顺序**，必要时 **砍范围或改日期**。**多线并行** 仍见 [A ⑥ Case C](#oral-06)；与 **[Q8](#q-08)** 可互指。**口试反模式**：开头不要连打 **工整三元组**（像 **sprint planning 条文**）；**borrow capacity** 易 **PMO 腔** → 口语用 **pull people in / get help from teammates**。**全栈一句** 勿写成 **resume breadth** 广告。**密度**：避免 **每分钟太多 mature insight**（句句像 slogan）；留 **plain sentence**、**未润色措辞**、**边想边说感**。

**Script（口语）** — **展开版（约 55–70s）** — **推荐**

> I usually prioritize based on three things — production impact, dependency risk, and uncertainty.
>
> If something is technically unclear or likely to cause delays later, I try to move it forward early instead of leaving it until the end. I've seen too many projects look "on track" because everyone finished the easy work first while the risky part stayed untouched.
>
> I also pay attention to dependencies. If another engineer, QA, or customer-side team is waiting on something from me, I try to unblock that early so the whole chain keeps moving.
>
> When workload starts becoming unrealistic, I don't hide it and try to hero through it quietly. In smaller engineering teams especially, that's usually how deadlines fail late instead of early.
>
> Normally I raise the risk early, suggest options, and see whether we should redistribute work, reduce scope, or adjust sequencing. In some projects we temporarily shifted people across teams to get critical work through, and I did the same for others when they were overloaded.
>
> I also became comfortable moving across frontend, backend, and integration work when needed. In small teams, sometimes flexibility matters more than strict role boundaries.

**临场**：**「three things」** 若嫌像清单，可改成更松的开场：**I think about impact first, and what blocks other people…** **shifted people across teams** 即 **临时拉人**，避免念 **borrow capacity**。**密度**：中间可插半句 **plain**（**it was messy / we were guessing**）打断「金句链」。

**Script（极简 backup · ~30–38s）**

> I think about **impact**, **dependencies**, and **uncertainty** — **risky unclear work** I try to pull **forward**, not hide behind easy tasks. I **unblock others early**. If the load goes unrealistic, I **don't hero through it quietly** — that's when **deadlines fail late instead of early**. I **raise risk early** with options — **redistribute**, **scope**, **sequencing**; we **sometimes pulled people across teams**. In **small teams** I'm **comfortable across frontend, backend, and integration** when it's needed.

**追问**
- **Example when escalation failed?** → 诚实：**仍有一次延期** → 转 **Q22** 或 **早沟通** 教训；或说最终 **砍范围**。
- **How say no to extra work?** → **用优先级表** + **问替换哪一项**。
- **Remote vs onsite priority?** → **依赖现场证据的优先现场**。

**短答英文**
> **Unclear risky work earlier**; **unblock dependencies**; **no heroing quietly** — **raise early** with **options** (**people / scope / sequencing**); **small-team flexibility** across **layers** when **needed**.

<a id="q-37"></a>
### 37) What's the Number One Accomplishment You're Most Proud Of?
**提示（STAR）**（与 `projects/smart-factory/facts.yaml` 对齐）：**核心记忆点**：**factory floor + operators + years + reliability**。**主叙事**：Smart Factory **周期长**（**2018–2024**）、**10+ 工厂**、**每天被工人使用**、**~30% 产效提升**、**高可用**；**成长**：多栈**边学边交付**、与**客户/一线工人**沟通、在**约 6 人**团队里**推动计划与 sprint**。**备用**（被追问 pure systems 时再讲）：**Enterprise Messaging NDK** — **sub-200ms**、**~5k DAU**、**10+ 年**生产（与 Q17 备用段同源）。

**Script（口语）** — **主：Smart Factory（约 70–85s）**
> The **accomplishment** I'm **most proud** of is the **Smart Factory** program.
>
> Not because it was **flashy**, but because it **lasted for years** and **people genuinely depended on it every day**.
>
> We **deployed it across more than ten manufacturing sites**. The system touched a lot of layers — **backend services**, **Android applications on the factory floor**, **device integration**, **local Windows services**, **RFID and production equipment**. It wasn't the kind of project where you could stay inside **one technical box**.
>
> A lot of the work happened in **real production environments**, not controlled demos. **Operators were using the system every shift**, so **stability and usability mattered immediately**. If something slowed down or behaved badly, **people felt it right away on the line**.
>
> Over time, the program helped **improve operational efficiency by around 30%** based on the metrics the project tracked, and we **kept the system running reliably** across pretty difficult factory conditions.
>
> **Personally**, I **grew a lot** from that project because I had to **keep learning while delivering** — different layers of the stack, customer discussions, production issues, sprint coordination, prioritization. In a **small team** there wasn't much room to say "that's not my area."
>
> What makes me proud is probably the **combination of longevity and real usage**. **A lot of software looks good in a demo. This was software people actually relied on for years.**

**Script（极简 backup · ~35–42s）**
> **Smart Factory** — **years**, **10+ sites**, **real production** with **operators on the factory floor every shift**. **~30% efficiency gain**, **high uptime** in difficult conditions. I **learned across layers** while delivering, and in a **small team** you just **handle what's needed**. That's why it's my number one.

**追问**
- **What was *your* biggest mistake on that program?** → 可接 **分期/估时** 或 **Q34** 数据库权衡；**勿空**。
- **How prove 30%?** → **项目侧指标/客户现场反馈**（与 facts 表述一致，**不夸大**到未写明的审计口径）。
- **Why not pick NDK story as #1?** → **人每天用 + 栈跨度 + 行业现场** 对你更有意义。

**短答英文**
> I **pick Smart Factory first** because **operators depended on it every day** — **metrics and uptime stories match facts I can defend**.

<a id="q-38"></a>
### 38) Tell me about a time when you had an excessive amount of work and you knew you could not meet the deadline. How did you manage then?
**提示（STAR）**（与 `projects/picture-book-locker/facts.yaml` 对齐，已含你的叙事）：**绘本智能柜（Picture Book Locker）** — 同事 **意外离职**；你 **接手大块遗留 + 仍做自己的活** → **遗留、新功能、硬件侧修复、支持** 叠加，**原排期不再符合现实**。**行动**：**不假装一人全能** — **尽早**与 **team lead** 讲清风险并 **再平衡**；**按系统上下文分工**：他人多接 **借还书侧、偏 borrower-facing 的 Android 客户端**；你保留 **柜体侧 Android**（**锁、传感器、硬件控制、现场集成**）— **你最熟、运维风险最高** 的一块，**减少交接摩擦**。**结果**：优先级略调，**交付可预期**、**无人临近发布才吃惊**。**备选**：估错工期类 → **Q4/Q22** 中草药 **pilot**。**口试反模式**：少用 **interview quote**（如 **adult delivery**）、**LinkedIn 式金句**（**projects win when…**）；少用 **Android surface area** 这类 **架构抽象词** → 口语用 **user-facing app / cabinet-side / hardware integration**。**收尾**：不必每故事都 **提炼中心思想**；可平静停在 **「早拆负载，否则发布风险会在后面叠起来」**。

**Script（口语）** — **展开版（约 60–75s）** — **推荐**

> On the Picture Book Locker project, one of the engineers left unexpectedly, and I inherited a large part of their work while still handling my own tasks.
>
> For a while I was trying to keep everything moving — legacy issues, new features, hardware-side fixes, ongoing support — but it became pretty clear the original timeline no longer matched reality.
>
> Instead of pretending I could absorb everything myself, I raised the risk early with the team lead and we rebalanced the work before the milestone got too close.
>
> We split the system by context. Another engineer took over more of the borrower-facing Android client work, while I stayed focused on the cabinet-side Android stack, hardware control, locks, sensors, and on-site integration because I already had the deepest understanding there.
>
> That let us reduce handover overhead and keep the most operationally risky part stable.
>
> We still had to adjust priorities a bit, but the important thing was that the project stayed predictable. Nobody was surprised late, and the workload became manageable again.
>
> In smaller teams I've learned it's usually better to redistribute work early than quietly overload one person and discover the problem near release.

**临场**：若时间紧，**保留** 金句 **「one person couldn't keep all dates green without lying to myself」** 可插在 **第二段末**（与 **timeline no longer matched reality** **二选一** 或 **先后各一句**，勿堆三句总结）。**避免** 在结尾再叠 **team owns the date** 类 slogan。

**Script（极简 backup · ~28–36s）**

> **Picture Book Locker** — **teammate left**, I **inherited a big chunk** **on top of my own work**; **timeline stopped matching reality**. I **raised it early** with the **lead**, we **rebalanced**: **borrower-facing Android** → **another engineer**; I **kept cabinet-side Android**, **locks/sensors/hardware**, **on-site integration** — **less handover**, **riskier part stable**. **Predictable** for the team; **no late surprises**. **Small teams**: **redistribute early** beats **quiet overload near release**.

**Script（口语）** — **备选：中草药标注（与 Q4/Q22 同源 · ~20s）**

> **Herbal** labels — timeline **wasn't real**. I **owned** it, **new** schedule, **pilot** to know **speed** and **error rate**. **Cleaner** data, **better** next estimate.

**追问**
- **Did the handover delay the release?** → **透明排期** + **并行交接**；若 **仍滑点** 转 **Q22** 诚实版。
- **How split work without blame?** → **按模块与上下文** 谁最熟；**对事**。
- **What if colleague also overloaded?** → **升级** 主管、**砍范围** 或 **阶段交付**（与 **Q36** 一致）。

**短答英文**
> **Teammate left** → **unrealistic load**; **raised early** with **lead**, **rebalanced** by **context** — **borrower-facing Android** out, I **kept cabinet / hardware / on-site** to **cut handover** and **stabilize risk**; **predictable delivery**, **no late surprises**.

<a id="q-39"></a>
### 39) What will be your course of action if you are assigned some task which you don’t know at all?
**提示（STAR）**（已对齐你的表述，例证见 `projects/chinese-herbal-recognition/facts.yaml`）：**学习路径** — **官方文档** + **GitHub** 上 **同类开源项目** 对照「别人怎么做」；**边学边做小验证**（**spike / 小实例**），再 **渐进接到真实环境**。**团队习惯**：可有 **技术储备 / 探索任务** — 新技术先做一个 **简单 demo 内部分享**（适用场景、能解决的问题）。**中草药识别平台**：先 **检索 GitHub** 与资料，当时主流多走 **YOLO 系**，用 **YOLOv4 一代** 做 **基线训练与验证** → 再 **抽象成通用流程**：**上传标注数据 → 训练模型 → 批量/在线分类** → 从 **中药** 场景 **扩展到** 动物、其它 **产品视觉类目**，形成 **平台化交付**。**原则**：站在前人可复现路径上 **验证 → 改造 → 分步交付**；全程 **澄清范围**、**小块可交付**、**同步干系人**（忌 silent drift）。

**Script（口语）** — **展开版（约 70–85s）**

> If I'm **assigned** something I **don't** **know**, I **don't** **guess** in **silence**. I **clarify** **success** **criteria** first, then **learn** from **official** **docs** and **real** **GitHub** **projects** that **look** **like** my **problem** — **what** **they** **measured**, **what** **they** **skipped**.
>
> In **our** **team** we also **budget** **small** **exploration** **tasks** — a **tiny** **demo** and a **short** **share** on **where** it **fits** and **what** it **won't** **fix**.
>
> **Concrete** **example** — **Chinese** **herbal** **recognition** **platform**: I **surveyed** **open-source** **work**; **most** **paths** **pointed** to **YOLO-style** **pipelines** **back** **then**, so I **ran** a **YOLOv4-era** **baseline** **experiment** on **herb** **images** **before** **committing** **to** **a** **product** **shape**. **Then** we **turned** it into a **repeatable** **workflow** — **upload** **labeled** **data**, **train**, **publish** **models**, **run** **classification** — and **extended** the **same** **platform** **beyond** **TCM** into **other** **visual** **categories** **like** **animals** and **other** **product** **lines**.
>
> **Pattern**: **borrow** **proven** **ideas**, **verify** **fast**, **adapt**, **ship** in **steps**, **update** **people** **while** I **learn**.

**Script（极简 backup · ~22–28s）**

> **Clarify** scope, **read** **official** **docs** and **good** **GitHub** **examples**, **spike** a **tiny** **proof**, **then** **grow** it into a **shippable** **slice**. **Herbal** **platform** started that way — **YOLOv4-era** **baseline**, **then** a **general** **train-and-classify** **workflow**. **No** **silent** **drift** — I **sync** **early**.

**追问**
- **How long would you need before first commit?** → **小时～数日 spike** + **里程碑对齐**。
- **What if docs are wrong?** → **跑代码验证** + **问内部专家**。
- **Production tech X — you used Y?** → **诚实差距** + **迁移计划**。

**短答英文**
> **Spike** **first**, **sync** **often** — **docs** **lie**, **repos** **don't**.

<a id="q-40"></a>
### 40) Describe a time when you had to work simultaneously on both high-priority urgent projects as well as long-term projects. How did you go about handling both?
**提示（STAR）**（已对齐你的表述，例：**Smart Factory**）：**张力**：**产线问题会打断计划**；但若 **天天只救火**，**路线图停滞**，**同类运维痛会以别的形式反复出现**。**做法**：**产线正在受影响** 的优先（**当班操作员**、**现场系统** — 仍可自然带一句 **real machines / downtime / money** 类 **physical consequence**，**勿**堆成口号）；**同时** **刻意留出** 给 **长线** 的时间，**进度可碎步**。**认知**：性能、集成清理、流程类 **多在系统在线前提下多轮迭代**，**非一次通关**。**可见性**：别让 **紧急活把路线图完全盖住**，也别让 **路线图无视产线现实**。**延展**：[A ⑥](#oral-06) 产线 vs 路线图。**口试反模式**：少念 **工整三桶**（urgent / non-urgent / long-term **像 workshop**）；避免 **protect dates / neither track silently dies**、**ops stays calm, milestones still move** 等 **博客腔总结**；**60 秒内不必强行「完整闭环」** — 可 **半收不收**：**yeah, we were mostly trying not to let the roadmap completely die while production was noisy.**

**Script（口语）** — **展开版（约 60–75s）** — **推荐**

> Smart Factory was probably the clearest example of this.
>
> We always had two kinds of work happening at the same time — immediate production issues and longer-term roadmap work.
>
> If something was actively affecting factory operations, that came first. Real operators were depending on the system during live shifts, so production issues couldn't sit around waiting for the next sprint.
>
> But at the same time, if you only firefight every day, eventually the roadmap stalls and the same operational problems keep coming back in different forms.
>
> So I tried to separate the work intentionally. Urgent issues were handled first and usually in smaller focused blocks, then I protected some remaining time for longer-term tasks even if progress was incremental.
>
> A lot of the long-term work wasn't something you solved in one pass anyway. Performance issues, integration cleanup, workflow redesign — those usually improved over multiple iterations while the system stayed live.
>
> The important thing for me was visibility. I didn't want urgent work to completely hide the roadmap, and I also didn't want roadmap work to ignore production reality. Both tracks needed to keep moving, even if not at the same speed every day.

**临场**：若嫌 **「two kinds of work」** 仍略像框架，中间可插半句 **plain**：**it was messy / we were guessing priorities some weeks**。**「real machines, real downtime, real money」** 可 **一句** 接在 **factory operations** 后作 **口语锚点**，**勿**与 **visibility** 段各写一遍总结。

**Script（极简 backup · ~28–36s）**

> **Smart Factory** — **production issues** and **roadmap work** at the same time. **Floor first** when **operators** were actively blocked — you **can't** queue that for the **next sprint**. **Only firefighting** and the **roadmap stalls**, same pain **comes back** in new forms. So I **split intentionally**: **small urgent blocks**, then **some leftover time** for **long-term**, even **incremental**. **Bigger fixes** **iterate while the system stays live**. **Visibility** — **both tracks kept moving**, just **not at the same speed every day**.

**追问**
- **What if PM always marks everything P0?** → **一起排序** + **书面**只保 Top-N；见 **Q8/Q36**。
- **How protect deep work for long-term?** → **日历块** + **早关断** 即时消息；或 **协定** 某时段不排会。
- **Give another project besides Smart Factory.** → **enterprise IM** 产线 vs 路线图一句。

**短答英文**
> **Smart Factory**: **production-first** when **operators** are **hit**, but **roadmap** **can't** **starve** — **intentional split**, **incremental long-term**, **iterate while live**; **visibility** so **both** **tracks** **move** at **different speeds**.

<a id="q-41"></a>
### 41) What is something new that you’ve learned recently?
**提示（STAR）**（与 `kb/profile.yaml` **AUT MCIS** 时间线一致，并含你的表述）：**主线**：**实践 AI 工程** — **本地模型**、**部署约束**、**非理想环境下的系统行为**（**AUT**、**ChatClothes**）。**最强证据句**：**全链路 profiling 后瓶颈往往不在最初假设处** — **推理** 有时 **不是主问题**；**延迟、编排、工作流开销** 更关键 — **empirical / systems / anti-hype**。**并行**：**个人开发流里** 用 **LLM 工具**（**编码辅助、脚本自动化、小工具、快速原型**）— **务实**，**少** 堆 **Hermes / ecosystem / agent patterns** 等 **AI Twitter 腔**。**行业观感**：只限 **「我接触过的项目/环境」** — **工程工作流里** AI **已很实用**；**许多运营/客户侧系统** 仍难在 **可靠、集成、长期可用** 上稳定落地 — **勿** 写成 **全行业唱衰** 或 **宏观趋势评论员**（**industry commentator mode**）。**结尾**：用 **部署后整个系统是否仍有用** 收束，**勿** 再叠 **measurable outcomes not demos** 类与其它题重复的 **mission statement**。

**Script（口语）** — **展开版（约 60–75s）** — **推荐**

> Probably the biggest thing I've been learning recently is practical AI engineering — especially around local models, deployment constraints, and how these systems behave outside ideal environments.
>
> During my Master's at AUT and the ChatClothes project, I spent a lot of time profiling end-to-end workflows on smaller hardware and offline setups. One thing that surprised me was that the real bottlenecks often weren't where I first expected them to be. Sometimes model inference wasn't the main problem at all — latency, orchestration, or workflow overhead mattered more.
>
> At the same time, I've been using LLM tooling heavily in my own development workflow — coding assistance, automation scripts, small internal tools, rapid prototyping. The practical impact there already feels very real to me because the cost of trying ideas has dropped a lot compared to a few years ago.
>
> I still think there's a difference between demos and production though. In software engineering workflows, AI is already genuinely useful day to day. In a lot of operational environments or customer-facing systems, I think the harder part is still reliability, integration, and long-term usability.
>
> That's probably the part I'm most interested in going forward — not just whether a model works once, but whether the whole system remains useful after deployment.

**临场**：**AI 类题**优先 **一条具体工程观察**（**意外瓶颈**）+ **一条工作流改变**（**试想法成本下降**）+ **一条部署现实**；**少做** 行业级判断与 **hype 评论**。**工具名** 若被追问再 **举 1 个真名**，勿在首段 **名词串**。

**Script（极简 backup · ~28–36s）**

> **Practical AI engineering** through **AUT / ChatClothes** — I **profiled end-to-end** on **small offline hardware**; **bottlenecks** often **weren't where I expected** — sometimes **not inference** but **latency, orchestration, workflow overhead**. **LLM tooling** in my **daily dev** — **much cheaper to try ideas**. **Demos vs production**: **engineering workflows** already **useful day to day**; **ops / customer-facing** still **harder** on **reliability and integration**. I care whether the **whole system stays useful after deployment**.

**追问**
- **Concrete ChatClothes bottleneck?** → **Cloud LLM** **round-trips** → **local** **Ollama**；**vision** **YOLO12n-LC**（与 **[Q31](#q-31)** 一致）。
- **Name one automation you shipped for yourself.** → 准备 **1 个** 可公开描述的例子（脚本/小工具/工作流），**勿编**商业客户名。
- **Aren't you dismissing AI adoption?** → **限定个人观察** + **我接触过的交付环境**；收束到 **部署后可用性 / 集成 / 可靠**，**非** 全行业结论。

**短答英文**
> **Practical AI engineering** from **AUT/ChatClothes** — **profiling showed bottlenecks** often **not** at **inference**; **LLM tools** **changed** my **daily** **dev** **workflow**; **most** **interested** in **systems** that **stay** **useful** **after** **deployment**, **not** **one-off** **demos**.

<a id="q-42"></a>
### 42) Tell me about a time when you had a hard time working with someone in your team. How did you handle it?
**提示（STAR）**：**二选一**。**Option A**（同 **Q6/Q24**）：**Enterprise Messaging** — 同事在 **review** 上退缩、参与度低 → **1:1** + **私下具体反馈** + **短结对**。**Option B**（**口述经历**，尚未写入 `projects/*/facts.yaml`；口试 **勿编造** 客户/项目正式名称，可统称 **入口称重/地磅联动** 类交付）：团队里 **资深同事** 习惯用 **Delphi** 做**新项目**（车辆 **上秤称重 → 超重预警 → 联动抬杆/报警** 等现场逻辑）；你当时 **~5–6 年**经验，对方 **行业经验更长**但 **工具链偏旧**、更倾向 **老栈**；你认为 **.NET 等团队已在用的栈** 更利于 **封装复用、协作与工期压缩时他人能接手**。**分歧处理**：先 **1:1** 表达对其 **现场经验** 的尊重，再把讨论落到 **可维护性 / 知识传承 / 工期与接手面** 等**可验证风险**；**同时**承认 **新技术需要学习窗口**。**结果**：**工程/甲方侧决策**采纳 **Delphi 路线** — 你 **书面保留技术顾虑** 后仍 **专业配合交付**，并尽量补 **文档/边界说明** 降低后续维护成本。**Reflection**：**尊重人 ≠ 回避栈决策**；**负责人拍板**后 **执行到位**；长期仍应推动 **团队默认技术栈** 与 **学习节奏** 对齐。

**Script（口语）** — **Option A（约 25–35s）**

> **Enterprise Messaging** — someone **froze** on **review**. **Private** talk, **gentle** **specific** notes, **pair** a bit. **Quality** and **mood** improved; **same playbook** as conflict question.

**Script（口语）** — **Option B（约 65–80s）**

> I once had a **difficult disagreement** with a very **experienced teammate** on a **roadside weighing system** project.

> The system handled things like **vehicle weighing, overload alerts, and barrier control** at the site level. The teammate had **much deeper industry experience** than I did, especially around the operational side of those environments.

> The disagreement was mainly about **technology choice**. They strongly preferred **Delphi** because that was the stack they were most comfortable and productive with. I was more concerned about **long-term maintainability and team support** because most of the rest of the engineering team was already working in **.NET and related tooling**.

> My concern wasn't really **"old versus new."** It was more practical than that — if **deadlines got tight or ownership changed later**, there were **very few people** who could comfortably step into the **Delphi side of the system**.

> I didn't try to **turn it into a public argument**. We discussed it **directly one-on-one** first, and I tried to keep the discussion around **delivery risk, maintainability, onboarding, and support coverage** rather than personal preference.

> In the end, **leadership and the customer decided to continue with Delphi**. Once that decision was made, I **supported it professionally**. I **documented interfaces carefully**, clarified integration boundaries, and tried to **reduce future maintenance risk** as much as possible instead of holding onto the disagreement emotionally.

> That experience taught me that **respecting someone's experience and disagreeing with their technical direction are not mutually exclusive**. Sometimes your role is to **make the trade-offs visible clearly**, even if the final decision goes another way.

**追问**
- **Option A**：**What if they still resist?** → **升级** TL/经理；**记录**风险；**换结对**节奏。 / **Cultural barrier?** → **验收标准写清** + **图示**。 / **Your part?** → 早期语气 → **改**私下+具体（**Q21**）。
- **Option B**：**Aren't you dismissing older engineers?** → **强调尊重现场经验**；争议在 **可维护性/接手面**。**What did you do after Delphi was chosen?** → **文档、接口、风险清单**、正常协作。**Would you fight again?** → **用数据+默认栈规范** 走 **RFC/评审**，仍由 **负责人拍板**。

**短答英文**
> **Private 1:1**, **respect first**, then **name maintainability and team support risks** — if the org picks Delphi, I **still ship cleanly** and **document what the next person needs**.

<a id="q-43"></a>
### 43) How do you assure code quality in your team?
**提示（STAR）**（facts 仍可从 **`smart-factory`** / **`enterprise-messaging`** 深挖，**主答勿一次背全书**）：核心不是「多写单测」口号，而是 **上线前减少可避免的不稳定** — **技术流程**（review、CI、发版校验、环境隔离）与 **长期纪律** 叠加。**Smart Factory**：多栈 **Android / 后端 / 设备 / IoT** 同演进，**单靠隔离测试不够** → **定期真机、接近产线的集成 demo**；很多问题 **系统真正联动后才出现**。**enterprise-messaging**：曾 **误将测试环境配置打进生产包** → 之后 **环境硬拆分、发布前多轮校验、部署逐步自动化**，减少 **纯靠记忆的步骤**。**立场**：**工具不单独保证质量** — 人仍要对 **边界条件、运维行为、可维护性** 负责。**口试克制（restraint）**：behavioral **默认** **一件真事 + 一项改进 + 一条运维洞见**；其余（静态扫描、MR 互审、Junior checklist、监控回滚等）**等追问再补**，勿开场叠成 **engineering handbook**。**反模式**：勿口头 **挂「防 / 抓 / 救」三字框架**（像培训课件）；**少叠 quotable clever phrase**；**《阿里巴巴 Java 开发手册》** 等 **仅追问「团队 Java 规范」时一句带过**「公开 industry style guide + 团队约定」— **非中国面试官** 可能无感。**节奏/工具链细节** → **[Q44](#q-44)**、**[A ⑦](#oral-07)**；IM 平台化 → **facts**、**[oral-09 Case B](#oral-09)**。

**Script（口语）** — **推荐版（融合 A+B · 约 55–70s）**

> For me, code quality is mostly about reducing avoidable instability before software reaches production.
>
> Part of that is technical process — code reviews, CI checks, release validation, environment separation, things like that — but a lot of it is really about engineering discipline over time.
>
> On the Smart Factory projects, we had Android apps, backend services, device integrations, and IoT components all moving together, so isolated testing wasn't enough. We did regular integrated demos with real devices and realistic workflows because many issues only appeared once systems interacted in production-like conditions.
>
> We also used merge reviews and CI pipelines to catch lower-level problems early, especially on higher-risk changes. But I don't think tooling alone guarantees quality. Tools help reduce repetitive mistakes; humans still need to think about edge cases, operational behavior, and maintainability.
>
> One lesson that stayed with me came from the enterprise messaging system. We once accidentally shipped a production build with incorrect environment configuration. After that, we tightened environment separation, added stronger release checks, and gradually automated more of the deployment process so fewer steps depended purely on memory.
>
> I think long-term quality comes from layers working together — architecture choices, reviews, release discipline, monitoring, and teams being honest about operational risk instead of assuming testing alone will save everything.

**临场**：主答 **已含两线精华**；若仍嫌长，可删 **第二段** 中 **半句**（保留 **集成 demo** 或 **CI** 其一）。**勿** 在主答里再念 **Alibaba / prevent-catch-recover / config dialects**。

**Script（极简 backup · ~25–32s）**

> **Quality** = **fewer avoidable surprises** in prod — **reviews**, **CI**, **release checks**, **env separation**, plus **discipline over time**. **Smart Factory**: **integrated demos** on **real devices** — lots of bugs only when **layers interact**. **Enterprise IM**: **wrong config shipped once** → **tighter env split**, **stronger checks**, **more automation**. **Tools** reduce **dumb mistakes**; **people** still own **edge cases** and **ops risk**.

**面试官追问时再展开（勿主答堆砌）**
- **工厂线工具链**：**GitLab + Jenkins**、周 **集成 demo**、接口契约 → **[Q44](#q-44)** / **[A ⑦](#oral-07)**。
- **IM 缺陷面**：自建 **C++** 路径噪音 → **核心管道迁 Easemob SDK**、自研聚焦业务层 — **定性**、**勿编** facts 未写百分比。
- **可叠加习惯**：CI **静态扫描分级**（阻断 vs 警告 backlog）；**MR 交叉 review**；大版本 **spot-check**；新人 **checklist + 前几个 PR 高密度 review**（与 **Q45** 一致）。
- **共用**：**速度 vs 覆盖** → **风险分级**（**Q34**）；**周五 hotfix** → **Q18**。

**追问**
- **Option A 深挖**：**Who owns QA?** → **开发者自测矩阵** + **清单** + **灰度**；**Q4 Option B**。**Metrics?** → **缺陷趋势**、**回滚**、**demo 可集成度**（与 smart-factory 叙事一致处再说）。
- **Option B 深挖**：**外包 IM 风险?** → **对价是自建 C++ 长期缺陷与运维**。**Mobile 矩阵?** → **OEM 长尾**、实验室下限、**真机反馈**（与 facts `Managed Android device long-tail` 一致）。
- **Static analysis 太吵?** → **分级**：阻断 vs 警告进 backlog。**Tooling vs culture?** → **CI + MR + 文档约定** 三件套，工具 **不替代** 判断。

**短答英文**
> **Fewer avoidable prod surprises**: **reviews + CI + release discipline**; **Smart Factory** used **integrated demos on real stacks**; **enterprise IM** taught me **hard lessons from a bad config release** — **tools help**, **humans still own risk**.

<a id="q-44"></a>
### 44) Describe the project workflow in your previous team.
**提示（STAR）**：**二选一**。**Option A** **`smart-factory`**（与 `projects/smart-factory/facts.yaml`、[A ⑦](#oral-07) 一致）：**~六年** **双周 Sprint** — plan、standup、review、retro；每 Sprint **可运行 demo**（**mobile / backend / IoT** 对齐）；**接口契约** 先于破坏性改动；发布从**手动复制**演进到 **Jenkins + GitLab CI/CD**，**工厂项目先试点**再**各交付线统一迁移**，辅以清单与短文档；**团队侧**可安排 **定期技术分享**（新工具/适用问题/优劣与边界），与 Sprint 节奏并行、不必等「项目结束才补课」。**Option B** **`enterprise-messaging`**（与 `projects/enterprise-messaging/facts.yaml`、[A ⑨ Case B](#oral-09) 一致）：产品从**独立 IM** 渐进 **平台化**（用户中心、文件中心、子系统接入）；工程上 **Spring Cloud 微服务 + Node** 多子系统并行；团队扩大与**多项目穿插**后，协作流引入 **飞书（Lark）**、**协作文档**（如用过的 **石墨**）、**PM / 预算 / 审批** 纪律，并 **渐进自动化** 减轻行政摩擦；**极早期**你是 **唯一 Android**，**数周级**原型窗口上线后靠 **每日缺陷清单 + 尽量每日发版** 与 **产品/设计对用户解释预期** 收敛 — 与 **[Q43](#q-43)** 的「**质量 / 发版纪律 / 配置教训**」叙事可同场串讲，勿重复堆砌细节。

**Script（口语）** — **Option A（约 40–50s）**
> On the **Smart Factory** program, the workflow was fairly **iterative** but also very **operationally focused** because the software was tied closely to live factory environments.
>
> We worked in roughly **two-week sprint cycles** with planning, standups, reviews, and retrospectives, but the most important part for us was the **integrated demo at the end of each sprint**.
>
> We had **Android applications, backend services, IoT devices, and hardware integrations** all evolving together, so a feature **wasn't considered "done" just because one team finished their own piece**. We tried to show **running workflows with real devices and realistic data** as early as possible.
>
> Another thing we learned over time was to **align API contracts and integration boundaries early** before large changes. Otherwise teams would individually move fast but **collide later during integration**.
>
> Deployment also evolved gradually. Early on, a lot of releases were still fairly **manual**. As the projects and factory sites grew, we introduced **Jenkins and GitLab-based CI/CD pipelines** to make builds and deployments more **repeatable and less dependent on tribal knowledge**.
>
> We didn't force every change across all projects immediately though. Usually we'd **pilot workflow improvements on one production line first**, **stabilize** them, then **roll them out more broadly** once the process was proven workable in practice.

**Script（口语）** — **Option B（约 50–60s）**

> On **`enterprise-messaging`**, the workflow didn't feel like **one** neat **Scrum** template for the whole decade — it **changed** as the **product** grew into a **platform**.
>
> Early on I was often the **only Android** engineer in a **tight** window: **ship a prototype**, **launch**, then **stabilize** with **daily** prioritized bug lists and **frequent** builds — **product** and **design** helped keep **user** **expectations** **honest** when we were on fire.
>
> Later, with **more people** and **parallel** projects, the **process** layer mattered: **Feishu** (**Lark**), **collaborative docs**, **PM / budget / approvals** so engineering didn't drown in admin — plus **progressive automation** where it actually saved time.
>
> Engineering-wise it was **many subsystems** — **Spring Cloud** microservices, **Node** services for messaging/workflow/audit — integrating **identity**, **files**, **permissions** as **shared** **primitives** while IM transport moved to **managed** **SDK** paths. **Same story** as **[oral-09](#oral-09)** — **platform** rhythm, not only tickets.

**追问**
- **Option A**：**Biggest friction?** → **流水线首期 wiring 成本** → **试点**再推广。**Hotfix outside sprint?** → **分支** + **回滚** + **补复盘**。**Docs vs code?** → **契约 + demo** 为对齐面。
- **Option B**：**Was it still "Agile"?** → 诚实：**节奏随团队规模与产品线形态演变**；核心是 **可见进度 + 跨职能对齐**，不必硬套名词。**How prioritize platform vs fires?** → **线上/支付类风险** 与 **共享基础能力** 分层；与 **Q8/Q40** 一致口径。**Feishu = silver bullet?** → **工具承载流程**；关键仍是 **决策人与完成定义**（可点 **oral-08 Case B**）。
- **共用**：与 **[Q43](#q-43)** 的 **CI/MR** 习惯如何接？→ **同一套 Git 流** 上挂 **门禁与发布**；工厂线 **Jenkins/GitLab** 为主，IM 线侧重 **发版纪律 + 缺陷节奏**（勿编两条线未写的统一工具名）。

**短答英文**
> **Sprints** **plus** **contracts** **plus** **weekly** **integrated** **demos** on **one** **program** — **and** **on** **another**, **workflow** **grew** **with** **the** **platform**: **docs**, **approvals**, **automation**, **honest** **release** **cadence**.

<a id="q-45"></a>
### 45) How do you support and track a junior developer's progress?
**提示（STAR）**（与 `projects/smart-factory/facts.yaml` **Led and mentored a 6-person…** 及 **Q12/Q20** 一致）：把辅导定位成 **delivery enablement**（帮人 **在交付里变有效**），**不是** HR 式「领导力表演」或 **完整 operating model 演讲**。**主答克制**：**一条习惯行为**（如 **不急着抢键盘**）往往比 **cadence+board+ADR+demo+tech talk 全清单** 更 **好记**；其余 **站会/看板/30·60·90/契约与 24h review** → **追问再展开**（见 **[Q12](#q-12)**、**[Q44](#q-44)**）。**Review 口语升级**：除「review is coaching」外，可具体为 **reviews explain future maintenance cost**（**维护成本、边界、集成风险、命名** — **beyond making the compiler happy**）。**文档/ADR/onboarding** 与 **难反馈** 叙事 → **[Q21](#q-21)**、**[Q13](#q-13)**（本题 **不重复念长段**）。**反模式**：**board for truth** 等 **slogan**；**mentoring the system** 等 **过度抽象**。**与 Q43**：新人 **checklist + 前几个 PR 高密度 review** 一致处 **一句带过即可**。

**Script（口语）** — **推荐版（融合 · 约 55–70s）**

> On the Smart Factory projects, I helped mentor junior engineers inside a relatively small cross-functional team. I usually think of that more as helping people become productive in delivery rather than formal management.
>
> One thing I tried to do was make progress visible and predictable. We worked in small vertical slices, used regular demos, and reviewed integration early so juniors weren't coding for two weeks in isolation and only discovering problems at the end.
>
> Day to day, I checked in pretty simply: what they're working on, what they've already tried, and where the uncertainty is. I try not to immediately take over the keyboard. Usually I explain how I would reason through the problem, then let them implement the solution themselves.
>
> Code review was also a big part of mentoring. Not just saying "change this line," but explaining maintainability, edge cases, naming, integration risk — why the change matters beyond making the compiler happy.
>
> We also did lightweight internal sharing sessions when someone tried a new tool or approach. The useful part wasn't the technology itself; it was understanding where it actually helped and where it created extra complexity.
>
> Over time I found juniors improve faster when expectations are clear, feedback is continuous, and progress is connected to running software instead of only ticket counts.

**临场**：若时间紧，**删**「**lightweight sharing**」整段或缩成 **一句**。**review** 若嫌套路，用 **「explain maintenance cost for the next reader」** 替换半句。**具体行为锚**：**I try not to take over the keyboard too quickly** — 可单独 **强调一遍**。

**Script（极简 backup · ~22–28s）**

> **Smart Factory** — **small team**, I helped juniors **ship in delivery**, not **HR management**. **Small slices**, **early integration**, **demos** so they **don't** code **alone for weeks**. **Simple check-ins** — **what they tried**, **where stuck** — **I don't grab the keyboard**; I **talk reasoning**, they **implement**. **Reviews**: **maintainability**, **edges**, **integration risk**, **not** just **compiler green**. **Light sharing** for **real trade-offs**. **Running software** **>** **ticket counts**.

**面试官追问时再展开（勿主答堆砌）**
- **站会 / 晚间扫板 / 阻塞文化**、**30/60/90 定性里程碑**、**接口契约 + 24h review** → 对齐 **Q12**、**Q44**；**勿** 开场背成全套 handbook。
- **文档薄 / ADR / onboarding** → 转 **Q21**、**Q13** 主叙事。

**追问**
- **Micromanagement?** → **切片小 + 目标清**；加密只在 **集成/生产配置风险**；日常 **放手 + review 守门**。**How delegate under deadline?** → **并行可拆子任务**；Junior **边界清晰**，你握 **契约/集成**。
- **Tech talks 水?** → **绑定真实试点结论**；**短** + **Q&A**；**不讲未落地 PPT 选型**。
- **Junior underperforming — escalate?** → **结对 + 书面期望**；**连续两轮 review 无改善**再与经理对齐。**Remote onboarding?** → **录屏** + **重叠窗** + **异步文档**（与 **Q43** checklist **一句**）。

**短答英文**
> **Delivery mentoring** on **Smart Factory**: **small slices**, **early integration**, **demos** — **no two-week isolation surprises**; **check-ins on what they tried**; **I don't take the keyboard first**; **reviews spell maintenance + integration cost**, **not** just **style nits**; **progress tied to running software**.

---

<a id="section-toolbox"></a>
## Part 4 — Quick Review Sheet

Use this section in the last few minutes before an interview. It is a memory trigger, not another long script.

### 3-minute warm-up

| 面试官想听 | 你先想 | 可用故事 |
|---|---|---|
| Who are you? | **13y production + AUT AI + Auckland full-time** | [① Tell me about yourself](#oral-01) |
| Hard technical problem | **Android reliability is layered** | [② Enterprise IM](#oral-02) / [Q31](#q-31) |
| Pressure / workload | **triage, communicate, shrink risk** | [⑤ Under pressure](#oral-05) / [Q38](#q-38) |
| Conflict / disagreement | **respect people, argue trade-offs** | [③ Conflict](#oral-03) / [Q42](#q-42) |
| Failure | **own it, fix it, change process** | [④ Failure](#oral-04) / [Q4](#q-04) |
| Leadership / junior | **small slices, early integration, coaching reviews** | [Q45](#q-45) |
| Why company / why move | **family move + stable NZ engineering role** | [Q29](#q-29) / [Q32](#q-32) |

### Oral guardrails

- **Start short**: answer in **60–90s**, then invite depth: *"I can go deeper into the Android side if useful."*
- **Use plain words**: messy system, real users, trade-off, release risk, fast recovery.
- **Do not overclaim**: when a number is not in YAML, say the effect qualitatively or mark `MISSING_INFO`.
- **One story, one lesson**: do not stack three projects unless the question asks for breadth.
- **End with behavior**: what you now do differently, not only what happened.

### Reusable closing lines

- *What I learned is that reliability usually comes from layers, not one trick.*
- *I try to make risk visible early, before it becomes a deadline surprise.*
- *I don't see disagreement as a problem by itself; I try to move it toward evidence and constraints.*
- *For production work, speed matters, but repeatable release habits matter just as much.*
- *I enjoy turning unclear, messy problems into something users can actually rely on.*

<a id="section-appendix"></a>
<a id="section-personal-drafts"></a>
## Appendix · Personal Drafts

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
- 【2026-05-09 新增】`MISSING_INFO(project_id)` / **入口地磅称重联动**（车辆上秤 → 超重预警 → 抬杆/报警）— **Delphi vs 团队主流栈（如 .NET）**（可用于：**[Q42](#q-42) Option B**、Conflict、技术选型、难合作）
  - Situation: 新项目现场逻辑复杂；团队里资深同事习惯用 **Delphi** 全栈交付；你更倾向团队已在用的栈（封装、协作面、工期紧时他人能接手）。工程/甲方侧最终采纳 Delphi。
  - Task: 不伤协作的前提下把分歧从「偏好」落到可讨论条款（可维护性、接手面、工期、学习窗口）。
  - Action: 1:1 先尊重对方现场经验；书面或评审中列风险与选项；决策后仍配合交付并补文档/接口说明。
  - Result: 按组织决策用 Delphi 交付（具体客户、年份、量化待补：`MISSING_INFO`）。
  - Reflection: 软件栈会迭代，团队需要默认技术车道与学习节奏；个人不认同决策时仍可专业执行并把维护成本显性化。
  - 合并状态：□ 已建 `projects/<id>/facts.yaml` 并 `validate.py` □ 已同步 Q42 英文稿细节
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
- 【2026-05-10 新增】`banknote-paper-mill` / 造币印纸厂断网现场与联调压力（可用于：Under pressure / Ambiguity / Stakeholder / 交付节奏）
  - Situation: 客户为造币印纸厂类高保密场景，现场不允许联网；仅能以断网笔记本进入，分析、导出数据格式并在内网环境测试；在外部常网环境开发后，需再次进入客户内网验证。**每次进场与出场均需申请审批；通常单次进场需提前约一周办理**，现场可用调试时间稀缺。**断网环境下部署/升级同样麻烦**：无法依赖外网即时拉包与热修，需离线打包、受控介质传递与更重的安装校验与回滚准备。流程环节多、开发周期紧；易出现整日工作但无「可展示」进展，客户与开发团队均高度焦虑。
  - Task: 在强约束下仍推进集成与验证，并管理各方对进度与「无进展日」的预期；在极短的现场窗口内完成有效验证。
  - Action: 将每次进场目标拆为可验证的最小检查点；**场外完成充分准备**（复现步骤、**离线安装/升级包**、样例数据、回滚与备选路径、校验说明），避免把「到现场再排查」或「到现场再下依赖」当作默认；完整记录可带出的样本与格式说明；与 PM/客户提前对齐断网联调的真实节拍，排期按「**审批提前量** + **离线发布准备** + 进场—外发—再进场」循环而非纯办公室迭代；空转日主动说明阻塞原因（权限、环境、路径试错）避免被误解为拖延。
  - Result: 在约束下逐步完成格式对齐与内网验证（具体客户名、进场次数、周期量化待补：`MISSING_INFO`）。
  - Reflection: 物理隔离与保密流程本身就是风险与工期来源；**审批周期**、**单次进场成本**与**断网发布/部署摩擦**必须写进计划。压力管理的核心是预期对齐、检查点粒度、离线制品与场外准备，而非单纯加班。事实条目见 `projects/banknote-paper-mill/facts.yaml`（`timeline` 若与履历需精确对齐可再改）。
  - Suggested line (EN): "One plant visit cost a week of paperwork — and you couldn’t patch like the cloud: offline bundles, controlled transfer, and rollback had to be designed in, not improvised after a failed push."
- 【2026-05-12 新增】`cross-project` / 多项目并行：外部交付 vs 自营产品线（可用于：Prioritization / Time management / Stakeholder / 资源协调）
  - Situation: 同一时期并行的项目多；既有外部客户交付（如工厂类 `smart-factory`、企业即时通讯 `enterprise-messaging`），也有公司自营产品线（如图书馆智能借阅柜 `picture-book-locker`、互联网相关自营项目等）；个人需同时跟进多条线的开发与问题处理。
  - Task: 在有限时间内为各项目推进度、满足临近节点，并对未攻克难点分配深度工作时间；避免「全是 P0」导致全线失控。
  - Action: 以日/周为单位列出各项目：临近交付项、当前阻塞与难点、可延后但不伤信任项；按影响、承诺日期与风险排序；进度与排序对 PM/相关方保持透明；在自身无法单独解阻塞时尽早申请其他组人力支援（短时结对、并行分担或明确责任边界）。
  - Result: 多线并行下仍维持可预期交付与问题收敛（具体并行项目数、周期量化待补：`MISSING_INFO`）。
  - Reflection: 组合工作的瓶颈常是「可见的优先级 + 及时的资源升级」，而非单纯延长单人工时。口稿与锚点见 [A ⑥ Case C](#oral-06)、**Q8**、**Q36**、**B2-06**。
  - Suggested line (EN): "External factory deadlines and internal product lines don’t share one inbox — I pick today’s fire from who’s waiting and what’s still a real unknown, and I borrow hands early when parallel streams need more than one brain."
- 【2026-05-13 新增】`enterprise-messaging` / Android 厂商 ROM 与版本碎片化、复现与测试策略（可用于：Complex technical / Trade-off / Quality / 客户问题）
  - Situation: 企业即时通讯 Android 客户端在用户侧呈现类 C 端的设备与系统长尾；国内 **小米、华为、OPPO** 等对系统有深度定制，同一应用在不同真机上表现可能不一致。**不少缺陷只在用户真实使用环境中才暴露**，实验室与常规用例难以在发版前穷尽所有「小问题」。实验室以主流机型与版本为主（常规测试下限约 **Android 7/8**，更老机型一般不入常规矩阵；很新的系统也可能暂缺测试机）。用户反馈的问题有时在相同 API 级别的模拟器上仍无法稳定复现。
  - Task: 在有限开发周期与测试预算下保持可发布质量，并对线上疑难问题形成可验证的复现与修复闭环；在 **发布时间**、**测试成本（人力/时长）**、**测试机型与设备投入** 之间做出可沟通、可执行的权衡。
  - Action: 发版前以主流覆盖 + 核心路径守门，控制测试范围与周期；对无法复现或影响面大的工单，以反馈驱动在目标真机上验证，必要时采购对应机型，或通过远程/现场方式贴近用户真实设置与环境后再定位；与产品/发布节奏对齐「已知风险窗」与后续补丁策略（定性表述，非编造 SLA）。
  - Result: 在「理想全矩阵」与「可承受成本/节奏」之间取得可操作平衡；疑难问题多通过真机路径收敛（具体机型库规模、成本与工单比例待补：`MISSING_INFO`）。
  - Reflection: 移动交付需显式接受「实验室覆盖 ⊂ 全国 ROM × 用户设置」；策略是 **主流守门 + 成本可控的测试深度 + 强信号下的真机补洞**，而不是假装测试能消灭长尾上所有细问题。口稿见 [A ② 延展](#oral-02)、**B2-02**、**Q31 Option B**。
  - Suggested line (EN): "Users outnumbered our test rack — we balanced ship date, test hours, and how many phones we could own; mainstream gates first, then we paid for the exact device path when the bug report was serious enough."
- 【2026-05-15 新增】`enterprise-messaging` / 自建文件平台：FastDFS、容量与私密性、多子系统文档（可用于：Complex technical / Architecture / Trade-off / Security 与运维交叉）
  - Situation: 早期文档集中在一台服务器；用户上传、即时通讯**聊天附件**、**合同管理**、**设计图管理**等模块带来持续增长的文件量，单机存储难以承载。
  - Task: 提供可扩展、可运维的文件能力，供多个子系统复用；在**数据私密性/可控性**约束下，不默认采用**公有云文件服务**。
  - Action: 基于**开源 FastDFS**构建自建分布式文件存储；与 **User、Message、Workflow** 等子系统对接统一文档访问；工程上处理**存储分片、冗余、备份与恢复**，并与**权限/访问控制**策略对齐。
  - Result: 文件基础设施从单机演进为可横向扩展的自建方案，支撑高附件量与多业务文档场景（具体节点数、容量、RPO/RTO 等待补：`MISSING_INFO`）。
  - Reflection: 自建分布式文件要同时付「容量、可靠性、安全、备份」账，不是装完即忘；与**头像路径安全事件后迁移云端对象存储**可分**分层存储/分阶段**叙述，避免口试时听起来自相矛盾。口稿见 [oral-enterprise-files](#oral-enterprise-files)、**B2-02**、**B1-05**、**Q31 Option C**；事实见 `projects/enterprise-messaging/facts.yaml`。
  - Suggested line (EN): "Attachments and contract PDFs don’t belong on one disk forever — we scaled with self-hosted FastDFS, and we still had to own redundancy, backups, and who can read what."
- 【2026-05-16 新增】`enterprise-messaging` / 约束与时代驱动：存储与消息架构、组织流程、职责演进（可用于：**Adapted to change** / 架构演进 / Leadership & scaling / Q23 Option B）
  - Situation: 十年周期内业务体量、运营成本与外部生态变化；早期消息以 **C++** 自建服务端为主**稳定性差、缺陷难收敛**；文件多自建；团队从小到多项目并行。
  - Task: 在容量、成本、可控性之间持续重定价架构与协作方式，使 IM 从「自建管道」演进为可支撑多子系统的平台能力。
  - Action: 文件侧由单机演进为**开源 FastDFS** 分布式存储（可裁剪、可运维）；消息侧早期 **C++** 自建服务端**稳定性差、缺陷持续**，整体切换至 **环信 Easemob（Hyphenate）** 云消息与**多端 SDK**，个人消息、群消息与底层消息基础设施由其承载（群聊、多消息类型、已读/重发等封装），自研侧重业务与中台与各子系统复用；**极光（JPush）** 并行作为**推送备用通道**，主要用于**通知类**下发与到达/唤醒补充，与环信主 IM 分层。组织侧引入**飞书**、**协作文档（如石墨）**、项目管理/预算/审批与自动化以匹配复杂度。个人从单一开发到全栈交付，并承担进度协调、人员与资源分配。
  - Result: 架构与流程与约束对齐，产品以平台化方式扩展子系统（具体迁移年份、工单下降比例待补：`MISSING_INFO`）。
  - Reflection: 「适应变化」在此是**约束变了就改系统与改协作**；IM 用 **Easemob** 换稳定性；**JPush** 专注**通知兜底**，避免把「聊天主链路」和「系统通知唤醒」绑死在一条通道上。口稿见 [A ⑨ Case B](#oral-09)、**B2-09**、**B1-08**、**Q23**、**A ②**；事实见 `projects/enterprise-messaging/facts.yaml`。
  - Suggested line (EN): "Easemob carried the real IM; JPush backed us on notification-style pushes and wake-ups — two channels, one product, less single-point pain on Android."
- 【2026-05-14 新增】`smart-factory` / 创意：串口电子秤 → 本地 WebSocket → 网页光标处自动填重（可用于：Creative / Initiative / Customer-centric / 复杂技术小题）
  - Situation: 工厂网页流程需录入材料克重；原流程为工人将物料置于电子秤、读数后在网页输入框**手动键入**，易出错、耗时且占用双手。
  - Task: 减少操作步骤、提高录入准确性，使工人可更顺畅地连续称重、换料。
  - Action: 确认电子秤可通过串口输出重量数据；在工人使用的 **Windows** 电脑侧实现本地服务：**监听串口**、解析/稳定读数，并内嵌 **WebSocket 服务端**；浏览器页面作为 **WebSocket 客户端**接收重量，并将数值写入**当前焦点**的输入框（或等价目标字段），替代读数再手敲。
  - Result: 称重与录入环节简化，减少人工转录错误，提升产线操作节奏（量化如节省单次录入秒数、差错率待补：`MISSING_INFO`）。
  - Reflection: 创意常来自「观察多余动作」：设备已输出数字，就不应再让人当二次传感器。口稿见 [oral-creative](#oral-creative)、**Q7 Option B**、**B2-02**。
  - Suggested line (EN): "The scale already knew the grams — I stopped making humans re-type what the serial port already said."
- 【2026-05-14 新增】`cross-project` / 多头用户与需求：原型对齐 + 单一决策人（可用于：**⑧ Tough feedback Case B** / Stakeholder / 需求治理 / 与产品协作）
  - Situation: 在 `smart-factory`、`picture-book-locker` 等项目中，工人或管理人员提出功能诉求，但往往不清楚实现方式与成本；产品与技术共同讨论方案后，向用户解释实现细节，用户仍难以理解，常需依赖**可触摸的原型**才能对齐预期。现场**多名用户**想法不一，容易导致范围摇摆、反复修改与开发工作量膨胀，团队间易出现抱怨。
  - Task: 将模糊、分散的口头需求转为可执行的开发范围；降低「开发对多人同时负责」带来的返工与冲突。
  - Action: 与产品、设计共同收敛候选方案；优先用**原型/可演示版本**与用户对齐「长什么样、怎么用」；对需求进行过滤与条目化；推动明确**客户侧唯一决策负责人**对需求做**拍板**（哪些做、哪些不做、何时做），开发不对接多头随意变更；将方案、里程碑与验收标准与产品、设计及需求方书面或可追溯方式对齐。
  - Result: 需求变更从「无序拉扯」转为「有主人的决策链」；开发节奏与预期更可管理（具体项目、轮次、量化待补：`MISSING_INFO`）。
  - Reflection: 「众人提需求」不等于「众人都是产品经理」；没有单一决策责任人，工程团队会被无限队列拖垮。口稿见 [A ⑧ Case B](#oral-08)、**B2-08**、**B1-09**。
  - Suggested line (EN): "Ten friendly users still make ten conflicting specs — we needed one customer owner to say yes or no, and a prototype so operators didn’t have to understand our architecture to understand the feature."
