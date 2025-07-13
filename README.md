# SurgiSR4K: A High-Resolution Endoscopic Video Dataset for Robotic-Assisted Minimally Invasive Procedures

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2507.00209-red)](https://arxiv.org/abs/2507.00209)

## Overview

SurgiSR4K is the first publicly accessible surgical imaging and video dataset captured at native 4K resolution (3840×2160), specifically designed for robotic-assisted minimally invasive surgery (MIS). This dataset addresses the critical need for high-resolution surgical data to advance computer vision applications in medical robotics.

## Dataset Description

### Key Features
- **Native 4K Resolution**: All videos captured at 3840×2160 pixels
- **Realistic Surgical Scenarios**: Authentic robotic-assisted laparoscopic procedures
- **Diverse Challenging Conditions**: Specular reflections, tool occlusions, bleeding, smoke, tissue deformations
- **Multi-Task Support**: Designed for super resolution, instrument detection, depth estimation, segmentation, and more

### Dataset Statistics
- **Total Videos**: 150 surgical procedures
- **Total Duration**: ~45 hours of 4K footage
- **Frame Count**: ~4.86M frames
- **Video Format**: MP4 (H.264/H.265)
- **Frame Rate**: 30 FPS
- **Procedures**: Laparoscopic cholecystectomy, appendectomy, hernia repair

## Dataset Structure

```
SurgiSR4K/
├── LICENSE                          # CC-BY-NC-4.0 license
├── README.md                        # This file
├── data/
│   ├── videos/
│   │   ├── 4k/                      # Native 4K video files
│   │   └── downsampled/             # Lower resolution versions
│   │       ├── 1080p/
│   │       ├── 720p/
│   │       └── 480p/
│   ├── frames/                      # Extracted frames (optional)
│   │   ├── 4k/
│   │   └── downsampled/
│   └── metadata/
│       ├── video_metadata.csv       # Video-level information
│       ├── frame_annotations.csv    # Frame-level annotations
│       └── quality_metrics.csv      # Technical quality assessments
├── splits/
│   ├── train.txt                    # Training set (70%)
│   ├── val.txt                      # Validation set (15%)
│   └── test.txt                     # Test set (15%)

```

## Task Definition and Labels

### Primary Task: Super Resolution (SR)
- **Input**: Lower resolution frames (480p, 720p, 1080p)
- **Target**: Native 4K resolution frames
- **Evaluation**: PSNR, SSIM, LPIPS, and perceptual quality metrics

### Secondary Tasks
- **Smoke Removal**: Frames with/without smoke artifacts
- **Instrument Detection**: Bounding boxes for surgical tools
- **Depth Estimation**: Monocular depth maps
- **Segmentation**: Tissue, instrument, and background masks
- **Novel View Synthesis**: Multi-view reconstruction

### Label Formats
- **Video Metadata**: CSV with procedure info, quality scores, technical parameters
- **Frame Annotations**: CSV with frame-level quality indicators, scene complexity
- **Bounding Boxes**: COCO format JSON for instrument detection
- **Segmentation Masks**: PNG format for pixel-level annotations

## Data Fields

### Video Metadata
- `video_id`: Unique identifier
- `procedure_type`: Surgical procedure category
- `duration_seconds`: Video length
- `fps`: Frames per second
- `resolution`: Video resolution
- `quality_score`: Overall video quality (1-5 scale)
- `challenging_scenarios`: Presence of difficult conditions

### Frame Annotations
- `frame_id`: Frame identifier
- `timestamp`: Time in video
- `blur_score`: Motion blur assessment
- `lighting_quality`: Illumination quality
- `instrument_present`: Boolean for tool visibility
- `smoke_present`: Boolean for smoke artifacts
- `blood_present`: Boolean for bleeding
- `specular_reflection`: Boolean for reflections

## Getting Started

### Download
```bash
# Download dataset (requires authentication)
python scripts/download_data.py --output_dir ./SurgiSR4K
```


## Evaluation Metrics

### Super Resolution
- **PSNR**: Peak Signal-to-Noise Ratio
- **SSIM**: Structural Similarity Index
- **LPIPS**: Learned Perceptual Image Patch Similarity
- **Medical Quality**: Custom metrics for surgical video assessment

### Benchmarking
```python
from scripts.evaluation.metrics import evaluate_sr_model

results = evaluate_sr_model(
    model=your_model,
    test_loader=test_loader,
    metrics=['psnr', 'ssim', 'lpips']
)
```

## Licensing and Usage

### License
This dataset is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

### Citation
```bibtex
@article{jiang2025surgisr4k,
  author    = {Fengyi Jiang and Xiaorui Zhang and Lingbo Jin and Ruixing Liang and Yuxin Chen and Adi Chola Venkatesh and Jason Culman and Tiantian Wu and Lirong Shao and Wenqing Sun and Cong Gao and Hallie McNamara and Jingpei Lu and Omid Mohareri},
  title     = {SurgiSR4K: A High‐Resolution Endoscopic Video Dataset for Robotic‐Assisted Minimally Invasive Procedures},
  journal   = {arXiv preprint arXiv:2507.00209},
  year      = {2025},
  volume    = {2507.00209},
  doi       = {10.48550/arXiv.2507.00209},
  url       = {https://arxiv.org/abs/2507.00209}
}

```

## Data Privacy and Ethics


## Contributing

### Reporting Issues
Please report any issues or questions via GitHub issues or contact the maintainers.

### Contributing Code
We welcome contributions to preprocessing scripts, evaluation tools, and baseline implementations.

## Acknowledgments

We thank the surgical teams, patients, and institutions that made this dataset possible. Special recognition to the robotic surgery programs that provided the clinical data.

## Contact

For questions, issues, or collaboration opportunities:
- **Primary Contact**: Fengyi Jiang (fengyi_jiang@alumni.brown.edu)

- **Dataset Inquiries**: art.jiang@intusurg.com

## Version History

- **v1.0** (2025-07): Initial release
---

*This dataset supports research in computer vision for surgical applications. Use responsibly and cite appropriately.* 