# Interview Q&A — All Projects

> Consolidated interview questions and answers from all 21 projects. Use for interview preparation and English practice.
> 每个答案上方的中文关键词用于提示回忆，练习时先看中文关键词，再回忆英文表达。

---

## #1 Android Hotfix Framework (android-hotfix-framework)

### Q1: Walk me through your role on this hotfix framework.
**🔑 角色演变：早期构建 → 中期兼容性验证 → 后期主导退役评估**

**A:** I was involved from the start in 2017. Role shifted: early = building patching mechanisms (method hooks, dex diff gen, signature verification). Middle = compatibility validation across Android versions and vendor ROMs (MIUI, EMUI, ColorOS). Late = led retirement evaluation. Primary Android-side owner throughout — classloader hooking, NDK patching, canary rollout SDK. Server team contributed patch distribution backend.

### Q2: When did you start thinking hotfix needed to die?
**🔑 三个因素累积：ROM兼容性 + QA矩阵指数增长 + CI/CD成熟**

**A:** The decision accumulated over years, no single incident. Three factors: (1) Each Android version broke hooks on vendor ROMs. (2) 4-5 active Base APK versions each needing own patch = exponential QA matrix. (3) CI/CD matured to sub-2hr full releases. Tipping point: during yet another ROM fix, realized maintenance effort exceeded value.

### Q3: Who pushed back against retiring hotfix and how did you convince them?
**🔑 量化成本 + 3个月并行试验 + 真实bug用灰度发布解决**

**A:** Product and QA teams — operational fear: Friday night critical bug with no hotfix? Quantified cost (15-20% engineer time + 2-3 extra QA days per release). Demonstrated sub-2hr CI/CD. Proposed 3-month parallel trial. During trial, a real bug was resolved via staged rollout alone in 3 hours — zero hotfix patches needed. Data convinced skeptics.

### Q4: Give me a concrete example where hotfix could not resolve a production bug.
**🔑 服务端协议变更 → 客户端无法热修复 → Manifest不能改 → 只能全量升级**

**A:** IM product versioned serialization protocol. Server API change introduced new required field — old clients crashed on deserialization. Hotfix could null-check symptom, but: (a) new field carried routing metadata old client could not use, (b) protocol version in AndroidManifest cannot be hotfixed. Full APK upgrade was inevitable — hotfix bought 4 hours.

### Q5: After retiring hotfix, how many releases until confident?
**🔑 分阶段退役：1-2月Feature Flag → 3月并行 → 4月废弃SDK → 5-6月彻底移除**

**A:** Phased: Month 1-2 built feature flags + remote config. Month 3 parallel run (deliberately no hotfix use). Month 4 deprecated hotfix SDK. Month 5-6 removed entirely. Confident after ~5 releases — three real bugs resolved via staged rollout alone, zero fallback.

### Q6: Looking back, was building a hotfix framework a mistake?
**🔑 2017年是正确工具，但世界变了 → 要持续重新评估工具**

**A:** Right tool for 2017 — slow Play reviews, primitive staged rollout, immature CI/CD. By 2023, world changed. Lesson: continuously re-evaluate tools against changing landscape. Would have started retirement evaluation a year earlier.

---

## #2 Android Performance & Optimization Framework (android-performance-optimization)

### Q1: What was the single most effective optimization you applied?
**🔑 最有效：删除无用x86 SO库 + 图片压缩 → APK降55%；懒加载SDK → 冷启动快47%**

**A:** Removing unused x86/x86_64 SO libs from map/audio/video SDKs — saved most space in single action, zero runtime risk (never loaded on ARM devices). Combined with image compression: 200MB+ to 80-90MB (55%+). Cold-start: lazy init + async SDK loading reduced 1.5s to 800ms (47%). Measured via Android Profiler + CI benchmarks.

### Q2: How did you find and fix the toughest memory leak?
**🔑 两大根因：线程持有Activity引用 + Handler持有Context；WeakReference修复**

**A:** Two root causes across 8+ apps: (1) thread holding — background threads retaining Activity via ThreadLocal. Fix: cancel Runnables in onDestroy, WeakReference. (2) Handler retaining Context — static Handler + WeakReference, remove pending messages in onDestroy. Heap Dump reference chains confirmed fixes.

### Q3: How did product team react to cutting image quality for APK size?
**🔑 盲测对比：看不出差别就压缩，看得出来就保留；协作式权衡**

