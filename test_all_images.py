#!/usr/bin/env python3
"""
Test ShadeAI on all test images and generate accuracy report
"""
import os
import sys
import cv2
import numpy as np
from pathlib import Path
from backend.pipeline.preprocessor import preprocess_image
from backend.pipeline.face_detector import detect_and_crop
from backend.pipeline.skin_segmentor import segment_skin_rule_based, get_skin_pixels
from backend.pipeline.feature_extractor import extract_all_features
from backend.pipeline.classifier import classify_tone_from_ita, detect_undertone
from backend.pipeline.shade_recommender import recommend_shades
from backend.utils.photo_quality import check_photo_quality
import time


def test_image(image_path):
    """Test a single image and return results"""
    print(f"\n{'='*80}")
    print(f"Testing: {image_path}")
    print('='*80)
    
    try:
        # Photo Quality Check
        quality_report = check_photo_quality(image_path)
        print(f"Quality Score: {quality_report['overall_score']}/100 ({quality_report['quality_level']})")
        
        if quality_report['issues']:
            print("Issues:", ', '.join(quality_report['issues']))
        
        start = time.time()
        
        # Read image
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Stage 1: Preprocess
        spaces = preprocess_image(image_bytes)
        
        # Stage 2: Face Detection
        face_crop, detection = detect_and_crop(spaces['rgb'])
        if face_crop is None:
            print("❌ No face detected")
            return None
        
        # Stage 3: Skin Segmentation
        mask = segment_skin_rule_based(face_crop)
        skin_pixels = get_skin_pixels(face_crop, mask)
        
        if len(skin_pixels) < 100:
            print("❌ Insufficient skin pixels")
            return None
        
        # Stage 4: Feature Extraction
        features = extract_all_features(face_crop, skin_pixels)
        
        # Stage 5: Classification
        tone = classify_tone_from_ita(features['ita_degrees'])
        undertone = detect_undertone(features['ita_degrees'], features['mean_lab'])
        
        # Stage 6: Shade Recommendation
        recommendations = recommend_shades(
            features['mean_lab'],
            undertone['label'],
            'backend/data/foundation_shades.json',
            top_k=5
        )
        
        inference_time = (time.time() - start) * 1000
        
        # Print results
        print(f"\n✅ Analysis Complete:")
        print(f"   Skin Tone: {tone['label']} ({tone['group']})")
        print(f"   Undertone: {undertone['label']}")
        print(f"   ITA°: {features['ita_degrees']:.2f}")
        print(f"   LAB: L*={features['mean_lab'][0]:.2f}, a*={features['mean_lab'][1]:.2f}, b*={features['mean_lab'][2]:.2f}")
        print(f"   Inference: {inference_time:.1f} ms")
        
        print(f"\n🏆 Top 5 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            status = "✅" if rec['delta_e'] < 3.0 else "⚠️"
            print(f"   {i}. {rec['brand']} {rec['shade_name']} - ΔE = {rec['delta_e']:.3f} {status}")
        
        return {
            'image': os.path.basename(image_path),
            'quality_score': quality_report['overall_score'],
            'quality_level': quality_report['quality_level'],
            'skin_tone': tone['label'],
            'undertone': undertone['label'],
            'ita': features['ita_degrees'],
            'lab': {'L': float(features['mean_lab'][0]), 'a': float(features['mean_lab'][1]), 'b': float(features['mean_lab'][2])},
            'top1_delta_e': recommendations[0]['delta_e'],
            'top5_avg_delta_e': np.mean([r['delta_e'] for r in recommendations]),
            'top1_brand': recommendations[0]['brand'],
            'top1_shade': recommendations[0]['shade_name'],
            'inference_ms': inference_time,
            'recommendations': recommendations
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    """Test all images in test_images folder"""
    test_dir = Path("test_images")
    
    if not test_dir.exists():
        print("❌ test_images folder not found")
        return
    
    # Get all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
        image_files.extend(test_dir.glob(ext))
    
    if not image_files:
        print("❌ No images found in test_images folder")
        return
    
    print(f"\n{'='*80}")
    print(f"ShadeAI - Comprehensive Accuracy Test")
    print(f"{'='*80}")
    print(f"Testing {len(image_files)} images...")
    
    results = []
    for image_path in sorted(image_files):
        result = test_image(str(image_path))
        if result:
            results.append(result)
    
    # Generate summary report
    print(f"\n\n{'='*80}")
    print(f"ACCURACY SUMMARY REPORT")
    print(f"{'='*80}")
    
    if not results:
        print("❌ No successful analyses")
        return
    
    print(f"\nTotal Images Tested: {len(image_files)}")
    print(f"Successful Analyses: {len(results)}")
    print(f"Success Rate: {len(results)/len(image_files)*100:.1f}%")
    
    # Quality statistics
    print(f"\n📊 Photo Quality Statistics:")
    quality_scores = [r['quality_score'] for r in results]
    print(f"   Average Quality Score: {np.mean(quality_scores):.1f}/100")
    print(f"   Min Quality Score: {np.min(quality_scores):.1f}/100")
    print(f"   Max Quality Score: {np.max(quality_scores):.1f}/100")
    
    excellent = sum(1 for r in results if r['quality_level'] == 'Excellent')
    good = sum(1 for r in results if r['quality_level'] == 'Good')
    acceptable = sum(1 for r in results if r['quality_level'] == 'Acceptable')
    print(f"   Excellent: {excellent}, Good: {good}, Acceptable: {acceptable}")
    
    # Accuracy statistics
    print(f"\n🎯 Accuracy Statistics:")
    top1_deltas = [r['top1_delta_e'] for r in results]
    top5_deltas = [r['top5_avg_delta_e'] for r in results]
    
    print(f"   Top-1 Average ΔE: {np.mean(top1_deltas):.3f}")
    print(f"   Top-1 Median ΔE: {np.median(top1_deltas):.3f}")
    print(f"   Top-1 Min ΔE: {np.min(top1_deltas):.3f}")
    print(f"   Top-1 Max ΔE: {np.max(top1_deltas):.3f}")
    print(f"   Top-1 Std Dev: {np.std(top1_deltas):.3f}")
    
    print(f"\n   Top-5 Average ΔE: {np.mean(top5_deltas):.3f}")
    print(f"   Top-5 Median ΔE: {np.median(top5_deltas):.3f}")
    
    # Match quality distribution
    print(f"\n📈 Match Quality Distribution:")
    perfect = sum(1 for d in top1_deltas if d < 1.0)
    outstanding = sum(1 for d in top1_deltas if 1.0 <= d < 2.0)
    excellent = sum(1 for d in top1_deltas if 2.0 <= d < 3.0)
    good = sum(1 for d in top1_deltas if 3.0 <= d < 5.0)
    acceptable = sum(1 for d in top1_deltas if d >= 5.0)
    
    print(f"   Perfect (ΔE < 1.0):      {perfect:2d} ({perfect/len(results)*100:5.1f}%)")
    print(f"   Outstanding (1.0-2.0):   {outstanding:2d} ({outstanding/len(results)*100:5.1f}%)")
    print(f"   Excellent (2.0-3.0):     {excellent:2d} ({excellent/len(results)*100:5.1f}%)")
    print(f"   Good (3.0-5.0):          {good:2d} ({good/len(results)*100:5.1f}%)")
    print(f"   Acceptable (≥5.0):       {acceptable:2d} ({acceptable/len(results)*100:5.1f}%)")
    
    # Performance statistics
    print(f"\n⚡ Performance Statistics:")
    inference_times = [r['inference_ms'] for r in results]
    print(f"   Average Inference Time: {np.mean(inference_times):.1f} ms")
    print(f"   Min Inference Time: {np.min(inference_times):.1f} ms")
    print(f"   Max Inference Time: {np.max(inference_times):.1f} ms")
    
    # Skin tone distribution
    print(f"\n🎨 Skin Tone Distribution:")
    tones = {}
    for r in results:
        tone = r['skin_tone']
        tones[tone] = tones.get(tone, 0) + 1
    for tone, count in sorted(tones.items()):
        print(f"   {tone}: {count}")
    
    # Detailed results table
    print(f"\n📋 Detailed Results:")
    print(f"{'Image':<40} {'Quality':<12} {'Skin Tone':<15} {'Top-1 ΔE':<10} {'Status'}")
    print('-' * 90)
    for r in results:
        status = "✅" if r['top1_delta_e'] < 3.0 else "⚠️"
        print(f"{r['image']:<40} {r['quality_level']:<12} {r['skin_tone']:<15} {r['top1_delta_e']:<10.3f} {status}")
    
    # Overall assessment
    print(f"\n{'='*80}")
    print(f"OVERALL ASSESSMENT")
    print(f"{'='*80}")
    
    avg_delta = np.mean(top1_deltas)
    excellent_rate = (perfect + outstanding + excellent) / len(results) * 100
    
    if avg_delta < 1.5:
        assessment = "OUTSTANDING"
        emoji = "🏆"
    elif avg_delta < 2.5:
        assessment = "EXCELLENT"
        emoji = "✅"
    elif avg_delta < 3.5:
        assessment = "GOOD"
        emoji = "👍"
    else:
        assessment = "ACCEPTABLE"
        emoji = "⚠️"
    
    print(f"\n{emoji} System Performance: {assessment}")
    print(f"   Average ΔE: {avg_delta:.3f}")
    print(f"   Excellent Match Rate: {excellent_rate:.1f}%")
    print(f"   Success Rate: {len(results)/len(image_files)*100:.1f}%")
    
    if avg_delta < 2.7:
        print(f"\n✅ System exceeds research target (ΔE < 2.7)")
        print(f"   Performance: {(2.7 - avg_delta) / 2.7 * 100:.1f}% better than target")
    
    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
