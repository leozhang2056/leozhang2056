# ChatClothes Virtual Try-On

> AI-powered virtual try-on system with multimodal interaction and edge deployment
> Master's Thesis Project at AUT, New Zealand

---

## Overview

ChatClothes is a multimodal AI virtual try-on system that combines diffusion models, computer vision, and LLM-driven user interaction. The system enables users to virtually try on clothing items through text descriptions, image uploads, or multimodal inputs, generating realistic try-on results in real-time.

**Project Type:** AI Research / Master's Thesis  
**Timeline:** November 2024 - April 2025  
**Role:** Sole Developer & System Designer  
**Institution:** Auckland University of Technology (AUT), New Zealand

---

## Key Features

- **Multimodal Input Support:** Text prompts, image uploads, or combined inputs
- **AI-Powered Generation:** Diffusion models for realistic clothing visualization
- **Intelligent Classification:** YOLO-based clothing detection and categorization
- **LLM Integration:** Natural language control and prompt parsing
- **Edge Deployment:** Optimized for Raspberry Pi 5 with offline capability
- **Web Interface:** Browser-based user interaction
- **Orchestration Platform:** ComfyUI + Dify integration for workflow management

---

## Architecture

```
User Input (Text/Image/Multimodal)
         ↓
   LLM Parser (Dify)
         ↓
   +------------------+
   |  Control Layer   |
   +------------------+
         ↓
   +------------------+
   | ComfyUI Pipeline |
   | - YOLO Detection |
   | - Diffusion Gen  |
   +------------------+
         ↓
   Generated Try-On Image
```

### Components

1. **Frontend Interface**
   - Web-based user interface
   - Supports multiple input modes
   - Real-time preview

2. **LLM Control Layer (Dify)**
   - Prompt parsing and understanding
   - Intent classification
   - Parameter extraction

3. **Generation Pipeline (ComfyUI)**
   - YOLO: Clothing detection and segmentation
   - Diffusion Model: High-quality image generation
   - Post-processing: Result refinement

4. **Edge Optimization**
   - Model quantization
   - Inference optimization for ARM architecture
   - Memory-efficient execution on Raspberry Pi 5

---

## Technologies

### AI/ML
- **PyTorch** - Deep learning framework
- **OpenCV** - Image processing
- **YOLO** - Object detection
- **Diffusion Models** - Image generation
- **LLM Integration** - Natural language processing

### Tools & Platforms
- **ComfyUI** - Visual workflow orchestration
- **Dify** - LLM application platform
- **Raspberry Pi 5** - Edge deployment target

### Programming
- **Python** - Primary development language
- **JavaScript** - Frontend development

---

## Key Achievements

- ✅ **Thesis completed 6 months early** (submitted April 2025)
- ✅ **Full-stack AI solution** developed independently
- ✅ **Edge deployment** on Raspberry Pi 5 with real-time performance
- ✅ **Working demo** with comprehensive documentation
- ✅ **Multimodal interaction** supporting text, image, and combined inputs
- ✅ **Offline capability** for privacy and accessibility

---

## Results

- Successfully demonstrated virtual try-on with various clothing types
- Achieved low-latency inference on edge devices
- Validated approach through user testing and evaluation
- Delivered complete deployment guide for reproducibility

---

## Challenges & Solutions

### Challenge 1: Edge Performance
**Problem:** Diffusion models are computationally intensive for edge devices  
**Solution:** Model optimization, quantization, and efficient pipeline design

### Challenge 2: Multimodal Integration
**Problem:** Combining text, image, and LLM control seamlessly  
**Solution:** Modular architecture with Dify orchestration layer

### Challenge 3: Real-time Response
**Problem:** Users expect quick try-on results  
**Solution:** Optimization of inference pipeline and caching strategies

---

## Future Enhancements

- [ ] Mobile application development
- [ ] Support for more clothing categories
- [ ] Enhanced personalization features
- [ ] Cloud deployment option
- [ ] Integration with e-commerce platforms

---

## Repository & Links

- **Thesis:** Submitted to AUT (April 2025)
- **Demo:** Available upon request
- **Documentation:** Complete deployment guide included

---

## Evidence

![Architecture Diagram](images/arch.png)
*System architecture overview*

![Demo Screenshot](images/demo.png)
*Virtual try-on results*

---

## Skills Demonstrated

- **AI/ML:** PyTorch, OpenCV, YOLO, Diffusion Models, LLM integration
- **System Design:** End-to-end AI pipeline architecture
- **Edge Computing:** Model optimization for resource-constrained devices
- **Full-stack Development:** Frontend, backend, and AI model integration
- **Research:** Independent thesis work with early completion

---

**Tags:** #AI #MachineLearning #ComputerVision #VirtualTryOn #EdgeComputing #PyTorch #Python #Thesis
