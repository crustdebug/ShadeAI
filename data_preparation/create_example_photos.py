#!/usr/bin/env python3
"""
Create Example Photos for UX Guidelines
Generates or downloads example good/bad photos for the Streamlit UI
"""
import os
import cv2
import numpy as np
from pathlib import Path
import urllib.request


def create_placeholder_image(width=800, height=600, text="", color=(200, 200, 200)):
    """Create a placeholder image with text"""
    img = np.ones((height, width, 3), dtype=np.uint8) * np.array(color, dtype=np.uint8)
    
    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    thickness = 2
    
    # Calculate text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Center text
    x = (width - text_width) // 2
    y = (height + text_height) // 2
    
    cv2.putText(img, text, (x, y), font, font_scale, (50, 50, 50), thickness)
    
    return img


def create_example_photos():
    """Create example photos for UX guidelines"""
    
    print("=" * 60)
    print("Example Photo Generator")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("frontend/assets")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Define examples
    examples = {
        # Good examples
        "example_good_1.jpg": {
            "text": "GOOD: Natural Window Light",
            "color": (220, 240, 220),
            "description": "Perfect natural lighting from window"
        },
        "example_good_2.jpg": {
            "text": "GOOD: Overcast Daylight",
            "color": (220, 240, 220),
            "description": "Soft diffused outdoor light"
        },
        "example_good_3.jpg": {
            "text": "GOOD: Soft Indoor Lighting",
            "color": (220, 240, 220),
            "description": "Even indoor LED lighting"
        },
        
        # Bad examples
        "example_bad_flash.jpg": {
            "text": "BAD: Flash Photography",
            "color": (240, 220, 220),
            "description": "Harsh flash causes color distortion"
        },
        "example_bad_shadow.jpg": {
            "text": "BAD: Strong Shadows",
            "color": (240, 220, 220),
            "description": "Uneven lighting with shadows"
        },
        "example_bad_angle.jpg": {
            "text": "BAD: Side Profile",
            "color": (240, 220, 220),
            "description": "Face not forward-facing"
        },
        "example_bad_filter.jpg": {
            "text": "BAD: Beauty Filter",
            "color": (240, 220, 220),
            "description": "AI smoothing alters skin tone"
        },
        "example_bad_makeup.jpg": {
            "text": "BAD: Heavy Makeup",
            "color": (240, 220, 220),
            "description": "Foundation covers natural tone"
        },
        "example_bad_lighting.jpg": {
            "text": "BAD: Colored Lighting",
            "color": (240, 220, 220),
            "description": "Warm/cool bulbs distort color"
        }
    }
    
    print("\n🎨 Creating placeholder images...")
    
    for filename, info in examples.items():
        output_path = output_dir / filename
        
        # Create placeholder
        img = create_placeholder_image(
            width=800,
            height=600,
            text=info['text'],
            color=info['color']
        )
        
        # Save image
        cv2.imwrite(str(output_path), img)
        print(f"  ✓ Created: {filename} - {info['description']}")
    
    # Create Monk Scale chart placeholder
    monk_chart_path = output_dir / "monk_scale_chart.png"
    monk_img = create_monk_scale_chart()
    cv2.imwrite(str(monk_chart_path), monk_img)
    print(f"  ✓ Created: monk_scale_chart.png")
    
    print(f"\n✅ Created {len(examples) + 1} example images")
    
    # Create README
    readme_path = output_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write("""# Frontend Assets

## Example Photos

These images demonstrate good and bad photo practices for skin tone analysis.

### Good Examples
- **example_good_1.jpg**: Natural window light, face forward
- **example_good_2.jpg**: Overcast daylight, soft diffused
- **example_good_3.jpg**: Soft indoor LED lighting

### Bad Examples
- **example_bad_flash.jpg**: Flash photography (avoid)
- **example_bad_shadow.jpg**: Strong shadows (avoid)
- **example_bad_angle.jpg**: Side profile (avoid)
- **example_bad_filter.jpg**: Beauty filter/AI smoothing (avoid)
- **example_bad_makeup.jpg**: Heavy makeup covering skin (avoid)
- **example_bad_lighting.jpg**: Colored lighting (avoid)

### Monk Scale Chart
- **monk_scale_chart.png**: Visual reference for 10 MST classes

## Replacing Placeholders

To replace with real photos:
1. Take or source appropriate photos
2. Resize to 800x600 pixels
3. Save as JPEG (quality 85%)
4. Replace placeholder files

## Sources for Real Photos

- **Stock Photos**: Unsplash, Pexels, Pixabay
- **Your Own**: Follow guidelines in data_preparation/README_DATA.md
- **AI Generated**: Use Stable Diffusion with appropriate prompts
""")
    
    print(f"\n📄 Created README: {readme_path}")
    
    print("\n" + "=" * 60)
    print("⚠️  PLACEHOLDER IMAGES CREATED")
    print("=" * 60)
    print("These are placeholder images with text labels.")
    print("For production, replace with real photos:")
    print()
    print("1. Take photos following the guidelines")
    print("2. Or download from stock photo sites:")
    print("   - Unsplash: https://unsplash.com/s/photos/portrait")
    print("   - Pexels: https://www.pexels.com/search/portrait/")
    print("   - Pixabay: https://pixabay.com/images/search/portrait/")
    print()
    print("3. Resize to 800x600 and save as JPEG")
    print("4. Replace files in frontend/assets/")
    print("=" * 60)


def create_monk_scale_chart():
    """Create a visual Monk Scale chart"""
    width = 1000
    height = 400
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # MST colors (approximate RGB)
    mst_colors = [
        (245, 228, 208),  # MST-01 Porcelain
        (237, 213, 181),  # MST-02 Fair
        (232, 201, 160),  # MST-03 Light
        (220, 186, 140),  # MST-04 Light-Medium
        (207, 171, 120),  # MST-05 Medium
        (194, 156, 100),  # MST-06 Medium-Dark
        (181, 141, 80),   # MST-07 Tan
        (168, 126, 60),   # MST-08 Brown
        (155, 111, 40),   # MST-09 Deep Brown
        (119, 84, 40),    # MST-10 Deep
    ]
    
    # Draw title
    cv2.putText(img, "Monk Skin Tone Scale", (300, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    
    # Draw color swatches
    swatch_width = 80
    swatch_height = 200
    start_x = 50
    start_y = 100
    
    for i, color in enumerate(mst_colors):
        x = start_x + i * (swatch_width + 10)
        
        # Draw swatch
        cv2.rectangle(img, (x, start_y), (x + swatch_width, start_y + swatch_height),
                     color, -1)
        cv2.rectangle(img, (x, start_y), (x + swatch_width, start_y + swatch_height),
                     (0, 0, 0), 2)
        
        # Draw label
        label = f"MST-{i+1:02d}"
        cv2.putText(img, label, (x + 10, start_y + swatch_height + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return img


if __name__ == "__main__":
    create_example_photos()
