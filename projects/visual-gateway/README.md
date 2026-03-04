# Visual Gateway / IoT Data Visualization Platform

> Industrial IoT gateway for multi-protocol data ingestion, real-time monitoring, alerts, and visualization dashboards.

---

## Overview

An industrial IoT visualization gateway that centralizes and visualizes data from various devices. It supports multiple industrial protocols, real-time monitoring, alert management, and large-screen dashboards. Used in factories, buildings, energy management, and similar scenarios.

**Project Type:** IoT / Industrial IoT / Data Visualization  
**Timeline:** 2018 – 2023  
**Role:** Full-stack Developer / Architecture  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Multi-protocol:** Modbus, MQTT, HTTP, TCP, and others
- **Edge computing:** Local preprocessing and filtering
- **Real-time monitoring:** Device status and metrics visualization
- **Alert management:** Thresholds, anomaly detection, multi-channel notifications
- **Dashboards:** Industrial-grade large-screen displays
- **History:** Storage, query, trend analysis
- **Remote config:** Remote device config and firmware updates
- **High availability:** Hot standby, automatic failover

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Field Devices                   │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │Sensors │ │  PLC   │ │ Smart    │    │
│  │Collectors│ │Controllers│ │ Meters  │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
└──────┼───────────┼──────────┼──────────┘
       │           │          │
       │ Modbus    │ MQTT     │ HTTP
       │ RS485     │ TCP/IP   │ API
       ▼           ▼          ▼
┌─────────────────────────────────────────┐
│         Visual Gateway                  │
│  ┌─────────────────────────────────┐   │
│  │   Protocol adaptation           │   │
│  │   Modbus  MQTT  HTTP  TCP/UDP   │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │   Data processing               │   │
│  │   Parse  Filter  Calculate      │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │   Local services                │   │
│  │   Cache  Rules  Alerts          │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
         ┌─────┴─────┐
         │           │
┌────────▼───┐  ┌────▼──────────┐
│ Local Store│  │ Cloud Sync    │
│ SQLite     │  │ WebSocket     │
└────────────┘  └───────────────┘
                        │
┌───────────────────────▼─────────────────┐
│         Cloud Platform                   │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Time-series│ │ Viz     │ │ Alert   │ │
│  │ Storage  │ │ Dashboard│ │ Center  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

---

## Technologies

### Protocols
- **Modbus RTU/TCP** – Industrial standard
- **MQTT** – IoT messaging
- **HTTP/REST** – API access
- **TCP/UDP** – Custom protocols
- **RS485/RS232** – Serial

### Gateway
- **Java** – Core service
- **Spring Boot** – Application framework
- **Netty** – High-performance I/O
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
- **Docker** – Containerization
- **Linux** – Gateway OS
- **Nginx** – Reverse proxy

---

## Key Achievements

- ✅ **10+ protocols** – Mainstream industrial protocols supported
- ✅ **Sub-100ms latency** – From acquisition to display
- ✅ **24/7 stability** – Industrial-grade uptime
- ✅ **1000+ devices** – Single gateway scale
- ✅ **Multi-scenario** – Factories, buildings, energy, etc.

---

## Responsibilities

### Architecture
- Layered gateway (protocol / processing / service)
- Data flow and storage strategy
- HA and failover design
- Extensibility for new protocols

### Protocol Adapters
- Modbus, MQTT, and other adapters
- Parsing and data transformation
- Custom protocol support
- Serial and network I/O

### Backend
- Data ingestion and preprocessing
- Alert rules and engine
- Storage and query
- Remote config and OTA

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

- **Wide deployment** – Multiple factories and building projects
- **Unified data** – Single gateway for heterogeneous devices
- **Efficiency** – Real-time monitoring reduced manual inspection
- **Cost** – Edge computing reduced bandwidth and cloud cost
- **Digitalization** – Support for enterprise digital initiatives

---

## Evidence

![Gateway architecture](images/gateway-arch.png)
*Visual gateway architecture*

![Dashboard](images/dashboard.png)
*Industrial data dashboard*

![Device monitor](images/device-monitor.png)
*Real-time device monitoring*

---

## Skills Demonstrated

- **Industrial protocols:** Modbus, MQTT, RS485, TCP/IP
- **Backend:** Java, Spring Boot, Netty, high concurrency
- **Visualization:** Vue.js, ECharts, WebSocket, dashboard design
- **Databases:** Time-series, MySQL, Redis, data modeling
- **IoT architecture:** Edge computing, protocol gateway, distributed systems
- **DevOps:** Docker, Linux, deployment and ops

---

**Tags:** #IoT #IndustrialIoT #Modbus #MQTT #DataViz #Java #SpringBoot #Vue.js #EdgeComputing #Gateway
