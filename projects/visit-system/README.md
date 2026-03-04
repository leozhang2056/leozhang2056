# Visit Booking & Access Management System

> Smart visit booking and access management platform for high-security sites (especially prisons), with admin portal, client terminals, and visitor-side apps.

---

## Overview

A visit booking and access management **platform** designed for high-security scenarios such as **prison visitation** (and can be adapted to hospitals, ICUs, NICUs, infectious wards, etc.).  
The system provides a **management side, client/terminal side, and visitor side**: families use mobile/mini‑program to make appointments, on-site terminals handle face-based identity verification and gate control, and the admin backend manages visit rules, approvals, schedules, and statistics.

**Project Type:** Security Visit Platform / Face Recognition / Audio-Video  
**Timeline:** 2020 – 2022  
**Role:** Full-stack Developer  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Multi-role platform:** Separate experiences for prison/hospital admin, on-site terminals, and visitors/family.
- **Online visit booking:** Families book visit time slots in advance, reducing on-site queuing and conflict.
- **Approval & quota rules:** Configurable visit policies (frequency, duration, number of visitors, relationship, blacklist, etc.).
- **Face recognition access:** Face-based entry/exit at gates or doors; blocks unauthorized or expired visits.
- **Time management:** Automatic visit timing, warnings before end of slot, and automatic end of visit.
- **Remote video visits:** Video visitation for special periods (e.g., epidemic) or remote relatives.
- **Family & inmate management:** Family registration, relationship binding, and face database management.
- **Statistics & audit:** Visit records, frequency analysis, abnormal behavior tracing, and audit logs.

---

## Core Subsystems / 核心子系统

The platform is built around three main subsystems, with **audio-video session management** at the center of remote visits:

| Subsystem | Role |
|-----------|------|
| **预约系统（Booking）** | Time-slot reservation, approval workflow, visit rules, and family/inmate binding. |
| **音视频系统（A/V）** | Real-time audio/video calls between visitors and inmates; session creation, join/leave, duration control, and quality management. |
| **聊天系统（Chat）** | Text messaging between parties (e.g., pre/post visit), message history, and moderation where required. |

- **音视频会话管理（A/V session management）：** Create and manage A/V sessions (e.g., one-to-one video visit), control who can join, set max duration, handle reconnection and end-of-session cleanup, and optionally record or archive for compliance.

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Access Terminal Devices         │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │Face Rec│ │Access  │ │ Display  │    │
│  │ Camera │ │Lock    │ │ & Prompt  │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │IC Card │ │QR Code │ │ Voice    │    │
│  │ Reader │ │Scanner │ │ Announce │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
└──────┼───────────┼──────────┼──────────┘
       │           │          │
       └───────────┴──────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Android Terminal Control           │
│  ┌─────────────────────────────────┐   │
│  │  - Face recognition & match      │   │
│  │  - Access lock control           │   │
│  │  - Local face database           │   │
│  │  - Network sync & offline mode   │   │
│  └─────────────────────────────────┘   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│        Visit Management Platform         │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Booking  │ │ Family   │ │ Visit   │ │
│  │ & Slots  │ │ Face DB  │ │ Records │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Video    │ │ Reports  │ │ System  │ │
│  │ Visit    │ │ & Stats  │ │ Config  │ │
│  │ HIS      │ │          │ │         │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

---

## Technologies

### Face Recognition
- **Face detection** – Fast detection
- **Face SDK** – High-accuracy matching
- **Liveness** – Anti photo/video spoofing
- **Face database** – Family feature management

### Access Control
- **Electromagnetic lock** – Door control
- **Door sensor** – Door state
- **IR sensor** – Presence detection
- **Voice** – Prompts and guidance

### Mobile
- **WeChat Mini Program** – Family booking
- **Android app** – On-site terminal / staff side
- **Web admin** – Prison/hospital management portal

### Backend
- **Spring Boot** – Business services
- **MySQL** – Data storage
- **Redis** – Cache and session
- **WebRTC** – Real-time audio/video; A/V session management (create, join, leave, timeout, recording)
- **IM / Chat** – Chat system for text messages and history

### Integration
- **Prison/Hospital data interface** – Optional external system integration
- **WeChat template messages** – Booking and visit notifications
- **SMS gateway** – SMS notifications

---

## Key Achievements

- ✅ **<1s recognition** – Face recognition speed
- ✅ **99.5% accuracy** – Face recognition accuracy
- ✅ **~30% efficiency gain** – Visit management
- ✅ **Multi-site deployment** – Adapted to different high-security visit scenarios
- ✅ **Session compliance** – Audio-video session lifecycle under policy control

---

## Responsibilities

### Face Recognition
- Access terminal face recognition
- Feature extraction and matching
- Liveness anti-spoofing
- Local face DB and sync

### Access Control
- Lock control logic
- Door state and alarms
- Voice announcements
- Exception handling

### Booking
- WeChat Mini Program booking
- Time slot management
- Reminders and notifications
- Booking statistics

### Chat System
- Text messaging between visitors and inmates
- Message history and moderation
- Integration with visit and A/V flows

### Audio-Video & Session Management
- WebRTC-based real-time audio/video
- A/V session lifecycle (create, join, leave, timeout)
- Duration control and end-of-session cleanup
- Room/session management and optional recording

### Admin
- Family and face DB management
- Visit record query
- Reports
- HIS integration

---

## Challenges & Solutions

### Challenge 1: Masked Faces
**Problem:** Masks during pandemic reduced recognition.  
**Solution:** Mask-aware algorithm, stronger eye-region features.

### Challenge 2: Unstable Network
**Problem:** Complex on-site networks in security facilities.  
**Solution:** Local face cache, offline recognition, sync when online.

### Challenge 3: Visit Duration
**Problem:** Strict time limits, no overstay.  
**Solution:** Auto timer, advance reminder, auto lock at end of slot.

### Challenge 4: Privacy
**Problem:** Family data and visit records must be protected.  
**Solution:** Encrypted storage, access control, audit logs.

---

## Results & Impact

- **Efficiency** – ~30% improvement in visit management
- **Order** – Less congestion at peak times
- **Security** – Unauthorized access prevented
- **Compliance** – Session timing and operation logs for traceability
- **Data** – Visit data for management and audit
- **Satisfaction** – Booking reduced wait time

---

## Evidence

> 当前仓库暂未提交该项目截图。补充以下文件到 `images/` 后会自动展示：
> - `access-terminal.png`
> - `booking-miniapp.png`
> - `visit-admin.png`

---

## Skills Demonstrated

- **Face recognition:** Detection, features, liveness
- **Android:** Terminal app, hardware integration
- **WeChat Mini Program:** Booking, UX
- **Video:** WebRTC, real-time communication
- **Backend:** Spring Boot, data management
- **Healthcare:** HIS integration, data security

---

**Tags:** #FaceRecognition #AccessControl #BookingSystem #ChatSystem #WebRTC #PrisonVisitation #SecurityPlatform
