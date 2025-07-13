# SurgiSR4K Dataset Organization

## Overview

The SurgiSR4K dataset is organized in a hierarchical structure that captures surgical video frames across multiple resolutions with tool complexity annotations. This document explains the original organization format before any data splitting or reorganization.

## Directory Structure

```
data/
├── images/
│   ├── 480x270p/           # Low resolution frames (480×270 pixels)
│   ├── 960x540p/           # Medium resolution frames (960×540 pixels)
│   └── 3840x2160p/         # High resolution frames (3840×2160 pixels)
└── videos/
    └── 3840x2160_30fps/    # Source 4K videos at 30 FPS
```

## Resolution Hierarchy

The dataset contains three resolution levels, each representing the same surgical content at different quality levels:

### 1. **480x270p** (Low Resolution)
- **Resolution**: 480×270 pixels
- **Purpose**: Baseline/input for super-resolution tasks
- **File Size**: ~220KB per frame
- **Use Cases**: Input for 2×, 4×, and 8× super-resolution

### 2. **960x540p** (Medium Resolution)  
- **Resolution**: 960×540 pixels
- **Purpose**: Intermediate target for multi-stage super-resolution
- **File Size**: ~880KB per frame
- **Use Cases**: Input for 2× and 4× super-resolution, target for 2× SR

### 3. **3840x2160p** (High Resolution)
- **Resolution**: 3840×2160 pixels (4K)
- **Purpose**: Ground truth for super-resolution tasks
- **File Size**: ~12MB per frame
- **Use Cases**: Target for all super-resolution tasks

## Tool-Based Organization

Each resolution directory contains video-specific folders organized by surgical tool complexity:

### Folder Naming Convention
```
vid_{video_id}_{resolution}_{tool_category}/
```

**Components:**
- `vid_`: Fixed prefix
- `{video_id}`: 3-digit zero-padded video identifier (001-025)
- `{resolution}`: Resolution specification (480x270p, 960x540p, 3840x2160p)
- `{tool_category}`: Tool complexity indicator (1tool, 2tool, 3tool, 4tool)

### Tool Categories

The tool categories represent the complexity of surgical procedures based on the number of instruments visible:

| Category | Description | Complexity Level |
|----------|-------------|------------------|
| **1tool** | Single instrument procedures | Simplest |
| **2tool** | Two instrument procedures | Moderate |
| **3tool** | Three instrument procedures | Complex |
| **4tool** | Four instrument procedures | Most Complex |

### Examples
```
vid_001_480x270p_1tool/     # Video 1, 480p, single tool
vid_002_960x540p_4tool/     # Video 2, 960p, four tools
vid_018_3840x2160p_3tool/   # Video 18, 4K, three tools
```

## Frame Naming Convention

Individual frames within each video folder follow a consistent naming pattern:

### Format
```
vid_{video_id}_{resolution}_{tool_category}_{frame_number}.png
```

### Examples
```
vid_001_480x270p_1tool_1.png        # First frame
vid_001_480x270p_1tool_37.png       # Last frame (37 frames total)
vid_002_960x540p_4tool_38.png       # Frame 38 from video 2
vid_018_3840x2160p_3tool_533.png    # Frame 533 from video 18
```

## Frame Sequences

- **Frame Numbering**: Sequential integers starting from 1
- **Frame Count**: Varies by video (typically 30-540 frames per video)
- **Frame Format**: PNG with lossless compression
- **Frame Rate**: Extracted from 30 FPS source videos

## Dataset Statistics

### Distribution by Resolution
- **Total Frames**: 2,400 (800 frames per resolution)
- **Video Count**: 25 videos per resolution
- **Resolution Variants**: 3 (480p, 960p, 4K)

### Distribution by Tool Complexity
The dataset contains varying numbers of videos for each tool category:

| Tool Category | Number of Videos | Percentage |
|---------------|------------------|------------|
| 1tool         | ~6 videos        | ~24%       |
| 2tool         | ~7 videos        | ~28%       |
| 3tool         | ~8 videos        | ~32%       |
| 4tool         | ~4 videos        | ~16%       |

## Data Consistency

### Cross-Resolution Alignment
- **Temporal Alignment**: Frames across resolutions represent identical time points
- **Content Alignment**: Same surgical content at different quality levels
- **Filename Consistency**: Frame numbers match across resolution variants

### Example of Aligned Frames
```
vid_001_480x270p_1tool_5.png    # Low-res version of frame 5
vid_001_960x540p_1tool_5.png    # Mid-res version of frame 5  
vid_001_3840x2160p_1tool_5.png  # High-res version of frame 5
```

## Access Patterns

### By Resolution
```python
# Low resolution frames
data/images/480x270p/vid_*/vid_*_480x270p_*tool_*.png

# Medium resolution frames  
data/images/960x540p/vid_*/vid_*_960x540p_*tool_*.png

# High resolution frames
data/images/3840x2160p/vid_*/vid_*_3840x2160p_*tool_*.png
```

### By Tool Complexity
```python
# Single tool procedures across all resolutions
data/images/*/vid_*_*_1tool/

# Multi-tool procedures (2+ tools)
data/images/*/vid_*_*_[2-4]tool/
```

### By Video ID
```python
# All variants of video 001
data/images/*/vid_001_*_*tool/

# Specific video-resolution combination
data/images/960x540p/vid_015_960x540p_3tool/
```

## Use Cases

### Super-Resolution Tasks
- **2× SR**: 480p → 960p
- **4× SR**: 480p → 3840p  
- **8× SR**: 480p → 3840p (via 960p intermediate)

### Tool Detection/Classification
- Use tool category labels for instrument detection training
- Progressive complexity for model evaluation

### Multi-Scale Analysis
- Compare feature extraction across resolution levels
- Evaluate scale-invariant algorithms

## Quality Considerations

### Resolution-Specific Characteristics
- **480p**: Suitable for fast processing, limited detail
- **960p**: Balance between quality and computational cost
- **4K**: Full detail preservation, computationally intensive

### Tool Complexity Impact
- **1tool**: Cleaner scenes, less occlusion
- **4tool**: Higher complexity, more occlusions and interactions

---

*This organization ensures consistent access to surgical video data across multiple resolutions and complexity levels, supporting diverse computer vision research applications.* 