# Smart Factory System

> Microservice-based manufacturing platform deployed across 5+ factory sites

---

## Overview

Led the development of a **full value-chain smart manufacturing platform** for textile factories, connecting **brands/customers, factories, and frontline workers** on one system.  
The platform not only manages production workflows, inventory, and IoT equipment, but also **accepts customer orders, allocates them to suitable factories, tracks per-garment production progress, and synchronizes shipping status back to the customer side**, supporting hundreds of workers across multiple sites.

**Android shop-floor app:** Workers carry a **mobile production client** for daily tasks—**today’s output counter**, **search by customer style or package ID**, **tabs for not-started / in-progress / completed work**, and a **center “scan” action** tied to barcode/QR flows on the line. **Task detail** surfaces progress (e.g. completed vs planned pieces), **tech pack / process tabs**, and **quality requirements** (e.g. textile industry standards) on the device. **My / profile** ties **employee ID, on-duty status, work log, messages**, and **scan configuration** to the same floor workflow.

In addition, I implemented a **weighing integration module**: electronic scale data is collected through serial communication, monitored by a Windows service, and synchronized to web pages and core business systems in real time.

**Project Type:** Enterprise System / Industrial IoT  
**Timeline:** 2018 - 2024  
**Role:** Frontend Developer (Vue.js)  
**Company:** Chunxiao Technology Co., Ltd., China  
**Team Size:** 6 people (cross-functional)

---

## Key Features

- **End-to-end order platform:** From customer order → factory scheduling → production → shipment
- **Multi-role portals:** Separate experiences for brands/customers, factory management, and workers
- **Android mobile client:** Task list with status filters, task detail (progress, tech pack, process & quality text), scan-centric navigation, and worker profile (duty status, logs, messages, scan settings)
- **Order allocation engine:** Distributes orders to different factories based on capacity and skills
- **Per-garment progress tracking:** Realtime view of each garment’s process and station
- **Microservice architecture:** Scalable, modular backend services
- **IoT integration:** Real-time tracking via RFID, barcode scanners, conveyors
- **Weighing integration:** Electronic scale data acquisition and synchronization to web/system
- **Production management:** Workflow orchestration and process tracking
- **Multi-site deployment:** Supports 5+ manufacturing locations
- **High availability:** 99.9% uptime maintained
- **CI/CD pipeline:** Automated deployment and testing
- **Real-time monitoring:** Live production status and alerts

---

## End-to-End Flow / 全链路流程

1. **Customer side（客户端）**：品牌或客户在平台上下单，配置款式、尺码、交期等需求。  
2. **Platform scheduling（平台排产）**：系统根据各工厂产能与能力，将订单拆分并分配到不同工厂、产线。  
3. **Factory execution（工厂执行）**：  
   - 车间终端为工人下发工序任务；  
   - 工人通过生产端扫码/刷卡完成工序上报；  
   - RFID / 条码 / 产线设备实时回传进度与产量；  
   - 电子秤通过串口上报称重数据，由 Windows 服务监控并推送到网页与业务系统。  
4. **Progress tracking（进度追踪）**：客户在平台上可以看到每个订单、每一批甚至每件衣服的实时生产进度。  
5. **Shipping & delivery（发货与交付）**：生产完成后，系统生成出货信息并同步给客户，形成从下单到收货的闭环数据链路。

---

## Architecture

```
┌─────────────────────────────────────┐
│         Client Applications         │
│   (Android, Web Dashboard, IoT)    │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│          API Gateway (Nginx)        │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Microservices (Spring Boot)    │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │Production│ │ Inventory│ │ Device ││
│  │ Service  │ │ Service  │ │ Service││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Data Layer                    │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │  MySQL  │ │  Redis  │ │ MongoDB││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────────────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      IoT Hardware Layer            │
│ (RFID, Barcode, Conveyors, Scales) │
└─────────────────────────────────────┘
```

---

## Technologies

### Frontend
- **Vue.js** - Web portals and dashboard development
- **JavaScript** - Frontend business logic and interaction handling
- **HTML/CSS** - Responsive UI implementation

