#!/usr/bin/env python3
"""
Validate Data Preparation
Checks that all data files are present and correctly formatted
"""
import json
import os
from pathlib import Path


def validate_foundation_database():
    """Validate foundation shade database"""
    print("\n📊 Validating Foundation Database...")
    
    db_path = Path("backend/data/foundation_shades.json")
    
    if not db_path.exists():
        print("  ❌ Database not found!")
        return False
    
    with open(db_path, 'r') as f:
        shades = json.load(f)
    
    print(f"  ✓ Found {len(shades)} shades")
    
    # Check required fields
    required_fields = ['id', 'brand', 'product', 'shade_name', 'L', 'a', 'b', 
                      'undertone', 'mst_range', 'hex_approx', 'buy_url']
    
    errors = []
    for i, shade in enumerate(shades):
        for field in required_fields:
            if field not in shade:
                errors.append(f"Shade {i} missing field: {field}")
        
        # Validate CIELAB ranges
        if not (0 <= shade.get('L', -1) <= 100):
            errors.append(f"Shade {shade.get('id', i)}: Invalid L* value")
        if not (-128 <= shade.get('a', -200) <= 127):
            errors.append(f"Shade {shade.get('id', i)}: Invalid a* value")
        if not (-128 <= shade.get('b', -200) <= 127):
            errors.append(f"Shade {shade.get('id', i)}: Invalid b* value")
    
    if errors:
        print(f"  ❌ Found {len(errors)} errors:")
        for error in errors[:5]:
            print(f"     - {error}")
        if len(errors) > 5:
            print(f"     ... and {len(errors) - 5} more")
        return False
    
    # Check MST coverage
    mst_coverage = {}
    for shade in shades:
        for mst in shade['mst_range']:
            mst_coverage[mst] = mst_coverage.get(mst, 0) + 1
    
    print(f"  ✓ MST Coverage:")
    for mst in sorted(mst_coverage.keys()):
        print(f"     {mst}: {mst_coverage[mst]} shades")
    
    # Check brand distribution
    brands = {}
    for shade in shades:
        brand = shade['brand']
        brands[brand] = brands.get(brand, 0) + 1
    
    print(f"  ✓ Brands: {len(brands)}")
    for brand, count in sorted(brands.items()):
        print(f"     {brand}: {count} shades")
    
    print("  ✅ Database validation passed!")
    return True


def validate_example_photos():
    """Validate example photos"""
    print("\n📸 Validating Example Photos...")
    
    assets_dir = Path("frontend/assets")
    
    if not assets_dir.exists():
        print("  ❌ Assets directory not found!")
        return False
    
    required_files = [
        "example_good_1.jpg",
        "example_good_2.jpg",
        "example_good_3.jpg",
        "example_bad_flash.jpg",
        "example_bad_shadow.jpg",
        "example_bad_angle.jpg",
        "example_bad_filter.jpg",
        "example_bad_makeup.jpg",
        "example_bad_lighting.jpg",
        "monk_scale_chart.png"
    ]
    
    missing = []
    for filename in required_files:
        filepath = assets_dir / filename
        if not filepath.exists():
            missing.append(filename)
        else:
            size = filepath.stat().st_size
            print(f"  ✓ {filename} ({size:,} bytes)")
    
    if missing:
        print(f"  ⚠️  Missing {len(missing)} files:")
        for filename in missing:
            print(f"     - {filename}")
        print("  Run: python data_preparation/create_example_photos.py")
        return False
    
    print("  ✅ All example photos present!")
    return True


def validate_data_scripts():
    """Validate data preparation scripts"""
    print("\n🔧 Validating Data Preparation Scripts...")
    
    scripts_dir = Path("data_preparation")
    
    required_scripts = [
        "README_DATA.md",
        "download_mst_dataset.py",
        "annotate_mst_dataset.py",
        "expand_foundation_database.py",
        "create_example_photos.py",
        "validate_data.py"
    ]
    
    missing = []
    for filename in required_scripts:
        filepath = scripts_dir / filename
        if not filepath.exists():
            missing.append(filename)
        else:
            print(f"  ✓ {filename}")
    
    if missing:
        print(f"  ❌ Missing {len(missing)} scripts:")
        for filename in missing:
            print(f"     - {filename}")
        return False
    
    print("  ✅ All scripts present!")
    return True


def validate_dataset_structure():
    """Check if dataset directory exists"""
    print("\n📁 Checking Dataset Structure...")
    
    dataset_dir = Path("dataset")
    
    if not dataset_dir.exists():
        print("  ⚠️  Dataset directory not found")
        print("  This is OK - dataset is optional for current system")
        print("  To download: python data_preparation/download_mst_dataset.py")
        return True
    
    mst_dir = dataset_dir / "mst"
    if mst_dir.exists():
        # Count images
        total_images = 0
        for mst_class in range(10):
            class_dir = mst_dir / f"mst_{mst_class+1:02d}"
            if class_dir.exists():
                count = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.png")))
                if count > 0:
                    print(f"  ✓ MST-{mst_class+1:02d}: {count} images")
                    total_images += count
        
        if total_images > 0:
            print(f"  ✅ Found {total_images} training images")
        else:
            print("  ⚠️  No images found in dataset/mst/")
    else:
        print("  ⚠️  dataset/mst/ not found")
        print("  To download: python data_preparation/download_mst_dataset.py")
    
    return True


def main():
    """Run all validations"""
    print("=" * 60)
    print("ShadeAI Data Validation")
    print("=" * 60)
    
    results = []
    
    # Run validations
    results.append(("Foundation Database", validate_foundation_database()))
    results.append(("Example Photos", validate_example_photos()))
    results.append(("Data Scripts", validate_data_scripts()))
    results.append(("Dataset Structure", validate_dataset_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:25s}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All validations passed!")
        print("\nSystem is ready to use:")
        print("  python shadeai_cli.py test1.jpg")
        print("  streamlit run streamlit_app.py")
    else:
        print("⚠️  Some validations failed")
        print("\nCheck errors above and run:")
        print("  python data_preparation/expand_foundation_database.py")
        print("  python data_preparation/create_example_photos.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