**A:** Negotiation, not demand. Blind comparison: multi-MB to tens-of-KB screenshots. If no one could tell difference, compressed shipped. If visible, kept higher quality. Made trade-off visual and collaborative.

---

## #3 Banknote Paper Mill Customer Integration (banknote-paper-mill)

### Q1: What was unique about air-gapped development?
**🔑 断网环境 + 提前1周审批 + 离线开发 + 每次进场需可验证交付物**

**A:** No internet on-site. ~1 week advance approval per visit. All development offline on external laptops — analyze data, build, package, deploy during visit. Each visit required provable checkpoint. Forced extreme preparation discipline and pre-tested rollback paths.

### Q2: How did you handle invisible progress between site visits?
**🔑 按可展示检查点安排进场：验证数据 → 端到端流水线 → 生产部署**

**A:** Structured visits around demonstrable checkpoints: Visit 1 = data validated + first read. Visit 2 = pipeline end-to-end. Visit 3 = production deploy. Transparent scheduling: next week no output, but on [date] we demo X.

---

## #4 Boobit Crypto Trading App (boobit)

### Q1: ~1-month freelance — how did you ramp up on an unfamiliar crypto codebase?
**🔑 学习已有MVVM模式 → 2-3天追踪数据流 → 只学需要的模块（钱包/行情/兑换）**

**A:** Existing MVVM architecture — just learn patterns. First 2-3 days traced existing flows to understand data layer, ViewModels, API patterns. Only learned paths I needed (wallet, market, exchange, recharge).

### Q2: High-precision decimal problem — worst case and solution?
**🔑 BTC 18位 vs 其他8位 + 后端格式不一致 → BigDecimal归一化 + 字符串传输**

**A:** BTC returned 18 decimal places, others 8. Backend format inconsistent (string vs number). Built normalization: BigDecimal → round to per-token precision → format. Without this: unreadable or incorrect prices.

### Q3: HTTPS + request signing + parameter encryption — what did it look like?
**🔑 三层防护：HTTPS加密传输 + HMAC签名防篡改 + AES加密敏感参数**

**A:** HTTPS for transport. Request signing: timestamp + nonce + HMAC-SHA256 over body+timestamp+nonce with pre-shared key. Parameter encryption: AES-encrypted payload with session key. Defense in depth — TLS compromise alone insufficient to read/modify payloads.

---

## #5 Broadcast Control Platform (broadcast-control)

### Q1: Why MQTT over HTTP/WebSocket for broadcast?
**🔑 MQTT天然支持一对多发布订阅；HTTP是O(N)轮询；长连接WebSocket服务器资源消耗大**

**A:** One-to-many pub/sub maps to device groups = MQTT topics. Single publish reaches all subscribed screens. HTTP push is O(n) iteration. Persistent WebSocket to thousands of screens is resource-heavy on server.

### Q2: You wore three hats — PM, system designer, Android dev. How did you balance?
**🔑 不是同时做，而是分阶段：前期架构设计 → 中期Android开发 → 全程轻量PM**

**A:** They shifted over time, not simultaneous. Early = system design (device model, MQTT hierarchy, campaign schema). Middle = Android dev (screen client). PM was lightweight throughout (stand-ups, task board, demos).

---

## #6 ChatClothes Virtual Try-On (chatclothes)

### Q1: Why two separate GPU servers instead of a single larger one?
**🔑 腾讯云免费16GB限制 → ComfyUI+OOTDiffusion占10GB → Ollama+DeepSeek占10GB → 必须分开**

**A:** Necessity — two free-tier Tencent Cloud GPUs, 16GB each. ComfyUI/OOTDiffusion ~10GB VRAM, Ollama/DeepSeek ~10GB — too much for single 16GB card. Dify orchestrated across both via FastAPI REST. Production would use single larger GPU or optimize model to fit.

### Q2: YOLO12n-LC — what does LC stand for and what changed from base YOLO12n?
**🔑 LC = Lightweight Classification；通道裁剪 + ARM量化 → 5MB（8倍缩小）+ 94.2%准确率**

**A:** Lightweight Classification. Separate research project for garment classification, reused in ChatClothes. Reduced channels, ARM quantization for RPi5, trained on 4 garment categories. Result: 5MB (8x smaller), 94.2% accuracy, 35ms inference on RPi5.

