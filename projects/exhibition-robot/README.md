# Exhibition Service Robot

> Intelligent exhibition service robot for guided tours, reception, and information queries at trade shows, malls, museums, and similar venues.

---

## Overview

An intelligent exhibition service robot system that provides guided tours, reception, information lookup, and related services at exhibitions, malls, museums, and similar scenarios. It supports voice interaction, face recognition, autonomous navigation, and customizable content. **The project was carried out mainly in 2019**; AI technology was not yet mature at the time, so the solution used rule-based logic combined with existing ASR/TTS and face APIs rather than large models or deep conversational AI.

**Project Type:** AI / Robotics / Service Automation  
**Timeline:** Primarily **2019**  
**Role:** Full-stack Developer / System Integration  
**Company:** Chunxiao Technology Co., Ltd., China

---

## Key Features

- **Voice Interaction:** Speech recognition and synthesis, natural-language dialogue
- **Face Recognition:** Visitor identification, VIP greeting, attendance statistics
- **Autonomous Navigation:** SLAM mapping, path planning, obstacle avoidance
- **Guided Tours:** Fixed-point narration, automatic patrol, content push
- **Information Query:** Exhibition info, booth navigation, schedule lookup
- **Multimodal Interaction:** Voice, touchscreen, and gesture input
- **Remote Monitoring:** Real-time monitoring, remote control, data analytics
- **Content Customization:** Configurable content and interaction logic

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Robot Hardware Layer          │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │ Chassis│ │ Lidar  │ │Depth Cam │    │
│  │Diff-drive│ │ SLAM  │ │ RGB-D    │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
│  ┌────────┐ ┌────────┐ ┌──────────┐    │
│  │ Voice  │ │ Display│ │Ultrasonic│    │
│  │ Mic    │ │Touch   │ │ Obstacle │    │
│  └───┬────┘ └────┬───┘ └────┬─────┘    │
└──────┼───────────┼──────────┼──────────┘
       │           │          │
       └───────────┴──────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Android / ROS Main Control         │
│  ┌─────────────────────────────────┐   │
│  │  - SLAM mapping & localization  │   │
│  │  - Path planning & navigation   │   │
│  │  - Voice interaction pipeline  │   │
│  │  - Face recognition            │   │
│  │  - Motion control              │   │
│  └─────────────────────────────────┘   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Cloud / Backend Services         │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Dialogue│ │ Content  │ │ Remote  │ │
│  │ NLP Svc │ │ Booth    │ │ Monitor │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

---

## Technologies

### Robot Stack
- **ROS (Robot Operating System)** – Robot middleware
- **Android** – Application and UI layer
- **SLAM** – Autonomous navigation and mapping
- **OpenCV** – Computer vision
- **PCL** – Point cloud processing

### AI Capabilities
- **ASR (Speech Recognition)** – Baidu / iFlytek / Alibaba APIs
- **TTS (Speech Synthesis)** – Voice playback
- **NLP** – Intent recognition, dialogue management
- **Face Recognition** – Visitor ID, VIP greeting
- **Person Detection** – Footfall and heatmap stats

### Motion Control
- **Differential drive** – Kinematic model
- **Path planning** – A*, Dijkstra
- **Obstacle avoidance** – Dynamic Window Approach (DWA)
- **PID control** – Velocity closed-loop

### Sensors
- **Lidar** – 2D/3D environment scan
- **Depth camera** – RGB-D vision
- **Ultrasonic** – Short-range obstacle detection
- **IMU** – Inertial measurement
- **Encoders** – Odometry

### Backend
- **Spring Cloud** – Business services
- **WebSocket** – Real-time communication
- **MQTT** – Device communication
- **MySQL** – Data storage
- **Redis** – Caching

---

## Key Achievements

- ✅ **Autonomous navigation** – Centimeter-level localization, stable in complex environments
- ✅ **Natural dialogue** – Multi-turn conversation, >90% understanding rate
- ✅ **Face recognition** – Sub-second recognition, >98% accuracy
- ✅ **Multi-venue deployment** – Deployed at multiple exhibitions and malls
- ✅ **24/7 operation** – Round-the-clock service during events
- ✅ **Footfall analytics** – Automatic visitor counts and heatmaps

---

## Responsibilities

### System Integration
- ROS and Android integration
- Sensor drivers (lidar, depth camera)
- Voice module integration (mic array, speakers)
- Motion control tuning and parameter optimization

