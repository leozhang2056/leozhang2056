# Hospital Visit Management System

> Smart visit management for ICU, NICU, infectious wards: face-based access, booking, time control, and remote video visits.

---

## Overview

A hospital visit management system for special wards (ICU, NICU, infectious disease, etc.). It provides face recognition access, booking, visit duration control, and remote video visits, improving both management efficiency and visitor experience.

**Project Type:** Healthcare IT / Smart Hardware / Face Recognition  
**Timeline:** 2020 – 2022  
**Role:** Full-stack Developer  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Face recognition access:** Face-based entry/exit; blocks unauthorized access
- **Visit booking:** Online booking of time slots to avoid queues
- **Time management:** Automatic duration control and end-of-slot reminders
- **Remote video visits:** Video visits to reduce cross-infection risk
- **Family management:** Family registration and face database management
- **Staff channel:** Dedicated fast lane for medical staff
- **Statistics:** Visit records and footfall analysis
- **HIS integration:** Integration with hospital information systems

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
- **Android app** – Management
- **Web admin** – Hospital management

### Backend
- **Spring Boot** – Business services
- **MySQL** – Data storage
- **Redis** – Cache and session
- **WebRTC** – Video visits

### Integration
- **HIS interface** – Hospital system integration
- **WeChat template messages** – Notifications
- **SMS gateway** – SMS notifications

---

## Key Achievements

- ✅ **<1s recognition** – Face recognition speed
- ✅ **99.5% accuracy** – Face recognition accuracy
- ✅ **~30% efficiency gain** – Visit management
- ✅ **Multi-ward deployment** – ICU, NICU, infectious, etc.
- ✅ **Contact reduction** – Remote video during pandemic

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

### Video Visits
- WebRTC integration
- Room management
- Duration control
- Recording and archive

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
**Problem:** Complex hospital networks.  
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
- **Infection control** – Less contact; remote video option
- **Data** – Visit data for hospital management
- **Satisfaction** – Booking reduced wait time

---

## Evidence

![Access terminal](images/access-terminal.png)
*Face recognition access terminal*

![Booking miniapp](images/booking-miniapp.png)
*Family booking WeChat Mini Program*

![Visit admin](images/visit-admin.png)
*Visit management backend*

---

## Skills Demonstrated

- **Face recognition:** Detection, features, liveness
- **Android:** Terminal app, hardware integration
- **WeChat Mini Program:** Booking, UX
- **Video:** WebRTC, real-time communication
- **Backend:** Spring Boot, data management
- **Healthcare:** HIS integration, data security

---

**Tags:** #FaceRecognition #Healthcare #AccessControl #WeChatMiniapp #Android #WebRTC #Hospital
