# Smart Factory Backend System

> Microservice-based manufacturing platform deployed across 5+ factory sites

---

## Overview

Led the development of a comprehensive microservice-based backend system for textile manufacturing operations. The platform manages production workflows, inventory tracking, and IoT device integration across multiple manufacturing sites, supporting hundreds of workers daily.

**Project Type:** Enterprise System / Industrial IoT  
**Timeline:** 2018 - 2024  
**Role:** Technical Lead  
**Company:** Chunxiao Technology Co., Ltd., China  
**Team Size:** 6 people (cross-functional)

---

## Key Features

- **Microservice Architecture:** Scalable, modular backend services
- **IoT Integration:** Real-time tracking via RFID, barcode scanners, conveyors
- **Production Management:** Workflow orchestration and process tracking
- **Multi-site Deployment:** Supports 5+ manufacturing locations
- **High Availability:** 99.9% uptime maintained
- **CI/CD Pipeline:** Automated deployment and testing
- **Real-time Monitoring:** Live production status and alerts

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
│   (RFID, Barcode, Conveyors)       │
└─────────────────────────────────────┘
```

---

## Technologies

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

---

## Challenges & Solutions

### Challenge 1: Multi-site Synchronization
**Problem:** Keeping data consistent across 5+ factory locations  
**Solution:** Distributed architecture with centralized configuration management

### Challenge 2: Hardware Integration Complexity
**Problem:** Integrating diverse IoT devices with different protocols  
**Solution:** Unified device abstraction layer and protocol adapters

### Challenge 3: High Availability Requirements
**Problem:** Manufacturing cannot tolerate system downtime  
**Solution:** Redundant deployments, automated failover, and comprehensive monitoring

### Challenge 4: Team Coordination
**Problem:** Coordinating Android, backend, and hardware teams  
**Solution:** Agile methodologies, clear documentation, and regular sync meetings

---

## Results & Impact

- **Operational Excellence:** System supports daily operations for hundreds of workers
- **Efficiency Gains:** Production efficiency improved by 30%+
- **Scalability:** Successfully scaled from 1 to 5+ sites
- **Reliability:** Achieved and maintained 99.9% uptime
- **Team Development:** Successfully mentored and led 6-person team

---

## Evidence

![System Architecture](images/arch.png)
*Microservice architecture diagram*

![Dashboard](images/dashboard.png)
*Production monitoring dashboard*

![IoT Integration](images/iot.png)
*Hardware integration setup*

---

## Skills Demonstrated

- **Backend Engineering:** Spring Boot, microservices, REST APIs
- **Database Design:** MySQL, Redis, MongoDB optimization
- **DevOps:** Docker, Jenkins, CI/CD, Linux administration
- **IoT Integration:** Hardware protocols, real-time processing
- **Team Leadership:** Cross-functional team management, agile practices
- **System Architecture:** Scalable distributed systems design

---

**Tags:** #Java #SpringBoot #Microservices #IoT #DevOps #Docker #Jenkins #MySQL #Redis #TeamLeadership