### Q3: ~7s pipeline latency on RPi5 — how make it feel acceptable to users?
**🔑 感知延迟优化：分类35ms反馈 + LLM提示150ms + WebSocket渐进更新 + 进度指示器**

**A:** Focused on perceived latency: 35ms classification feedback, 150ms LLM prompt display, WebSocket progressive updates during diffusion, clear progress indicator. 7s felt shorter because system visibly worked at every stage rather than showing a spinner.

---

## #7 Chinese Herbal Recognition Platform (chinese-herbal-recognition)

### Q1: What made the platform reusable across different classification domains?
**🔑 五个领域无关阶段：类别创建 → 标注 → 训练 → 评估 → 推理；低置信度反馈循环通用**

**A:** Five domain-agnostic stages: category creation → annotation → training → evaluation with release gates → inference. Each stage configurable, not hardcoded. Low-confidence feedback loop also domain-agnostic — unsure samples routed to re-annotation for any domain.

### Q2: What was the model release gate criteria?
**🔑 三道门：整体准确率 + 类别平衡（F1≥85%）+ 关键类别假阳性率**

**A:** Three gates: (1) Overall accuracy above domain minimum. (2) Per-class balance — no single category below 85% F1. (3) False positive rate below safety threshold for critical categories (e.g., misidentifying toxic herb as edible). Passing = promoted to serving. Failing = diagnostics showing which categories need more data.

---

## #8 Device Maintenance Prediction Platform (device-maintenance-prediction)

### Q1: This was experimental with limited data. What would it take for production?
**🔑 三个条件：更多标注数据 + 传感器特征（振动/温度）+ 反馈闭环**

**A:** (1) More data — at least 6-12 months continuous records with labeled outcomes (did equipment actually fail?). (2) Domain features — vibration, temperature trends, cycle counts (need sensor instrumentation). (3) Feedback loop — did predicted maintenance actually happen? Production scaling is primarily a data infrastructure problem, not an algorithm problem.

### Q2: Why Spark MLlib over scikit-learn?
**🔑 可扩展性：本地开发+集群运行同一代码；随机森林可解释性高，工厂经理能理解**

**A:** Future-proof — same pipeline code runs locally for dev and on Spark cluster if data grows. Random Forest over deep learning for interpretability — can explain to factory manager why specific equipment scored high risk by showing feature contributions. Black-box predictions do not build trust in industrial settings.

---

## #9 Enterprise Messaging Platform (enterprise-messaging)

### Q1: Why did the C++ core need migration to Easemob? What was the breaking point?
**🔑 创业期原型未重构 → 紧耦合+测试不足 → 持续生产事故 → 90%+缺陷消除**

**A:** Legacy C++ core had chronic stability issues — start-up phase prototype never refactored for reliability at scale. Years of patching introduced new edge cases because core was tightly coupled and poorly tested. Breaking point: series of production incidents where message delivery failures affected business operations. Easemob replaced entire unstable transport layer (90%+ defect elimination) while keeping our NDK TCP/UDP for <200ms delivery.

### Q2: Under 2% downtime over 10 years — what architectural decisions enabled this?
**🔑 三原则：无单点故障+优雅降级+保守迁移（并行运行验证后再切换）**

**A:** Three principles: (1) No SPOF — message gateway, file storage, push channels, databases all had redundancy. JPush as backup push alongside Easemob. (2) Graceful degradation — partial failures did not cascade. If FastDFS was slow, text messages still delivered. (3) Conservative migration — C++ to Easemob was incremental, not big-bang. Ran both systems in parallel, verified on subset of users, then expanded.

---

## #10 Exhibition Service Robot (exhibition-robot)

### Q1: Buy-vs-build: why was purchasing a complete robot the right call here?
**🔑 核心价值是上层功能（人脸/语音/导览）而非导航；ROS/SLAM要6-12月；SDK让团队聚焦客户价值**

**A:** Core value was upper-layer features — product introductions, face recognition check-in, voice-guided tours — not robot navigation. Building ROS/SLAM/navigation from scratch would consume 6-12 months on a commodity capability vendors already solved well. The SDK meant we called robot.navigateTo(waypoint) instead of tuning SLAM parameters. Navigation was infrastructure, not product — buying let the 4-person team focus entirely on what created client value.

### Q2: What were the limitations of relying on vendor SDKs?
**🔑 受限于供应商的bug和功能；无法修复算法只能调环境；通过实地测试+降级方案缓解**

