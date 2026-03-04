# Picture Book Locker / Smart Library Cabinet

> 24/7 self-service borrow/return for school and community libraries, with face recognition, QR code, and card support.

---

## Overview

A smart picture-book locker system for school and community libraries. It provides 24-hour self-service borrow and return with face recognition, QR code, and card options, plus smart lighting and UV disinfection for hygienic book handling.

**Project Type:** IoT / Smart Library / Self-Service  
**Timeline:** 2020 – 2023  
**Role:** Android Developer / Embedded Development  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Face recognition borrow:** Quick borrow/return by face
- **Multiple auth:** QR code, IC card, PIN
- **Smart doors:** Auto-open target compartment, LED guidance
- **UV disinfection:** Built-in UV module
- **Inventory:** Real-time stock and location
- **Borrow history:** Full history and overdue reminders
- **Admin:** Stock management, analytics, remote monitoring
- **Multi-cabinet:** Multiple units networked and managed together

---

## Architecture

```
┌─────────────────────────────────────────┐
│            Hardware Layer               │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │ Main   │ │Solenoid│ │ UV       │    │
│  │ Board  │ │ Lock   │ │ Module   │    │
│  │ (ARM)  │ │Control │ │          │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │Face Rec│ │QR Code │ │ LED      │    │
│  │ Camera │ │Scanner │ │ Strip    │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
└──────┼───────────┼──────────┼──────────┘
       │           │          │
       └───────────┴──────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Android Main Control                │
│  ┌─────────────────────────────────┐   │
│  │  - Face recognition SDK         │   │
│  │  - QR code scan                  │   │
│  │  - Serial (lock/sensors)         │   │
│  │  - Local DB                      │   │
│  │  - Network sync                  │   │
│  └─────────────────────────────────┘   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Backend (Spring Boot)              │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Borrow   │ │ Book     │ │ User    │ │
│  │ Inventory│ │ Notify   │ │ Stats   │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

---

## Technologies

### Android
- **Android SDK** – Main control app
- **Java/Kotlin** – Language
- **Face SDK** – Face auth
- **ZXing** – QR scanning
- **SQLite** – Local cache

### Embedded
- **ARM main board** – Controller
- **Solenoid lock** – Door control
- **UART/RS485** – Hardware comms
- **GPIO** – LED, UV control
- **Sensors** – Door, temperature, etc.

### Backend
- **Spring Boot** – Services
- **MySQL** – Business data
- **Redis** – Cache and session
- **MQTT** – Device communication

### Third-Party
- **WeChat/Alipay** – Scan auth (optional)
- **SMS** – Notifications
- **Push** – Mobile notifications

---

## Key Achievements

- ✅ **24/7 service** – Unmanned self-service
- ✅ **<3s borrow** – Average face-based borrow time
- ✅ **Multi-site** – Deployed in multiple schools and libraries
- ✅ **UV disinfection** – Automatic book disinfection
- ✅ **Zero loss** – Lock control for book security

---

## Responsibilities

### Android
- Locker main control app
- Face recognition and QR integration
- Serial communication and hardware
- Local DB and sync logic
- UI and flows

### Hardware
- Solenoid lock integration
- LED strip control
- UV module scheduling
- Sensor data
- Fault detection and alerts

### Backend
- Book management APIs
- Borrow record service
- User auth and permissions
- Notifications
- Reports and stats

### Deployment
- On-site installation and debugging
- Hardware integration testing
- User training and handover

---

## Challenges & Solutions

### Challenge 1: Face Recognition Accuracy
**Problem:** Children’s faces harder to recognize.  
**Solution:** Camera angle and lighting, child-optimized face algorithm.

### Challenge 2: Hardware Reliability
**Problem:** Solenoid locks overheating over time.  
**Solution:** Cooling, periodic checks, automatic failover.

### Challenge 3: Unstable Network
**Problem:** Poor library network, frequent disconnects.  
**Solution:** Offline mode, local cache, resume sync.

### Challenge 4: Book Size Variation
**Problem:** Different book sizes, compartment design.  
**Solution:** Multiple compartment sizes, allocation logic.

---

## Results & Impact

- **Convenience** – Students can borrow/return anytime
- **Extended hours** – 24/7 beyond library opening
- **Hygiene** – UV disinfection for children
- **Efficiency** – Auto stats and reports, less manual work
- **Multi-scenario** – Schools, communities, malls

---

## Evidence

### Hardware & Deployment / 硬件与部署现场

![Picture book locker front](./images/picture-book-locker-front.png)  
*Deployed picture-book locker with visible book slots and screen*

![Campus hallway deployment](./images/picture-book-locker-campus-hall.png)  
*Two picture-book lockers installed in a school canteen corridor*

![Smart library room exterior](./images/smart-library-room-exterior.jpg)  
*24/7 smart library room built around the locker system*

![Bank of China deployment](./images/picture-book-locker-bank-of-china.png)  
*Outdoor deployment in front of a public site*

### Locker Variants / 柜机款式

![Locker exterior blue](./images/locker-exterior-blue-site.png)  
*Blue locker cabinet with integrated touch screen*

![Locker exterior green](./images/locker-exterior-green.jpg)  
*Green picture-book locker with dense slots*

![Locker exterior red](./images/locker-exterior-red.jpg)  
*Red/grey locker variant with high capacity*

![Locker exterior with gates](./images/locker-exterior-with-gates.png)  
*Locker with anti-theft gates for entrance/exit control*

![Locker exterior with gates (alt)](./images/locker-exterior-with-gates-alt.png)  
*Alternative angle of locker plus gate combination*

### UV & Night Mode / 消毒与夜间效果

![Picture-book locker UV mode](./images/picture-book-locker-uv-mode.png)  
*Locker running with illuminated UV/lighting effect*

![Borrow UI close-up](./images/borrow-ui-closeup.png)  
*Touch screen UI for borrow / return / exchange*

![Borrow UI on device](./images/borrow-ui-on-device.png)  
*Borrow UI running on the actual locker device*

### Related Devices & Concept / 相关设备与概念图

![Cartoon illustration locker](./images/locker-illustration-cartoon.png)  
*Concept illustration showing a user interacting with the locker*

![Smart cabinet recycle style](./images/smart-cabinet-recycle-style.jpg)  
*Another IoT cabinet form factor used in similar scenarios*

---

## Skills Demonstrated

- **Android:** Main control app, face recognition, QR scan
- **Embedded:** Serial, GPIO, hardware integration
- **IoT:** Device networking, MQTT, remote management
- **Hardware:** Solenoid lock, LED, sensors
- **Backend:** Spring Boot, book management logic

---

**Tags:** #IoT #Android #FaceRecognition #QRCode #SmartLocker #Library #Embedded #SpringBoot
