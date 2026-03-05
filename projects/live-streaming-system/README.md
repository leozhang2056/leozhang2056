# Live Streaming Commerce System

> A 2018 live streaming project focused on audio/video broadcasting and online shopping, with Android client-side implementation for live viewing and interactive purchase scenarios.

---

## Overview

This project is a **live streaming + e-commerce** system for online real-time content and shopping conversion.  
Users can watch live sessions and complete product purchase actions during the stream.

The project includes audio/video transmission capability, live room interaction, and shopping flow integration on the mobile client.

**Project Type:** Live Streaming / Live Commerce  
**Timeline:** 2018  
**Role:** Android Client Developer  
**Company:** TBD

---

## My Responsibilities

- Developed Android live streaming client modules and user-facing features.
- Implemented core live room experiences: stream playback, room entry/exit, and interaction flow.
- Integrated live streaming with online shopping process on mobile side.
- Participated in audio/video transmission-related client optimization and playback stability tuning.
- Collaborated with backend and product teams for protocol alignment and release delivery.

---

## Key Capabilities

- **Live stream playback:** Mobile live room video/audio viewing experience.
- **Live interaction flow:** User interaction features in live sessions.
- **Live commerce integration:** Product display and purchase path during live stream.
- **Audio/video transport support:** Client integration for streaming transmission and decoding pipeline.
- **Playback stability optimization:** Improved startup, buffering handling, and weak-network tolerance.
- **Session and status sync:** Basic live room state synchronization with backend services.

---

## Typical User Flow

1. User enters a live room from the app home/live list.
2. Android client connects to live stream source and starts playback.
3. User interacts with live content while browsing recommended products.
4. User enters product detail/order flow during the live session.
5. Client reports playback and interaction status for service-side analytics/monitoring.

---

## Architecture (Conceptual)

```
┌────────────────────────────────────────────────────┐
│                   Android Client                    │
│ Live Room UI | Player | Interaction | Shopping Flow │
└─────────────────────────────┬───────────────────────┘
                              │
                   A/V Stream + API Requests
                              │
┌─────────────────────────────▼───────────────────────┐
│                    Platform Services                 │
│ Live Service | User Service | Product/Order Service │
└─────────────────────────────┬───────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────┐
│                Streaming Infrastructure              │
│ Ingest/Transcode/CDN Delivery (per deployment)      │
└──────────────────────────────────────────────────────┘
```

---

## Project Impact

- Delivered mobile live streaming capability for business usage scenarios.
- Enabled live shopping experience by linking stream traffic to purchase flow.
- Improved client-side playback robustness for real-time streaming sessions.
- Built reusable Android-side live module foundation for future iterations.

---

## Evidence

> No screenshots committed yet.  
> Suggested files under `images/`:
> - `live-room-ui.png`
> - `streaming-flow.png`
> - `live-commerce-path.png`

---

## Skills Demonstrated

- Android client development
- Live streaming app development
- Audio/video transmission integration
- Streaming playback optimization
- Live commerce interaction design

---

**Tags:** #Android #LiveStreaming #LiveCommerce #AudioVideo #MobileDevelopment
