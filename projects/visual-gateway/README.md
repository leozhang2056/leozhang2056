# Visual Gateway / Breaker Control Gateway Platform

> Gateway-centric platform for unified monitoring and control of serial-connected circuit breakers, with cloud reporting and centralized management.

---

## Overview

A gateway-centric industrial IoT platform built to manage **multiple circuit breakers connected via serial ports (RS485/RS232)**.  
The breakers themselves do **not need direct Internet access**; the gateway collects breaker metrics (current, voltage, power, energy, status), executes open/close control commands, applies local rules/alerts, and reports data to the cloud platform for unified monitoring and operations.

**Project Type:** Android IoT Gateway / Power Control  
**Timeline:** 2018 – 2023  
**Role:** Android Developer / Gateway Control  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Serial breaker access:** One gateway connects and manages many non-networked breakers via RS485/RS232.
- **Per-breaker telemetry:** Real-time current, voltage, power, energy, switch status, and other electrical indicators.
- **Remote open/close control:** Execute breaker ON/OFF commands from web/admin side through the gateway.
- **Unified gateway management:** Centralized management of all breakers under each gateway.
- **Cloud reporting:** Gateway uplinks telemetry and event data to cloud for dashboards and history analysis.
- **Alert rules:** Overcurrent, over/undervoltage, leakage, offline, and abnormal behavior alarms.
- **Edge reliability:** Local cache, retry, and offline buffering when network is unstable.
- **Batch operations:** Group control and scheduled strategies for multiple breaker circuits.

---

## Device Access & Control Flow

1. **Physical wiring:** Breakers connect to gateway serial bus (RS485/RS232), no per-breaker Internet needed.  
2. **Gateway discovery:** Gateway scans addresses and registers breakers/circuits.  
3. **Telemetry collection:** Gateway polls breaker registers for current, voltage, power, energy, and status.  
4. **Cloud sync:** Gateway sends normalized data/events to cloud via MQTT/HTTP.  
5. **Remote control:** Platform sends open/close and parameter commands to gateway, which relays them via serial protocol.  
6. **Alerts & audit:** Rule engine triggers alarms and stores operation/command logs for traceability.

---

## Architecture

```
┌─────────────────────────────────────────┐
│     Serial-connected Circuit Breakers   │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │Breaker │ │Breaker │ │ Breaker  │    │
│  │  #01   │ │  #02   │ │   #N     │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
└──────┼───────────┼──────────┼──────────┘
       │           │          │
       │ Modbus RTU / vendor protocol
       │ RS485 / RS232 serial bus
       ▼           ▼          ▼
┌─────────────────────────────────────────┐
│      Visual Breaker Control Gateway     │
│  ┌─────────────────────────────────┐   │
│  │   Serial protocol adapter       │   │
│  │   Modbus RTU + vendor drivers   │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │   Telemetry & control engine    │   │
│  │   Polling  Parse  Open/Close    │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │   Local services                │   │
│  │   Cache  Rules  Alerts  Retry   │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
         ┌─────┴─────┐
         │           │
┌────────▼───┐  ┌────▼──────────┐
│ Local Store│  │ Cloud Sync    │
│ SQLite     │  │ MQTT / HTTP   │
└────────────┘  └───────────────┘
                        │
┌───────────────────────▼─────────────────┐
│         Cloud Platform                   │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Time-series│ │ Web/App │ │ Alert   │ │
│  │ Storage  │ │ Dashboard│ │ Center  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Gateway  │ │ Breaker  │ │ Command │ │
│  │ Mgmt     │ │ Mgmt     │ │ Audit   │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

---

## Technologies

### Protocols
- **RS232** – Primary serial communication to breakers
- **Modbus RTU / vendor protocol** – Breaker register read/write
- **MQTT** – Gateway-to-cloud telemetry uplink
- **HTTP/REST** – Management APIs

### Android Gateway
- **Android SDK** – Gateway control app runtime
- **Java/Kotlin** – Core implementation
- **SerialPort API** – RS232 polling and command delivery
- **SQLite** – Local embedded DB

### Visualization
- **Vue.js** – Frontend
- **ECharts** – Charts
- **WebSocket** – Real-time push
- **DataV** – Large-screen components

### Storage
- **InfluxDB** – Time-series
- **MySQL** – Config and metadata
- **Redis** – Cache and real-time
- **MongoDB** – Logs and unstructured

### Deployment
- **Android device deployment** – On-site gateway terminals
- **Linux/cloud servers** – Platform services
- **Nginx** – Reverse proxy

---

## Key Achievements

- ✅ **Non-networked breakers enabled** – Existing serial breakers managed without retrofit networking
- ✅ **Unified gateway control** – One gateway centrally controls multiple breaker circuits
- ✅ **Real-time visibility** – Current/voltage/power/status synchronized to cloud dashboards
- ✅ **Reliable operations** – Local buffering + retry ensures stable data in weak-network sites
- ✅ **Scalable deployment** – Multi-gateway management across sites/buildings

---

## Responsibilities

### Architecture
- Android-based gateway control architecture
- RS232 command/data flow design
- Local cache and offline resilience strategy
- Extensibility for new breaker models/protocols

### Protocol Adapters
- Serial Modbus RTU and vendor-specific breaker protocol adapters
- Breaker register mapping and data normalization
- RS232 communication stability and retry control
- Command framing for remote open/close operations

### Backend
- Gateway data ingestion and preprocessing
- Breaker management, grouping, and policy control
- Alert rules and event engine
- Storage, query, and operation audit logs

### Dashboards
- Visualization and layout
- Real-time dashboards
- Alert display
- Responsive layout

---

## Challenges & Solutions

### Challenge 1: Multi-Protocol Compatibility
**Problem:** Different vendors, different protocols.  
**Solution:** Pluggable adapter architecture, standardized data model.

### Challenge 2: High Data Volume
**Problem:** Many devices, high frequency; system load.  
**Solution:** Edge preprocessing, compression, batch write, tiered storage.

### Challenge 3: Real-Time Requirements
**Problem:** Millisecond-level response in industrial use.  
**Solution:** In-memory cache, WebSocket push, async processing, DB tuning.

### Challenge 4: Harsh Environments
**Problem:** EMI, unstable network in the field.  
**Solution:** Resume transfer, local cache, watchdog, hardware hardening.

---

## Results & Impact

- **Lower retrofit cost** – Legacy non-network breakers reused through gateway access
- **Unified control** – Centralized open/close and alarm management per gateway/site
- **Operational efficiency** – Reduced manual on-site switching and inspections
- **Safety improvement** – Faster anomaly detection and response through platform alerts
- **Cloud visibility** – Full historical and real-time breaker data for maintenance decisions

---

## Evidence

> 当前仓库暂未提交该项目截图。补充以下文件到 `images/` 后会自动展示：
> - `gateway-arch.png`
> - `dashboard.png`
> - `device-monitor.png`

---

## Skills Demonstrated

- **Android gateway development:** Android SDK, Java/Kotlin, device integration
- **Industrial protocols:** RS232, Modbus RTU, MQTT
- **Gateway logic:** Breaker polling, command control, retry, local cache
- **Visualization:** Vue.js, ECharts, WebSocket, dashboard design
- **Databases:** Time-series, MySQL, Redis, data modeling
- **IoT architecture:** Edge gateway, serial bus control, cloud synchronization
- **Deployment:** On-site Android terminals, Linux server operations

---

**Tags:** #Android #IoT #RS232 #ModbusRTU #Gateway #BreakerControl #MQTT #DataViz
