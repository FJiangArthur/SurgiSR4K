#!/bin/bash

# Example usage of the split.py script
# This script demonstrates how to organize the SurgiSR4K dataset based on tool folders

echo "SurgiSR4K Tool-Based Dataset Organization Examples"
echo "================================================="

# Basic usage - organize with default 70/15/15 split
echo "1. Basic organization (default 70/15/15 split):"
echo "python scripts/split.py --input_dir ./data/images --output_dir ./data/images_organized"
echo ""

# Custom split ratios
echo "2. Custom split ratios (80/10/10):"
echo "python scripts/split.py --input_dir ./data/images --output_dir ./data/images_organized --train_ratio 0.8 --val_ratio 0.1 --test_ratio 0.1"
echo ""



# Different seed for reproducibility
echo "4. Different random seed:"
echo "python scripts/split.py --input_dir ./data/images --output_dir ./data/images_organized --seed 123"
echo ""

echo "Expected output structure:"
echo "data/images_organized/"
echo "├── train/"
echo "│   ├── 3840x2160p/"
echo "│   │   ├── vid_014_3840x2160p_3tool/"
echo "│   │   │   ├── image1.png"
echo "│   │   │   └── image2.png"
echo "│   │   └── ..."
echo "│   ├── 960x540p/"
echo "│   │   ├── vid_014_3840x2160p_3tool/"
echo "│   │   │   ├── image1.png"
echo "│   │   │   └── image2.png"
echo "│   │   └── ..."
echo "│   └── 480x270p/"
echo "├── val/"
echo "│   ├── 3840x2160p/"
echo "│   ├── 960x540p/"
echo "│   └── 480x270p/"
echo "└── test/"
echo "    ├── 3840x2160p/"
echo "    ├── 960x540p/"
echo "    └── 480x270p/"
echo ""

echo "Note: The same frames will be in the same split across all resolutions"
echo "For example, if image1.png is in train for 3840x2160p, it will also be in train for 960x540p and 480x270p"
