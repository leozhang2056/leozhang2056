# Live Streaming Commerce System

**Multi-Language Live Streaming Platform (.NET + Android + C++)**

A comprehensive live streaming commerce platform developed from 2015 to 2018, featuring a **multi-language technology stack** including .NET Framework (ASP.NET), Android (Java/Kotlin), C++ (streaming core), Python (data processing), and Lua (scripting). The system delivered real-time live streaming with integrated e-commerce capabilities across mobile and web platforms.

> **Tech Stack:** .NET Framework | ASP.NET | C# | C++ | Python | Lua | Java | Kotlin | Android NDK

---

## 🎯 Project Overview

This project represents a **3-year full-stack development** effort (2015-2018) building a live streaming commerce platform. It showcases expertise in **multi-language system architecture**, combining Microsoft's .NET ecosystem with native mobile development and scripting languages.

**Key Capabilities:**
- Real-time live streaming with low-latency playback
- Android mobile client with custom C++ streaming core
- ASP.NET web admin dashboard for stream management
- Multi-language backend architecture (.NET + C++ + Python + Lua)
- Integrated e-commerce flow for in-stream purchases

---

## 🛠️ Multi-Language Technology Stack

| Layer | Technologies | Purpose |
|-------|-------------|---------|
| **Web Backend** | .NET Framework 4.5, ASP.NET Web Forms/MVC, WCF | Admin dashboard, API services |
| **Web Frontend** | ASP.NET Web Forms, JavaScript, jQuery | Stream management UI |
| **Mobile Client** | Android SDK, Java, Kotlin | Live streaming mobile app |
| **Native Core** | C++, Android NDK, JNI | High-performance streaming engine |
| **Data Processing** | Python 2.7/3.x, Pandas | Analytics, reporting, automation |
| **Configuration** | Lua 5.x | Dynamic business rules, hot-swappable configs |
| **Database** | SQL Server 2012, Redis, MongoDB | Data persistence and caching |
| **Streaming** | RTMP, WebRTC, HLS, FFmpeg | Audio/video transmission |
| **DevOps** | Windows Server, IIS | Deployment and hosting |

---

## ✨ Key Features

