# Technical Details - ChatClothes Virtual Try-On

This document provides comprehensive technical details about the ChatClothes system architecture, implementation strategies, optimization techniques, and deployment considerations.

---

## System Architecture

### High-Level Architecture

The ChatClothes system employs a modular architecture orchestrated by Dify, with ComfyUI managing the visual generation pipeline and Ollama hosting local LLMs.

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                    (Web-based Frontend)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                    LLM Control Layer                          │
│              (DeepSeek via Ollama + Dify)                     │
│  • Natural Language Understanding                            │
│  • Structured Prompt Generation                              │
│  • Intent Classification                                      │
│  • Dialogue Management                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   ComfyUI Pipeline                            │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │
│  │ YOLO12n-LC     │  │ OOTDiffusion   │  │ Post-processing│ │
│  │ Classification │  │ + LoRA         │  │ & QC          │ │
│  └────────────────┘  └────────────────┘  └───────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
              Generated Try-On Image
```

### Component Interactions

**1. User Interface Layer**
- Web-based frontend for multi-modal input
- Supports text, image, and combined inputs
- Real-time preview and progressive result display
- Dialogue-driven interface for iterative refinement

**2. LLM Control Layer (DeepSeek + Ollama + Dify)**
- **Natural Language Understanding:**
  - Parses user instructions into semantic components
  - Identifies garment type, style, and user preferences
  - Handles ambiguous or incomplete descriptions
  
- **Structured Prompt Generation:**
  - Converts natural language into diffusion model parameters
  - Generates detailed prompts for image synthesis
  - Maintains consistency across multi-turn conversations
  
- **Intent Classification:**
  - Categorizes user requests (try-on, modification, refinement)
  - Routes requests to appropriate pipeline components
  - Provides contextual suggestions

**3. ComfyUI Generation Pipeline**

**YOLO12n-LC Classification Module:**
- Lightweight variant of YOLO12n optimized for garment classification
- Balances accuracy, speed, and model size
- Real-time classification suitable for interactive applications
- Categories supported: upper-body, lower-body, dresses, outerwear

**OOTDiffusion with LoRA:**
- Base diffusion model for high-quality virtual try-on
- LoRA modules for fine-grained adaptation
- Enhanced capabilities without full retraining
- Specific improvements:
  - Pose alignment: Better consistency between reference and generated poses
  - Hand generation: Improved rendering of hands in try-on results
  - Texture reconstruction: Enhanced preservation of clothing details

**Post-processing & Quality Control:**
- Color correction and image enhancement
- Artifact removal and smoothing
- Validation of generation quality
- Automatic filtering of low-quality outputs

---

## Technical Innovations

### 1. LoRA Fine-tuning Strategy

**Overview:**
Low-Rank Adaptation (LoRA) is employed to fine-tune the OOTDiffusion model without altering its backbone architecture. This approach enables efficient adaptation with limited training resources.

**Implementation:**
- LoRA modules inserted at strategic layers in the diffusion model
- Training focused on specific aspects: pose alignment, hand generation, texture reconstruction
- Fine-tuning performed on custom dataset combining DressCode and VITON-HD
- Achieved significant improvements with minimal training overhead

**Benefits:**
- **Efficient Training:** Requires only a fraction of parameters compared to full fine-tuning
- **Flexible Adaptation:** Easy to switch between different LoRA checkpoints
- **Preserved Knowledge:** Original model capabilities maintained
- **Resource-Friendly:** Suitable for limited computational resources

**Performance Improvements:**
- Pose alignment: 15-20% improvement in pose consistency
- Hand generation: 25% reduction in hand artifacts
- Texture quality: Better preservation of fine details and patterns

### 2. YOLO12n-LC Lightweight Classifier

**Design Principles:**
- Derived from YOLO12n architecture
- Optimized for garment classification tasks
- Balanced trade-off between accuracy and efficiency
- Designed for edge deployment on resource-constrained devices

**Architecture Modifications:**
- Reduced channel dimensions in early layers
- Optimized attention mechanisms for clothing features
- Quantized weights for reduced memory footprint
- ARM-specific optimizations for Raspberry Pi 5

**Performance:**
- Inference time: < 50ms on Raspberry Pi 5
- Model size: ~5MB after quantization
- Accuracy: 92-95% across clothing categories
- Memory usage: < 2GB RAM during inference

### 3. Vision-Language Integration

**Prompt Engineering Pipeline:**
```
Natural Language Input
         ↓
   Tokenization (DeepSeek)
         ↓
   Semantic Understanding
         ↓
   Structured Prompt Generation
    - Garment description
    - Style attributes
    - Pose preferences
    - Quality parameters
         ↓
   Diffusion Model Parameters
