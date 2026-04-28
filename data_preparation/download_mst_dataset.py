#!/usr/bin/env python3
"""
Download Monk Skin Tone Dataset
Automatically downloads and organizes the MST dataset for training
"""
import os
import urllib.request
import zipfile
from pathlib import Path

def download_mst_dataset():
    """Download MST dataset from Google Research"""
    
    print("=" * 60)
    print("Monk Skin Tone Dataset Downloader")
    print("=" * 60)
    
    # Create dataset directory
    dataset_dir = Path("dataset/mst")
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n📥 Downloading MST Dataset...")
    print("Source: Google Research - Monk Skin Tone Scale")
    print("URL: https://skintone.google/mste-dataset")
    
    # Note: This is a placeholder URL - replace with actual dataset URL
    dataset_url = "https://storage.googleapis.com/monk-skin-tone-dataset/mst_dataset.zip"
    zip_path = "dataset/mst_dataset.zip"
    
    print(f"\n⚠️  MANUAL DOWNLOAD REQUIRED")
    print("=" * 60)
    print("The Monk Skin Tone dataset requires manual download:")
    print()
    print("1. Visit: https://skintone.google/mste-dataset")
    print("2. Request access to the dataset")
    print("3. Download the dataset ZIP file")
    print("4. Place it in: dataset/mst_dataset.zip")
    print("5. Run this script again to extract")
    print()
    print("Alternative datasets:")
    print("- FairFace: https://github.com/joojs/fairface")
    print("- UTKFace: https://susanqq.github.io/UTKFace/")
    print("- Diversity in Faces: https://www.research.ibm.com/artificial-intelligence/trusted-ai/diversity-in-faces/")
    print("=" * 60)
    
    # Check if ZIP already exists
    if os.path.exists(zip_path):
        print(f"\n✅ Found dataset ZIP: {zip_path}")
        print("📦 Extracting...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("dataset/mst")
        
        print(f"✅ Extracted to: dataset/mst/")
        print("\n📊 Dataset Statistics:")
        
        # Count images per class
        for mst_class in range(1, 11):
            class_dir = dataset_dir / f"mst_{mst_class:02d}"
            if class_dir.exists():
                count = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.png")))
                print(f"   MST-{mst_class:02d}: {count} images")
        
        print("\n✅ Dataset ready for training!")
        print("Next step: python data_preparation/annotate_mst_dataset.py")
    else:
        print(f"\n❌ Dataset ZIP not found: {zip_path}")
        print("Please download manually and place in dataset/ folder")
    
    # Create README
    readme_path = dataset_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write("""# Monk Skin Tone Dataset

## Structure

```
mst/
├── mst_01_porcelain/
├── mst_02_fair/
├── mst_03_light/
├── mst_04_light_medium/
├── mst_05_medium/
├── mst_06_medium_dark/
├── mst_07_tan/
├── mst_08_brown/
├── mst_09_deep_brown/
└── mst_10_deep/
```

## Annotation Format

Each image should have corresponding metadata:
- MST class (0-9)
- Undertone score (-1.0 to +1.0)
- Mean CIELAB values (L*, a*, b*)

## Usage

```bash
# Annotate dataset
python data_preparation/annotate_mst_dataset.py

# Train classifier
python training/train_classifier.py --data dataset/mst/
```

## Sources

- Google MST: https://skintone.google/mste-dataset
- FairFace: https://github.com/joojs/fairface
- UTKFace: https://susanqq.github.io/UTKFace/
""")
    
    print(f"\n📄 Created README: {readme_path}")


if __name__ == "__main__":
    download_mst_dataset()
