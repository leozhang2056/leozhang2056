# ChatClothes Virtual Try-On

> A modular and multimodal AI virtual try-on system integrating diffusion models, YOLO-based classification, and LLM-driven user interaction
> Master's Thesis Project at Auckland University of Technology (AUT), New Zealand

---

## 1. Introduction & Overview

ChatClothes is a state-of-the-art multimodal AI virtual try-on (VTON) system that bridges vision-language interaction with diffusion-based generation. The system integrates controllable diffusion-based generation with dialogue-driven garment interaction, providing a unified framework for scalable, user-centered, and device-adaptable fashion AI systems.

![System Demo](images/demo.png)
*ChatClothes in action: From natural language request to high-fidelity virtual try-on result*

### Project Details
**Project Type:** AI Research / Master's Thesis  
**Timeline:** November 2024 - April 2025  
**Role:** Sole Developer & System Designer  
**Institution:** Auckland University of Technology (AUT), New Zealand  
**Status:** ✅ Thesis completed 6 months early (April 2025)

---

## 2. System Architecture & Components

The foundational architecture orchestrates LLMs, Computer Vision algorithms, and Generative Diffusion models.

| Architecture | Components | Data Flow | Pipeline Overview |
| :---: | :---: | :---: | :---: |
| ![Arch](images/arch.png) | ![Components](images/slide09_system_components.PNG) | ![Data Flow](images/slide08_data_flow.PNG) | ![Pipeline](images/slide10_pipeline_overview.PNG) |

---

## 3. Core Technical Workflow

### 3.1 Vision-Language Input & Interaction (LLM)
Natural language instructions are processed by **DeepSeek LLM** to generate structured prompts and control signals.

| Multi-modal Input | Dify Orchestration |
| :---: | :---: |
| ![Input](images/slide12_multimodal_input.PNG) | ![Dify](images/slide14_dify_integration.PNG) |

### 3.2 Intelligent Pre-processing (YOLO & Computer Vision)
Before generation, the input source and target images are strictly analyzed to preserve structural facts.

| YOLO Garment Detection | Body Pose Estimation | Semantic Segmentation |
| :---: | :---: | :---: |
| ![YOLO](images/slide02_yolo_detection.PNG) | ![Pose](images/slide03_pose_estimation.PNG) | ![Segmentation](images/slide04_clothing_segmentation.PNG) |

### 3.3 Diffusion Generation & Post-Processing
The core generative process uses **OOTDiffusion** enhanced with **LoRA** fine-tuning, managed entirely within custom ComfyUI workflows.

| Diffusion Model | ComfyUI Workflow | Post-Processing | Quality Control |
| :---: | :---: | :---: | :---: |
| ![Diffusion](images/slide05_diffusion_model.PNG) | ![Workflow](images/slide13_comfyui_workflow.PNG) | ![Post](images/slide06_post_processing.PNG) | ![QC](images/slide07_quality_control.PNG) |

---

## 4. Results & Performance

### 4.1 Try-On Quality & Accuracy
The system maintains realistic fabric textures, poses, and shading across different physical builds and garments.

![Results Grid](images/slide15_results.PNG)
*Qualitative try-on results*

| Performance Evaluation | Accuracy Metrics |
| :---: | :---: |
| ![Performance](images/slide17_performance.PNG) | ![Accuracy](images/slide18_accuracy.PNG) |

### 4.2 Application Environments & Deployment

The application adapts elegantly from local Edge Devices directly to Cloud Enterprise and Mobile platforms.

| Edge Deployment (RPi 5) | Mobile App UI | Cloud Deployment | E-Commerce Integration |
| :---: | :---: | :---: | :---: |
| ![Edge](images/slide11_edge_deployment.PNG) | ![Mobile](images/slide22_mobile_app.PNG) | ![Cloud](images/slide23_cloud_deployment.PNG) | ![Ecommerce](images/slide24_ecommerce_integration.PNG) |

---

## 5. User Testing & Validation

The system successfully underwent intensive integration testing and practical user testing.

| Complete Interface | Demo Workflow | Test Cases | User Testing Results |
| :---: | :---: | :---: | :---: |
| ![UI](images/slide16_user_interface.PNG) | ![Demo Flow](images/slide28_demo_workflow.PNG) | ![Test Cases](images/slide29_test_cases.PNG) | ![User Test](images/slide30_user_testing.PNG) |

---

## 6. Research Impact & Future Outlook

I independently addressed the key challenges in the domain of virtual try-on, delivering real technical innovation and research contributions.

| Technical Innovation | Research Contribution |
| :---: | :---: |
| ![Innovation](images/slide26_technical_innovation.PNG) | ![Contribution](images/slide25_research_contribution.PNG) |

| Challenges Solved | Optimizations Applied | Future Work Roadmap |
| :---: | :---: | :---: |
| ![Challenges](images/slide19_challenges.PNG) | ![Optimization](images/slide20_optimization.PNG) | ![Future](images/slide21_future_work.PNG) |

### Conclusion

![Conclusion](images/slide31_conclusion.PNG)

---

## Technical Stack
- **AI/ML Core:** DeepSeek LLM, PyTorch, OOTDiffusion, LoRA, YOLO12n-LC
- **Platforms:** Dify, ComfyUI, Ollama, Raspberry Pi 5
- **Languages:** Python, JavaScript

## Citation

If you find this project useful for your research, please consider citing our work:

### Master's Thesis
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

### Conference Publication
```bibtex
@inproceedings{Zhang2025ChatClothes,
  author    = {Yuchao Zhang and Kien Tran and Minh Nguyen and Wei Qi Yan},
  title     = {ChatClothes: A Lightweight Diffusion-Based Virtual Try-On System with Multimodal Control},
  booktitle = {Proceedings of the 40th International Conference on Image and Vision Computing New Zealand (IVCNZ 2025)},
  year      = {2025},
  month     = {Nov},
  address   = {Wellington, New Zealand},
  doi       = {10.1109/IVCNZ67716.2025.11281834}
}
```

**Tags:** #AI #VirtualTryOn #DiffusionModels #LLM #LoRA #YOLO #EdgeComputing #Thesis