### Software Development
- Android interaction app
- Voice dialogue system
- Face recognition integration
- Navigation and obstacle-avoidance tuning
- Remote monitoring backend

### AI Integration
- ASR/TTS service integration
- NLP dialogue management
- Face recognition model optimization
- Custom Q&A and content configuration

### Content & Customization
- Exhibition content planning and data entry
- Tour route planning
- Interaction flow design
- Multilingual support (Chinese, English)

---

## Challenges & Solutions

### Challenge 1: Navigation in Crowded Environments
**Problem:** Dense crowds and highly dynamic exhibition floors.  
**Solution:** Multi-sensor fusion, dynamic obstacle avoidance, optional manual override.

### Challenge 2: Speech Recognition in Noisy Environments
**Problem:** High ambient noise reduces ASR accuracy.  
**Solution:** Mic array noise reduction, near-field pickup, touchscreen fallback.

### Challenge 3: Long-Duration Reliability
**Problem:** Multi-day continuous operation during events.  
**Solution:** Auto docking/recharge, fault recovery, remote ops and monitoring.

### Challenge 4: Multi-Scenario Adaptation
**Problem:** Different venues and content per exhibition.  
**Solution:** Modular software, visual configuration tools, streamlined deployment.

---

## Results & Impact

- **Exhibition impact** – Highlight of events, high visitor engagement
- **Service level** – 24/7 automated service, reduced manual workload
- **Data value** – Visitor analytics for organizers
- **Brand** – Strong tech showcase, improved brand image
- **Reuse** – Applicable to exhibitions, malls, museums, and similar venues

---

## Evidence

### Robot Hardware & Design

<table>
  <tr>
    <td align="center">
      <img src="./images/robot_compenent.png" width="280" alt="Hardware component diagram with annotated features"/><br/>
      <sub>Hardware component diagram with annotated features</sub>
    </td>
    <td align="center">
      <img src="./images/robot_face.png" width="280" alt="Full-body robot photo with touchscreen and mobility base"/><br/>
      <sub>Full-body robot photo with touchscreen and mobility base</sub>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <img src="./images/robot_screen.png" width="400" alt="Mobile app interface with camera feed and troubleshooting"/><br/>
      <sub>Mobile app interface with camera feed and troubleshooting</sub>
    </td>
  </tr>
</table>

### Navigation & Mapping

<table>
  <tr>
    <td align="center">
      <img src="./images/map1.png" width="280" alt="Route comparison: straight-line vs U-shaped paths"/><br/>
      <sub>Route comparison: straight-line vs U-shaped paths</sub>
    </td>
    <td align="center">
      <img src="./images/map2.png" width="280" alt="SLAM mapping with virtual warehouse editing mode"/><br/>
      <sub>SLAM mapping with virtual warehouse editing mode</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="./images/map3.png" width="280" alt="Special area editing with dimension annotations"/><br/>
      <sub>Special area editing with dimension annotations</sub>
    </td>
    <td align="center">
      <img src="./images/map4.png" width="280" alt="Waypoint marking and navigation route management"/><br/>
      <sub>Waypoint marking and navigation route management</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="./images/map5.png" width="280" alt="Navigation calibration with waypoint coordinates"/><br/>
      <sub>Navigation calibration with waypoint coordinates</sub>
    </td>
    <td align="center">
      <img src="./images/map_scan.png" width="280" alt="SLAM scanning mode with trajectory lines"/><br/>
      <sub>SLAM scanning mode with trajectory lines</sub>
    </td>
  </tr>
</table>

### Interaction & Management

<table>
  <tr>
    <td align="center">
      <img src="./images/knowledge.png" width="400" alt="Admin backend with knowledge base association settings"/><br/>
      <sub>Admin backend with knowledge base association settings</sub>
    </td>
  </tr>
</table>

---

## Skills Demonstrated

- **Robotics:** ROS, SLAM, motion control
- **Android:** Robot interaction application
- **AI integration:** ASR/TTS, NLP, face recognition
- **Sensor fusion:** Lidar, depth camera, IMU
- **Backend:** Spring Cloud, WebSocket, remote monitoring
- **System integration:** Hardware–software co-development, multi-system coordination

---

**Tags:** #Robotics #ROS #SLAM #AI #VoiceInteraction #FaceRecognition #AutonomousNavigation #Android #Exhibition
