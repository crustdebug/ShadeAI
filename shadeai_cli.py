#!/usr/bin/env python3
"""
ShadeAI Command Line Interface
Analyze skin tone from an image file
"""
import sys
import cv2
import numpy as np
from backend.pipeline.preprocessor import preprocess_image
from backend.pipeline.face_detector import detect_and_crop
from backend.pipeline.skin_segmentor import segment_skin_rule_based, get_skin_pixels
from backend.pipeline.feature_extractor import extract_all_features
from backend.pipeline.classifier import classify_tone_from_ita, detect_undertone
from backend.pipeline.shade_recommender import recommend_shades
from backend.utils.photo_quality import check_photo_quality
import time


def analyze_image_file(image_path: str):
    """Analyze skin tone from image file"""
    print(f"🔍 Analyzing: {image_path}")
    print("=" * 60)
    
    # Photo Quality Check
    print("\n📊 Photo Quality Check...")
    quality_report = check_photo_quality(image_path)
    print(f"   Quality Score: {quality_report['overall_score']}/100 ({quality_report['quality_level']})")
    
    if quality_report['issues']:
        print("\n   ⚠️ Issues Found:")
        for issue in quality_report['issues']:
            print(f"      - {issue}")
    
    if quality_report['warnings']:
        print("\n   ⚠️ Warnings:")
        for warning in quality_report['warnings']:
            print(f"      - {warning}")
    
    if quality_report['suggestions']:
        print("\n   💡 Suggestions:")
        for suggestion in quality_report['suggestions']:
            print(f"      - {suggestion}")
    
    if not quality_report['is_acceptable']:
        print("\n⚠️ Photo quality is low. Results may be less accurate.")
        print("   Continuing with analysis...")
    
    print("\n" + "=" * 60)
    
    start = time.time()
    
    # Read image
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Stage 1: Preprocess
    print("Stage 1: Preprocessing...")
    spaces = preprocess_image(image_bytes)
    
    # Stage 2: Face Detection
    print("Stage 2: Face Detection...")
    face_crop, detection = detect_and_crop(spaces['rgb'])
    if face_crop is None:
        print("❌ No face detected. Please use a clear, front-facing photo.")
        return
    
    print(f"   ✓ Face detected (confidence: {detection['confidence']:.3f})")
    
    # Stage 3: Skin Segmentation
    print("Stage 3: Skin Segmentation...")
    mask = segment_skin_rule_based(face_crop)
    skin_pixels = get_skin_pixels(face_crop, mask)
    
    if len(skin_pixels) < 100:
        print("❌ Could not extract sufficient skin pixels. Try better lighting.")
        return
    
    print(f"   ✓ Extracted {len(skin_pixels):,} skin pixels")
    
    # Stage 4: Feature Extraction
    print("Stage 4: Feature Extraction...")
    features = extract_all_features(face_crop, skin_pixels)
    print(f"   ✓ ITA°: {features['ita_degrees']:.2f}")
    print(f"   ✓ Mean LAB: L*={features['mean_lab'][0]:.2f}, "
          f"a*={features['mean_lab'][1]:.2f}, b*={features['mean_lab'][2]:.2f}")
    
    # Stage 5: Classification
    print("Stage 5: Classification...")
    tone_result = classify_tone_from_ita(features['ita_degrees'])
    undertone_result = detect_undertone(features['ita_degrees'], features['mean_lab'])
    
    print(f"   ✓ Skin Tone: {tone_result['label']} ({tone_result['group']})")
    print(f"   ✓ Undertone: {undertone_result['label']} — {undertone_result['description']}")
    
    # Stage 6: Shade Recommendation
    print("Stage 6: Shade Recommendation...")
    recommendations = recommend_shades(
        mean_lab=features['mean_lab'],
        undertone_label=undertone_result['label'],
        db_path="backend/data/foundation_shades.json",
        top_k=5
    )
    
    inference_ms = (time.time() - start) * 1000
    
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print(f"Skin Tone:  {tone_result['label']}")
    print(f"Group:      {tone_result['group']}")
    print(f"Undertone:  {undertone_result['label']}")
    print(f"ITA°:       {features['ita_degrees']:.2f}")
    print(f"Inference:  {inference_ms:.1f} ms")
    
    print("\n🏆 TOP 5 FOUNDATION SHADE RECOMMENDATIONS")
    print("=" * 60)
    for i, shade in enumerate(recommendations, 1):
        match_icon = "✅" if shade['delta_e'] < 3.0 else "⚠️"
        print(f"\n{i}. {shade['brand']} — {shade['shade_name']}")
        print(f"   Product:   {shade['product']}")
        print(f"   Undertone: {shade.get('undertone', 'N/A')}")
        print(f"   Match:     {match_icon} ΔE = {shade['delta_e']:.3f}")
        print(f"   Buy:       {shade.get('buy_url', 'N/A')}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python shadeai_cli.py <image_path>")
        print("Example: python shadeai_cli.py my_photo.jpg")
        return
    
    image_path = sys.argv[1]
    
    try:
        analyze_image_file(image_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