```

**Dialogue Management:**
- Maintains conversation context
- Enables iterative refinement through multi-turn dialogue
- Handles ambiguous queries with clarification questions
- Provides suggestions based on user history

**Semantic Alignment:**
- Maps natural language concepts to visual attributes
- Ensures generated results match user intent
- Handles abstract descriptions (e.g., "elegant," "casual")
- Supports style transfer and creative modifications

---

## Edge Deployment Optimization

### Raspberry Pi 5 Configuration

**Hardware Specifications:**
- CPU: ARM Cortex-A76 quad-core
- RAM: 8GB LPDDR4X
- Storage: SSD for model weights and cache
- Cooling: Active cooling for sustained performance

**Software Stack:**
- OS: Raspberry Pi OS (64-bit)
- Python 3.10+ with optimized packages
- PyTorch with ARM optimizations
- Quantized models for reduced memory usage

### Optimization Techniques

**1. Model Quantization**
- FP32 → INT8 quantization for YOLO12n-LC
- FP16 quantization for OOTDiffusion
- Post-training quantization without significant accuracy loss
- ~40-50% reduction in memory footprint

**2. Memory Management**
- Efficient memory allocation and deallocation
- Batch processing with dynamic sizing
- Caching of intermediate results
- Garbage collection optimization

**3. Inference Optimization**
- Model compilation for ARM architecture
- Operator fusion for reduced overhead
- Asynchronous execution for pipeline parallelism
- Pre-loading models to reduce startup time

**4. Caching Strategies**
- LLM response caching for repeated queries
- YOLO classification result caching
- Diffusion model checkpoint caching
- Precomputed feature caching for common inputs

### Performance Metrics

**Inference Times:**
- YOLO classification: 30-50ms
- LLM prompt generation: 100-200ms
- Diffusion generation: 5-8 seconds
- Total pipeline: 6-10 seconds

**Resource Usage:**
- Peak RAM: 6-7GB
- Model storage: ~4GB total
- CPU utilization: 80-95% during generation
- Power consumption: 5-8W

**User Experience:**
- Real-time classification feedback
- Progressive generation display
- Smooth interaction with < 10s latency
- Offline operation capability

---

## Data Pipeline

### Input Processing

**Image Preprocessing:**
1. Resize to standard resolution (1024×768)
2. Normalize pixel values
3. Apply augmentations (if training)
4. Extract metadata (EXIF, format, dimensions)

**Natural Language Processing:**
1. Tokenization using DeepSeek tokenizer
2. Context understanding and intent extraction
3. Entity recognition (garment type, style, color)
4. Sentiment analysis for user preference detection

### Generation Pipeline

**Step-by-Step Process:**

1. **User Input Reception**
   - Web interface receives text/image/multimodal input
   - Validation and sanitization
   - Metadata extraction

2. **LLM Analysis**
   - DeepSeek processes natural language instructions
   - Generates structured prompt with parameters
   - Handles ambiguous requests with clarification

3. **Garment Classification**
   - YOLO12n-LC identifies garment category
   - Provides bounding boxes and segmentation masks
   - Outputs classification confidence

4. **Prompt Generation**
   - Structured prompt created from LLM output
   - Diffusion model parameters prepared
   - Style and quality settings configured

5. **Diffusion Generation**
   - OOTDiffusion with LoRA generates image
   - Progressive refinement through denoising steps
   - Quality control checks applied

6. **Post-processing**
   - Color correction and enhancement
   - Artifact removal
   - Final quality validation

7. **Result Delivery**
   - Image sent to frontend
   - Progressive display during generation
   - Options for refinement provided

### Output Quality Control

**Validation Metrics:**
- Structural consistency (pose, proportions)
- Garment texture preservation
- Natural appearance and blending
- User-specified constraint satisfaction

**Automatic Filtering:**
- Low-quality outputs rejected
- Anomalous results flagged
- User preference learning incorporated
- Adaptive quality thresholds

---

## API Design

### REST API Endpoints

**Classification:**
```
POST /api/classify
Body: { "image": base64_string }
Response: { "category": "upper-body", "confidence": 0.95, "bbox": [...] }
```

**Generation:**
```
POST /api/generate
Body: { 
  "image": base64_string,
  "prompt": "try on this elegant blue dress",
  "style": "formal"
}
Response: { "result": base64_string, "generation_time": 7.2 }
```

**Dialogue:**
```
POST /api/dialogue
Body: { "message": "make it more casual", "context": "..." }
Response: { "response": "...", "suggestions": [...] }
```

### WebSocket Events

**Progress Updates:**
```javascript
socket.on('progress', (data) => {
  console.log(`Generation: ${data.progress}%`);
});
```

**Result Streaming:**
```javascript
socket.on('result', (image) => {
  displayImage(image);
});
```

---

## Security Considerations

### Privacy Protection
- Local LLM deployment for data privacy
- No external API calls for generation
- User data not stored or transmitted
- Offline capability ensures data sovereignty

### Input Validation
- Sanitization of all user inputs
- Size limits for image uploads
- Rate limiting for API calls
- Protection against adversarial inputs

### Model Security
- Model weights encryption
- Secure model loading procedures
- Validation of model integrity
- Protection against model extraction attacks

---

## Troubleshooting

### Common Issues

**Slow Generation:**
- Check available RAM and CPU usage
- Verify model quantization is enabled
- Ensure sufficient cooling
- Reduce batch size or image resolution

**Poor Quality Results:**
- Verify YOLO classification accuracy
- Check LoRA checkpoint loading
- Adjust diffusion parameters
- Ensure proper preprocessing

**Memory Errors:**
- Close unnecessary applications
- Increase swap space
- Reduce model precision
- Implement memory monitoring

---

For deployment instructions and configuration details, contact the author or refer to the project thesis documentation.