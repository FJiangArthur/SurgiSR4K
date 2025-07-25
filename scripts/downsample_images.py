#!/usr/bin/env python3
"""
Script to downsample SurgiSR4K images from 3840x2160 to 960x540 and 480x270
while preserving folder structure and filenames.
"""

import os
import sys
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import argparse


def downsample_image(input_path, output_path, target_size):
    """
    Downsample a single image to target size.
    
    Args:
        input_path (Path): Path to input image
        output_path (Path): Path to save downsampled image
        target_size (tuple): Target size as (width, height)
    """
    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open and resize image
        with Image.open(input_path) as img:
            # Use LANCZOS for high-quality downsampling
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
            resized_img.save(output_path, 'PNG', optimize=True)
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False
    
    return True


def process_dataset(source_dir, output_dirs, target_sizes):
    """
    Process entire dataset, downsampling all images.
    
    Args:
        source_dir (Path): Source directory containing 3840x2160 images
        output_dirs (list): List of output directories for each target size
        target_sizes (list): List of target sizes as (width, height) tuples
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory {source_dir} does not exist!")
        return
    
    # Find all PNG files in subdirectories
    image_files = list(source_path.rglob("*.png"))
    
    if not image_files:
        print(f"No PNG files found in {source_dir}")
        return
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each target size
    for output_dir, target_size in zip(output_dirs, target_sizes):
        print(f"\nProcessing images for size {target_size[0]}x{target_size[1]}...")
        
        output_path = Path(output_dir)
        successful = 0
        
        # Process each image with progress bar
        for img_file in tqdm(image_files, desc=f"Downsampling to {target_size[0]}x{target_size[1]}"):
            # Calculate relative path from source directory
            rel_path = img_file.relative_to(source_path)
            
            # Modify filename to reflect new resolution
            filename = rel_path.name
            # Replace 3840x2160p with target resolution in filename
            new_filename = filename.replace('3840x2160p', f'{target_size[0]}x{target_size[1]}p')
            
            # Create corresponding output path with modified filename
            output_file = output_path / rel_path.parent / new_filename
            
            # Skip if output file already exists
            if output_file.exists():
                continue
            
            # Downsample the image
            if downsample_image(img_file, output_file, target_size):
                successful += 1
        
        print(f"Successfully processed {successful} images for {target_size[0]}x{target_size[1]}")


def main():
    parser = argparse.ArgumentParser(description='Downsample SurgiSR4K images')
    parser.add_argument('--source', 
                       default='./data/images/3840x2160p',
                       help='Source directory containing 3840x2160 images')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without actually doing it')
    
    args = parser.parse_args()
    
    # Define paths and target sizes
    source_dir = args.source
    base_dir = Path(source_dir).parent
    
    output_dirs = [
        base_dir / "960x540p",
        base_dir / "480x270p"
    ]
    
    target_sizes = [
        (960, 540),   # Quarter resolution
        (480, 270)    # Sixteenth resolution
    ]
    
    print("SurgiSR4K Image Downsampling Script")
    print("=" * 40)
    print(f"Source directory: {source_dir}")
    print(f"Output directories:")
    for out_dir, size in zip(output_dirs, target_sizes):
        print(f"  - {out_dir} (size: {size[0]}x{size[1]})")
    
    if args.dry_run:
        print("\nDRY RUN MODE - No files will be processed")
        source_path = Path(source_dir)
        if source_path.exists():
            image_files = list(source_path.rglob("*.png"))
            print(f"Would process {len(image_files)} images")
        return
    
    # Confirm before proceeding
    response = input("\nProceed with downsampling? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Process the dataset
    process_dataset(source_dir, output_dirs, target_sizes)
    print("\nDownsampling complete!")


if __name__ == "__main__":
    main()