**A:** You are at the vendor mercy for bugs and feature requests. If ArcSoft face recognition had accuracy issues in certain lighting, we could not fix the algorithm — only adjust lighting and camera angle. Mitigation: (1) test SDKs in actual exhibition environment during evaluation, not just demo bench, (2) build fallbacks (QR code if face fails), (3) maintain good vendor relationships for priority fixes. Acceptable trade-off for a one-off deployment.

---

## #11 Highway Toll Station Vehicle Inspection System (field-weighing-access-control)

### Q1: How did you communicate with the electronic scale?
**🔑 RS232串口 + C# SerialPort类 + 读取连续数据流 + 等待读数稳定后记录**

**A:** RS232 serial port. The scale had a serial output that sent weight readings in a specific format. We used C#'s System.IO.Ports.SerialPort class to open the connection, configure baud rate and data format, and read the weight data. The scale would send a continuous stream of weight values, and our software would parse the latest stable reading — waiting for the value to stabilize before recording it.

---

## #12 Forest Patrol Inspection System (forest-patrol-inspection)

### Q1: Coordinate system conversion — WGS-84, BD-09, GCJ-02. How does that work?
**🔑 中国法律要求GCJ-02偏移坐标；百度进一步偏移为BD-09；同一GPS点在不同地图偏差100-500米；需自动转换**

**A:** China mandates domestic map providers use GCJ-02 (encrypted offset of WGS-84). Baidu further encrypts to BD-09. The same GPS coordinate can appear 100-500m offset on different map layers. A conversion layer auto-detects which map source is active and applies the appropriate transformation. Trickiest part: user switching map sources mid-session — all existing GIS annotations must re-project instantly, and GPS trajectory must store points in a canonical system (WGS-84) to avoid corruption when switching back and forth.

### Q2: GPS signals took up to 30 seconds in dense forest. How did you keep the app from looking broken?
**🔑 超过60秒才显示无信号；期间用航位推算+不确定性圆圈+缓冲轨迹点**

**A:** Never showed no signal unless >60 seconds without a fix. During gaps: (1) held last known position with updated X seconds ago indicator, (2) dead reckoning (continue along last direction/speed) displayed in lighter color as estimated, (3) buffered trajectory points and retroactively corrected when new satellite fix arrived. UX principle: expanding uncertainty circle communicates trying to get better fix rather than broken.

---

## #13 IoT Device Management Platform (iot-solutions)

### Q1: This product line spanned 7 years. What evolved the most?
**🔑 架构思维演进最大：早期三个独立项目 → 后期设计为单一分布式系统（边缘计算+本地控制面+云端管理）**

**A:** My architecture thinking evolved the most. Early on (2016-2017), I thought of the Android app, gateway firmware, and backend as three separate projects. By 2019-2020, I was designing them as a single distributed system: gateway = edge compute (local MQTT, protocol translation, offline behavior), Android = local control surface, backend = fleet management and analytics. This shift changed how I thought about failure modes, data ownership, and deployment coordination.

---

## #14 Live Streaming Chat Room System (live-streaming-system)

### Q1: The C++ server core was rewritten multiple times. What did each rewrite solve?
**🔑 V1单进程瓶颈 → V2进程间同步bug → V3多线程但太复杂 → 创业公司典型迭代**

**A:** V1: monolithic C++ handling everything in one process — worked for small rooms but bottlenecked at few hundred viewers on message dispatch. V2: split message routing and media streaming into separate processes via shared memory — scaled to 1000+ but introduced synchronization bugs between processes. V3: multi-threaded with per-room workers and shared message bus — solved sync issues but C++ codebase became too complex for the 2-person server team. This iterative churn is typical of start-ups figuring out architecture through production pain.

### Q2: What did building a monolithic admin backend in DNN/ASP.NET teach you?
**🔑 服务端渲染→每次操作全页刷新→设计最小化往返；后来用SPA时更理解两者的时代背景**

**A:** DNN rendered HTML server-side — every user action required a full page reload. This taught pre-SPA constraints: design workflows minimizing round-trips. State was simpler (server-side session) but UX was clunkier. When later using Vue.js on Smart Factory, I appreciated what SPA enabled but also understood why monoliths made sense in their era — single deployable artifact, simpler debugging. Architecture is a product of its time: DNN was state-of-the-art in 2015, legacy by 2018.

---

## #15 Patent Search System (patent-search-system)

