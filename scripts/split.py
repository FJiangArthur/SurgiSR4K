#!/usr/bin/env python3
"""
Script to organize SurgiSR4K dataset into train/val/test splits based on tool folders.
Handles resolution-specific frame naming correctly.

Usage:
    python scripts/split.py --input_dir ./data/images --output_dir ./data/images_organized
"""

import os
import shutil
import argparse
import random
import re
from pathlib import Path
from tqdm import tqdm
import pandas as pd


def normalize_tool_folder_name(folder_name):
    """Normalize tool folder name by removing resolution part"""
    # Pattern to match: vid_XXX_RESOLUTIONxRESOLUTIONp_Ytool
    # We want to extract: vid_XXX_Ytool
    pattern = r'(vid_\d+)_\d+x\d+p_(\d+tool)'
    match = re.match(pattern, folder_name)
    if match:
        return f"{match.group(1)}_{match.group(2)}"
    return folder_name


def extract_frame_number_from_name(frame_name):
    """Extract frame number from frame filename"""
    # Pattern: vid_XXX_RESOLUTIONxRESOLUTIONp_Ytool_FRAMENUM.png
    pattern = r'vid_\d+_\d+x\d+p_\d+tool_(\d+)\.png'
    match = re.match(pattern, frame_name)
    if match:
        return int(match.group(1))
    return None


def generate_frame_name_for_resolution(reference_frame_name, target_resolution, tool_folder_actual_name):
    """Generate the expected frame name for a different resolution"""
    frame_number = extract_frame_number_from_name(reference_frame_name)
    if frame_number is None:
        return None
    
    # Extract the base name from the tool folder
    # tool_folder_actual_name example: vid_014_3840x2160p_3tool
    pattern = r'(vid_\d+)_\d+x\d+p_(\d+tool)'
    match = re.match(pattern, tool_folder_actual_name)
    if not match:
        return None
    
    vid_part = match.group(1)
    tool_part = match.group(2)
    
    return f"{vid_part}_{target_resolution}_{tool_part}_{frame_number}.png"


def discover_dataset_structure(images_dir):
    """Discover the existing dataset structure"""
    images_dir = Path(images_dir)
    
    # Find all resolution folders
    resolution_folders = [d for d in images_dir.iterdir() if d.is_dir() and 'x' in d.name]
    print(f"Found resolution folders: {[d.name for d in resolution_folders]}")
    
    # Find all tool folders within each resolution and normalize names
    tool_folders = {}
    normalized_mapping = {}  # Maps normalized name to actual folder names per resolution
    
    for res_folder in resolution_folders:
        tool_dirs = [d for d in res_folder.iterdir() if d.is_dir()]
        tool_folders[res_folder.name] = [d.name for d in tool_dirs]
        
        # Create mapping for this resolution
        normalized_mapping[res_folder.name] = {}
        for tool_dir in tool_dirs:
            normalized_name = normalize_tool_folder_name(tool_dir.name)
            normalized_mapping[res_folder.name][normalized_name] = tool_dir.name
        
        print(f"Resolution {res_folder.name}: {len(tool_dirs)} tool folders")
    
    # Get common normalized tool folders
    first_res = list(normalized_mapping.keys())[0]
    common_normalized = set(normalized_mapping[first_res].keys())
    
    for res, mapping in normalized_mapping.items():
        common_normalized &= set(mapping.keys())
    
    print(f"Common tool folders across all resolutions: {len(common_normalized)}")
    
    return list(resolution_folders), sorted(common_normalized), normalized_mapping


