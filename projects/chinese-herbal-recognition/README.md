# Chinese Herbal Recognition Platform

> A platform-oriented AI project using traditional Chinese medicine (TCM) recognition as the sample scenario: users create classes, annotate data, train models, evaluate results, and deploy models for real recognition.

---

## Overview

This project is designed as a reusable **AI data-and-model platform**.  
Traditional Chinese medicine recognition is used as the first business sample to validate the full workflow from data preparation to model usage.

Users can:

- Create custom classification categories
- Annotate herb image data
- Train classification models
- Evaluate model quality through testing
- Use trained models to identify TCM materials

**Project Type:** AI Platform / Computer Vision Classification  
**Scenario Sample:** Traditional Chinese Medicine Recognition  
**Role:** Platform Designer & AI Workflow Developer  
**Timeline:** TBD

---

## My Responsibilities

- Designed the end-to-end platform workflow for AI classification projects.
- Built category management and annotation process for custom datasets.
- Designed model training pipeline with configurable parameters.
- Implemented testing/evaluation process for model effect verification.
- Connected model inference to practical recognition usage.
- Structured the platform to support future domain expansion beyond TCM.

---

## Key Capabilities

- **Category management:** Users define project-specific herb classes.
- **Data annotation:** Label image samples with task-specific attributes and quality checks.
- **Training pipeline:** Build models from labeled datasets with configurable strategies.
- **Model evaluation:** Validate quality with both aggregate metrics and per-class analysis.
- **Recognition inference:** Submit images and return predicted herb class with confidence.
- **Model versioning:** Support iterative optimization, rollback, and A/B comparison.
- **Platform extensibility:** Reuse same workflow for other visual classification tasks.

---

## Data Specification

### Class Schema

- `class_id`: Unique category ID (system generated)
- `class_name`: Herb name (for example: Huangqi, Danggui, Ginseng)
- `alias`: Optional common names
- `status`: active / archived
- `sample_count`: Number of labeled samples under this class

### Sample Metadata

- `sample_id`: Unique sample ID
- `image_uri`: Storage path
- `source`: mobile upload / camera / import batch
- `label_class_id`: Target class ID
- `annotator`: Operator identity
- `quality_flag`: pass / review / reject
- `created_at`: Annotation timestamp

### Dataset Version

- `dataset_version`: Semantic version (`v1.0.0`, `v1.1.0`)
- `split_strategy`: train/val/test split policy
- `class_distribution`: Per-class sample statistics
- `label_consistency_score`: Consistency check indicator
- `frozen`: Whether this dataset is immutable for reproducible training

---

## Annotation and QA Workflow

1. **Category setup:** Create classes and naming conventions.
2. **Data upload:** Batch import or manual upload herb images.
3. **Primary labeling:** Annotators assign class labels.
4. **Quality review:** Reviewer verifies hard cases and low-quality images.
5. **Dispute handling:** Resolve ambiguous samples and update label policy.
6. **Dataset freeze:** Freeze approved version for training jobs.

Quality control rules:

- Mandatory class balance check before training.
- Duplicate/near-duplicate image detection to reduce leakage.
- Blur/occlusion/overexposure filtering for invalid samples.
- Inter-annotator consistency spot-check for difficult classes.

---

## End-to-End Workflow

1. **Create categories:** Define herb classes (for example: Huangqi, Danggui, Ginseng, etc.).
2. **Collect data:** Upload raw herb images for each category.
3. **Annotate dataset:** Label samples and perform quality check.
4. **Train model:** Start training with selected data and hyperparameters.
5. **Test effect:** Evaluate accuracy/precision/recall and confusion patterns.
6. **Publish model:** Select qualified model as active version.
7. **Use recognition:** Run inference on new images to identify herbs.

---

## Model and Training Strategy

### Baseline and Production Candidates

- **Baseline:** ResNet50 / MobileNetV3 classifier for quick iteration
- **Production candidate:** EfficientNet or ConvNeXt family based on latency budget
- **Loss strategy:** Cross-entropy + class weight for imbalance handling
- **Augmentation:** Random crop, color jitter, rotation, mixup/cutmix (optional)

### Typical Training Configuration

- Input size: `224x224` or `320x320`
- Optimizer: `AdamW` or `SGD`
- Initial learning rate: `1e-3` (with cosine decay / step decay)
- Batch size: `32/64` based on GPU resources
- Epochs: `50-150` with early stopping
- Validation frequency: each epoch
- Seed control: fixed random seed for reproducibility

### Experiment Tracking

- Track dataset version, model config, metrics, and artifact path
- Store confusion matrix and per-class precision/recall for each run
- Keep best checkpoint and final checkpoint separately

---

## Evaluation and Release Gates

Core metrics:

- Top-1 Accuracy
- Macro Precision / Macro Recall / Macro F1
- Per-class Recall (critical for confusing herb classes)
- Inference latency (P95)

Suggested release gates (configurable by project owner):

- Top-1 Accuracy >= `0.85`
- Macro F1 >= `0.80`
- Worst-class Recall >= `0.70`
- P95 single-image latency <= `300ms` (service-side target)

Only models that pass release gates can be promoted to production versions.

---

## Architecture (Conceptual)

```
┌──────────────────────────────────────────────┐
│                Platform Console              │
│ Class Mgmt | Annotation | Training | Eval    │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│      Data & Label Management Layer           │
│ Upload | Labeling | Dataset Version | QA     │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│         Model Training & Registry Layer      │
│ Jobs | Config | Checkpoints | Model Registry │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│      Evaluation & Inference Service Layer    │
│ Metrics | Reports | A/B | Recognition API    │
└───────────────────────────────────────────────┘
```

---

## Inference API (Example)

`POST /api/v1/recognition/predict`

Request:

- `model_version`: Model version to use (`prod-v3`, `exp-v17`)
- `image`: Multipart image file or image URL
- `top_k`: Optional, default `3`

Response:

- `predictions`: Top-k class results with confidence
- `model_version`: Actual model version used
- `latency_ms`: Inference latency
- `trace_id`: Request trace ID for debugging/audit

---

## Deployment and Iteration

- **Packaging:** Export trained model as versioned artifact
- **Serving:** Deploy through API service with autoscaling support
- **Rollback:** One-click rollback to previous stable model
- **Monitoring:** Track latency, error rate, and confidence drift
- **Data flywheel:** Send low-confidence samples back to annotation queue

This forms a continuous closed-loop:
**data -> annotation -> training -> evaluation -> deployment -> feedback -> retraining**

---

## Project Value

- **Low entry barrier:** Non-algorithm users can still complete AI workflow steps.
- **Closed-loop iteration:** Data, model, and evaluation form continuous optimization loop.
- **Domain validation:** Proven with practical TCM recognition scenario.
- **Reusable platform:** Same workflow can support other medicine/material recognition domains.

---

## Evidence

> No screenshots committed yet.  
> Suggested files under `images/`:
> - `platform-overview.png`
> - `annotation-workbench.png`
> - `training-dashboard.png`
> - `recognition-result.png`

---

## Skills Demonstrated

- AI platform workflow design
- Dataset annotation and quality process design
- Computer vision classification pipeline
- Model evaluation, release-gate, and iteration strategy
- Productized AI capability integration

---

**Tags:** #AIPlatform #ComputerVision #Classification #MLOps #DataAnnotation #TraditionalChineseMedicine