### 1. Multi-Language Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    System Architecture                   │
├─────────────────────────────────────────────────────────┤
│  Web Layer (ASP.NET C#)                                 │
│  ├─ Stream Management Dashboard                         │
│  ├─ User & Content Admin                                │
│  └─ Real-time Analytics (Viewer count, gifts, sales)    │
├─────────────────────────────────────────────────────────┤
│  API Layer (.NET WCF)                                   │
│  ├─ RESTful APIs for mobile clients                     │
│  ├─ WebSocket for real-time notifications               │
│  └─ Authentication & Session Management                 │
├─────────────────────────────────────────────────────────┤
│  Streaming Core (C++)                                   │
│  ├─ RTMP ingestion and distribution                     │
│  ├─ Transcoding and adaptive bitrate                    │
│  └─ Low-latency delivery optimization                   │
├─────────────────────────────────────────────────────────┤
│  Data Layer                                             │
│  ├─ SQL Server (C# Entity Framework)                    │
│  ├─ Redis Cache (C# StackExchange.Redis)                │
│  ├─ Python Analytics Engine                             │
│  └─ Lua Configuration Engine                            │
└─────────────────────────────────────────────────────────┘
```

### 2. Android Live Streaming Client
- **Java/Kotlin** for UI and business logic
- **C++ NDK** for custom streaming protocol implementation
- **JNI** bridge for Java-C++ communication
- Optimized for varying network conditions (3G/4G/WiFi)

### 3. ASP.NET Web Admin
- **ASP.NET Web Forms** for rapid admin interface development
- **ASP.NET MVC** for API endpoints
- Real-time dashboard with SignalR (WebSocket)
- Stream moderation and user management

### 4. Python Data Processing
- Automated stream analytics and reporting
- Viewer behavior analysis
- Gift and revenue statistics
- Integration with SQL Server via pyodbc

### 5. Lua Configuration
- Hot-swappable business rules without redeployment
- Dynamic streaming quality settings
- A/B testing configuration
- Feature flags management

---

## 📊 System Metrics

| Metric | Value |
|--------|-------|
| Development Period | 2015 - 2018 (3 years) |
| Team Size | 8 developers |
| Peak Concurrent Viewers | 1,000+ |
| Streaming Uptime | 99.5% |
| Supported Platforms | Android, Web Admin |
| Languages Used | 6 (C#, C++, Java, Kotlin, Python, Lua) |

---

## 💻 Code Examples

### C# ASP.NET Web API Controller
```csharp
public class StreamController : ApiController
{
    private readonly IStreamService _streamService;
    private readonly RedisCache _cache;
    
    [HttpGet]
    public IHttpActionResult GetLiveStreams()
    {
        // Check cache first
        var cached = _cache.Get("live_streams");
        if (cached != null) return Ok(cached);
        
        // Query database
        var streams = _streamService.GetActiveStreams();
        
        // Cache for 30 seconds
        _cache.Set("live_streams", streams, TimeSpan.FromSeconds(30));
        
        return Ok(streams);
    }
    
    [HttpPost]
    public IHttpActionResult StartStream([FromBody] StreamRequest request)
    {
        // Lua script for dynamic quality settings
        var qualityConfig = LuaEngine.Execute(@"
            return get_stream_quality(user_count, network_type)
        ");
        
        var stream = _streamService.CreateStream(request, qualityConfig);
        return Ok(stream);
    }
}
```

### C++ Streaming Core (Android NDK)
```cpp
// JNI bridge for Android streaming
extern "C" JNIEXPORT void JNICALL
Java_com_streaming_core_StreamEngine_startStream(
    JNIEnv* env, jobject thiz, jstring rtmpUrl) {
    
    const char* url = env->GetStringUTFChars(rtmpUrl, nullptr);
    
    // Initialize FFmpeg for RTMP streaming
    AVFormatContext* fmt_ctx = nullptr;
    avformat_alloc_output_context2(&fmt_ctx, nullptr, "flv", url);
    
    // Configure codec
    AVCodec* codec = avcodec_find_encoder(AV_CODEC_ID_H264);
    AVCodecContext* codec_ctx = avcodec_alloc_context3(codec);
    
    // Set adaptive bitrate based on network
    codec_ctx->bit_rate = getAdaptiveBitrate();
    
    // Start streaming loop
    startStreamingLoop(fmt_ctx, codec_ctx);
    
    env->ReleaseStringUTFChars(rtmpUrl, url);
}
```

### Python Analytics Script
```python
import pyodbc
import pandas as pd
from datetime import datetime

def generate_stream_report():
    # Connect to SQL Server
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=StreamingDB;UID=user;PWD=pass'
    )
    
    # Query stream data
    query = """
    SELECT stream_id, viewer_count, gift_amount, duration
    FROM streams 
    WHERE start_time >= DATEADD(day, -1, GETDATE())
    """
    
    df = pd.read_sql(query, conn)
    
    # Analytics
    report = {
        'total_streams': len(df),
        'avg_viewers': df['viewer_count'].mean(),
        'total_revenue': df['gift_amount'].sum(),
        'avg_duration': df['duration'].mean()
    }
    
    return report
```

### Lua Configuration Script
```lua
-- Dynamic stream quality configuration
function get_stream_quality(user_count, network_type)
    local quality = {}
    
    -- Base quality settings
    if network_type == "4G" then
        quality.bitrate = 1500000  -- 1.5 Mbps
        quality.resolution = "720p"
    elseif network_type == "WiFi" then
        quality.bitrate = 2500000  -- 2.5 Mbps
        quality.resolution = "1080p"
    else
        quality.bitrate = 800000   -- 800 Kbps
        quality.resolution = "480p"
    end
    
    -- Adjust based on viewer count
    if user_count > 500 then
        quality.bitrate = quality.bitrate * 0.8  -- Reduce 20%
    end
    
    return quality
end
```

---

## 🎓 Technical Highlights

### Multi-Language Integration Challenges
1. **JNI Complexity**: Managing Java-C++ object lifecycle and memory
2. **Python-C# Interop**: Using IronPython and process-based communication
3. **Lua Sandboxing**: Securing dynamic script execution
4. **Debugging Across Languages**: Multi-language profiling and logging

### .NET Specific Experience
- **ASP.NET Web Forms**: Rapid admin interface development
- **ASP.NET MVC**: RESTful API design and implementation
- **WCF Services**: Service-oriented architecture
- **Entity Framework**: ORM for SQL Server data access
- **SignalR**: Real-time web functionality
- **IIS Deployment**: Windows Server hosting and configuration

### Performance Optimizations
- C++ streaming core for minimal latency
- Redis caching for hot data
- SQL Server indexing for analytics queries
- Lua JIT for configuration processing

---

## 🔗 Related Projects

This project built upon and contributed to:

- **[Patent Search System](../patent-search-system/)** — Early .NET 2.0 foundation
- **[Enterprise Messaging](../enterprise-messaging/)** — Multi-language architecture experience applied to messaging

---

## 📅 Timeline

- **2015**: Project initiation, ASP.NET web admin development
- **2016**: Android client development, C++ streaming core integration
- **2017**: Python analytics, Lua configuration system
- **2018**: Production deployment, performance optimization

---

*Part of the Career Knowledge Base project — showcasing multi-language full-stack development expertise.*