def split_frames_randomly(frame_files, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    """Randomly split frame files into train/val/test"""
    
    # Ensure ratios sum to 1
    total_ratio = train_ratio + val_ratio + test_ratio
    if abs(total_ratio - 1.0) > 1e-6:
        raise ValueError(f"Split ratios must sum to 1.0, got {total_ratio}")
    
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Shuffle frames
    frame_files = list(frame_files)
    random.shuffle(frame_files)
    
    total_frames = len(frame_files)
    train_count = int(total_frames * train_ratio)
    val_count = int(total_frames * val_ratio)
    
    # Split frames
    train_frames = frame_files[:train_count]
    val_frames = frame_files[train_count:train_count + val_count]
    test_frames = frame_files[train_count + val_count:]
    
    return {
        'train': train_frames,
        'val': val_frames,
        'test': test_frames
    }


def create_organized_structure(output_dir, resolutions, splits=['train', 'val', 'test']):
    """Create the organized directory structure"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    created_dirs = []
    
    for split in splits:
        split_dir = output_dir / split
        split_dir.mkdir(exist_ok=True)
        
        for resolution in resolutions:
            res_dir = split_dir / resolution
            res_dir.mkdir(exist_ok=True)
            created_dirs.append(res_dir)
            print(f"Created: {res_dir}")
    
    return created_dirs


def copy_frames_for_split(input_dir, output_dir, resolution, actual_tool_folder, split_name, reference_frame_names):
    """Copy frames for a specific split, handling resolution-specific naming"""
    
    source_dir = Path(input_dir) / resolution / actual_tool_folder
    target_dir = Path(output_dir) / split_name / resolution / actual_tool_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    
    for ref_frame_name in reference_frame_names:
        # Generate the correct frame name for this resolution
        target_frame_name = generate_frame_name_for_resolution(ref_frame_name, resolution, actual_tool_folder)
        
        if target_frame_name is None:
            print(f"Warning: Could not generate frame name for {ref_frame_name} in {resolution}")
            continue
            
        source_path = source_dir / target_frame_name
        target_path = target_dir / target_frame_name
        
        if source_path.exists():
            shutil.copy2(source_path, target_path)
            copied_count += 1
        else:
            print(f"Warning: {source_path} not found")
    
    return copied_count


def organize_dataset(input_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    """Main function to organize the dataset"""
    
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    # Discover dataset structure
    resolution_folders, common_normalized_tools, normalized_mapping = discover_dataset_structure(input_dir)
    resolution_names = [rf.name for rf in resolution_folders]
    
    # Create output structure
    create_organized_structure(output_dir, resolution_names)
    
    # Process each tool folder
    total_stats = {
        'train': {res: 0 for res in resolution_names},
        'val': {res: 0 for res in resolution_names},
        'test': {res: 0 for res in resolution_names}
    }
    
    split_info = []  # To save split information
    
    print(f"\nProcessing {len(common_normalized_tools)} tool folders...")
    
    for normalized_tool in tqdm(common_normalized_tools, desc="Processing tool folders"):
        
        # Get the actual folder name for the reference resolution (first one)
        reference_resolution = resolution_names[0]
        actual_ref_folder = normalized_mapping[reference_resolution][normalized_tool]
        ref_tool_path = input_dir / reference_resolution / actual_ref_folder
        
        if not ref_tool_path.exists():
            print(f"Warning: Reference tool folder not found: {ref_tool_path}")
            continue
        
        # Get all frame files from reference resolution
        frame_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            frame_files.extend(ref_tool_path.glob(ext))
        
        frame_names = [f.name for f in frame_files]
        
        if not frame_names:
            print(f"Warning: No frames found in {ref_tool_path}")
            continue
        
        # Split frames randomly
        splits = split_frames_randomly(
            frame_names, 
            train_ratio=train_ratio, 
            val_ratio=val_ratio, 
            test_ratio=test_ratio, 
            seed=seed
        )
        
        # Record split information
        split_info.append({
            'normalized_tool_folder': normalized_tool,
            'reference_folder': actual_ref_folder,
            'total_frames': len(frame_names),
            'train_frames': len(splits['train']),
            'val_frames': len(splits['val']),
            'test_frames': len(splits['test'])
        })
        
        # Copy frames for each split and resolution
        for split_name, split_frames in splits.items():
            if not split_frames:
                continue
                
            for resolution in resolution_names:
                # Get the actual folder name for this resolution
                actual_tool_folder = normalized_mapping[resolution][normalized_tool]
                
                copied_count = copy_frames_for_split(
                    input_dir, output_dir, resolution, actual_tool_folder, 
                    split_name, split_frames
                )
                total_stats[split_name][resolution] += copied_count
    
    # Save split information
    split_df = pd.DataFrame(split_info)
    split_df.to_csv(output_dir / 'split_info.csv', index=False)
    print(f"\nSplit information saved to {output_dir / 'split_info.csv'}")
    
    # Print summary
    print("\n" + "="*60)
    print("DATASET ORGANIZATION SUMMARY")
    print("="*60)
    
    for split_name in ['train', 'val', 'test']:
        print(f"\n{split_name.upper()} SPLIT:")
        split_total = sum(total_stats[split_name].values())
        print(f"  Total frames: {split_total:,}")
        
        for resolution in resolution_names:
            count = total_stats[split_name][resolution]
            percentage = (count / split_total * 100) if split_total > 0 else 0
            print(f"  {resolution}: {count:,} frames ({percentage:.1f}%)")
    
    # Overall statistics
    grand_total = sum(sum(split_stats.values()) for split_stats in total_stats.values())
    print(f"\nGRAND TOTAL: {grand_total:,} frames")
    
    # Split ratios
    train_total = sum(total_stats['train'].values())
    val_total = sum(total_stats['val'].values())
    test_total = sum(total_stats['test'].values())
    
    if grand_total > 0:
        print(f"\nACTUAL SPLIT RATIOS:")
        print(f"  Train: {train_total/grand_total:.1%}")
        print(f"  Val: {val_total/grand_total:.1%}")
        print(f"  Test: {test_total/grand_total:.1%}")
    
    print(f"\nDataset organized successfully in: {output_dir}")
    return total_stats


def verify_organization(organized_dir):
    """Verify the organized dataset structure"""
    
    organized_dir = Path(organized_dir)
    
    print("\nVerifying organized dataset structure...")
    
    splits = ['train', 'val', 'test']
    verification_results = {}
    
    for split in splits:
        split_dir = organized_dir / split
        if not split_dir.exists():
            print(f"ERROR: {split} directory not found")
            continue
        
        split_results = {}
        
        # Find resolution folders
        resolution_folders = [d for d in split_dir.iterdir() if d.is_dir()]
        
        for res_folder in resolution_folders:
            resolution = res_folder.name
            
            # Count tool folders and frames
            tool_folders = [d for d in res_folder.iterdir() if d.is_dir()]
            tool_count = len(tool_folders)
            
            frame_count = 0
            for tool_folder in tool_folders:
                frames = list(tool_folder.glob('*.png')) + list(tool_folder.glob('*.jpg'))
                frame_count += len(frames)
            
            split_results[resolution] = {
                'tool_folders': tool_count,
                'frames': frame_count
            }
            
            print(f"OK: {split}/{resolution}: {tool_count} tool folders, {frame_count} frames")
        
        verification_results[split] = split_results
    
    return verification_results


def main():
    parser = argparse.ArgumentParser(
        description='Organize SurgiSR4K dataset into train/val/test splits based on tool folders'
    )
    parser.add_argument(
        '--input_dir', 
        type=str, 
        required=True,
        help='Input directory containing the images (e.g., ./data/images)'
    )
    parser.add_argument(
        '--output_dir', 
        type=str, 
        required=True,
        help='Output directory for organized dataset'
    )
    parser.add_argument(
        '--train_ratio',
        type=float,
        default=0.7,
        help='Training set ratio (default: 0.7)'
    )
    parser.add_argument(
        '--val_ratio',
        type=float,
        default=0.15,
        help='Validation set ratio (default: 0.15)'
    )
    parser.add_argument(
        '--test_ratio',
        type=float,
        default=0.15,
        help='Test set ratio (default: 0.15)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducible splits (default: 42)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify the organized dataset after creation'
    )
    
    args = parser.parse_args()
    
    # Validate ratios
    total_ratio = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(total_ratio - 1.0) > 1e-6:
        print(f"ERROR: Split ratios must sum to 1.0, got {total_ratio}")
        return 1
    
    try:
        # Organize the dataset
        stats = organize_dataset(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            train_ratio=args.train_ratio,
            val_ratio=args.val_ratio,
            test_ratio=args.test_ratio,
            seed=args.seed
        )
        
        # Verify if requested
        if args.verify:
            verify_organization(args.output_dir)
        
        print(f"\nDataset organization completed successfully!")
        print(f"Organized dataset available at: {args.output_dir}")
        
    except Exception as e:
        print(f"ERROR: Error organizing dataset: {str(e)}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