### Q1: .NET Framework 2.0 and Lucene.NET 2.9 in 2014 — quite old even for 2014. Why?
**🔑 企业内部工具，Windows XP/Server 2003环境只能跑.NET 2.0；升级OS影响其他关键业务**

**A:** Enterprise internal tool on existing corporate Windows XP/Server 2003 infrastructure. .NET 2.0 was the latest version supported on those systems — upgrading the OS was not an option because other business-critical applications depended on it. Delivering a working tool on existing infrastructure was more valuable than advocating for upgrades that would delay the project by months.

### Q2: Lucene.NET for full-text search on 10,000+ patents — how did you achieve sub-2s?
**🔑 多字段索引（标题/摘要/发明人/分类号/日期）+ 增量索引（只索引新导入的）**

**A:** Multi-field index schema designed around how researchers actually searched: separate indexed fields for title, abstract, inventor names, classification codes, dates. Enabled field-specific queries without scanning full documents. Incremental indexing: when new patents were batch-imported via Excel, only new documents indexed, not entire corpus. Performance came from index structure, not hardware horsepower.

---

## #16 Picture Book Locker / Smart Library Cabinet (picture-book-locker)

### Q1: 10+ hardware peripherals via UART/RS485 and GPIO — which one caused the most trouble?
**🔑 电磁锁时序要求最严：亚秒开锁 + 同步LED + 门传感器 + 看门狗；非实时Linux调度**

**A:** Electromagnetic locks due to timing requirements. Sub-1s open after face/QR authentication, coordinated simultaneously with LED strip lighting target compartment, door sensor confirming opening, watchdog timer auto-closing if door stayed open too long — all on ARM board running Android with non-real-time Linux scheduling. Achieved by prioritizing GPIO write for the lock above all other operations on auth success path, and using hardware timer for the auto-close watchdog (not software timer that could be delayed by GC).

### Q2: When your colleague resigned and you had to split scope — walk me through that conversation.
**🔑 用数据而非抱怨：展示backlog+时间线+风险 → 提出方案（我做擅长的硬件端，另一人做借阅App）→ 早期上报**

**A:** I came with a problem statement, not a complaint: here is the inherited backlog, here is my existing workload on other projects, here is the combined timeline showing milestone X would slip by Y weeks. Then I proposed the split: I keep cabinet-side Android host (hardware control, UART/RS485, GPIO — my deepest expertise), To-C borrower mobile app goes to another engineer I had already confirmed had capacity and interest. The framing was not I cannot handle this — it was here is the math, the risk, and my proposed solution. Leadership appreciated the early escalation (before the milestone was at risk) and the solution-oriented framing.

---

## #17 School Face Recognition Attendance System (school-attendance)

### Q1: Liveness detection for face recognition attendance — did you catch any real spoofing attempts?
**🔑 SDK要求眨眼/转头防照片攻击；学生试用手机照片帮迟到同学签到被拦截；家长推送是第二道防线**

**A:** Face SDK required blinking or slight head turn — defeats photo and static video attacks. 200-300ms overhead but non-negotiable for a school environment. During testing, students tried checking in friends running late by showing photos on their phones — liveness detection caught all attempts. JPush real-time parent notification was the second half of anti-fraud: even if someone beat liveness, parents would immediately see an unexpected attendance notification and flag it.

---

## #18 Smart Factory System (smart-factory)

### Q1: Walk me through the serial-to-WebSocket weighing bridge. Why not read from the browser directly?
**🔑 浏览器无法访问串口 → 本地Windows服务读串口 → WebSocket推送到浏览器 → 输入框自动填充**

**A:** Browsers cannot access serial ports — fundamental web platform restriction. The factory weighing workflow was browser-based (Vue.js web app on shop-floor PCs), but electronic scales connected via RS232/RS485 serial ports. A local Windows service opened the serial port, listened for stabilized weight readings, and forwarded them to the browser via a local WebSocket server. When operator focused on a weight input field, WebSocket message auto-filled — eliminating the read scale, type number loop. Before: 3-step (read → remember → type). After: 1-step (place item on scale → weight auto-fills). Reduced transcription errors.

### Q2: You wrote ~1/4 of backend, owned all Android, built hardware comms, helped Vue.js. How did you context-switch?
**🔑 按天分区而非一天内切换：周一/二Android → 周三后端 → 周四硬件 → 周五规划**

