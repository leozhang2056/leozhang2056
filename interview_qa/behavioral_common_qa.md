# Behavioral Interview — Leo Zhang

## 目录（概要）

| 块 | 概要 | 跳转 |
|----|------|------|
| 一 | **文档说明 + 规则**：简报、事实来源、自填临场规则 | [→](#section-doc-about) |
| A | **临场口语**：10 题；**①** 两档时长，**②—⑩** 每题一版；**补充** [创意 · 电子秤](#oral-creative)、[企业 IM · FastDFS 文件](#oral-enterprise-files) | [→](#section-oral-only) |
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

**提示（STAR）**：**主线**（S）企业即时通讯 Android 要后台也实时收消息；（T）省电杀后台 + 耗电；（A）优先级 + 白名单 + widget + 第三方推送（如 JPush）+ 重同步 + 状态对账；（R）更及时、更稳。**延展（可选口稿）**：**设备矩阵**像 **C 端**一样碎 — **小米/华为/OPPO** 等 **ROM** 定制；**很多问题只在用户真实环境里才冒头**，实验室无法穷尽所有「小问题」。需在 **发布时间**、**测试深度/人力成本**、**测试机型与设备投入** 之间做显式权衡；常规测 **主流版本**（约 **Android 7/8** 为下限）；报障 **模拟器未必复现** → **反馈驱动真机**、必要时 **购机** 或贴近用户现场/远程。**另一延展**：单机存不下聊天与业务文档 → **自建 FastDFS** 分布式文件能力（见 [oral-enterprise-files](#oral-enterprise-files)）。

One hard problem I worked on was **real-time messaging** on Android. The app needed to receive messages in the background, but Android may kill background apps to save battery.

So first I had to understand Android system behavior: **process priority**, **why apps get killed**, and what we could do to reduce that risk.

I used a layered approach. We guided users to add the app to the battery whitelist. We added a home-screen widget to improve app priority. We also used a third-party push channel (like **JPush**) so incoming push could wake the app and trigger sync. On top of that, we added other small reliability steps to improve survival chance.

The result was better message timeliness and fewer missed messages in background cases. What I learned is: on Android, one trick is not enough - you need multiple layers.

Another hard part was the trade-off between **real-time** and **battery**. If keep-alive is too aggressive, battery gets worse. If it's too weak, messages arrive late. So we tuned heartbeat/reconnect strategy and used push wake-up where possible.

We also planned for process death. If the app got killed, we restored session and ran fast re-sync on reconnect/resume. We used sent/delivered/read state checks to reduce message loss risk.

And yes, we saw edge bugs like "read state updated, but UI did not show it." We added stronger state reconciliation between local cache and server state, plus UI refresh triggers after ack.

**（延展）Enterprise IM — Android OEM / version fragmentation**  
Another messy side wasn't only **logic** — it was **where** the app ran. **Enterprise IM** still hits a **consumer-style Android long tail**: many OS levels, and in China **Xiaomi**, **Huawei**, **OPPO** ROMs change behavior again.

We focused routine QA on **mainstream** devices and versions — roughly down to **Android 7 or 8** as our lab floor; older phones we usually didn't keep. Brand-new OS drops sometimes lagged because we didn't own the hardware yet.

Users still reported bugs we couldn't replay on an emulator with the same API level — **vendor layers matter**. When we were stuck, we **bought a target phone**, or worked with the user **remotely / on-site** to see their real settings.

A lot of issues only **showed up in real user environments** — permissions, power policies, OEM tweaks we didn't mirror in the lab. The **usage surface** is too wide to **pre-catch** every **small** defect without paying **huge** time, people, and **device** money.

So we **balanced** three things: **release clock**, **how deep we test**, and **what hardware we can afford** to keep in-house. **Perfect** pre-release coverage wasn't the goal — **good** mainstream gates plus **fast** **narrow** follow-up when **signals** were **strong** was.

Ideally you'd run a **full matrix** before every ship — reality is **cycle time** and **cost**. We shipped on strong mainstream coverage, then closed repro on the **exact device path** when tickets came in.

<a id="oral-enterprise-files"></a>
### （补充）Enterprise IM — 自建文件平台（FastDFS）

**提示（STAR）**：（S）早期文件堆在一台服务器；用户上传、**聊天附件**、**合同管理**、**设计图**等子系统文件暴涨；（T）单机容量不够 + **数据私密性** → 不愿依赖**公有云文件 SaaS**；（A）选型 **开源 FastDFS**，做分布式存储、与 **User / Message / Workflow** 等子系统对接；处理**分片/冗余、备份、权限**；（R）容量与可控性上来，多业务共用同一套文档能力。**与事实对齐**：头像等路径曾出过安全事件后**迁移云端对象存储**（见 [A ④ Case C](#oral-04)）；**业务文档层**仍以**自建分布式文件**为主叙事，口试可一句话分层说明。

Early on, almost everything lived on **one file server**. As usage grew, it wasn't just "a few uploads" — **chat attachments** piled up, and other modules needed files too: **contracts**, **design drawings**, things you don't want to lose or leak.

We couldn't keep **all** of that on a single box forever. At the same time, **privacy / data control** mattered for the customer, so we didn't want to push **all** enterprise documents to a **public cloud file service** as the default answer.

So we built a **self-hosted** style file layer around **FastDFS** (an open-source distributed file system). The idea was **scale-out storage**, **redundancy**, and a **single document backbone** that **User**, **Messaging**, and **workflow-style** subsystems could all call into — not three different ad-hoc upload folders.

Operationally, that forced real engineering work: how files are **sharded**, how we think about **backup and restore**, and how **access control** stays consistent when many features touch the same files. It wasn't "install and forget" — it was **capacity + reliability + security** together.

*(Layering note for interviews: later, after a serious incident on a **Windows avatar upload path**, we tightened controls and moved some **user-facing blobs** to **cloud object storage**. That's a different slice of the same product — the **business document** story here is still **on-prem / self-managed** **FastDFS** for the heavy volume.)*

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

**提示（STAR）**：三选一。**Case A** **Smart Factory** 发布窗口；**Case B** **`enterprise-messaging`（企业即时通讯）** 早期**单人安卓**、几周原型上线、爆 bug、**日更**清优先级 + **产品**帮对接用户；**Case C** **`banknote-paper-mill`（造币印纸厂 / 保密断网）**：**断网**、仅可带离线笔记本进场；**每次进出需申请**，通常**提前约一周**才能进场；**断网部署/升级也麻烦**（离线包、受控传递、重验证）；内外环境反复联调、周期紧，**调试须场外充分准备**，易出现「一整天无可见进展」。

**Case A — Smart Factory（发布窗）**  
**Smart Factory** before release — **shop floor** doesn't wait. I split it: **triage**, **fix**, **verify**, **watch**. Pull the **owner** of the broken layer, **short** updates. We got it **out** without **breaking** the line. **Shrink unknowns fast** — that's how I handle heat.

**Case B — Enterprise IM（单人原型 + 上线救火）**  
Early on the **enterprise instant messaging** app — I was the **only Android dev**. We had **a few weeks** to build a **prototype**, test it, and **go live**.

After launch we hit **a lot of bugs**, and I was still the **only one** fixing them. Pressure was real — **users** wanted fixes fast, and I also had to **keep shipping**.

So I worked in a tight loop: every day I **listed** issues, **ranked** them by **priority**, fixed **high** items first, **shipped a build** every day, then **tested** again. Some fixes created **new** bugs — I kept **re-prioritizing** and focused on what hurt users most until things got **stable**.

I wasn't alone on the **people** side — **product / design** helped **explain** to users **why** things broke, **how long** fixes take, and they aligned **priority** and **dates**. They also shared **what we shipped each day** and **what we fixed**.

**Lesson**: under pressure, **visible order** + **daily rhythm** beats panic; **cross-team** user comms is part of the fix, not extra work.

**Case C — Air-gapped site（造币印纸厂 / 保密断网）**  
We had a **banknote paper mill** customer — **high secrecy** — **no internet** on site. I could only go in with an **offline laptop**: **export** their **data formats**, **inspect** samples, **test** what we could **inside**, then **leave** and **build** in our normal environment, then **come back** to **validate** in their **locked-down** network again.

**Every** **entry** and **exit** needed **customer** **approval**. In practice, **one** **on-site** **visit** often meant **asking** about **a week** **ahead** — so **floor** **time** was **rare** and **expensive**. I **prepared** **hard** **before** I walked in: **repro** steps, **builds**, **sample** **files**, **fallback** plans — because I couldn't **afford** to **improvise** there.

**Deploying** there was **not** like a **normal** **office** **push** — **no** **open** **internet** to **pull** **deps** or **patch** **fast**. We **carried** **offline** **packages**, **checked** **everything** through their **rules**, and **planned** **rollback** because **fix** **forward** was **slow** when **each** **visit** **cost** **so** much **calendar** **time**.

The **loop** was **heavy**: travel, **access** friction, and **tight** deadlines. Some days I **burned** a **whole day** and still had **nothing** that **looked** like **progress** — just **setup**, **permissions**, or a **dead** path. **Their** team was **stressed**; **we** were **stressed** too.

What helped: **tiny** goals per **visit** — "today I only prove **X** format / **one** import path"; **write down** every **artifact** I could take out; **tell** PM and the customer **early** that **air-gap** work has **empty-looking** days, and **re-scope** dates from **real** **cycle** time — including **approval** **lead** **time**, not **ideal** **office** time.

**Lesson**: **classified / offline** sites change what **pressure** means — you manage it with **honest** **expectations**, **checkpoint-sized** wins, **prep** that respects **access** **lead** **time**, and **release** **packages** built for **no-net** **installs**, not **last-minute** **downloads**.

<a id="oral-06"></a>
### ⑥ Prioritize quickly

**提示（STAR）**：三选一。**Case A** 产线问题 + PM 要功能；**Case B** 无对标、**下车间**澄清模糊需求、**快原型**迭代、大版本演进；**Case C** **多项目并行**：外部（`smart-factory`、`enterprise-messaging` 等）+ 自营（`picture-book-locker` 图书馆借阅柜、互联网产品线等），**按交付/风险/难点**排每日焦点，必要时**跨组协调人力**。

**Case A — 产线 vs 里程碑**  
**Smart Factory** — **line** issues, **PM** wants features. I fix what **hurts operators** first, then what's **on the milestone**, and I'm **honest** about dates on the rest. **Clear order** beats a **pretty** plan nobody follows.

**Case B — 下车间 + 模糊需求 + 原型迭代**  
**Smart Factory** had **no product we could copy** — we went **into the workshops**, watched **how people really worked**, and turned **vague** asks into plans we could **negotiate** with the team: **what** to build first, **how long** a slice could take.

We had to **ship prototypes fast**, then **keep changing** them as understanding improved. Requirements stayed **fuzzy** for a long time — people felt something was wrong but couldn't spell the **exact** flow — so we **validated on real screens**, not only in meetings. **Pressure** was on the **whole** team. Even after **first delivery**, users sometimes **weren't fully on board**; we needed **bigger** follow-on releases — **second**, **third** major versions — **adding** what stuck and **trimming** what didn't.

**Lesson**: when nobody has a crisp spec, **prototype + tight feedback** sets the real priority list; **big** replans aren't shame — they're how **shop-floor** software matures.

**Case C — Many projects at once（外部 + 自营）**  
At **Chunxiao** I often had **several projects moving at once** — not just one backlog. Some were **external**: **factory** work (**Smart Factory**), **enterprise messaging** for customers. Some were **our own products**: **library smart lockers** (**picture-book-locker**), plus other **internal internet-facing** lines.

I couldn't treat every ping as **P0**. Each day I wrote down: which **release** is **nearest**, where I'm still **stuck** on a **hard** problem, and what can **slide** a little without **breaking trust**. **Impact** and **deadline** first — then **depth** time on **blockers**.

When I couldn't **unblock** alone, I **asked early**: **borrow** time from **another group**, **pair** for a day, or **split ownership** clearly so nobody assumed **magic capacity**.

**Lesson**: **portfolio** pressure is **scheduling** plus **escalation** — a **visible** order for yourself and **honest asks** when **parallel** streams need **more hands**.

<a id="oral-07"></a>
### ⑦ Process improvement

**提示（STAR）**：（S）多厂上线曾以**手动复制文件**为主；（A）**Jenkins** 连 **GitLab**、**CI/CD**，**首期配置麻烦**；**工厂项目先试点**，再**全线迁移**同一套流程；辅以容器、清单、文档；（R）部署更可重复、少人为漏操作。

For a long time we mostly **deployed by hand** — copy builds, sync files, easy to miss a step or ship the wrong piece. **Smart Factory** had many sites, so the pain scaled.

We brought in **Jenkins** hooked to **GitLab**: **CI/CD pipelines** for build and deploy, less tribal knowledge, fewer midnight surprises. The **early setup was tedious** — wiring repos, agents, secrets, getting the first pipeline green — but we paid that cost once.

**Smart Factory** was the **first** place we ran it for real. After it looked stable, **the rest of the team moved to the same flow** so we didn't maintain two different release worlds. I still used **Dockerized Spring** where it helped, plus checklists and short docs so new people weren't chasing chat. Boring infra — but rollouts got predictable.

<a id="oral-08"></a>
### ⑧ Tough feedback

**提示（STAR）**：**二选一**。**Case A** **经理**直接反馈：架构/大决策**没写清** → **ADR** + **onboarding**。**Case B** **需求侧难协同**（`smart-factory` / `picture-book-locker` 等）：用户要功能但**不懂实现**；产品+技术定方案后**讲解用户仍听不懂** → 靠**原型**对齐；**多人各执一词** → 反复改、开发量大、互相抱怨 → **过滤需求**、明确范围，找**客户方唯一拍板人**决定做/不做，**不对多头负责**；与**产品、设计、需求方**书面对齐方案与「完成定义」。*注：Case B 更偏 **Stakeholder / 需求治理**；题干若严格要求「上司给你的批评」优先 **Case A**。*

**Case A — Manager（文档习惯）**  
Manager said my **big decisions** weren't **written** enough — next hire would get **lost**. Fair. I added **light ADRs** and **short** onboarding notes — **why**, not **novels**. **Onboarding** sped up. I should've started earlier.

**Case B — Many user voices（原型 + 单一决策人）**  
On **Smart Factory** and **library / picture-book** work, **users** asked for **features** but **didn't** know what each **option** **cost**. **Product** and **engineering** **shaped** the **plan** **together** — then we tried to **explain** **how** we'd **build** it, and **honestly** **many** **operators** and **managers** **couldn't** **follow** **internals**. A **working** **prototype** **moved** the **talk** **faster** than **slides**.

The **hard** part was **several** **people** **pulling** **different** **ways** — **scope** **churn**, **blame** between **teams**, **huge** **rewrite** **risk**. We **stopped** **treating** **every** **chat** as a **spec**: **filtered** **asks** into **clear** **buckets**, and got **one** **named** **customer** **owner** to **decide** **what** **ships** — **not** **ten** **part-time** **bosses** for **dev**. **PM**, **design**, and **that** **owner** **aligned** on **plan**, **timeline**, and **what** **done** **means**; then **engineering** **executed**.

**Lesson**: **noise** isn't a **requirements** **doc** — **one** **named** **customer** **owner** plus a **prototype** **beats** **ten** **part-time** **architects**.

<a id="oral-09"></a>
### ⑨ Adapted to change

**提示（STAR）**：（S）**ChatClothes** 中途约束变紧；（A）**重测**、**LLM** 本地、砍范围；（R）**honours** 稳住。

Thesis mid-way — **offline** and **speed** became **hard** rules. Numbers didn't support the **old** design. I **re-measured**, **LLM** **local**, **cut** scope where needed. Finished **strong** with **honours**. **Measure, then change your mind**.

<a id="oral-10"></a>
### ⑩ Why should we hire you?

**提示（STAR）**：（T）为什么选我；（A）**十年**交付 + 最近 **AI**；（R）奥克兰 + **full-time** + 愿意扛事。

You get **~ten years** shipping **mobile**, **backends**, and the **messy** middle — plus recent **applied AI** where it still has to **run** for users. I'm in **Auckland**, **full-time** **OK**, flexible on **Kotlin** / **Spring** / **new** AI bits. Point me at a **real user problem** — I'll **push** it **over the line** with the team.

<a id="oral-creative"></a>
### （补充）Creative idea — Smart Factory（电子秤串口 → WebSocket → 网页自动填重）

**提示（STAR）**：（S）网页端要录**材料克重**，工人原先**上秤 → 读数 → 手敲**，易错、慢、占手；（T）尽量少操作、保证准确；（A）确认秤可**串口输出**；在工人 **Windows** 电脑上跑**本地服务**：**串口监听** + 内嵌 **WebSocket server**，浏览器作 **WS client** 收重量，**填入光标所在输入框**；（R）免手敲、连续称重换料更顺。

**Script（口语）**  
On **Smart Factory**, workers used a **web** screen to record **fabric weight**. The old loop was **annoying**: put the roll on the **scale**, **read** the number, **type** it into the box — slow, easy to **mistype**, and it **ties up** **hands**.

I checked the **scale** — it could **push** weight over **serial**. On the **Windows** **PC** next to the scale, I shipped a **small** **local** **service**: **listen** to **COM**, normalize the reading, and run a tiny **WebSocket** **server**. The **browser** **page** opened a **WS** **client**, got **stable** **grams**, and **dropped** the value **into** **whatever** **field** had **focus**.

So the operator just **keeps** **weighing** and **swapping** **pieces** — **no** **re-keying**, **fewer** **errors**, **faster** **line**. Same **idea** I like elsewhere: **remove** **dumb** **friction** **between** **physical** **truth** and **software**.

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
- Tell me about a time you worked under pressure.（产线发布窗；或 **造币印纸厂** 等断网进场联调，见 [A ⑤ Case C](#oral-05)）
- How do you prioritize when everything feels urgent?（影响 × 风险 × 透明沟通；多线并行见 [A ⑥ Case C](#oral-06)、**Q8** / **Q36**）
- Tell me about a time you had multiple deadlines.（多项目并行 + 内外部混排，见 [A ⑥ Case C](#oral-06)；或与 Smart Factory 单项目排优先合并准备）

<a id="b1-04"></a>
### 4) 失败与复盘
- Tell me about a time you failed.（中草药标注周期低估 → 小样试点；安全/基础设施教训见 **`enterprise-messaging`** [A ④ Case C](#oral-04)）
- Tell me about a time you missed a deadline.（同上故事，见 **Q22**）
- Describe a production issue you handled.（电子秤采集 / 发布窗口 triage，用 Smart Factory；安全向可选 **`enterprise-messaging`** 头像上传入侵与恢复，见 [A ④ Case C](#oral-04)）

<a id="b1-05"></a>
### 5) 复杂问题解决与技术判断
- Tell me about a complex technical problem you solved.（ChatClothes 剖延迟 + 本地 LLM + YOLO12n-LC；**或** `enterprise-messaging` **Android OEM/版本碎片化**与复现策略，见 [A ② 延展](#oral-02)；**或** **FastDFS** 自建文件平台：容量 + 私密性 + 备份/权限，见 [A ② · 文件](#oral-enterprise-files)）
- Tell me about a difficult decision you made.（范围 / 技术路径取舍，可接 ChatClothes 或产线优先；**云文件 SaaS vs 自建 FastDFS** 见 [oral-enterprise-files](#oral-enterprise-files)）
- Describe a trade-off you had to make (speed vs quality, etc.).（速度 vs 可观测性 / 范围 vs 信任，用 Smart Factory 分期上线；**Android** 全机型矩阵 vs 发版周期，见 [A ② 延展](#oral-02)；**运维成本 vs 数据可控**：自建分布式文件 vs 公有云，见 [oral-enterprise-files](#oral-enterprise-files)）

<a id="b1-06"></a>
### 6) 主动性与影响力
- Tell me about a time you took initiative.（论文交付物超出要求：部署文档 + API 说明，见 **Q7**；**或** **Smart Factory** 串口秤 + **WebSocket** 网页自动填重，见 [创意 · 电子秤](#oral-creative)）
- Describe a process improvement you drove.（手动复制 → **Jenkins + GitLab CI/CD**；容器/清单/文档，见 [A ⑦](#oral-07)）
- Tell me about a time you influenced without authority.（用数据推动分期试点，与经理分歧题同源）

<a id="b1-07"></a>
### 7) 反馈与成长
- Describe a time you received critical feedback.（**Case A** 经理 + ADR / onboarding；**Case B** 多方用户与需求拉扯 → 原型 + 客户方拍板人，见 [A ⑧](#oral-08)）
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
- Describe a difficult customer/stakeholder situation.（范围拉扯 → 数据 + 试点；**多头需求** → [A ⑧ Case B](#oral-08)）
- Tell me about a time you managed unclear requirements.（先澄清指标与「完成定义」，见 **Q30**；**听不懂实现** → **原型** + 拍板人，见 [A ⑧ Case B](#oral-08)）
- How do you handle conflicting stakeholder expectations?（透明优先级 + 书面契约；**单一客户决策人**，见 [A ⑧ Case B](#oral-08)）

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
**STAR — `smart-factory`（创意/减负，可选）**：网页录克重原需读秤手敲；**Windows 本地服务**串口监听 + **WebSocket** 推浏览器，**光标处自动填重**；工人连续换料称重。**Reflection：**把物理读数直接接进 UI，砍掉无意义复制。口稿见 [oral-creative](#oral-creative)。  
**STAR — `enterprise-messaging`（Android 碎片化，可选）**：类 C 端设备长尾；**小米/华为/OPPO** 等 ROM 差异；**大量问题仅在用户真实环境暴露**，测试无法前置穷尽所有小问题；在 **发版节奏 / 测试成本 / 测试机型投入** 间权衡；常规测主流版本（约 **Android 7/8** 为下限）；报障模拟器未必复现 → **反馈驱动真机**、必要时购机或贴近用户环境。**Reflection：**接受「实验室 ⊂ 真实长尾」，用主流守门 + 强信号下的真机补洞，而不是无限拉长测试或无限买机。  
**STAR — `enterprise-messaging`（FastDFS 文件平台，可选）**：单机扛不住用户上传 + **聊天附件** + **合同/设计图**等业务文档；**私密性** → 不默认走**公有云文件服务**；**开源 FastDFS** 自建分布式存储；对接多子系统；**分片、冗余、备份、权限**一体化考虑。**Reflection：**文件是共享基础设施，选型要同时付「容量 + 可靠 + 安全」的运维账；与头像路径事后**迁云**可分层叙述（见 [oral-enterprise-files](#oral-enterprise-files)、facts `highlights`）。  
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
**STAR — `banknote-paper-mill`（断网保密现场，可选）**：造币印纸厂类涉密环境禁止联网；仅离线笔记本进场分析/导出数据格式、内网测试；外场开发后再进场验证；**每次进出须申请，通常提前约一周才能进场**；**断网部署/升级依赖离线包与受控传递，步骤与验证更重**；现场调试窗口极短，**场外做足脚本/安装包/回滚与复现准备**；流程冗长、周期紧；易出现整日无可交付进展；客户与开发方双重焦虑。**Reflection：**排期要计入审批提前量 + 离线发布成本；进场分钟级宝贵，不能把「到现场再想」当常态。

---

<a id="b2-06"></a>
### 6) Tell me about a time you had to prioritize quickly.

**口语 →** [专页 ⑥](#oral-06)  
**STAR — Smart Factory（产线窗）**：产线 vs 里程碑 vs 维护；先产线影响 → 再里程碑；其余标日期透明。**Reflection：**可见顺序 > 全是 P0。可接 **high uptime** 口径若追问。  
**STAR — Smart Factory（模糊需求，可选）**：无对标、下车间理解工人/工厂真实痛点；与团队对齐开发节奏与任务切分；快原型 → 反复确认 → 需求逐步精确；首版上线后可能仍需大版本调整；多轮大版本边加边减功能。**Reflection：**模糊需求时优先级由「验证假设」驱动，而非一开始的文档。  
**STAR — 多项目组合（可选，`cross-project`）**：同时推进外部客户项目（如 `smart-factory`、`enterprise-messaging`）与自营产品线（如 `picture-book-locker` 图书馆借阅柜、互联网相关自营项目）；按**临近交付、未攻克难点、影响与承诺**排每日任务；进度与阻塞透明；需支援时**尽早跨组协调**。**Reflection：**组合压力=个人日程可见性+敢于升级要资源，而不是假装能并行无限深度工作。

---

<a id="b2-07"></a>
### 7) Tell me about a process improvement you drove.

**口语 →** [专页 ⑦](#oral-07)  
**STAR — `smart-factory`（DevOps）**：长期以手动复制/同步为主、易漏易错；引入 **Jenkins** 对接 **GitLab**，落地 **CI/CD**；**前期流水线/凭证/执行机等配置耗时**，先在**工厂项目试点**，验证稳定后**各项目统一迁移**到同一套发布流程；结合容器化 Spring、清单与短文档，多厂 rollout 更可预期。**Reflection：**一次性付清「标准化」成本，比长期维持多套手搓发布更省团队总时间。

---

<a id="b2-08"></a>
### 8) Describe a time you received tough feedback.

**口语 →** [专页 ⑧](#oral-08)  
**STAR — Case A（经理）**：经理点架构未写清；ADR + onboarding；默认「写完再收工」。**Reflection：**文档 = 长期功能。  
**STAR — Case B（多方需求，可选）**：`smart-factory` / `picture-book-locker`；用户要功能不懂实现；产品+技术定方案讲解困难 → **原型**对齐；多人意见不一反复改 → **过滤需求**、**客户方唯一拍板人**、不对多头负责；与产品/设计对齐计划与验收。**Reflection：**没有决策人的「众人需求」会变成无限返工。

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
**提示（STAR）**：**Option A** **ChatClothes** 额外 **部署文档 / API / 手册**；（R）导师认可 + **提前交**。**Option B** **Smart Factory** 创意简化称重录入（[创意 · 电子秤](#oral-creative)）。
**Script（口语）**
> **ChatClothes** — school asked demo + thesis; I added **deploy docs**, **API** spec, **user manual** so others could **run** it alone. Supervisor **praised** the docs. I **submitted six months early** — writing forced **clear** design choices.
> **Smart Factory** — workers were **re-typing** **scale** **readings** into a **web** **form**. I **bridged** **serial** **weight** through a **Windows** **service** with a **local** **WebSocket** **server**; the **browser** **client** **filled** the **focused** **field**. **Less** **typing**, **fewer** **mistakes**, **faster** **hands** on the **floor**.

<a id="q-08"></a>
### 8) How do you prioritize when you have multiple deadlines?
**提示（STAR）**：**影响 × 风险**；**Smart Factory** **产线** 优先；需求模糊时 **下车间 + 快原型**（见 [A ⑥ Case B](#oral-06)）；**多项目并行**见 [A ⑥ Case C](#oral-06)；早说 **排序变化**。
**Script（口语）**
> I sort by **impact** and **risk**, not loudest voice. **Smart Factory** — **production** issues before **nice-to-have** features when users are **on the line**. Then **milestone** work. I **say early** when order **changes**. We kept **uptime** and still **shipped**.
> When **several** **projects** ran **together** — **external** **factories**, **enterprise** **messaging**, plus **our** **own** **products** like **library** **lockers** — I **listed** **nearest** **deadlines**, **open** **blockers**, and **what** could **wait**. I **reached** **out** **early** for **help** from **other** **teams** when I **couldn't** **unblock** **alone**.

<a id="q-09"></a>
### 9) How do you handle stress and pressure?
**提示（STAR）**：**习惯**：里程碑 + 范围 + 节奏；**故事（可选）**：`enterprise-messaging` 早期单人安卓日更救火，见 [A ⑤ Case B](#oral-05)；**造币印纸厂（`banknote-paper-mill`）断网进场**见 [A ⑤ Case C](#oral-05)。
**Script（口语）**
> I **cut unknowns early** — **milestones**, **check-ins**. Under heat: **smaller scope**, **stable core** first, then grow. **Routine** and **exercise** to reset. **ChatClothes** was tight — **early plan** helped me **finish ahead**.
> When it was really hot — like **solo Android** on our **enterprise IM** app after a fast launch with **many bugs** — I used a **daily** list, **priority** order, **ship a build** every day, and let **product** help users with **honest** timelines. **Rhythm + clarity** beats panic.
> Another kind of pressure was **air-gapped** customers — a **banknote paper mill**: **no internet** on site and **strict secrecy**. **Every** **in** and **out** needed **approval** — usually **~a week** to **book** **one** **visit**. **Offline laptop** only: **grab** formats, **test** inside, **code** outside, **return** to verify. **Deploying** there was **slow** too — **offline** **bundles**, **controlled** **transfer**, **heavy** **check** steps, not a quick **online** **push**. I **prepped** **before** each **visit** so **short** **floor** **time** wasn't **wasted**. Some days **zero** visible **progress** — still **cost** a full day. I set **small** checkpoints per **visit**, **documented** exports, and **reset** timelines with PM and the customer so **nobody** thought we were **stalling** when **access** and **process** were the **bottleneck**.

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
**提示（STAR）**：问清 **目标/约束**；**画架构**；**spike** 模糊点；**写**大决策；模糊需求时 **下车间/用户** + **快原型** 验证（见 **A ⑥ Case B**）；若含 **断网/保密现场**，把**进场节拍**、**进出审批与提前量（如约一周）**、**离线部署/升级成本（制品、传递、校验、回滚）**与可带出资产写进约束（见 **A ⑤ Case C**）。
**Script（口语）**
> I **ask** until **goals** and **constraints** are clear — put **unknowns** on the table. Sketch **architecture** and **interfaces**, **spike** if two paths are fuzzy. **Document** big calls, **iterate** with **feedback** and **numbers**. When users only have a **fuzzy** picture, I **go to the floor**, **prototype fast**, and **tighten** requirements from **what they actually do**.

<a id="q-31"></a>
### 31) What is the biggest technical challenge you have worked on?
**提示（STAR）**：**Option A** **ChatClothes** **端到端延迟** + 离线；（A）**profile** → **LLM** 本地 + **YOLO12n-LC**；（R）可演示 + **早交论文**。**Option B** **`enterprise-messaging`**：**Android** **OEM/版本**碎片化、难复现、测试矩阵 vs 周期（见 [A ② 延展](#oral-02)）。**Option C** **`enterprise-messaging`**：**FastDFS** 自建分布式文件 — 聊天与业务文档体积、**私密性**、子系统统一接入、备份与权限（见 [oral-enterprise-files](#oral-enterprise-files)）。
**Script（口语）**
> **ChatClothes** — make the **whole** path **fast** on **small** hardware **offline**. I thought **diffusion** was the problem — **profiling** showed **LLM** **cloud** trips were. I went **local LLM**, lighter **vision** (**YOLO12n-LC**). **System worked**; thesis **handed in early**.
> Another big one was **enterprise IM on Android** — not one Android, thousands of real phones. **Xiaomi / Huawei / OPPO** ROMs bend the rules again. A lot of bugs only showed up in **real user settings**, and we couldn't pre-find every small issue without blowing **schedule**, **test cost**, and **device** budget. We tested mainstream versions (**~7/8 floor** in lab), then closed hard tickets on **real hardware** — sometimes **buying** a phone, sometimes **sitting** with the user. Full matrix every release wasn't affordable; we **traded** **depth** for **ship date** and **paid** for the **exact** repro path when it **mattered**.
> A third challenge was **file volume** at scale. **Chat attachments** and business modules like **contracts** and **drawings** outgrew **one server**. For **privacy / control**, we didn't default to **public cloud file SaaS**. We used **self-hosted** **FastDFS** for **distributed** storage, wired it into multiple subsystems, and had to own **sharding**, **redundancy**, **backup**, and **access control** — not just "upload works".

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
**提示（STAR）**：**影响+风险**；**切块**；**早说**；必要时 **砍范围**保核心；多线并行时见 [A ⑥ Case C](#oral-06)。
**Script（口语）**
> **Too much** work — I sort **impact** and **risk**, break into **chunks**, **say early** if dates move. If needed I **cut** scope to save the **must-have**, then **grow** back when **stable**.
> With **many** **queues** **at** **once**, I **pick** **today's** **focus** from **who** **waits** on **me** **next** and **what** **still** **needs** **deep** **thinking** — and I **ask** for **backup** **before** I'm **late**, not **after**.

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
**提示（STAR）**：**双周 Sprint** **六年**；**demo**；**接口契约**；交付侧从**手动部署**演进到 **GitLab + Jenkins CI/CD**；**先工厂项目试点、后统一迁移**（见 [A ⑦](#oral-07)）。
**Script（口语）**
> **Smart Factory** — **two-week sprints** **~six years**: plan, standup, review, retro. Every sprint **demo** with **real** software. **Shared API contracts** before **breaking** changes — **mobile**, **backend**, **IoT** stayed aligned.
> On **release**, we moved from mostly manual copy deploys to **Jenkins** tied to **GitLab** — **CI/CD pipelines** so build and deploy were repeatable, not hero runs. **Setup was painful at first** — we **piloted on Smart Factory**, then **everyone migrated to the same pattern** so we didn't run old and new side by side forever.

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