### Backend
- **Java** - Primary development language
- **Spring Boot** - Microservice framework
- **Spring Cloud** - Distributed system support
- **MyBatis** - Data access layer
- **RESTful APIs** - Service communication

### Data & Storage
- **MySQL** - Primary database
- **Redis** - Caching and session management
- **MongoDB** - Document storage

### DevOps & Infrastructure
- **Docker** - Containerization
- **Jenkins** - CI/CD automation
- **Nginx** - Load balancing and reverse proxy
- **CentOS** - Production servers

### IoT & Hardware
- **RFID** - Asset and inventory tracking
- **Barcode Scanners** - Product identification
- **Conveyors** - Automated material handling
- **UART/Serial** - Device communication
- **Electronic Scales** - Weight data capture for production/business workflows
- **Windows Service** - Serial listener, health monitoring, and auto-reconnect
- **RS232/RS485** - Stable scale communication channel

---

## Key Achievements

- ✅ **5+ factory sites** deployed and operational
- ✅ **30%+ efficiency improvement** in production
- ✅ **99.9% uptime** maintained over years
- ✅ **Hundreds of workers** supported daily
- ✅ **Cross-functional team leadership** (6 members)
- ✅ **Agile practices** implementation

---

## Responsibilities

### Frontend Development (Vue.js)
- Developed web portals and operational dashboards with Vue.js
- Implemented production, equipment, and workflow visualization pages
- Built frontend modules for order progress, status monitoring, and data forms
- Integrated frontend with backend APIs and real-time update mechanisms

### Technical Leadership
- Designed overall system architecture
- Established coding standards and best practices
- Code review and technical mentoring
- Technology stack selection

### Backend Development
- Core microservices implementation
- Database design and optimization
- API design and documentation
- Performance tuning

### DevOps & Deployment
- CI/CD pipeline setup (Jenkins)
- Docker containerization
- Nginx configuration
- Production deployment management

### Team Management
- 6-person cross-functional team leadership
- Sprint planning and task allocation
- Stakeholder communication
- Delivery timeline management

### IoT Integration
- Hardware device integration (RFID, barcode, conveyors)
- Protocol design and implementation
- Real-time data processing
- System monitoring and maintenance
- Electronic scale serial data acquisition and parsing
- Windows service watchdog, reconnect, and exception recovery
- Scale data synchronization to web dashboards and backend business system

---

## Challenges & Solutions

### Challenge 1: Multi-site Synchronization
**Problem:** Keeping data consistent across 5+ factory locations  
**Solution:** Distributed architecture with centralized configuration management

### Challenge 2: Hardware Integration Complexity
**Problem:** Integrating diverse IoT devices with different protocols  
**Solution:** Unified device abstraction layer and protocol adapters

### Challenge 6: Usable Shop-Floor Mobile UX
**Problem:** Workers need fast lookup, scanning, and spec viewing on phones without leaving the line  
**Solution:** Android client with filtered task queues, task detail tabs for tech pack / process / requirements, and profile + scan configuration aligned to floor roles

### Challenge 3: High Availability Requirements
**Problem:** Manufacturing cannot tolerate system downtime  
**Solution:** Redundant deployments, automated failover, and comprehensive monitoring

### Challenge 4: Team Coordination
**Problem:** Coordinating Android, backend, and hardware teams  
**Solution:** Agile methodologies, clear documentation, and regular sync meetings

### Challenge 5: Stable Weighing Data Pipeline
**Problem:** Serial scale data may be noisy, interrupted, or disconnected in factory environments  
**Solution:** Implemented Windows service-based serial monitoring with heartbeat, auto-reconnect, buffering, and retry to ensure reliable web/system data sync

---

## Results & Impact

- **Operational Excellence:** System supports daily operations for hundreds of workers
- **Efficiency Gains:** Production efficiency improved by 30%+
- **Scalability:** Successfully scaled from 1 to 5+ sites
- **Reliability:** Achieved and maintained 99.9% uptime
- **Team Development:** Successfully mentored and led 6-person team

---

## Evidence

### Mobile worker app (Android) / 手机端工人应用

Real screenshots from the **shop-floor Android** experience: production task list, task detail with progress and requirements, and worker profile with duty status and scan-related settings.

