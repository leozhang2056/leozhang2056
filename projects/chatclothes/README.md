# ChatClothes Virtual Try-On

> A modular and multimodal AI virtual try-on system integrating diffusion models, YOLO-based classification, and LLM-driven user interaction
> Master's Thesis Project at Auckland University of Technology (AUT), New Zealand

---

## Overview

ChatClothes is a state-of-the-art multimodal AI virtual try-on (VTON) system that bridges vision-language interaction with diffusion-based generation. The system integrates controllable diffusion-based generation with dialogue-driven garment interaction, providing a unified framework for scalable, user-centered, and device-adaptable fashion AI systems.

### Key Innovations

- **Natural Language Control:** DeepSeek LLM interprets natural language instructions and transforms them into structured prompts
- **LoRA Fine-tuning:** Enhanced OOTDiffusion model with improved pose alignment, hand generation, and texture reconstruction
- **YOLO12n-LC:** Lightweight classifier optimized for edge deployment
- **Dialogue-Driven Interaction:** Intuitive conversational interface for iterative refinement

**Project Type:** AI Research / Master's Thesis  
**Timeline:** November 2024 - April 2025  
**Role:** Sole Developer & System Designer  
**Institution:** Auckland University of Technology (AUT), New Zealand  
**Status:** ✅ Thesis completed 6 months early (April 2025)

---

## System Architecture

![System Architecture](images/arch.png)
*Complete system architecture: LLM control → YOLO classification → Diffusion generation → Try-on results*

![Pipeline Overview](images/slide10_pipeline_overview.PNG)
*Detailed pipeline workflow with ComfyUI + Dify + Ollama integration*

---

## Key Features

- **Multimodal Input:** Natural language descriptions, image uploads, or combined inputs
- **LLM-Powered Control:** DeepSeek interprets instructions for intuitive user interaction
- **Enhanced Generation:** LoRA-fine-tuned OOTDiffusion for realistic clothing synthesis
- **Efficient Classification:** YOLO12n-LC lightweight garment detection
- **Edge Deployment:** Optimized for Raspberry Pi 5 with offline capability
- **Dialogue Interface:** Conversational refinement for iterative improvements
- **Web Interface:** Browser-based interaction with real-time preview
- **Comprehensive Validation:** Tested on DressCode and VITON-HD datasets

---

## Technical Stack

### AI/ML Core
- **DeepSeek** - LLM for natural language understanding
- **OOTDiffusion** - State-of-the-art virtual try-on model
- **LoRA** - Fine-tuning for enhanced performance
- **YOLO12n-LC** - Lightweight garment classifier
- **PyTorch** - Deep learning framework

### Platforms
- **Dify** - Workflow orchestration
- **ComfyUI** - Visual pipeline management
- **Ollama** - Local LLM hosting
- **Raspberry Pi 5** - Edge deployment

### Languages
- **Python** - Core development
- **JavaScript** - Frontend interface

---

## Key Achievements

### Project Milestones
- ✅ **Thesis completed 6 months early** (submitted April 2025)
- ✅ **Full-stack AI solution** - End-to-end system independently built
- ✅ **Edge deployment** - Optimized for Raspberry Pi 5
- ✅ **Comprehensive validation** - Tested on standard benchmarks

### Technical Accomplishments
- ✅ **LoRA fine-tuning** - Enhanced pose alignment, hand generation, texture reconstruction
- ✅ **YOLO12n-LC development** - Lightweight classifier for edge deployment
- ✅ **Natural language integration** - Dialogue-driven garment interaction
- ✅ **Offline capability** - Full functionality without internet

### Research Impact
- ✅ **Unified framework** - Vision-language interaction with diffusion generation
- ✅ **Device adaptability** - Edge deployment feasibility demonstrated
- ✅ **Interactive paradigm** - Novel dialogue-driven approach

---

## Applications

**E-commerce:** Virtual try-on for online shopping with reduced return rates  
**AR Fitting Mirrors:** In-store augmented reality fitting experiences  
**Personalization:** Customized outfit recommendations and style exploration  
**Automated Design:** AI-powered fashion design assistance and rapid prototyping

---

## Quick Links

- 📄 [Technical Details](TECHNICAL_DETAILS.md) - Architecture, implementation, and optimization
- 📊 [Experiments & Results](EXPERIMENTS.md) - Datasets, metrics, and evaluation
- 🖼️ [Image Gallery](IMAGES.md) - Complete visual documentation
- 📖 [Thesis](http://hdl.handle.net/10292/20210) - Full academic thesis (AUT Open Repository)
- 📹 [Demo Video](#) - Available upon request
- 📥 [Documentation](#) - Deployment guide and API documentation

---

## Citation

```bibtex
@mastersthesis{zhang2025chatclothes,
  title={ChatClothes: An AI-Powered Virtual Try-On System},
  author={Zhang, Yuchao},
  year={2025},
  school={Auckland University of Technology},
  note={Master of Computer and Information Sciences},
  doi={10.10292/20210}
}
```

---

## Contact

**Author:** Yuchao Zhang  
**Supervisor:** Dr. Wei Qi Yan  
**Institution:** Auckland University of Technology (AUT)  
**Department:** Computer and Information Sciences  
**DOI:** [10.10292/20210](http://dx.doi.org/10.10292/20210)

---

**Tags:** #AI #VirtualTryOn #DiffusionModels #LLM #LoRA #YOLO #EdgeComputing #Thesis