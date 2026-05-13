# Behavioral Interview — Leo Zhang

## 目录（概要）

| Part | 内容 | 跳转 |
|----|------|------|
| Part 1 | **Core Behavioral Answers**：Q1–Q45 的主答，先看这个 | [→](#section-oral-only) |
| Part 2 | **Project Story Bank**：按项目归类的故事仓库 + B1/B2 分类索引 | [→](#section-part-b) |
| Part 3 | **Technical Deep Dive Notes**：Q1–Q45 全文脚本 + 深挖细节 | [→](#section-5-scripts) |
| Part 4 | **Quick Review Sheet**：工具、速查关键词、草稿模板、收件箱 | [→](#section-toolbox) / [→](#section-appendix) |

> 细粒度锚点（如 `oral-01`、`b1-03`、`q-12`、`d3-04`）在**正文各小节标题上方**；需要时搜索 `id="q-12"` 或先打开对应 Part 再按 `### 12)` 等标题浏览。

---

<a id="section-doc-about"></a>
## Part 1 — Core Behavioral Answers

This is the main speaking path. Keep the original answers here, and only use the story bank / deep dive / quick review when you need extra detail.

本文件是 **Behavioral 面试**用：**Part 1** 放主答，**Part 2** 放故事库，**Part 3** 放速查/工具，**Part 4** 放全文脚本/深挖；正文尽量先看主答，再回故事库和工具区。

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

**Key idea:** 讲 Android 后台收消息，强调多层保活和主通道/备用通道。

One hard problem I worked on was **real-time messaging** on Android. The app needed to receive messages in the background, but Android may kill background apps to save battery.

So first I had to understand Android system behavior: **process priority**, **why apps get killed**, and what we could do to reduce that risk.

I used a layered approach. We guided users to add the app to the battery whitelist. We added a home-screen widget to improve app priority. On the **transport** side, **Easemob** handled the **core IM** path. We also wired **Jiguang** (**JPush**) as a **backup push channel** for **notification-style** traffic — things like **alerts** and **wake-ups** — so delivery didn't depend on **one** pipe when the OS was aggressive about background work. On top of that, we added other small reliability steps to improve survival chance.

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

**Key idea:** 单机文件扛不住时，讲 FastDFS、自建分层和权限控制。

Early on, almost everything lived on **one file server**. As usage grew, it wasn't just "a few uploads" — **chat attachments** piled up, and other modules needed files too: **contracts**, **design drawings**, things you don't want to lose or leak.

We couldn't keep **all** of that on a single box forever. At the same time, **privacy / data control** mattered for the customer, so we didn't want to push **all** enterprise documents to a **public cloud file service** as the default answer.

So we built a **self-hosted** style file layer around **FastDFS** (an open-source distributed file system). The idea was **scale-out storage**, **redundancy**, and a **single document backbone** that **User**, **Messaging**, and **workflow-style** subsystems could all call into — not three different ad-hoc upload folders.

Operationally, that forced real engineering work: how files are **sharded**, how we think about **backup and restore**, and how **access control** stays consistent when many features touch the same files. It wasn't "install and forget" — it was **capacity + reliability + security** together.

*(Layering note for interviews: later, after a serious incident on a **Windows avatar upload path**, we tightened controls and moved some **user-facing blobs** to **cloud object storage**. That's a different slice of the same product — the **business document** story here is still **on-prem / self-managed** **FastDFS** for the heavy volume.)*

<a id="oral-03"></a>
### ③ Conflict with a teammate

**Key idea:** 先讲 1:1 和反馈方式怎么改，而不是对错。

In **Enterprise Messaging**, I had a teammate who pushed back on **code review** a lot.  
At first it looked like a skill issue, but after a **1:1** talk I found it was more about trust — they had bad experiences with public criticism before.

So I changed the way we worked: feedback was **private**, **specific**, and focused on code, not person. For tricky parts, we did short **pairing** sessions instead of long comment threads.

After that, review speed got better, code quality improved, and our release rhythm stayed stable.  
What I learned is simple: in team conflict, fixing the **communication style** is often as important as fixing the code.

**Case B（可选：技术选型分歧）**
**Key idea:** 讲技术选型时的约束、风险和团队共识。

In one new project, I had a teammate with very deep experience in older stacks like **C#** and **C++**.  
He preferred familiar tools for delivery control, while I thought some newer parts fit the new requirements better.

Instead of arguing by preference, we brought in the **PM**, **team lead**, and the team to evaluate options together: delivery time, risk, maintainability, and how well each stack matched the project direction.

That changed the discussion from "my tech vs your tech" to "what is best for this project now and later."  
We aligned on a practical plan, and the team moved forward with less friction.

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

**Key idea:** 先说压力来源，再说你怎么稳住节奏。

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

**Key idea:** 用 impact / risk / dependency 排序，再早沟通。

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

**Key idea:** 从手工到自动化，讲为什么更稳。

For a long time we mostly **deployed by hand** — copy builds, sync files, easy to miss a step or ship the wrong piece. **Smart Factory** had many sites, so the pain scaled.

We brought in **Jenkins** hooked to **GitLab**: **CI/CD pipelines** for build and deploy, less tribal knowledge, fewer midnight surprises. The **early setup was tedious** — wiring repos, agents, secrets, getting the first pipeline green — but we paid that cost once.

**Smart Factory** was the **first** place we ran it for real. After it looked stable, **the rest of the team moved to the same flow** so we didn't maintain two different release worlds. I still used **Dockerized Spring** where it helped, plus checklists and short docs so new people weren't chasing chat. Boring infra — but rollouts got predictable.

<a id="oral-08"></a>
### ⑧ Tough feedback

**Key idea:** 先承认反馈合理，再讲你怎么改。

**Case A — Manager（文档习惯）**  
Manager said my **big decisions** weren't **written** enough — next hire would get **lost**. Fair. I added **light ADRs** and **short** onboarding notes — **why**, not **novels**. **Onboarding** sped up. I should've started earlier.

**Case B — Many user voices（原型 + 单一决策人）**  
On **Smart Factory** and **library / picture-book** work, **users** asked for **features** but **didn't** know what each **option** **cost**. **Product** and **engineering** **shaped** the **plan** **together** — then we tried to **explain** **how** we'd **build** it, and **honestly** **many** **operators** and **managers** **couldn't** **follow** **internals**. A **working** **prototype** **moved** the **talk** **faster** than **slides**.

The **hard** part was **several** **people** **pulling** **different** **ways** — **scope** **churn**, **blame** between **teams**, **huge** **rewrite** **risk**. We **stopped** **treating** **every** **chat** as a **spec**: **filtered** **asks** into **clear** **buckets**, and got **one** **named** **customer** **owner** to **decide** **what** **ships** — **not** **ten** **part-time** **bosses** for **dev**. **PM**, **design**, and **that** **owner** **aligned** on **plan**, **timeline**, and **what** **done** **means**; then **engineering** **executed**.

**Lesson**: **noise** isn't a **requirements** **doc** — **one** **named** **customer** **owner** plus a **prototype** **beats** **ten** **part-time** **architects**.

<a id="oral-09"></a>
### ⑨ Adapted to change

**Key idea:** 讲约束变了，你也跟着改方案。

**Case A — ChatClothes**  
Thesis mid-way — **offline** and **speed** became **hard** rules. Numbers didn't support the **old** design. I **re-measured**, **LLM** **local**, **cut** scope where needed. Finished **strong** with **honours**. **Measure, then change your mind**.

**Case B — Enterprise IM（约束变了，系统跟时代一起改）**  
On our **enterprise IM** product, nothing stayed frozen for ten years — **constraints changed**.

The **product shape** evolved too: we started as a **standalone** **enterprise** **chat** **client**, not a **platform**. **Then** we **turned** **IM** **identity** into a **real** **user** **center** and **reused** it for **login** and **SSO-style** **access** **across** **modules**. **Next** we **added** a **central** **file** **service** that **grew** into the **shared** **file** **backbone** for **chat** **and** **business** **docs**. **Once** those **bases** **existed**, **other** **subsystems** **plugged** **in** — **attendance**, **engineering** **tools**, **finance** **approvals**, **hardware** **management**, **permissions** — **all** **on** the **same** **primitives**. We **borrowed** **ideas** from **how** the **industry** does **SSO**, **central** **file** **hosting**, **drag-and-drop** **upload** **flows** **like** **Qiniu** **Kodo-style** **products**, **Aliyun** **OSS-style** **object** **storage**, and **org** **permissions** (**Feishu**/**Lark**-style **patterns**), **but** **kept** **what** **had** to **stay** **self-hosted** **under** **control**.

**Files** first: we started with **one file server**, but **chat attachments** and business docs like **contracts** and **drawings** grew fast. We needed **distributed storage** with control over data, so we moved to **self-hosted FastDFS** — **open source** we could **tune**, not a black box we couldn't touch.

**Messaging** changed too. Our first **in-house** path was **C++** servers — **stability hurt us**: bugs kept coming back and the backlog never felt **done**. We **stopped** trying to **own every low-level detail** ourselves. We **migrated** **personal**, **group**, and **baseline** messaging to **Easemob** (**Hyphenate** / **环信**) — **cloud** **relay** plus **multi-platform** **SDKs**. It gave us **calmer** operations: **better** **APIs**, **rich** **message** **types**, **read** **receipts**, **resend** / **retry** semantics, and **clients** on **more** **surfaces** without reinventing the wheel. **Separately**, we kept **Jiguang** (**JPush**) as a **backup push** path for **notification-style** traffic — **alerts** and **wake-ups** — layered **next to** Easemob so we weren't **single-channel fragile** when Android got strict about background work. Our own stack moved **up** the stack — **business** rules, **permissions**, **files**, **user** **center** — **platform** **subsystems** on top of **shared** **infrastructure**.

**People and process** changed as well. When the team was small, everyone wore many hats. When projects **overlapped** and approvals got heavier, we adopted **Feishu** (**Lark**), **collaborative docs** (e.g. **Shimo** where we used it), **PM / budget / approval** discipline, and more **automation** so engineering didn't drown in admin.

My own role moved with that — from **one focused developer**, to **full-stack delivery**, to **owning schedule**, **coordination**, and **who gets bandwidth** when several fires burn.

**Lesson**: **Good** teams don't romanticize the first design — they **re-price** reality when **volume**, **cost**, or **risk** moves, and they **let tools** (open source **or** vendor cloud) **earn** their place.

<a id="oral-10"></a>
### ⑩ Why should we hire you?

**Key idea:** 先说你能交付什么，再说为什么对岗。

#### 30 秒版（约 30s）

You should hire me because I **ship end-to-end** — about **ten years** of **Android**, **Java** **backends**, and **web** when the product needs the **whole** stack — not just slides.

I recently finished **AUT** — **Master of Computer and Information Sciences**, **First Class Honours**, **applied AI**. **ChatClothes** shows I can make **AI** **work** on **real hardware**, **offline**, with **clear** **metrics**.

Before that, **Enterprise Messaging** and **Smart Factory** are my **proof** at **scale** — **latency**, **load**, **devices**, **factories**, **long** **releases**.

I'm in **Auckland** with **full-time** **work** **rights**. Point me at your **hardest** **user** **problem** — I'll **own** it with the team until it's **in** **production**.

#### 1 分钟版（约 60–75s）

Here's why I'm a **strong** **hire**: I **don't** **only** **code** **one** **layer** — I've spent roughly **ten years** turning **messy** **real-world** **constraints** into **software** **people** **use** **every** **day**.

On **Android**, I'm comfortable **deep** in the stack — **NDK**, **TCP/UDP**, **battery** and **push** **reality**, **OEM** **differences** — not just UI. On the **server**, I've lived in **Java**, **Spring**-style **services**, **integration**, **releases**, and **keeping** **systems** **up** when users depend on them.

I just finished **AUT** — **First Class Honours**, **applied AI**. My thesis, **ChatClothes**, is the **simplest** **proof** of how I work: **measure**, **cut** **what** **doesn't** **fit** the **hardware**, and **ship** a **full** **pipeline** — **local** **LLM**, **vision**, **offline** — that **still** **feels** **fast** to a **user**.

Before **AUT**, my **big** **production** **stories** are **Enterprise Messaging** — **real-time** **IM** at **thousands** of **DAU** and **very** **high** **daily** **message** **volume** — and **Smart Factory** — **IoT**, **shop-floor** **workflows**, **many** **sites**, **years** of **rollout** discipline.

I'm **based** in **Auckland** with **full-time** **work** **rights** in **New Zealand**. I'm **flexible** on **stack** details — **Kotlin**, **Spring**, **new** **AI** **tooling** — what I care about is **outcomes**: **clear** **ownership**, **honest** **trade-offs**, and **shipping** **with** the **team**.

#### 精简一句版（收尾用）

> Point me at a **real user problem** — I'll **push** it **over the line** with the team.

<a id="oral-creative"></a>
### （补充）Creative idea — Smart Factory（电子秤串口 → WebSocket → 网页自动填重）

**Key idea:** 讲串口秤到 WebSocket 的减负思路。

**Script（口语）**  
On **Smart Factory**, workers used a **web** screen to record **fabric weight**. The old loop was **annoying**: put the roll on the **scale**, **read** the number, **type** it into the box — slow, easy to **mistype**, and it **ties up** **hands**.

I checked the **scale** — it could **push** weight over **serial**. On the **Windows** **PC** next to the scale, I shipped a **small** **local** **service**: **listen** to **COM**, normalize the reading, and run a tiny **WebSocket** **server**. The **browser** **page** opened a **WS** **client**, got **stable** **grams**, and **dropped** the value **into** **whatever** **field** had **focus**.

So the operator just **keeps** **weighing** and **swapping** **pieces** — **no** **re-keying**, **fewer** **errors**, **faster** **line**. Same **idea** I like elsewhere: **remove** **dumb** **friction** **between** **physical** **truth** and **software**.

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
- Why do you want to join this company?（**见 [B1-01 口语专页 · 投公司](#oral-b1-01-why-company)** = **Q29** 模板；**业务 + 岗位 JD 对齐备忘](#oral-b1-01-why-company-research)**）

<a id="oral-b1-01"></a>
#### B1-01 口语专页（动机类 · 与 `kb/profile.yaml` 对齐）

<a id="oral-b1-01-sw"></a>
**What are your strengths and weaknesses?**

**提示**：优势 1 + **证据**；劣势 1 + **可改进动作**（忌假弱点「我太完美」）。劣势用 **经理反馈 → ADR / onboarding** 有真实故事（见 [A ⑧ Case A](#oral-08)）。

**Script（约 45–60s）**

> **Strength** — I **ship across layers**. About **ten years** I’ve taken **Android**, **Java** **backends**, and **integration** work from **idea** to **production** — **Enterprise Messaging** at **real** **user** **scale**, **Smart Factory** on the **shop** **floor** with **devices** and **long** **rollouts**. I’m **comfortable** **owning** the **messy** **middle** between **hardware**, **APIs**, and **clients**.
>
> I also **measure before I argue**. On **ChatClothes** I **profiled** the **pipeline**, found the **real** **bottleneck**, and **moved** **work** **local** so the **thesis** **system** **ran** **offline** on **small** **hardware** — that’s how I like to work: **evidence**, then **change** the **design**.
>
> **Weakness** — earlier I **under-wrote** **big** **decisions**. A **manager** called it out: the **next** **hire** would **get** **lost**. Fair. I **fixed** the **habit** with **light** **ADRs** and **short** **onboarding** **notes** — **why** we **picked** **X**, not **novels**. **Reviews** and **ramp-up** got **easier**. I still **push** myself to **write** the **decision** **when** it’s **bigger** than **one** **PR**.

---

<a id="oral-b1-01-why-move"></a>
**Why are you looking for a new opportunity?**（同 **Q32**）

**提示**（已对齐你的说法）：**主因是家庭** — 从 **中国** **迁居** **新西兰**，希望 **重新开始一种生活**；因此 **离开原来的公司**（地理与人生规划，**非绩效或与人闹翻**）。**来纽之后**：**2026-02** 完成 **AUT MCIS** **First Class**（**ChatClothes**）；现求 **Auckland** **稳定全职** 工程岗。**对前职**：仍 **认可原工作与技能积累**，下一份希望 **延续 Android / Java 后端 / 企业与工业交付 / applied AI** 等同一套能力；**不贬原雇主**。**PSWV** 全职权利（与 `kb/profile.yaml` 一致）。

**Script（口语）** → 见 **[Q32](#q-32)** 正文（展开版 + 极简）。

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
- **Describe a disagreement with your manager.** → **口稿**：[Q5](#q-05) · [Q33](#q-33)（分歧处理：约束下选**最合适**方案 + **调研/验证**统一意见；例：**Smart Factory** 分期 + 试点 + 数据）· 语境延展 [A ⑥ 产线 vs 里程碑](#oral-06)
- **Tell me about a time you had to collaborate cross-functionally.** → **口稿**：[Q12](#q-12) · [Q20](#q-20)（接口契约 + 周 demo + 多端对齐）

<a id="b1-03"></a>
### 3) 压力管理与优先级
- **Tell me about a time you worked under pressure.** → **口稿**：[A ⑤ Under pressure](#oral-05)（含 Smart Factory / Enterprise IM / 造币印纸厂）· [Q9](#q-09)
- **How do you prioritize when everything feels urgent?** → **口稿**：[A ⑥ Prioritize](#oral-06)（含多线并行 Case C）· [Q8](#q-08) · [Q36](#q-36)
- **Tell me about a time you had multiple deadlines.** → **口稿**：[A ⑥ Case C 多项目并行](#oral-06) · [Q8](#q-08)
- **Urgent work + long-term projects at the same time（紧急与长线并行）** → **口稿**：[Q40](#q-40)（**产线/用户** 优先 → **非紧急** → **长线**；同日 **时间盒**）
- **Excessive workload / at risk of missing deadline（工作量过大）** → **口稿**：[Q38](#q-38)（**绘本智能柜**：同事离职接手 + **To-C** 与 **柜体主机侧** **拆分** + **早与主管沟通**）；估错类备选 **[Q22](#q-22)**

<a id="b1-04"></a>
### 4) 失败与复盘
- **Tell me about a time you failed.** → **口稿**：[A ④ Failure](#oral-04) · [Q4](#q-04)
- **Tell me about a time you missed a deadline.** → **口稿**：[Q22](#q-22)（同中草药标注故事）
- **Describe a production issue you handled.** → **口稿**：[A ⑤ Case A 产线发布窗 triage](#oral-05) · [创意 · 电子秤](#oral-creative)（设备/网页链路）· 安全向 [A ④ Case C 头像入侵](#oral-04)

<a id="b1-05"></a>
### 5) 复杂问题解决与技术判断
- **Tell me about a complex technical problem you solved.** → **口稿**：[A ② Complex technical](#oral-02)（含 Android OEM 延展）· [oral-enterprise-files](#oral-enterprise-files)（FastDFS）· [Q31](#q-31)
- **Tell me about a difficult decision you made.** → **口稿**：[B1-05 补稿 · Difficult decision](#oral-b1-05-decision) · 可并讲 [A ⑨ Case B 架构演进](#oral-09)（Easemob / FastDFS 等）· [oral-enterprise-files](#oral-enterprise-files)
- **Describe a trade-off you had to make (speed vs quality, etc.).** → **口稿**：[B1-05 补稿 · Trade-off](#oral-b1-05-tradeoff) · [Q34](#q-34)（Smart Factory：**云端抬规格+读写分流**换时间 vs 成本；另：**产线 vs 里程碑**）· [A ② 延展 OEM 矩阵 vs 发版](#oral-02) · [oral-enterprise-files](#oral-enterprise-files)（自建文件 vs 公有云）

<a id="b1-06"></a>
### 6) 主动性与影响力
- **Tell me about a time you took initiative.** → **口稿**：[Q7](#q-07) · [创意 · 电子秤](#oral-creative)
- **Describe a process improvement you drove.** → **口稿**：[A ⑦ Process improvement](#oral-07) · [Q44](#q-44)（含 CI/CD 叙事）
- **Tell me about a time you influenced without authority.** → **口稿**：[B1-06 补稿](#oral-b1-06-influence) · 同源 [Q5](#q-05) / [Q33](#q-33)

<a id="b1-07"></a>
### 7) 反馈与成长
- **Describe a time you received critical feedback.** → **口稿**：[A ⑧ Tough feedback](#oral-08)（Case A 经理 ADR；Case B 原型 + 拍板人）· [Q13](#q-13)
- **Tell me about a time you gave difficult feedback.** → **口稿**：[Q21](#q-21)
- **What did you learn from your biggest mistake?** → **口稿**：[Q4](#q-04) Option A（中草药 pilot）· [A ④](#oral-04)
- **How do you assure code quality in your team?** → **口稿**：[Q43](#q-43)
- **How do you support and track a junior developer's progress?** → **口稿**：[Q45](#q-45)（**Option A** `smart-factory` **6 人**带人；**Option B** **[Q21](#q-21)** 文档反馈 + **[Q13](#q-13)** ADR/onboarding）

<a id="b1-08"></a>
### 8) 适应变化
- **Tell me about a time requirements changed suddenly.** → **口稿**：[A ⑨ Adapted to change](#oral-09)（Case A ChatClothes；Case B Enterprise IM）· [Q23](#q-23)
- **Describe a major change at work and how you adapted.** → **口稿**：[A ⑨](#oral-09) · [Q23](#q-23)
- **Tell me about a time you had to learn a new technology quickly.** → **口稿**：[Q14](#q-14) · [Q25](#q-25)（舒适区外快速学习）· **最近两年 AI 主线**见 **[Q41](#q-41)** · 完全不会的任务见 **[Q39](#q-39)**（GitHub/文档 + **中草药平台** YOLO 基线 → 平台化）
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

> On **enterprise IM**, we had a **real fork**: keep **fighting** our **own** **C++** **message** **servers**, or **move** **personal**, **group**, and **core** **chat** to **Easemob** (**Hyphenate** / **环信**). Staying **in-house** sounded **free**, but **reality** wasn't — **bugs** kept **coming** **back**, and we **never** **felt** **done**. **Switching** meant **vendor** **lock-in** **risk** and **integration** **work** — but it **bought** **stability** and **good** **SDK** **features** (**read** **receipts**, **resend**, **rich** **types**, **multi-platform** **clients**). We also kept **Jiguang** (**JPush**) as a **backup** **push** **lane** for **notification-style** **wake-ups**, **next to** Easemob, not **replacing** the **whole** **story**. Our **own** **team** **focused** **up** the **stack**: **permissions**, **files**, **user** **center**, **workflow** — **platform** **services** on **shared** **infra**. **Lesson**: **don't** **romanticize** **owning** **every** **layer** — **pay** for **maturity** where **commodity** **hurts** you.

<a id="oral-b1-05-tradeoff"></a>
**Describe a trade-off you had to make (speed vs quality, etc.).**

**提示（STAR）**：（T）Android 全矩阵测试 vs 发版节奏；（A）主流守门 + 强信号真机；（R）可发布节奏 + 疑难工单收敛。

**Script（约 45s）**

> **Enterprise IM on Android** — **perfect** **device** **coverage** **vs** **ship** **date** **vs** **money** for **phones**. We **couldn't** **pre-test** **every** **ROM** **setting**. We **chose** **mainstream** **first** (**~Android 7/8** **floor** in our **lab**), **shipped** on **that** **bar**, then **spent** **extra** **only** when a **bug** **report** was **serious** — **buy** a **phone**, **sit** with the **user**, **remote** **session**. **Trade**: **schedule** and **test** **hours** **for** **depth** **on** **the** **exact** **repro** **path** **when** it **mattered** — not **pretending** **full** **matrix** **every** **release**.

<a id="oral-b1-06-influence"></a>
#### B1-06 补稿：Influence without authority

**Tell me about a time you influenced without authority.**

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
**STAR — ChatClothes（Case A）**：中程约束变；重测；LLM 本地化 + 控 scope；honours + 提前节奏。**Reflection：**研究也按工程习惯 instrument。  
**STAR — `enterprise-messaging`（Case B，工作向）**：单机文件 → **FastDFS**；消息 **C++ 自建 → 环信 Easemob 云 + SDK**（单聊/群聊、已读/重发、多类型、多端）；**极光 JPush** = **通知推送备用**；IM **平台化** 子系统；团队扩大 → **飞书/文档/审批预算** + 自动化；个人 **开发 → 全栈 → 协调进度与资源**。**Reflection：**底层不稳就别硬扛——IM 用环信换确定性；到达再用 **JPush** 做通知兜底，别绑死单通道。

---

<a id="b2-10"></a>
### 10) Why should we hire you?

**口语 →** [专页 ⑩](#oral-10)（**30 秒 + 约 1 分钟**两档；末行「精简一句版」可作收尾）  
**STAR 备忘**：久经生产（Android / Java / 集成）；applied AI 能落地；Auckland + full-time；不挑栈、跟团队把事推上线。追问可补 **NDK / Spring / 论文** 等专名。

---

<a id="section-5-scripts"></a>
## Part 3 — Technical Deep Dive Notes

This section keeps the longer scripts and deeper notes. It is still answer material, but it is not the first thing you scan before the interview.

This section keeps the longer Q1–Q45 scripts and deeper notes. It is still part of the answer bank, but it is no longer the first thing you read.
> 与 **[第一部分 · 规则](#section-doc-about)** 一致：**短句、常用词、STAR 心里过**；每题 **一行中文提示（关键词）** + **一版英文**；**Q29–Q45** 已附 **追问 + 短答要点**（**Q1–Q28** 可按同模板自补）。事实只来自 KB。

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
| 3 | 挑战项目 | ChatClothes **或** Smart Factory 电子秤 |
| 4, 22, 38 | 失败 / 延期 / 做不完 | **Q38 主答** **绘本智能柜**（同事离职接手 + **范围拆分** To-C 客户端 vs **柜体主机侧** + **早与主管沟通**）；**Q4/Q22** 仍可用 **中草药标注** → **pilot** |
| 5, 27, 33 | 与上级或团队分歧 | Smart Factory 分期上线 + 数据 |
| 6, 24, 42 | 难合作 / 冲突 | **Q42**：**Option A** Enterprise IM 评审冻结；**Option B** **Delphi vs 团队栈**（地磅/入口称重联动，**口述待入库 facts**） |
| 7 | Above and beyond | ChatClothes 文档与可复现交付 |
| 8, 34, 36, 40 | 优先级 / 多解 | **Q40**：**紧急/影响用户与生产** 优先 → **非紧急** → **长线**；同日 **时间盒**（先救火再迭代）；**Q34/Q36** 见 Smart Factory / 影响×风险 |
| 9 | 压力 | 里程碑 + 可控动作 + 恢复习惯 |
| 10–11 | 工作风格 / 动机 | 证据驱动；真实业务影响 |
| 12, 20 | 团队 / 主导协调 | 接口契约 + 集成 Demo；弱化纯管理 |
| 13, 21 | 收反馈 / 给反馈 | ADR；Junior 文档 + 结对 |
| 14, 25, 41 | 快速学习 / 走出舒适区 / 新学 | **Q41**：**2024–2026 AUT** **LLM** + **agent**（Hermes 等）+ **web coding** + **全链路 profile**（**ChatClothes**）；**Q14/Q25** 扩散/LoRA 舒适区 |
| 15–16 | Agile / Code review | 六年 Sprint；先理解再反驳 |
| 17, 37 | 骄傲成就 | **Smart Factory** 主答 + **Enterprise IM NDK** 备选（见 Q17/Q37） |
| 18–19, 39 | 风险决策 / 不会答 / 全新任务 | 周五部署谨慎；诚实 + 澄清 |
| 23 | 重大变化 | ChatClothes 约束转向 |
| 26 | DEI 产品设计 | 诚实范围 + 可测包容标准 |
| 28, 35 | 持续学习 | 论文式深读 + 小实验 |
| 29–32 | Why company / 转职 | **Q29** Air NZ + [业务/JD](#oral-b1-01-why-company-research)；Hotter 备选需确认公司名；**Q32** **主因家庭**（**中国→纽**、新生活）→ **离原公司**；**MCIS 2026-02** + **稳定全职** + **延续技能**（[oral-b1-01-why-move](#oral-b1-01-why-move)） |
| 30 | 模糊需求 / 系统设计 | 澄清指标 + 轻量原型 |
| 31 | 最大技术挑战 | ChatClothes 延迟剖解 |
| 43 | 代码质量 | **Option A** Smart Factory：**防/抓/救** + 周 **demo** + **GitLab+Jenkins**；可叠 **静态扫描/MR 结对互审/大版本 spot-check/规范手册（如阿里 Java）/Spring 约定**。**Option B** **`enterprise-messaging`**：发版纪律、**C++→环信**、早期缺陷节奏（见 `facts.yaml`）；托管工具链若口试展开见 Q43「口述层」 |
| 44 | 团队工作流 | **Option A** Smart Factory：**双周 Sprint** + **接口契约** + **周 demo** + **GitLab/Jenkins** 试点推广（[A ⑦](#oral-07)）。**Option B** **`enterprise-messaging`**：平台化演进节奏 + **飞书/文档/审批/预算** + **渐进自动化**；早期 **数周原型→上线救火** 与 **产品/设计对用户透明**（见 `facts.yaml` / [A ⑨ Case B](#oral-09)） |
| 45 | 辅导 Junior | **Option A**：**晨站会+任务板**、阻塞早求助、**给思路不自代写**、**盯 MR/提交**；**定期技术分享**（新工具/问题/优劣）；**30/60/90** + **周 demo** + `smart-factory` **6 人 mentor**。**Option B**：**Q21+Q13** 文档/ADR |

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
**提示（STAR）**：**主**：**Enterprise Messaging**（与 **[Q42 Option A](#q-42)** 同源）；**1:1** + **私下** review + **结对**。**备选**：**技术栈/可维护性分歧** → **[Q42 Option B](#q-42)**。
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
**提示（STAR）**：经理要 **手写架构决策**；（A）**ADR** + **onboarding**；（R）新人更快。**与 [Q45 Option B](#q-45)** 同源扩展。
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
**提示（STAR）**：**主答** **`smart-factory`**（与 `projects/smart-factory/facts.yaml` 一致）：**多年**、**10+ 工厂**、**Vue** 门户 + **Java/Spring** 微服务 + **Android** 车间端 + **Windows** 服务（串口/秤/现场）；**IoT** 与产线结合；**~30%** 产效提升等可量化结果；**深入车间**、与 **工人/客户/产品** 协同；**带领约 6 人** 跨职能交付与发版节奏。**备用（偏纯技术深度）**：**Enterprise Messaging** **NDK**（**sub-200ms**、**~5k DAU**、**10+ 年**生产）。

**Script（口语）** — **主：Smart Factory（约 45–55s）**

> **Smart Factory** — I'm **genuinely** **proud** of that **program**. It **ran** **years**, **10+** **sites**, **real** **hardware** on the **floor** — **RFID**, **scales**, **conveyors** — not **slides**. **Vue** **portals**, **Java** **microservices**, **Android** **for** **workers**, **Windows** **services** where **the** **PC** **was** the **edge**. We **moved** **efficiency** **a** **lot** (**~30%** in the **program** **metrics** I **stand** **behind**) and **kept** **uptime** **high** in **messy** **factory** **conditions**.
>
> I **didn't** **start** **knowing** **every** **layer** — the **project** **forced** me to **learn** **while** **shipping**. I **spent** **serious** **time** **with** **operators** and **customers**, not **only** **tickets**, and I **helped** **drive** **day-to-day** **planning** and **task** **breakdown** for a **small** **cross-functional** **team** (**~6** **people**). **Software** **people** **use** **every** **shift** — that's the **bar** I **like**.

**Script（口语）** — **备用：Enterprise Messaging NDK（约 20–25s）**

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
**提示（STAR）**：Junior **文档**薄；（A）先夸 + **具体**标准 + **结对**；（R）评审顺了。**持续机制**可并讲 **[Q45 Option B](#q-45)**。
**Script（口语）**
> Juniors — code OK, **docs** weak. I started with **what worked**, then **clear cost** for the next person. Gave a **small template**, **paired** once. Over time **reviews** got easier.

<a id="q-22"></a>
### 22) Tell me about a time when you missed a deadline. What happened, and how did you handle it?
**提示（STAR）**：同 **Q4** 中草药标注；**早沟通** + **pilot**。
**Script（口语）**
> **Herbal CV** — labels took **~six weeks**, not **two**. I **owned** it, **reset** dates, **piloted** throughput. **Honest early** beats **silent slip**.

<a id="q-23"></a>
### 23) Tell me about a time when you had to deal with a significant change at work. How did you adapt to this change?
**提示（STAR）**：**Option A** **ChatClothes** 约束变；（A）**重测** + **LLM** 本地 + 控范围；（R）全链路可跑。**Option B** **`enterprise-messaging`**：**产品演进**（独立 IM → 用户中心/类 SSO → 文件中心 → 子系统平台；对标 **七牛式拖拽/分片直传**、**阿里云 OSS**、**飞书**组织权限，见 `facts.yaml`）；文件单机→**FastDFS**；消息 **C++ 自建不稳 → 环信 Easemob 云 + 多端 SDK**；**极光 JPush** 作**通知推送备用**；组织上飞书/审批/自动化；职责扩展（见 [A ⑨ Case B](#oral-09)）。
**Script（口语）**
> **ChatClothes** — **offline** + **speed** became hard rules. I **re-measured**, moved **LLM** **local**, **cut** scope where needed, **shipped** a full **pipeline** that fit the box.
> **Enterprise IM** — the **product** **shape** **evolved**, not only the **infra**. We **started** as **standalone** **chat**, **pulled** a **user** **center** from **IM** **identity** for **SSO-style** **logins**, **grew** a **central** **file** **hub** for **attachments** **and** **business** **docs**, **then** **subsystems** — **attendance**, **engineering** **tools**, **finance** **approvals**, **hardware** **management**, **permissions** — **reused** the **same** **primitives**. We **studied** **public** **patterns**: **Qiniu**-style **drag-upload**/**multipart** **flows**, **Aliyun** **OSS-style** **object** **storage** **thinking**, **Feishu**/**Lark**-style **org** **permissions** — **then** **self-hosted** **what** **data** **sovereignty** **required**.
> **Under** the **hood**, **files** outgrew **one server** → **FastDFS** we could **operate** and **tune**. **Messaging** was **worse** in a different way: **C++** **in-house** **servers** kept **breaking** — **bugs** **never** **felt** **finished**. We **moved** **personal**, **group**, and **core** **infra** to **Easemob** (**Hyphenate** / **环信**) — **stable** **cloud** **backbone** and **multi-platform** **SDKs**, **nice** **wrappers** for **groups**, **rich** **message** **types**, **read** **state**, **resend**. We kept **Jiguang** (**JPush**) as a **backup push** lane for **notifications** and **wake-ups** — **not** the **main** **chat** **pipe**, but a **second** **path** when Android got **mean** about background. Our **own** **code** focused on **business** **platform** **services** for **subsystems**. As the **team** grew, **Feishu** (**Lark**), **docs**, **approvals**, and **automation** caught the process side. My job widened from **coding one lane** to **full-stack** delivery and **owning** **schedule** and **who gets focus** when **parallel** projects compete.

<a id="q-24"></a>
### 24) Describe a time when there was a conflict within your team. How did you help resolve it? Did you do anything to prevent it in the future?
**提示（STAR）**：同 **Q6**：**主** **Enterprise Messaging**（**[Q42](#q-42) Option A**）；**备选** **技术栈协作**（**Option B**）。**处理**：**私下** + **具体** + **预防**：反馈方式。
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
**提示（STAR）**：**主练** **[Air New Zealand](#oral-b1-01-why-company)**（管理理念 + 真产品影响 + Smart Factory / smart-power / enterprise messaging 证据）；**投前**做 **[业务 + JD 对齐](#oral-b1-01-why-company-research)**。备选公司名 **Hotter** 见同锚点「备选」段（**请确认正式英文公司名**后替换）。其他雇主仍可用模板方括号。
**Script（口语）** — **Air New Zealand**
> I'm interested in **Air New Zealand** because it's **real** **customer-facing** **product** work at **scale** — **travelers** **feel** every **rough** **edge**, and **operations** **has** to be **boringly** **reliable**. I also want a **team** **culture** that **trusts** engineers — **clear** **ownership**, **less** **micromanagement**, **adult** **defaults**.
>
> I've already shipped that **kind** of **impact** in other domains: **Smart Factory** — we **helped** **plants** **run** **faster** with **less** **manual** **pain** on the **floor**; **smart-power** — **live** **energy** **data** and **sub-second** **alarms** so **people** **see** the **benefit**; **enterprise messaging** — **mobile** + **backend** at **thousands** of **DAU**. I want to **bring** the **same** **evidence-driven** **habits** to **Air** **New** **Zealand** — **quality** **software** **millions** of **people** **touch**.
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
**提示（STAR）**（已对齐你的表述）：**业务与流程优先** — 需求与 **端到端业务流程**（行业/公司/客户、**要解决什么**、**通过哪些实现路径** 可选方案与取舍）。**方案可视化与用户对齐** — **原型图 / 线框** 与 **用户确认流程与界面**，把不确定性在写死代码前消掉。**再转交付计划** — 拆成 **开发任务与接口**、**开发周期**、**成本与依赖**（人天、第三方、基础设施）。**资源与选型**：服务器/部署、第三方、数据库、通知、Web/App、分析可观测。**进入开发后**：列清 **项目里程碑**、标出 **关键关口 / 技术或业务难关**（依赖、集成、性能、合规等），排期里 **预留足够测试与回归** 窗口。**新 / 陌生领域**：不凭想象定稿，**快速原型 + 用户确认** 压不确定性（见 **A ⑥ Case B**）。**已熟悉领域**：可 **复用成熟模式与做法**，加快收敛、控成本。**断网/保密现场**：进场节拍、审批提前量、离线部署/升级（见 **A ⑤ Case C**）。**与 AI（一句）**：工具加速实现，竞争力仍在 **业务界定与可验证结果** — 口试用 **Smart Factory / smart-power / enterprise messaging** 举例更稳。

**Script（口语）** — **展开版（约 75–95s）**

> I start from the **business problem** and the **real workflow** — **who** the **customer** is, what **pain** we're removing, and **which solution paths** are realistic. **Implementation** is faster than before with **better tools**, but I still **design** from **process** first, not from **code** first.
>
> Before we **lock** scope, I like **wireframes** or a **quick prototype** and **walk users through** **flows** and **UI** — that removes **guesswork** early. Then I translate what we agreed into **engineering** language — **components**, **interfaces**, **milestones**, **timeline**, and **cost** (**people**, **infra**, **third parties**).
>
> In **build**, I keep **milestones** explicit and flag **risky gates** early — **integrations**, **performance**, **compliance**, **data** **ownership**. I **always** **buffer** for **testing** and **regression**; **shipping** without **time** for that is a **false** **economy**. For **new** **domains**, I rely on **fast** **prototypes** and **user** **sign-off**; in **areas** I **already** **know**, I'll **reuse** **proven** **patterns** so we **don't** **re-learn** the same **traps**.
>
> I **size** **compute**, **databases**, **third-party** services, **notifications**, **web** vs **app**, and **observability** so we can **prove** impact. When it's still **fuzzy**, I **spike** **risky** branches and **validate** **on** the **floor** or with **real** **users** — **document** big calls, then **iterate** with **numbers**.

**Script（极简 backup · ~30–35s）**

> I **ask** until **goals** and **constraints** are clear — put **unknowns** on the table. **Wireframe** or **prototype** **flows** with **users** when it's **new**; **reuse** **patterns** when I **already** **know** the **domain**. Sketch **architecture** and **interfaces**, **spike** if two paths are fuzzy. **Milestones** with **time** for **test** and **regression**. **Document** big calls, **iterate** with **feedback** and **numbers**. When it's still **fuzzy**, I **go to the floor**, **prototype fast**, and **tighten** from **what they actually do**.

**追问**
- **Give a concrete example.** → **Smart Factory** 下车间 + 分期试点；或 **断网厂区** 见 **A ⑤ Case C**。
- **How do you document decisions?** → **ADR / 一页架构** + 里程碑；大分叉 **spike** 再写结论。
- **What if stakeholders disagree after prototype?** → 回到 **约束与数据**；必要时 **试点范围** 缩小再量。

**短答英文**
> I **prototype** **early** on **fuzzy** **flows**, **write** **light** **ADRs** for **big** **forks**, and **resize** **scope** when **data** says we're **wrong**.

<a id="q-31"></a>
### 31) What is the biggest technical challenge you have worked on?
**提示（STAR）**：**Option A** **ChatClothes** **端到端延迟** + 离线；（A）**profile** → **LLM** 本地 + **YOLO12n-LC**；（R）可演示 + **早交论文**。**Option B** **`enterprise-messaging`**：**Android** **OEM/版本**碎片化、难复现、测试矩阵 vs 周期（见 [A ② 延展](#oral-02)）。**Option C** **`enterprise-messaging`**：**FastDFS** 自建分布式文件 — 聊天与业务文档体积、**私密性**、子系统统一接入、备份与权限（见 [oral-enterprise-files](#oral-enterprise-files)）。
**Script（口语）**
> **ChatClothes** — make the **whole** path **fast** on **small** hardware **offline**. I thought **diffusion** was the problem — **profiling** showed **LLM** **cloud** trips were. I went **local LLM**, lighter **vision** (**YOLO12n-LC**). **System worked**; thesis **handed in early**.
> Another big one was **enterprise IM on Android** — not one Android, thousands of real phones. **Xiaomi / Huawei / OPPO** ROMs bend the rules again. A lot of bugs only showed up in **real user settings**, and we couldn't pre-find every small issue without blowing **schedule**, **test cost**, and **device** budget. We tested mainstream versions (**~7/8 floor** in lab), then closed hard tickets on **real hardware** — sometimes **buying** a phone, sometimes **sitting** with the user. Full matrix every release wasn't affordable; we **traded** **depth** for **ship date** and **paid** for the **exact** repro path when it **mattered**.
> A third challenge was **file volume** at scale. **Chat attachments** and business modules like **contracts** and **drawings** outgrew **one server**. For **privacy / control**, we didn't default to **public cloud file SaaS**. We used **self-hosted** **FastDFS** for **distributed** storage, wired it into multiple subsystems, and had to own **sharding**, **redundancy**, **backup**, and **access control** — not just "upload works".

**追问**
- **Biggest mistake in that project?** → 可转 **Q4** 发版配置 / 头像安全；或 **剖分错了先优化 diffusion**。
- **How measured latency / DAU?** → **profiling**、日志与现场计时；DAU 来自 **运营侧指标**（与 facts 一致，勿编新数）。
- **Why not buy cloud IM earlier?** → **成本/可控/当时能力**，后迁 **Easemob** 换稳定性（**Q23**）。

**短答英文**
> I **measured** **first** — **profiling** beat **guessing**; for **scale** we **traded** **vendor** **risk** vs **self-hosting** **control** **explicitly**.

<a id="q-32"></a>
### 32) Why do you want to change your current company?
**提示（STAR）**（与 `kb/profile.yaml` 一致，并含你的叙事）：**首要原因：家庭** — 从 **中国** **迁至** **新西兰**，希望 **重新开始生活**；因此 **离开原公司**（**地理与家庭决策**，**非** 绩效或关系问题）。**来纽后**：**AUT MCIS** **2026-02** **First Class**，**ChatClothes**；现居 **Auckland**，求 **稳定全职** 工程交付。**对前职**：**仍很认可** 原工作与技能；下一份希望 **同一套栈**（**Android / backend / 企业与工业场景 / applied AI**）。**PSWV**。**口试边界**：简短、事实导向；**不贬** 原居地或原雇主。

**Script（口语）** — **展开版（约 55–70s）**

> **Honestly**, the **main** **reason** is **family**. My **family** and I **relocated** from **China** to **New Zealand** — we wanted a **fresh** **start** **here** and to **build** **life** in **Auckland**. That **move** naturally meant **leaving** my **previous** **company**; it was **life** **planning** first, **not** a **performance** **story** and **not** **drama** with people.
>
> **Since** **arriving**, I **finished** my **Master's** (**MCIS**) at **Auckland University of Technology** in **Feb 2026**, **First Class Honours** — **ChatClothes** is my main **applied** **AI** piece.
>
> I **really** **valued** my **past** **engineering** **work** — **Android**, **Java** **backends**, **enterprise** and **factory** **systems**. Now I'm **looking** for a **stable**, **full-time** **role** in **NZ** where I can **keep** **shipping** with the **same** **skills** — **Android** / **backend** / **applied** **AI** — with **clear** **full-time** **rights** (**PSWV**).

**Script（极简 backup · ~30–38s）**

> **Main** **reason** is **family** — we **moved** from **China** to **New Zealand** for a **new** **start**, so I **left** my **previous** **company** for **relocation**, **not** **performance**. I **finished** **MCIS** at **AUT** in **Feb 2026**, **First Class** — **ChatClothes**. I **liked** my **old** **engineering** **work** and want a **stable** **full-time** **job** **here** — **Android**, **backend**, **applied** **AI** — **PSWV**.

**追问**
- **Why this role / why leave last employer?** → 主叙事：**学业阶段结束 + 留纽家庭**；**非** 与老板不和。
- **Any gap on resume?** → **AUT** 全职读书；**ChatClothes** 为成果。
- **Salary / start date?** → **诚实** + **flexible**；工作权利 **PSWV**。

**短答英文**
> **Relocation** for **family**, **finished** **MCIS** in **NZ**, now I'm **ready** for **full-time** **engineering** again — **not** a **performance** **exit**.

<a id="q-33"></a>
### 33) Tell me about a time when you had a different opinion than the rest of the team. How did you handle it?
**提示（STAR）**（已对齐你的表述）：**分歧正常** — 各人 **经历 / 技术栈** 不同，对同一问题会有 **不同观点**。先对齐 **限制条件**：**预算**、**时间**、**风险**、**现场/运维** 承受度；列出 **在当前约束下允许的方案集**；目标不一定是纸面上「最优」，而是 **最合适、可交付** 的选项。若 **技术路线或架构** 仍有硬分歧 → **分别调研 / spike / 小范围验证**，用 **证据** 收敛意见、再拍板。**例证** 同 **[Q5](#q-05)**：**Smart Factory** — 先稳核心 **分期** + **试点** + **数据**，团队与用户对齐。

**Script（口语）** — **展开版（约 55–70s）**

> When people **disagree**, I **assume** it's **honest** — **different** **backgrounds**, **different** **stacks**, **different** **risk** **appetite**. I **don't** **start** with **"I'm right"**; I **surface** **constraints** first — **timeline**, **budget**, **who** **maintains** it, **what** **production** **can** **tolerate** — then **list** **realistic** **options** that **fit** **inside** those **rails**.
>
> I'm **not** **religious** about the **"best"** **design** on **paper**. I want the **most** **suitable** **choice** we can **actually** **ship** and **support**. When it's a **real** **fork** — **two** **technical** **paths** — I **prefer** **parallel** **spikes** or **small** **proofs** so we **decide** with **evidence**, **not** **opinions** **alone**.
>
> **Concrete** example — **Smart Factory**: I wanted a **small**, **stable** **first** **launch**; others wanted **more** **features** **breadth**. I argued **trust** on the **floor** beats **half-broken** **scope**. We used **data**, **phased** **rollout**, **pilots**. The **team** **aligned**; **users** **guided** what came **next**.

**Script（极简 backup · ~25–30s）**

> I **align** on **constraints** — **time**, **budget**, **ops** **risk** — then pick the **most** **suitable** **option**, not always the **"best"** **on** **paper**. If it's a **technical** **fork**, I **spike** and **compare** with **evidence**. **Smart Factory** — I pushed **stable** **core** **first**; **phased** **pilots** and **data** **settled** it.

**追问**
- **Were you ever wrong?** → 可承认试点后 **用户要的功能** 与最初假设不同 → **跟数据改计划**。
- **How handle strong personalities?** → 对事不对人；**书面**对齐目标。
- **What if manager overrides you?** → **执行** + **记录风险**；或转 **Q5** 经理分歧叙事。

**短答英文**
> I **disagree** with **data**, **not** **volume** — **pilots** **turn** **opinions** into **facts**.

<a id="q-34"></a>
### 34) Tell me about a time when you were faced with a problem that had a number of possible solutions. What was the problem and how did you determine the course of action? What was the outcome of that choice?
**提示（STAR）**（与 `projects/smart-factory/facts.yaml` 对齐）：**两难**：**MySQL** 随业务膨胀（**任务表**日增约 **十万级**、约 **半年**达 **百万级** 量级），大量 **JOIN 任务表** 的门户/界面查询变慢 → **影响现场生产使用**；若 **停下来做深度优化** → **拖新功能**、也 **打断交付节奏**；若 **硬扛不处理** → **用户不满**持续。**可选路径**：硬停开发做根治；或 **阶段性抬容量** 换时间。**取舍**：**先将数据库迁到云端托管 MySQL**，**提高规格/资源** + **主从/只读副本** 等 **读写分流** 缓解读压力；**先保在研功能上线**，再在后续窗口做 **慢查询与索引/结构** 根治；优化落地后 **回迁本地** 降 **持续运营成本**（云端阶段 **费用上升** 为明确 **交换**）。**简例（另一情境）**：**产线紧急** vs **里程碑** → **影响×风险** 排序（见 [A ⑥](#oral-06)）。

**Script（口语）** — **展开版（约 65–80s）**

> **Smart Factory** — **production** **MySQL** **grew** **fast**. We had a **high-churn** **task** **table** — **roughly** **~100k+** **new** **rows** **per** **day**, **millions** **within** **about** **half** **a** **year** — and **many** **portal** **queries** **joined** it. **Screens** got **slow** enough to **hurt** **shop-floor** **work**, not just **annoyance**.
>
> There were **several** **ways** to **react**. **Pause** **feature** **work** and **do** a **big** **rewrite** **now** — **risky** for **delivery** and **still** **noisy** for **users**. **Ignore** it — **bad** for **trust**. **Buy** **time** with **capacity** **instead** of **pretending** we could **optimize** **everything** **overnight**.
>
> We **chose** a **time-boxed** **mitigation**: **move** the **database** **workload** to **cloud-hosted** **MySQL**, **scale** **hardware**/**provisioned** **capacity**, and **split** **read** **traffic** (**primary** **plus** **read** **replicas** / **read** **routing**) so **heavy** **list**/**detail** **queries** **stopped** **blocking** **the** **floor**. **Cost** **went** **up** — **that** was the **explicit** **trade**. **Then** we **finished** the **in-flight** **features**, **scheduled** **real** **slow-query** and **index**/**schema** **work**, and **planned** **repatriation** **on-prem** **after** **optimizations** **landed** to **bring** **hosting** **cost** **back** **down**.

**Script（极简 backup · ~22s）** — **产线 vs 里程碑**

> **Smart Factory** — **live** issues vs **feature** deadlines. I ranked by **risk** and **impact** — **fix production** first, then **milestone** work. **Told** people when order **shifted**. **Uptime** held; roadmap **moved**.

**追问**
- **Exact metrics after cloud migration?** → 诚实：**响应/现场感受**改善为先；**根治**在后续慢查询窗口（**勿编**未在 facts 写的百分比）。
- **Who paid for cloud cost?** → **业务/项目**共同决策；**成本上升**是已说清的 **trade**。
- **Alternative you rejected?** → 硬停开发做重写 vs 完全不动 — 说明为何不可行。

**短答英文**
> We **bought** **time** with **capacity**, **then** **scheduled** **real** **SQL** **work** — **cost** **went** **up** **on** **purpose**, **not** **by** **surprise**.

<a id="q-35"></a>
### 35) What do you do to enhance your technical knowledge apart from your project work?
**提示（STAR）**（已对齐你的说法）：**业余习惯**见 **[Q41](#q-41)** 的「**最近两年主线**」；本节侧重 **社区 + 小项目/开源** 与 **Android** 跟进。仍保留 **读 → 小原型 → 短笔记**；口试避免与 Q41 **完全重复念同一段**，可 **Q35 一句带过** + **深挖交给 Q41**。

**Script（口语）** — **展开版（约 45–55s）**

> Outside **paid** **work**, I **follow** **communities** and **what's** **actually** **shipping** — **release** **notes**, **good** **blogs**, **forums** when a **topic** **matters** to me. I **learn** **fastest** when it's **personal** **interest**, so I **build** **small** **side** **projects** and **sometimes** **help** **open-source** when I can — **issues**, **small** **fixes**, **docs** — not **hero** **claims**, just **steady** **habits**.
>
> **Recently** I've been **deep** in **AI** **tooling** — **LLM** **agents**, **web**/**coding** **workflows**, and **model** **ecosystems** **like** **Hermes** — basically **anything** that **raises** **my** **own** **engineering** **leverage**. I still **track** **platform** **churn** too — **Android** **keeps** **moving**, and **I** **don't** want to **wake** **up** **surprised**.
>
> Same **pattern** as **thesis**: **read**, **try** a **tiny** **proof**, **write** **short** **notes** on what **worked** so it **sticks**.

**Script（极简 backup · ~22–28s）**

> I **follow** **communities** and **news**, then **build** **small** **toys** for **things** I **care** about — **lately** **AI** **agents**, **LLM** **coding** **workflows**, **Hermes**-style **models** — plus **Android** **platform** **updates**. **Read**, **mini** **demo**, **short** **notes** — same **habit** as **ChatClothes**.

**追问**
- **Name one repo or paper you read last month.** → 准备 **1 个真名**（Hermes 发行版 / 某 Agent 框架 / Android release note 皆可）。
- **How do you avoid tutorial hell?** → **小交付** + **记笔记** + 与 **项目**挂钩。
- **Company time vs personal time?** → **边界**：业余自学；**不泄露**上家机密。

**短答英文**
> I **stop** at **tiny** **shippable** **proofs** — **notes** what **worked**, **link** it to **real** **bugs** or **features** next week.

<a id="q-36"></a>
### 36) How do you prioritize your workload? What do you do when your work feels like it's just too much to get done?
**提示（STAR）**（已对齐你的表述）：**排序依据**：项目 **紧迫度** + 任务 **预估耗时** + **依赖/风险**（难点、不确定性高的往前排，预留 **攻关时间**，避免后期卡死整条链路）。**需他人协作** 的（接口、联调、评审依赖）→ **尽量提前启动**，避免 **挡同事进度**。**扛不住时**：若已威胁 **里程碑**，**尽早**在团队内 **申请加人 / 借调 / 任务分担**（你们习惯 **人员借用、临时支援**），**不把风险闷在自己手里**；若仍 **不可行**，与 **产品/客户** **透明沟通** **延期或砍范围** — **由团队共同承担**，而非个人硬扛。**小团队语境**：你也会 **帮别人分担**，因此 **前后端都能上手**（更广 **技术栈** / T 型能力）。仍可与 **影响×风险**、**切块**、**早沟通** 并用；多线并行见 [A ⑥ Case C](#oral-06)。

**Script（口语）** — **展开版（约 55–70s）**

> I **prioritize** by **urgency**, **how** **long** **work** **really** **takes**, and **who** **depends** on **me**. **Hard** **unknowns** **go** **earlier** — I **budget** **real** **time** to **break** **through**, not **hide** them **behind** **easy** **tasks** **until** the **end** **of** the **sprint**.
>
> If **someone** **else** **needs** my **output** to **move**, I **start** **that** **thread** **early** so I **don't** **become** the **bottleneck**.
>
> When it's **still** **too** **much** for **one** **person** and a **milestone** **is** **at** **risk**, I **escalate** **inside** the **team** **first** — **borrow** **capacity**, **split** **work**, **temporary** **help** — that's **normal** in **my** **experience**, and I **return** the **favor** when **others** **need** **cover**. If **reality** **still** **won't** **fit**, I **surface** it **early** to **PM**/**customer** — **date** or **scope** **has** to **move** **together**, **not** as a **solo** **secret**.
>
> **Small** **teams** **forced** me to **stretch** **across** **frontend** and **backend** — **that's** **how** I **keep** **delivery** **moving** when **queues** **collide**.

**Script（极简 backup · ~28–35s）**

> **Urgency**, **effort**, **dependencies** — **hard** **stuff** **first**, **collaboration** **threads** **early** so I **don't** **block** **people**. If a **milestone** **is** **at** **risk**, I **ask** for **help** **inside** the **team** **early**; if it **still** **won't** **fit**, I **raise** **scope**/**date** with **PM**/**customer** — **team** **owns** the **plan**, **not** **heroics**. **Small** **team** **habit**: I **cover** **frontend** **and** **backend** when **needed**.

**追问**
- **Example when escalation failed?** → 诚实：**仍有一次延期** → 转 **Q22** 或 **早沟通** 教训；或说最终 **砍范围**。
- **How say no to extra work?** → **用优先级表** + **问替换哪一项**。
- **Remote vs onsite priority?** → **依赖现场证据的优先现场**。

**短答英文**
> I **escalate** **with** **options** — **trade** **scope**, **date**, or **people**; **no** **silent** **overload**.

<a id="q-37"></a>
### 37) What’s the Number One Accomplishment You’re Most Proud Of?
**提示（STAR）**（与 `projects/smart-factory/facts.yaml` 对齐，已含你的叙事）：**Smart Factory** — **周期长**（**2018–2024**）、**栈广**：**Vue.js** 门户/管理端、**Java/Spring** 微服务、**Android** 车间应用、**Windows** 服务（串口秤、现场桥接等）、**IoT**（RFID、传送等）；**全程深度参与**产线与交付；**量化**：**10+** 工厂、**~30%** 产效提升、多年 **高可用**；**业务价值**：**传统工厂数字化**、软件 **每日被工人使用**。**成长**：多栈 **边学边交付**；与 **客户/产品/一线工人** 沟通；在 **约 6 人** 跨职能团队里 **推动计划与 sprint 执行、任务拆解与节奏**（事实表述为 **lead planning / sprint execution**，口试勿夸大成「公司级 PM 全权」）。**备用短答**（面试官只要「一个硬核点」）：**Enterprise Messaging NDK** — **sub-200ms**、**~5k DAU**、**10+ 年**生产（同 **[Q17](#q-17)** 备用段）。

**Script（口语）** — **主：Smart Factory（约 70–85s）**

> The **accomplishment** I'm **most** **proud** of is **Smart Factory** — not because it was **flashy**, but because it was **long**, **hard**, and **real**.
>
> It **spanned** **years** across **10+** **manufacturing** **sites**. The **stack** was **wide** — **Vue** **portals**, **Java** **Spring** **microservices**, **Android** on the **shop** **floor**, **Windows** **services** for **serial** **devices** and **local** **bridges**, plus **IoT** — **RFID**, **scales**, **conveyors**. A lot of that I **didn't** **already** **know** **day** **one**; I **learned** **while** **shipping** because the **project** **needed** it.
>
> What **hits** me **daily** is **impact** — **operators** **actually** **run** the **apps** **every** **shift**. We **moved** **efficiency** **materially** (**~30%** in the **program** **metrics** I **stand** **behind**) and **kept** **uptime** **high** in **rough** **factory** **conditions**. That's **digital** **transformation** with **evidence**, not **slides**.
>
> I also **grew** as a **delivery** **lead** on the **engineering** **side** — **planning**, **sprints**, **breaking** **work** **down**, **coordinating** with **customers**, **product**, and **people** on the **line**. **Small** **team** — you **can't** **hide** in **one** **role**.
>
> If you want a **second** **pure** **systems** **win**, **Enterprise Messaging** **NDK** is **special** too — **sub-200ms**, **~5k DAU**, **10+ years** in **prod** — but **Smart Factory** is my **number** **one** because of **breadth**, **years**, and **humans** **depending** on it.

**Script（极简 backup · ~35–42s）**

> **Smart Factory** — **years**, **10+** **sites**, **Vue** + **Java** + **Android** + **Windows** **IoT** **edges**. **Learned** **layers** **as** **we** **needed** them; **deep** **time** **with** **workers** and **customers**. **~30%** **efficiency** **gain**, **high** **uptime** in **factories**. I **helped** **run** **engineering** **cadence** for a **small** **team** — **proud** because **people** **use** it **every** **day**. **Runner-up**: **Enterprise Messaging** **NDK** — **sub-200ms**, **long** **prod** **life**.

**追问**
- **What was *your* biggest mistake on that program?** → 可接 **分期/估时** 或 **Q34** 数据库权衡；**勿空**。
- **How prove 30%?** → **项目侧指标/客户现场反馈**（与 facts 表述一致，**不夸大**到未写明的审计口径）。
- **Why not pick NDK story as #1?** → **人每天用** + **栈跨度** + **行业现场** 对你更有意义。

**短答英文**
> I **pick** **Smart Factory** **first** because **breadth** plus **daily** **operators** — **metrics** and **uptime** **stories** **match** **facts** **I** **can** **defend**.

<a id="q-38"></a>
### 38) Tell me about a time when you had an excessive amount of work and you knew you could not meet the deadline. How did you manage then?
**提示（STAR）**（与 `projects/picture-book-locker/facts.yaml` 对齐，已含你的叙事）：**绘本智能柜（Picture Book Locker）** — 同事 **离职**，其 **遗留代码维护 + 新功能 + 你自有项目** 叠加，**单人无法按期完成全部**。**行动**：**尽早**与 **主管/团队** 说明风险 — **不把 deadline 风险闷在自己身上**；**范围拆分**：将偏 **To-C** 的 **借还书客户端 Android** 分给 **另一位同事**，你保留 **柜体主机侧**（**柜端 Android**、**锁/传感器/现场控制** 等）开发与维护；**两人协同**完成交接，**保障里程碑**。**原则**：**项目优先**、**团队整体效率**；他人有余力时分担，他人困难时你也支援。**备选故事**（若对方要「估错工期」类）：**Q4/Q22** **中草药标注** — **早沟通** + **pilot** + 重排期。

**Script（口语）** — **展开版（约 65–80s）**

> On **Picture Book Locker** — **smart** **library** **cabinets** for **schools** — a **teammate** **left** and I **inherited** **their** **work** **on** **top** of **mine**. Suddenly I had **legacy** **bugs**, **new** **features**, **and** my **own** **queues** — **honestly**, **one** **person** **couldn't** **keep** **all** **dates** **green** **without** **lying** to **myself**.
>
> I **didn't** **try** to **be** a **hero**. I **went** to my **lead** **early**, **explained** the **math**, and we **re-balanced** **scope**. We **split** **the** **Android** **surface** **area**: **borrower-facing** **To-C** **client** **work** **went** to **another** **engineer** who **had** **capacity**, and I **kept** the **cabinet-side** **host** **stack** — **locks**, **sensors**, **hardware** **integration** — where **I** **already** **had** **the** **deepest** **context**.
>
> That **wasn't** **embarrassing** — it was **adult** **delivery**. **Projects** **win** when **the** **team** **routes** **load** **before** **the** **milestone** **burns**. I **also** **cover** **others** when **I'm** **light** — **same** **rule** **both** **ways**.

**Script（极简 backup · ~28–35s）**

> **Picture Book Locker** — **teammate** **quit**, I **inherited** **too** **much** **plus** my **own** **work**. I **told** my **manager** **early**, we **split** **To-C** **Android** to **someone** **else**, I **kept** **cabinet**/**host** **Android**. **Team** **owns** the **date**, **not** **solo** **heroics**.

**Script（口语）** — **备选：中草药标注（与 Q4/Q22 同源 · ~20s）**

> **Herbal** labels — timeline **wasn't real**. I **owned** it, **new** schedule, **pilot** to know **speed** and **error rate**. **Cleaner** data, **better** next estimate.

**追问**
- **Did the handover delay the release?** → **透明排期** + **并行交接**；若 **仍滑点** 转 **Q22** 诚实版。
- **How split work without blame?** → **按模块与上下文** 谁最熟；**对事**。
- **What if colleague also overloaded?** → **升级** 主管、**砍范围** 或 **阶段交付**（与 **Q36** 一致）。

**短答英文**
> We **re-balanced** **early** — **split** **Android** **surfaces** by **who** **knew** **the** **hardware** **path** **best**, **not** **politics**.

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
**提示（STAR）**（已对齐你的表述，例：**Smart Factory**）：**优先级** — 先 **紧急且影响用户/生产现场真实使用** 的问题（直接牵动 **生产环境**），再处理 **非紧急**，再挤 **长线/路线图**；目标仍是 **两条线都不明显拖垮交付**。**同一天必须并行时**：**时间盒** — 先集中清 **紧急队列**，再用 **剩余时间** 做 **非紧急**，最后用 **碎片/剩余深度时间** 推进 **long-term**（或拆成 **小步** 以免长期项永远为零）。**认知**：长线问题有时 **无法当场根治**，需要 **持续** 尝试新方案 — 口试里用 **一句** 承认即可，主证据仍放在 **你如何保产线 + 仍推进里程碑**。**延展**：[A ⑥](#oral-06) 产线 vs 路线图。

**Script（口语）** — **展开版（约 55–70s）**

> **Smart Factory** was **always** **two** **queues** at **once** — **hot** **production** **pain** and a **long** **roadmap**.
>
> My **rule** is **simple**: **fix** what **hurts** **users** **on** the **floor** **first** — **real** **machines**, **real** **downtime**, **real** **money**. **Then** I **pick** up **non-urgent** **bugs** and **internal** **asks**. **Long-term** **work** **still** **moves**, but **honestly** **some** **problems** **can't** be **fully** **solved** **in** **one** **afternoon** — you **iterate** **toward** **better** **designs** **over** **time**.
>
> On **days** I **had** to **touch** **everything**, I **timeboxed**: **clear** **the** **urgent** **slice** **first**, **use** **what's** **left** for **the** **next** **bucket**, **and** **protect** **dates** so **neither** **track** **silently** **dies**. **Small** **tasks**, **clear** **owners**, **visible** **order** — **ops** **stays** **calm**, **milestones** **still** **move**.

**Script（极简 backup · ~25–32s）**

> **Smart Factory** — **urgent** **prod** **first** (**users** **depend**), **then** **non-urgent**, **then** **long-term** in **leftover** **time** **same** **day** **when** **I** **must**. **Some** **long** **fixes** **need** **iterations**, **not** **one** **hero** **night** — I **keep** **both** **lines** **moving** **without** **pretending** **either** **doesn't** **exist**.

**追问**
- **What if PM always marks everything P0?** → **一起排序** + **书面**只保 Top-N；见 **Q8/Q36**。
- **How protect deep work for long-term?** → **日历块** + **早关断** 即时消息；或 **协定** 某时段不排会。
- **Give another project besides Smart Factory.** → **enterprise IM** 产线 vs 路线图一句。

**短答英文**
> I **timebox** **firefighting** so **roadmap** **doesn't** **starve** — **if** **everything** is **P0**, we **rewrite** the **list** **together**.

<a id="q-41"></a>
### 41) What is something new that you’ve learned recently?
**提示（STAR）**（与 `kb/profile.yaml` **AUT MCIS** 时间线一致，并含你的表述）：**约 2024 起至今（至 2026-02 毕业）** 在 **AUT** 以 **AI / 大模型（LLM）** 为主线系统学习；**ChatClothes** 强化 **弱硬件 + 离线** 下的 **全链路 profiling**（不只盯 diffusion）。**并行自学**：**LLM + web coding**、**Hermes / agent / 智能体**，用于 **个人自动化与小工具** — **AI + cloud + code** 显著提高 **开发与验证效率**，**实现创意的成本** 明显下降。**观察（个人观点）**：**对编程/软件工程** 的冲击与提效 **很直观**；但在 **许多其他行业**，AI **尚未稳定渗入生产环节** 与 **真实 C 端应用闭环**，现场体感 **增益仍有限** — 你希望继续做 **可验证、可交付的落地**（口试 **勿** 把观察说成全行业统计）。

**Script（口语）** — **展开版（约 60–75s）**

> Over the **last** **~two** **years** — basically **since** I **went** **deep** into **AUT** in **2024** through **finishing** **MCIS** in **Feb 2026** — I've been **living** in **modern** **AI**, not only **reading** it. **ChatClothes** **forced** **me** to **profile** the **full** **pipeline** on **small** **hardware** **offline** — the **bottleneck** **wasn't** the **part** I **guessed** **first**.
>
> **Alongside** that, I **follow** **LLM** **tooling** **seriously** — **web**/**coding** **workflows**, **agent** **patterns**, and **model** **ecosystems** **around** **Hermes** — and I **use** it for **real** **automation** **I** **actually** **needed**: **small** **tools**, **repeatable** **chores**, **faster** **experiments**. **AI** **plus** **cloud** **plus** **better** **editor** **workflows** **lowered** the **cost** to **try** **ideas** I **wouldn't** have **bothered** **starting** **five** **years** **ago**.
>
> **Personally**, I **see** **two** **different** **pictures** **right** **now** — **as** **an** **engineer**, **not** **as** **a** **statistician**. **In** **software** **development**, **AI** **already** **moved** **the** **floor**: **coding**, **review**, **small** **builds**, **and** **experiments** **got** **cheaper** **and** **faster** — **that's** **real** **leverage** **I** **use** **daily**.
>
> **Outside** **pure** **dev** **workflows**, **especially** **production** **lines** **and** **real** **consumer** **journeys**, **the** **penetration** **still** **often** **feels** **thin** — **lots** **of** **pilots** **and** **slides**, **less** **durable** **value** **where** **people** **clock** **in** **or** **where** **end** **users** **actually** **live** **in** **the** **product**. **I** **want** **my** **next** **role** **on** **the** **side** **that** **closes** **that** **gap** — **measurable** **outcomes**, **not** **only** **demos**.

**Script（极简 backup · ~32–38s）**

> **Last** **~two** **years** at **AUT** — **LLMs**, **agents** (**Hermes** **style**), **web**/**coding** **tooling**, plus **ChatClothes** **taught** me to **profile** **end-to-end** **latency** **offline**. **AI** **cut** **my** **cost** to **try** **ideas**. **Dev** **already** **feels** **the** **lift**; **many** **other** **domains** **still** **need** **real** **production** **and** **C**/**B** **end** **value** — **that's** **where** I **want** to **ship**.

**追问**
- **Concrete ChatClothes bottleneck?** → **Cloud LLM** **round-trips** → **local** **Ollama**；**vision** **YOLO12n-LC**（与 **[Q31](#q-31)** 一致）。
- **Name one automation you shipped for yourself.** → 准备 **1 个** 可公开描述的例子（脚本/小工具/工作流），**勿编**商业客户名。
- **You said other industries lag — isn't that controversial?** → **限定为个人观察** + **我接触过的交付/客户类型**；收束到你想做 **生产可测** 的落地。

**短答英文**
> **Software** **already** **feels** the **lift**; **production** **and** **real** **end-user** **loops** **still** **often** **need** **hard** **engineering** — **I** **want** to **work** **there**, **with** **metrics**, **not** **hype**.

<a id="q-42"></a>
### 42) Tell me about a time when you had a hard time working with someone in your team. How did you handle it?
**提示（STAR）**：**二选一**。**Option A**（同 **Q6/Q24**）：**Enterprise Messaging** — 同事在 **review** 上退缩、参与度低 → **1:1** + **私下具体反馈** + **短结对**。**Option B**（**口述经历**，尚未写入 `projects/*/facts.yaml`；口试 **勿编造** 客户/项目正式名称，可统称 **入口称重/地磅联动** 类交付）：团队里 **资深同事** 习惯用 **Delphi** 做**新项目**（车辆 **上秤称重 → 超重预警 → 联动抬杆/报警** 等现场逻辑）；你当时 **~5–6 年**经验，对方 **行业经验更长**但 **工具链偏旧**、更倾向 **老栈**；你认为 **.NET 等团队已在用的栈** 更利于 **封装复用、协作与工期压缩时他人能接手**。**分歧处理**：先 **1:1** 表达对其 **现场经验** 的尊重，再把讨论落到 **可维护性 / 知识传承 / 工期与接手面** 等**可验证风险**；**同时**承认 **新技术需要学习窗口**。**结果**：**工程/甲方侧决策**采纳 **Delphi 路线** — 你 **书面保留技术顾虑** 后仍 **专业配合交付**，并尽量补 **文档/边界说明** 降低后续维护成本。**Reflection**：**尊重人 ≠ 回避栈决策**；**负责人拍板**后 **执行到位**；长期仍应推动 **团队默认技术栈** 与 **学习节奏** 对齐。

**Script（口语）** — **Option A（约 25–35s）**

> **Enterprise Messaging** — someone **froze** on **review**. **Private** talk, **gentle** **specific** notes, **pair** a bit. **Quality** and **mood** improved; **same playbook** as conflict question.

**Script（口语）** — **Option B（约 65–80s）**

> I had **tension** with a **very** **senior** **teammate** — **not** **personal**, **stack** **and** **ownership**.
>
> They **preferred** **Delphi** for a **new** **roadside** **weighing** **project** — **truck** **rolls** **on** a **scale**, we **read** **weight**, **raise** **alarms** **for** **overload**, **and** **integrate** **barrier**/**signals**. **Their** **experience** on **site** **was** **real**. **My** **worry** was **team** **reality**: **tight** **schedule**, **few** **people** **who** **could** **debug** **Delphi** **fast**, and **harder** **handover** when **only** **one** **person** **owns** **the** **dialect** of the **codebase**.
>
> I **didn't** **win** a **public** **fight** in **the** **room**. I **went** **1:1**, **respected** **their** **years**, **then** **made** **the** **trade-offs** **explicit** — **maintainability**, **review** **coverage**, **who** **helps** **if** **they** **get** **pulled** **away**. I **argued** **.NET**/**team** **stack** **would** **spread** **load** **better** **for** **this** **org** — **more** **people** **could** **read** **it**, **more** **libraries** **already** **solved** **boring** **parts**.
>
> **Leadership**/**customer** **chose** **Delphi** **anyway**. **Fair** — **that's** **a** **decision** **I** **don't** **own**. **My** **job** **after** **the** **call** was **professional**: **ship**, **document** **interfaces** **and** **risks**, **don't** **sabotage** **with** **attitude**. **Lesson**: **software** **changes** **fast** — **everyone** **needs** **learning** **time** — **but** **teams** **still** **need** **a** **default** **lane** **so** **we** **aren't** **solo** **heroes** **on** **deadlines**.

**追问**
- **Option A**：**What if they still resist?** → **升级** TL/经理；**记录**风险；**换结对**节奏。 / **Cultural barrier?** → **验收标准写清** + **图示**。 / **Your part?** → 早期语气 → **改**私下+具体（**Q21**）。
- **Option B**：**Aren't you dismissing older engineers?** → **强调尊重现场经验**；争议在 **可维护性/接手面**。**What did you do after Delphi was chosen?** → **文档、接口、风险清单**、正常协作。**Would you fight again?** → **用数据+默认栈规范** 走 **RFC/评审**，仍由 **负责人拍板**。

**短答英文**
> **Private** **1:1**, **respect** **first**, **then** **name** **maintainability** **and** **bus-factor** **risks** — **if** **the** **org** **picks** **Delphi**, I **still** **ship** **cleanly** **and** **write** **down** **what** **the** **next** **person** **needs**.

<a id="q-43"></a>
### 43) How do you assure code quality in your team?
**提示（STAR）**：**二选一**，框架都是 **防 / 抓 / 救**。**Option A** **`smart-factory`**（与现场 **多厂**、**~六年** Sprint 叙事一致）：规范 + **GitLab + Jenkins CI/CD**（见 **[Q44](#q-44)** / **[A ⑦](#oral-07)**）+ **强制 review**；**每周集成 demo** 真机真数据对齐 **mobile / backend / IoT**；线上 **监控**、**回滚**、**复盘**。**Option B** **`enterprise-messaging`**（与 `projects/enterprise-messaging/facts.yaml` 对齐）：**长期生产**（**~5k DAU**、**10+ 年**）下，质量 = **架构减面** + **发布纪律** + **缺陷节奏** — 例如 **C++ 自建消息** 长期不稳定、缺陷面大 → **迁移环信 Easemob** 把底层管道交给成熟云 SDK，自研聚焦业务层；**误将测试环境配置打进生产包** 事件后 **拆分多环境配置**、**发布前多轮校验**、并逐步 **自动化** 降低人为漏操作（**数据库 / App / Web** 发布一视同仁）；早期 **单人 Android** 窗口：**每日优先级缺陷清单** + **尽量每日一版** + **产品/设计对用户透明** 预期与计划。

**可叠加层（你的协作习惯 · 与 A/B 兼容；托管细节未写入 facts 前口试勿断言「全公司唯一标准」）**：**CI/流水线里做静态扫描**（或门禁脚本）把低级问题挡在合并前；提交 **MR/PR** 走 **结对或交叉 review**，**互审通过后**再合入 **main**；你在 **大版本 / 高风险改动** 上会 **额外 spot-check** 伙伴的关键改动；代码托管常见组合包括 **GitLab**（与 smart-factory facts 一致）、以及视项目而定的 **GitHub**、**阿里云效** 等 — 若面试官追问「到底用哪个」，诚实答 **按仓库/客户/时期** 或标 **`MISSING_INFO`**；IDE **静态分析/规范类插件** 作个人兜底，**不替代** review。**新人 / Junior**：先读团队 **统一代码规范**（例如业界可参考的 **《阿里巴巴 Java 开发手册》** 等），再在 **Spring / Spring Cloud** 体系里按 **「约定优于配置」** 开发，少做「自创一套配置方言」。

**Reflection**：质量不是「多测一轮」口号，而是 **工具门禁 + 人审 + 约定** 叠在一起，**减少不可控面** + **可重复发布** + **可见缺陷收敛**。

**Script（口语）** — **Option A（约 45–55s）**

> I think about quality in **three** layers — **prevent**, **catch**, **recover**.
>
> **Prevent**: **clear** team standards — we leaned on **industry** guides too, like a **solid Java style baseline** (**Alibaba's** **Java** **guide** is a common reference in China teams), plus **Spring**/**Spring Cloud** **conventions** so people don't invent random config dialects. **Automation** helps: **static** **analysis** in **CI**, **IDE** plugins for fast feedback — but they're **assistants**, not the **real** gate.
>
> **Human** gate: **merge** requests get **pair**/**cross** **review** before **main**; on **big** releases I still **spot-check** risky diffs from teammates. Hosting was mostly **GitLab** + **Jenkins** on my **factory** program (**facts** I can point to); other streams sometimes used **GitHub** or **Alibaba Cloud DevOps** — I won't pretend one **global** **label** for every repo.
>
> **Catch**: real tests plus **weekly integrated demos** — **Smart Factory** forced **mobile**, **backend**, and **IoT** to show **running** software together, not **slides**.
> **Recover**: **monitoring**, **rollback**, **postmortems**.
>
> That mix is how we kept **uptime** across **many factory sites** for years — **speed** without pretending **safety** doesn't exist.

**Script（口语）** — **Option B（约 45–55s）**

> On **`enterprise-messaging`**, **quality** wasn't only **tests** — it was also **architecture** and **release hygiene** over a **long** **lifecycle** (**~5k DAU**, **10+ years** in prod).
>
> **Catch / reduce defect surface**: our **in-house C++** messaging path stayed **noisy** — bugs never felt "finished." We **migrated core IM** to **Easemob** cloud + **SDKs** so the **low-level pipe** was **someone else's** **battle-tested** layer, and we focused engineering on **platform** pieces we could **control**.
>
> **Prevent recurrence**: after we once shipped a **production** build still wired to **test** configs, we **split** environment configs hard, added **multi-pass** checks before release, and pushed **progressive automation** — same bar for **DB**, **mobile**, and **web** ships.
>
> Early **solo Android** crunch: **daily** prioritized bug lists, **frequent** builds, and **product**/**design** helping users with **honest** timelines — **visibility** beats hero debugging.

**追问**
- **Option A**：**Who owns QA if no dedicated QA?** → **开发者自测矩阵** + **清单** + **灰度**；见 **Q4 Option B**。**Metrics?** → **缺陷趋势**、**回滚**、**demo 可集成度**（与 smart-factory 叙事一致处再说）。
- **Option B**：**Isn't outsourcing IM risky?** → **对价是自建 C++ 长期缺陷与运维**；自研聚焦 **业务/权限/文件**。**How prove Easemob helped?** → **缺陷收敛/发版节奏/线上稳定** 的**定性**叙述；**勿编** facts 未写的百分比。**Mobile matrix?** → **OEM 长尾**、实验室 **Android 7–8 下限**、**真机反馈驱动**（与 facts `Managed Android device long-tail` 一致）。
- **共用 / 可叠加层**：**Static analysis noisy?** → **分级**：**阻断级**（安全/明显错误）vs **警告级**（技术债 backlog）；**避免**「全红无人看」。**Tooling vs culture?** → **CI 守门 + MR 互审 + 规范文档** 三件套，工具减轻重复劳动，**不替代**人对边界条件的判断。**Junior 不写规范?** → **先给一页团队 checklist** + **链到公开手册** + **前几个 PR 高密度 review**（与 **Q45** 一致）。
- **共用**：**Conflict: speed vs coverage?** → **守门规则** + **风险分级**（**Q34**）。**Friday hotfix?** → **Q18** 慢下来、回滚就绪。

**短答英文**
> **CI** **static** **checks**, **paired** **reviews**, **written** **style** **baselines**, **then** **integrated** **demos** — **tools** **speed** **up** **humans**, **they** **don't** **replace** **them**.

<a id="q-44"></a>
### 44) Describe the project workflow in your previous team.
**提示（STAR）**：**二选一**。**Option A** **`smart-factory`**（与 `projects/smart-factory/facts.yaml`、[A ⑦](#oral-07) 一致）：**~六年** **双周 Sprint** — plan、standup、review、retro；每 Sprint **可运行 demo**（**mobile / backend / IoT** 对齐）；**接口契约** 先于破坏性改动；发布从**手动复制**演进到 **Jenkins + GitLab CI/CD**，**工厂项目先试点**再**各交付线统一迁移**，辅以清单与短文档；**团队侧**可安排 **定期技术分享**（新工具/适用问题/优劣与边界），与 Sprint 节奏并行、不必等「项目结束才补课」。**Option B** **`enterprise-messaging`**（与 `projects/enterprise-messaging/facts.yaml`、[A ⑨ Case B](#oral-09) 一致）：产品从**独立 IM** 渐进 **平台化**（用户中心、文件中心、子系统接入）；工程上 **Spring Cloud 微服务 + Node** 多子系统并行；团队扩大与**多项目穿插**后，协作流引入 **飞书（Lark）**、**协作文档**（如用过的 **石墨**）、**PM / 预算 / 审批** 纪律，并 **渐进自动化** 减轻行政摩擦；**极早期**你是 **唯一 Android**，**数周级**原型窗口上线后靠 **每日缺陷清单 + 尽量每日发版** 与 **产品/设计对用户解释预期** 收敛 — 与 **[Q43](#q-43) Option B** 的「质量/发版」叙事可同场串讲，勿重复堆砌细节。

**Script（口语）** — **Option A（约 40–50s）**

> **Smart Factory** — **two-week sprints** for **~six years**: plan, standup, review, retro. Every sprint ended with a **demo** of **real** software — **not** slides — so **mobile**, **backend**, and **IoT** stayed honest about integration.
>
> Before risky changes, we aligned on **shared API contracts** so nobody "surprised" another lane at the last day.
>
> On **release**, we moved from mostly **manual** copy deploys to **Jenkins** tied to **GitLab** — **CI/CD** so builds and deploys were **repeatable**. **Setup hurt** at first, so we **piloted** on the **factory** program, then **migrated** other streams to the **same** pattern instead of running **two worlds** forever.

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
**提示（STAR）**：**二选一**。**Option A** **`smart-factory`**（与 `projects/smart-factory/facts.yaml` 中 **Led and mentored a 6-person engineering team through multi-year delivery** 及 **Q12/Q20** 一致）：把新人/初级同事放进 **可预测的节奏** — **30/60/90** 用**定性里程碑**即可（例如 **首月**：能在 **review** 指导下完成 **小垂直切片**；**~90 天**：能 **端到端** 跟一块功能进 **周集成 demo**），**勿编** facts 未写的 KPI 数字。任务拆解：**小切片** → **接口契约可读** → 对齐 **24h review 窗口**（见 **[Q12](#q-12)**）减少返工；**每周 demo** 把「进度」变成 **可运行软件**，避免只看工单数。**日常跟踪（你的习惯 · 可与双周 Sprint 并存）**：**晨间站会**各自说 **今日计划**；**晚间（或下班前）**过一遍 **任务板/看板** 看完成度与阻塞；中间 **卡住就主动找人**，不必闷到 standup；你对 Junior **定时扫一眼**是否需要帮助 — 先听 **他怎么想、试了什么**，再 **讲你的思路/方向**，让他 **自己落代码**（避免长期代写）；同时 **看他的提交与 MR**，在 **review** 里把标准 **具体化**。**周固定 1:1 或阻塞窗** 仍保留作补位。**团队学习**：**定期技术分享会**（内部分享即可）— 轮流讲 **最近落地的新工具/技术**、**它解决什么问题**、**优势与边界/代价**（何时 **不该** 用），避免只堆名词、不交代 **trade-off**；Junior 也能提前看到「**选型长什么样**」，减少 **review 里第一次才听说** 的摩擦。**Option B** **文档与可交接**（与 **[Q21](#q-21)**、**[Q13](#q-13)** 同源，适合题干偏 **feedback / difficult conversation**）：Junior **代码尚可、文档与交接薄** → **小模板** + **一次结对**；经理曾指出大决策 **未写清** → 养成 **轻量 ADR + onboarding 短页**，让后来者少重复问 — 这是对 **整个团队** 的「隐性辅导」。与 **[Q43](#q-43) 可叠加层** 一致：新人先 **规范 checklist**，前几个 **PR 高密度 review**。**Reflection**：辅导 = **清晰期望 + 可验证的小胜利 + 把知识写进系统**（降低 bus factor）；**技术分享**把「**为什么选这个工具**」**前置**，减少 **一对一重复讲课**。

**Script（口语）** — **Option A（约 60–80s）**

> On **`smart-factory`**, I **helped** **mentor** people inside a **~six-person** **cross-functional** team over **years** — that's in my **facts** as **delivery** **leadership**, not **HR** **management**.
>
> **Day-to-day** rhythm: **morning** **standup** — everyone says **today's** **plan** so dependencies surface early. **Later** **that** **day** I **glance** at the **task** **board** for **what** **landed** **vs** **what** **slid** — it's not **surveillance**, it's **visibility**. If someone is **blocked**, the **rule** is **ask** **early** — **don't** **wait** for **hero** **hours**.
>
> For **juniors**, I **check** **in** **on** a **steady** **cadence**: **what** **they** **tried**, **where** **they're** **stuck**. I **share** **how** **I'd** **think** **about** it — **direction**, **trade-offs**, **a** **sketch** — **then** **they** **implement**. I'm **not** **trying** to **type** **their** **keyboard** **forever**.
>
> I still **watch** **their** **commits** and **MRs** — **reviews** are **coaching**: **what** **worked**, **then** **specific** **fixes** and **why** it matters for the **next** **reader**.
>
> We also ran **regular** **internal** **tech** **talks** — **not** **theater**: **what** **tool** **we** **actually** **tried**, **what** **pain** it **solved**, **what** **it's** **good** **at**, **and** **where** it **breaks**. That **helps** **juniors** **hear** **the** **why** **before** **the** **first** **angry** **review**.
>
> Bigger picture: **30/60/90** milestones, **small** **vertical** slices, and **weekly integrated demos** so **progress** stays **real**, not **ticket** **theatre**.

**Script（口语）** — **Option B（约 35–45s）**

> Another **track** is **writing** **culture** — overlaps **[Q21](#q-21)** and **[Q13](#q-13)**.
>
> Juniors often **ship** **code** that **works**, but **docs** are **thin** — the **next** **hire** **pays** **tax**. I gave a **small** **template**, **paired** once on a **real** PR, and **kept** feedback **kind** **but** **specific**.
>
> After **manager** feedback, I made **light** **ADRs** and a **short** **onboarding** page — **why**, not **novels**. **Ramp** got faster and **reviews** stopped **repeating** the **same** **lecture**. That's **mentoring** the **system**, not only **one** **person**.

**追问**
- **Option A**：**Micromanagement?** → **目标清晰 + 切片小**；**只在风险面**（集成点、生产配置）加密；日常 **放手** + **review 守门**；**任务板**是 **对齐完成度** 不是 **盯人**。**Evening board = surveillance?** → **短扫一眼**状态与阻塞；**信任** + **早求助** 文化并存。**Tech talks 流于形式?** → **必须绑定真实采用或试点结论**；**短**（如 **15–25 分钟**）+ **Q&A**；**不讲未落地的 PPT 选型**。**How delegate under deadline?** → **先拆可并行**；Junior 做 **边界清晰** 子任务，你保留 **契约/集成**。**Burnout?** → **轮换任务类型** + **承认工厂现场噪音**；与 **Q9** 一致。
- **Option B**：**They ignore docs after one PR?** → **把文档放进 Definition of Done** + **review 里点名缺啥**；两次仍空 → **升级**经理对齐期望。**Conflict with Q21 tone?** → 本题强调 **持续机制**（ADR/onboarding），Q21 强调 **单次困难反馈** — 可同场一句串起来。
- **共用**：**Junior underperforming — when escalate?** → **先结对 + 书面期望**；**连续两轮 review 无改善**再与经理对齐。**How measure progress?** → **demo 可集成度** + **独立关单质量** + **review 往返次数下降**。**Remote onboarding?** → **录屏** + **时区重叠窗** + **异步文档**（与 **[Q43](#q-43)** checklist 一致）。**与 Q2「讲太细」?** → 对 Junior **先大图再代码**；对自己用 **ADR 分层**。

**短答英文**
> **Standup** **for** **plan**, **board** **for** **truth**, **reviews** **for** **coaching** — **I** **give** **direction**, **they** **ship** **the** **implementation**. **Short** **internal** **tech** **talks** **for** **shared** **context**. **Plus** **30/60/90** **milestones** **and** **light** **docs** **so** **ramp** **isn't** **mystery** **tickets**.

---

<a id="section-toolbox"></a>
## Part 4 — Quick Review Sheet

This section is the fast reference area: templates, reminders, sentence patterns, and the appendix.

This section keeps the templates, reminders, sentence patterns, and appendix material you use right before the interview.

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
