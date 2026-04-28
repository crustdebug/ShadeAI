#!/usr/bin/env python3
"""
Annotate MST Dataset
Automatically extracts skin tone features from images and creates training annotations
"""
import os
import csv
import cv2
import numpy as np
from pathlib import Path
from skimage import color as skcolor
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline.face_detector import detect_and_crop
from backend.pipeline.skin_segmentor import segment_skin_rule_based, get_skin_pixels
from backend.pipeline.feature_extractor import compute_ita


def annotate_image(image_path: str, mst_class: int):
    """Extract features from a single image"""
    try:
        # Read image
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            return None
        
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Detect face
        face_crop, detection = detect_and_crop(img_rgb)
        if face_crop is None:
            print(f"  ⚠️  No face detected: {os.path.basename(image_path)}")
            return None
        
        # Segment skin
        mask = segment_skin_rule_based(face_crop)
        skin_pixels = get_skin_pixels(face_crop, mask)
        
        if len(skin_pixels) < 100:
            print(f"  ⚠️  Insufficient skin pixels: {os.path.basename(image_path)}")
            return None
        
        # Extract features
        ita = compute_ita(skin_pixels)
        
        # Compute mean LAB
        skin_float = skin_pixels.astype(np.float32) / 255.0
        skin_lab = skcolor.rgb2lab(skin_float.reshape(-1, 1, 3)).reshape(-1, 3)
        mean_lab = skin_lab.mean(axis=0)
        
        # Estimate undertone from b* channel
        b_star = mean_lab[2]
        a_star = mean_lab[1]
        undertone_score = 0.0
        if b_star > 15:
            undertone_score += 0.4
        elif b_star < 10:
            undertone_score -= 0.4
        if a_star > 12:
            undertone_score += 0.3
        elif a_star < 8:
            undertone_score -= 0.3
        undertone_score = float(np.clip(undertone_score, -1.0, 1.0))
        
        return {
            'image_path': image_path,
            'mst_class': mst_class,
            'undertone_score': round(undertone_score, 3),
            'ita_degrees': round(ita, 2),
            'L_star': round(float(mean_lab[0]), 2),
            'a_star': round(float(mean_lab[1]), 2),
            'b_star': round(float(mean_lab[2]), 2),
            'skin_pixel_count': len(skin_pixels)
        }
    
    except Exception as e:
        print(f"  ❌ Error processing {os.path.basename(image_path)}: {e}")
        return None


def annotate_dataset(dataset_dir: str = "dataset/mst", output_csv: str = "dataset/annotations.csv"):
    """Annotate entire MST dataset"""
    
    print("=" * 60)
    print("MST Dataset Annotation Tool")
    print("=" * 60)
    
    dataset_path = Path(dataset_dir)
    if not dataset_path.exists():
        print(f"❌ Dataset directory not found: {dataset_dir}")
        print("Run: python data_preparation/download_mst_dataset.py")
        return
    
    annotations = []
    
    # Process each MST class
    for mst_class in range(10):
        class_dirs = [
            dataset_path / f"mst_{mst_class:02d}",
            dataset_path / f"mst_{mst_class+1:02d}",
            dataset_path / f"MST-{mst_class+1:02d}",
            dataset_path / f"class_{mst_class}"
        ]
        
        class_dir = None
        for d in class_dirs:
            if d.exists():
                class_dir = d
                break
        
        if class_dir is None:
            print(f"\n⚠️  MST-{mst_class+1:02d}: Directory not found")
            continue
        
        # Find all images
        image_files = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")) + list(class_dir.glob("*.jpeg"))
        
        if len(image_files) == 0:
            print(f"\n⚠️  MST-{mst_class+1:02d}: No images found")
            continue
        
        print(f"\n📊 Processing MST-{mst_class+1:02d} ({len(image_files)} images)...")
        
        success_count = 0
        for img_path in image_files:
            annotation = annotate_image(str(img_path), mst_class)
            if annotation:
                annotations.append(annotation)
                success_count += 1
                if success_count % 10 == 0:
                    print(f"  ✓ Processed {success_count}/{len(image_files)}")
        
        print(f"  ✅ Successfully annotated: {success_count}/{len(image_files)}")
    
    # Save annotations
    if len(annotations) == 0:
        print("\n❌ No annotations created. Check dataset structure.")
        return
    
    print(f"\n💾 Saving annotations to: {output_csv}")
    
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ['image_path', 'mst_class', 'undertone_score', 'ita_degrees', 
                     'L_star', 'a_star', 'b_star', 'skin_pixel_count']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(annotations)
    
    print(f"✅ Saved {len(annotations)} annotations")
    
    # Print statistics
    print("\n📊 Dataset Statistics:")
    print("=" * 60)
    
    class_counts = {}
    for ann in annotations:
        mst_class = ann['mst_class']
        class_counts[mst_class] = class_counts.get(mst_class, 0) + 1
    
    for mst_class in range(10):
        count = class_counts.get(mst_class, 0)
        label = ["Porcelain", "Fair", "Light", "Light-Medium", "Medium", 
                "Medium-Dark", "Tan", "Brown", "Deep Brown", "Deep"][mst_class]
        print(f"MST-{mst_class+1:02d} {label:15s}: {count:4d} images")
    
    print(f"\nTotal: {len(annotations)} annotated images")
    print("\n✅ Dataset ready for training!")
    print("Next step: python training/train_classifier.py")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Annotate MST dataset")
    parser.add_argument("--input", default="dataset/mst", help="Input dataset directory")
    parser.add_argument("--output", default="dataset/annotations.csv", help="Output CSV file")
    
    args = parser.parse_args()
    
    annotate_dataset(args.input, args.output)