<table>
  <tr>
    <td align="center">
      <img src="./images/ScreenShot_2026-04-01_161701_214.png" width="280" alt="Mobile task list: daily count, search, status tabs, scan"/><br/>
      <sub>Task list: today’s output, search, 未制作/制作中/已制作 tabs, bottom nav + 扫一扫</sub>
    </td>
    <td align="center">
      <img src="./images/ScreenShot_2026-04-01_161723_937.png" width="280" alt="Mobile task detail: progress, tech pack tabs"/><br/>
      <sub>Task detail: ID, spec, progress bar, 工艺单/工艺指示/基本要求 tabs, quality notes</sub>
    </td>
    <td align="center">
      <img src="./images/ScreenShot_2026-04-01_161819_162.png" width="280" alt="Mobile profile: employee, on-duty, work log, scan config"/><br/>
      <sub>我的: employee ID, 上班中, work log / messages / 扫码配置 / password, etc.</sub>
    </td>
  </tr>
</table>

### BI & Monitoring / BI 与监控大屏

<table>
  <tr>
    <td align="center">
      <img src="./images/bi-dashboard-overview.jpg" width="360" alt="BI dashboard overview"/><br/>
      <sub>Overall BI dashboard for factory KPIs</sub>
    </td>
    <td align="center">
      <img src="./images/equipment-dashboard-list.png" width="360" alt="Equipment dashboard list"/><br/>
      <sub>Web dashboard listing machines and status</sub>
    </td>
  </tr>
</table>

### Shop Floor Terminals / 车间终端

<table>
  <tr>
    <td align="center">
      <img src="./images/production-task-list.png" width="320" alt="Production task list screen"/><br/>
      <sub>Operator task list and completion progress</sub>
    </td>
    <td align="center">
      <img src="./images/production-input-keypad.png" width="320" alt="Production input keypad"/><br/>
      <sub>On-device numeric keypad for entering production data</sub>
    </td>
    <td align="center">
      <img src="./images/production-terminal-login.png" width="320" alt="Production terminal login"/><br/>
      <sub>Factory production terminal login screen</sub>
    </td>
  </tr>
</table>

### MOM Scenarios / MOM 现场场景

<table>
  <tr>
    <td align="center">
      <img src="./images/mom-quality-station.png" width="320" alt="MOM quality station"/><br/>
      <sub>Quality management station with on-site terminals</sub>
    </td>
    <td align="center">
      <img src="./images/mom-smart-washer.png" width="320" alt="MOM smart washer"/><br/>
      <sub>Smart washer control UI with live hardware</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="./images/mom-projector-ironing.png" width="320" alt="MOM projector ironing station"/><br/>
      <sub>Projector-assisted ironing station with size guidelines</sub>
    </td>
    <td align="center">
      <img src="./images/mom-smart-accessories-cabinet.png" width="320" alt="MOM smart accessories cabinet"/><br/>
      <sub>Smart accessories cabinet workflow (login, open, statistics)</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="./images/mom-customization-app.png" width="320" alt="MOM customization app"/><br/>
      <sub>Mobile app for garment customization and 3D try-on</sub>
    </td>
    <td align="center">
      <img src="./images/accessories-cabinet-design.jpg" width="320" alt="Accessories cabinet design"/><br/>
      <sub>Design drawing of multi-compartment accessories cabinet</sub>
    </td>
  </tr>
</table>

---

## Skills Demonstrated

- **Backend Engineering:** Spring Boot, microservices, REST APIs
- **Database Design:** MySQL, Redis, MongoDB optimization
- **DevOps:** Docker, Jenkins, CI/CD, Linux administration
- **IoT Integration:** Hardware protocols, real-time processing
- **Industrial Data Acquisition:** Electronic scale serial communication (RS232/RS485)
- **Windows Services:** Process monitoring, fault recovery, and long-running device integration
- **Team Leadership:** Cross-functional team management, agile practices
- **System Architecture:** Scalable distributed systems design

---

**Tags:** #Java #SpringBoot #Microservices #IoT #DevOps #Docker #Jenkins #MySQL #Redis #TeamLeadership
