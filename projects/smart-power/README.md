# Smart Power Management System

> Enterprise power monitoring, energy analysis, and optimization for factories, buildings, and campuses.

---

## Overview

A smart power management system that provides monitoring, energy analysis, and optimization for enterprises. It supports real-time data collection, consumption analysis, fault alerts, and remote control, helping factories, buildings, and campuses manage energy intelligently.

**Project Type:** IoT / Energy Management / Industrial Automation  
**Timeline:** 2019 – 2022  
**Role:** Full-stack Developer / System Architecture  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Real-time monitoring:** Current, voltage, power, energy, and other parameters in real time
- **Energy analysis:** Time-of-use stats, peak/valley analysis, consumption trends
- **Fault alerts:** Overload, leakage, temperature anomalies, and other safety alerts
- **Remote control:** Remote switching, scheduled tasks, policy execution
- **Reporting:** Multi-dimensional reports with export
- **Energy optimization:** Baseline comparison and optimization suggestions
- **Multi-tenant:** Multi-campus and multi-building hierarchy
- **Mobile:** App for real-time viewing and control

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Field Device Layer               │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │ Smart  │ │Temp/   │ │Circuit   │    │
│  │ Meters │ │Humidity│ │Breakers  │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │Reactive│ │Harmonic│ │Leakage   │    │
│  │Compens.│ │Monitor │ │Protection│    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
└──────┼───────────┼──────────┼──────────┘
       │ RS485    │ 4-20mA   │ Modbus
       └───────────┴──────────┘
                   │
┌──────────────────▼──────────────────────┐
│        Data Acquisition Gateway         │
│  ┌─────────────────────────────────┐   │
│  │  - Modbus/RS485 protocol        │   │
│  │  - Preprocessing & cache         │   │
│  │  - Edge logic (thresholds)       │   │
│  │  - Offline buffer & sync         │   │
│  └─────────────────────────────────┘   │
└──────────────────┬──────────────────────┘
                   │ MQTT/HTTP
┌──────────────────▼──────────────────────┐
│        Cloud Platform                    │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Data     │ │ Analytics│ │ Alert   │ │
│  │ Ingest   │ │ Engine   │ │ Center  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Reports  │ │ Device   │ │ User    │ │
│  │ Service  │ │ Mgmt     │ │ Service │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

---

## Technologies

### Hardware
- **Smart meters** – Three-phase/single-phase multi-function
- **Sensors** – Temperature, humidity, smoke
- **Circuit breakers** – Smart breakers with remote control
- **Reactive compensation** – Power factor correction
- **Harmonic monitoring** – Power quality

### Protocols
- **Modbus RTU/TCP** – Meter communication
- **RS485** – Field bus
- **MQTT** – IoT messaging
- **DL/T645** – Power industry standard
- **HTTP/REST** – APIs

### Backend
- **Spring Boot** – Microservices
- **InfluxDB** – Time-series data
- **MySQL** – Business data and config
- **Redis** – Cache and real-time data
- **RabbitMQ** – Message queue

### Data Processing
- **Apache Flink** – Stream processing
- **Elasticsearch** – Log and alert search
- **Quartz** – Scheduled jobs

### Frontend
- **Vue.js** – Admin UI
- **ECharts** – Charts
- **DataV** – Large-screen display
- **UniApp** – Mobile app

---

## Key Achievements

- ✅ **~15% energy reduction** – Via analysis and optimization
- ✅ **<1s alerts** – Near real-time anomaly push
- ✅ **99.9% collection rate** – Data completeness
- ✅ **Multi-campus** – 3+ campuses under one platform
- ✅ **Remote control** – Fast response to faults

---

## Responsibilities

### Architecture
- Layered design (devices – gateway – platform)
- Protocol and data format standards
- High-throughput data pipeline
- Alert rules and policy engine

### Gateway
- Modbus/RS485 data collection
- Edge computation and local alerts
- Offline buffer and sync
- Device discovery and auto-config

### Backend
- Data ingestion and parsing
- Real-time computation and aggregation
- Alert engine and notifications
- Report generation and export
- Device management and remote control APIs

### Visualization
- Energy dashboards and large screens
- Real-time monitoring
- Historical trends
- Mobile app

---

## Challenges & Solutions

### Challenge 1: High Data Volume
**Problem:** Thousands of meters, high-frequency data.  
**Solution:** InfluxDB time-series DB, tiered storage, hot/cold separation.

### Challenge 2: Real-Time Alerts
**Problem:** Sub-second response to anomalies.  
**Solution:** Edge + cloud, multi-level alerts, message queue.

### Challenge 3: Device Compatibility
**Problem:** Different meter vendors and protocols.  
**Solution:** Configurable protocol adapters for mainstream meters.

### Challenge 4: Data Accuracy
**Problem:** Interference causing loss or errors.  
**Solution:** Validation, retry, anomaly cleaning.

---

## Results & Impact

- **Energy savings** – ~15% average reduction, lower costs
- **Safety** – Timely detection of overload, leakage, etc.
- **Efficiency** – Remote reading replaced manual; ~80% efficiency gain
- **Decision support** – Data-driven consumption strategy
- **Sustainability** – Support for green/low-carbon goals

---

## Evidence

![Power dashboard](images/power-dashboard.png)
*Smart power monitoring dashboard*

![Data analysis](images/data-analysis.png)
*Energy analysis and trends*

![Alarm center](images/alarm-center.png)
*Real-time alerts and notifications*

---

## Skills Demonstrated

- **IoT acquisition:** Modbus, RS485, smart meters, sensors
- **Time-series DB:** InfluxDB, data modeling, query optimization
- **Stream processing:** Apache Flink, aggregation
- **Backend:** Spring Boot, microservices, high concurrency
- **Visualization:** ECharts, DataV, dashboard design
- **Mobile:** UniApp, cross-platform

---

**Tags:** #IoT #EnergyManagement #SmartMeters #Modbus #InfluxDB #Analytics #IndustrialAutomation