**A:** I blocked time per domain by day rather than context-switching within a day. Monday/Tuesday focused on Android features and releases. Wednesday on backend code review and my 3 modules. Thursday on hardware integration testing. Friday on team planning, code review, and whatever domain had most urgent need. Each domain had different done signals: app release, API deploy, successful scale readings. I did not try to make progress in all four daily — that leads to nothing finishing.

### Q3: MySQL grew to millions of rows and queries slowed. Why cloud MySQL as temporary fix?
**🔑 用钱买时间 → 先发版 → 再优化（索引+分区+ORM优化）→ 优化后迁回本地省成本**

**A:** Trade-off between stopping feature delivery and letting performance degrade. Pausing feature work for deep query/schema/index optimization would take 2-4 weeks, during which product roadmap would stall while shop floor already experienced slow queries. Moving to cloud-hosted MySQL with higher provisioned capacity and read-replica routing bought time — performance masked while shipping committed milestones. Then with feature pressure relieved, scheduled root-cause work: identified high-cardinality joins on daily task table, added composite indexes, partitioned by date, optimized ORM queries. Once optimizations landed, repatriated back to on-premises to eliminate recurring cloud cost. Sequence was deliberate: buy time with money → ship features → optimize → reduce cost.

---

## #19 Smart Power Management System (smart-power)

### Q1: You worked with Modbus RTU, DL/T645, RS485. What is the practical difference?
**🔑 协议抽象层：每个协议有独立适配器模块 → 统一read_register/write_register接口 → Spring Cloud不用关心具体协议**

**A:** Modbus RTU over RS485 is most common for power meters — request-response protocol where master polls each slave by address. DL/T645 is Chinese national standard for electric energy meters with different frame format and addressing scheme. The backend integration challenge was building a protocol abstraction layer in the gateway: each protocol's frame parsing and addressing logic encapsulated behind common read_register and write_register interface. Spring Cloud services did not need to know which protocol a specific meter used. Without this abstraction, every backend service would need to understand Modbus frame structure and DL/T645 addressing.

---

## #20 Visit Booking & Access Management System (visit-system)

### Q1: Prison visitation imposes unique constraints. What was the hardest one technically?
**🔑 无个人设备 + 严格时间限制（不能超1秒）→ 服务端倒计时强制断开WebRTC连接**

**A:** No personal devices — all inmate-side interaction happened through facility-managed Android terminals. Each session required clean start: logout previous user, clear local state, initialize fresh WebRTC session. Strict time limit: visits had fixed duration and system had to auto-end at exactly that time — not a second over, for compliance. WebRTC has no built-in session duration enforcement. Built server-side timer: 1-minute warning, 10-second countdown, then forcibly terminate peer connection from server side. Recording captured full session including auto-end for audit purposes.

### Q2: Face recognition at visitor entry — what happened when the system rejected a legitimate visitor?
**🔑 假拒绝代价高 → 阈值偏向低拒绝率 + 二维码降级路径 + 人工复查边界案例**

**A:** False rejections at a prison gate are high-stakes — they block a real visitor and create confrontation. Mitigation: (1) face recognition threshold tuned conservatively toward lower false rejection, accepting slightly higher false acceptance rate since guard at checkpoint was secondary verifier checking ID. (2) QR code from booking confirmation as fallback path with manual guard verification. (3) Recognition logs captured confidence scores so staff could review borderline cases. System designed as efficiency tool for guards, not autonomous gatekeeper — human override always available.

---

## #21 Visual Gateway / Breaker Control Gateway Platform (visual-gateway)

### Q1: Why an Android gateway for breaker control rather than traditional PLC or RTU?
**🔑 现有断路器只有RS232串口 → 换网络断路器每台$500-1000+ → Android板便宜+团队有经验 → 亚秒本地告警够用**

**A:** Existing circuit breakers were non-networked — RS232 serial only, no Ethernet/WiFi. Replacing them with networked breakers would cost $500-1000+ per breaker across multiple sites. Android board with serial port capability: commodity hardware much cheaper than industrial PLCs, handles serial polling protocol + cloud MQTT in one device, team already had Android expertise. Trade-off: Android is not a real-time OS — sub-second local alerting carefully implemented to avoid GC or UI thread delays. Sub-second is fast enough for breaker control; microsecond precision would need real-time controller.

---

*共 127 道面试题覆盖 21 个项目。Last updated: 2026-06-30*
