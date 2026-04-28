#!/usr/bin/env python3
"""
Evaluate ShadeAI Recommendation Accuracy

This script helps you evaluate the accuracy of shade recommendations by:
1. Testing against ground truth data (if you have actual shade matches)
2. Analyzing CIEDE2000 ΔE statistics
3. Checking undertone matching accuracy
4. Generating accuracy reports
"""
import sys
import csv
import json
import numpy as np
from pathlib import Path
from backend.pipeline.preprocessor import preprocess_image
from backend.pipeline.face_detector import detect_and_crop
from backend.pipeline.skin_segmentor import segment_skin_rule_based, get_skin_pixels
from backend.pipeline.feature_extractor import extract_all_features
from backend.pipeline.classifier import classify_tone_from_ita, detect_undertone
from backend.pipeline.shade_recommender import recommend_shades
from backend.utils.ciede2000 import ciede2000


def evaluate_single_image(image_path: str, ground_truth_shade_id: str = None):
    """
    Evaluate a single image and compare with ground truth if provided.
    
    Args:
        image_path: Path to test image
        ground_truth_shade_id: Known correct shade ID (optional)
    
    Returns:
        dict with evaluation metrics
    """
    print(f"\n{'='*60}")
    print(f"Evaluating: {image_path}")
    print('='*60)
    
    # Read image
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Run pipeline
    spaces = preprocess_image(image_bytes)
    face_crop, detection = detect_and_crop(spaces['rgb'])
    
    if face_crop is None:
        return {"error": "No face detected"}
    
    mask = segment_skin_rule_based(face_crop)
    skin_pixels = get_skin_pixels(face_crop, mask)
    
    if len(skin_pixels) < 100:
        return {"error": "Insufficient skin pixels"}
    
    features = extract_all_features(face_crop, skin_pixels)
    tone_result = classify_tone_from_ita(features['ita_degrees'])
    undertone_result = detect_undertone(features['ita_degrees'], features['mean_lab'])
    
    recommendations = recommend_shades(
        mean_lab=features['mean_lab'],
        undertone_label=undertone_result['label'],
        db_path="backend/data/foundation_shades.json",
        top_k=5
    )
    
    result = {
        "image_path": image_path,
        "skin_tone": tone_result['label'],
        "undertone": undertone_result['label'],
        "ita_degrees": features['ita_degrees'],
        "mean_lab": features['mean_lab'],
        "top_5_recommendations": recommendations,
        "top_1_delta_e": recommendations[0]['delta_e'] if recommendations else None,
        "top_5_avg_delta_e": np.mean([r['delta_e'] for r in recommendations]) if recommendations else None
    }
    
    # If ground truth provided, calculate accuracy metrics
    if ground_truth_shade_id:
        # Find ground truth shade in recommendations
        ground_truth_rank = None
        ground_truth_delta_e = None
        
        for i, rec in enumerate(recommendations):
            if rec['id'] == ground_truth_shade_id:
                ground_truth_rank = i + 1
                ground_truth_delta_e = rec['delta_e']
                break
        
        # If not in top 5, calculate ΔE to ground truth
        if ground_truth_rank is None:
            with open("backend/data/foundation_shades.json", 'r') as f:
                all_shades = json.load(f)
            
            for shade in all_shades:
                if shade['id'] == ground_truth_shade_id:
                    shade_lab = np.array([shade['L'], shade['a'], shade['b']])
                    ground_truth_delta_e = ciede2000(features['mean_lab'], shade_lab)
                    break
        
        result['ground_truth'] = {
            "shade_id": ground_truth_shade_id,
            "rank": ground_truth_rank,
            "delta_e": ground_truth_delta_e,
            "in_top_5": ground_truth_rank is not None,
            "in_top_3": ground_truth_rank is not None and ground_truth_rank <= 3,
            "in_top_1": ground_truth_rank == 1
        }
    
    # Print results
    print(f"\n📊 Analysis Results:")
    print(f"   Skin Tone: {result['skin_tone']}")
    print(f"   Undertone: {result['undertone']}")
    print(f"   ITA°: {result['ita_degrees']:.2f}")
    print(f"   Mean LAB: L*={result['mean_lab'][0]:.2f}, a*={result['mean_lab'][1]:.2f}, b*={result['mean_lab'][2]:.2f}")
    
    print(f"\n🏆 Top 5 Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        match_icon = "✅" if rec['delta_e'] < 3.0 else "⚠️"
        print(f"   {i}. {rec['brand']} {rec['shade_name']} - ΔE = {rec['delta_e']:.3f} {match_icon}")
    
    print(f"\n📈 Accuracy Metrics:")
    print(f"   Top-1 ΔE: {result['top_1_delta_e']:.3f}")
    print(f"   Top-5 Avg ΔE: {result['top_5_avg_delta_e']:.3f}")
    print(f"   Top-1 Excellent Match (ΔE<3): {'Yes ✅' if result['top_1_delta_e'] < 3.0 else 'No ⚠️'}")
    
    if ground_truth_shade_id and 'ground_truth' in result:
        gt = result['ground_truth']
        print(f"\n🎯 Ground Truth Comparison:")
        print(f"   Expected Shade: {gt['shade_id']}")
        print(f"   Rank in Results: {gt['rank'] if gt['rank'] else 'Not in top 5'}")
        print(f"   ΔE to Ground Truth: {gt['delta_e']:.3f}")
        print(f"   Top-1 Accuracy: {'✅ Correct' if gt['in_top_1'] else '❌ Incorrect'}")
        print(f"   Top-3 Accuracy: {'✅ Correct' if gt['in_top_3'] else '❌ Incorrect'}")
        print(f"   Top-5 Accuracy: {'✅ Correct' if gt['in_top_5'] else '❌ Incorrect'}")
    
    return result


def evaluate_batch(test_csv: str):
    """
    Evaluate multiple images from a CSV file.
    
    CSV format:
    image_path,ground_truth_shade_id,notes
    test1.jpg,MAC-NC45,User's actual foundation
    test2.jpg,FENTY-385N,Professional match
    """
    print("="*60)
    print("Batch Evaluation")
    print("="*60)
    
    results = []
    
    with open(test_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = evaluate_single_image(
                row['image_path'],
                row.get('ground_truth_shade_id')
            )
            results.append(result)
    
    # Calculate aggregate statistics
    print("\n" + "="*60)
    print("AGGREGATE STATISTICS")
    print("="*60)
    
    valid_results = [r for r in results if 'error' not in r]
    
    if not valid_results:
        print("No valid results to analyze")
        return
    
    # ΔE statistics
    top1_delta_es = [r['top_1_delta_e'] for r in valid_results]
    top5_delta_es = [r['top_5_avg_delta_e'] for r in valid_results]
    
    print(f"\n📊 ΔE Statistics:")
    print(f"   Top-1 Mean ΔE: {np.mean(top1_delta_es):.3f}")
    print(f"   Top-1 Median ΔE: {np.median(top1_delta_es):.3f}")
    print(f"   Top-1 Std ΔE: {np.std(top1_delta_es):.3f}")
    print(f"   Top-5 Mean ΔE: {np.mean(top5_delta_es):.3f}")
    
    excellent_matches = sum(1 for de in top1_delta_es if de < 3.0)
    print(f"\n   Excellent Matches (ΔE<3): {excellent_matches}/{len(top1_delta_es)} ({excellent_matches/len(top1_delta_es)*100:.1f}%)")
    
    # Ground truth accuracy (if available)
    gt_results = [r for r in valid_results if 'ground_truth' in r]
    
    if gt_results:
        top1_correct = sum(1 for r in gt_results if r['ground_truth']['in_top_1'])
        top3_correct = sum(1 for r in gt_results if r['ground_truth']['in_top_3'])
        top5_correct = sum(1 for r in gt_results if r['ground_truth']['in_top_5'])
        
        print(f"\n🎯 Ground Truth Accuracy:")
        print(f"   Top-1 Accuracy: {top1_correct}/{len(gt_results)} ({top1_correct/len(gt_results)*100:.1f}%)")
        print(f"   Top-3 Accuracy: {top3_correct}/{len(gt_results)} ({top3_correct/len(gt_results)*100:.1f}%)")
        print(f"   Top-5 Accuracy: {top5_correct}/{len(gt_results)} ({top5_correct/len(gt_results)*100:.1f}%)")
        
        gt_delta_es = [r['ground_truth']['delta_e'] for r in gt_results]
        print(f"\n   Mean ΔE to Ground Truth: {np.mean(gt_delta_es):.3f}")
    
    # MST distribution
    mst_counts = {}
    for r in valid_results:
        mst = r['skin_tone']
        mst_counts[mst] = mst_counts.get(mst, 0) + 1
    
    print(f"\n📊 MST Distribution:")
    for mst, count in sorted(mst_counts.items()):
        print(f"   {mst}: {count} images")
    
    # Save detailed results
    output_file = "evaluation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {output_file}")


def create_test_csv_template():
    """Create a template CSV for batch evaluation"""
    template = """image_path,ground_truth_shade_id,notes
test1.jpg,MAC-NC45,User's actual foundation shade
test2.jpg,FENTY-385N,Professional color match
test3.jpg,NARS-STROMBOLI,Self-reported match
"""
    
    with open("test_images_template.csv", 'w') as f:
        f.write(template)
    
    print("✅ Created test_images_template.csv")
    print("\nEdit this file with your test images and ground truth shades, then run:")
    print("  python evaluate_accuracy.py --batch test_images_template.csv")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate ShadeAI recommendation accuracy")
    parser.add_argument("--image", help="Single image to evaluate")
    parser.add_argument("--ground-truth", help="Ground truth shade ID for single image")
    parser.add_argument("--batch", help="CSV file with multiple test images")
    parser.add_argument("--create-template", action="store_true", help="Create test CSV template")
    
    args = parser.parse_args()
    
    if args.create_template:
        create_test_csv_template()
    elif args.batch:
        evaluate_batch(args.batch)
    elif args.image:
        evaluate_single_image(args.image, args.ground_truth)
    else:
        print("ShadeAI Accuracy Evaluation Tool")
        print("="*60)
        print("\nUsage:")
        print("  # Evaluate single image")
        print("  python evaluate_accuracy.py --image test1.jpg")
        print()
        print("  # Evaluate with ground truth")
        print("  python evaluate_accuracy.py --image test1.jpg --ground-truth MAC-NC45")
        print()
        print("  # Batch evaluation")
        print("  python evaluate_accuracy.py --batch test_images.csv")
        print()
        print("  # Create template CSV")
        print("  python evaluate_accuracy.py --create-template")
        print()
        print("Accuracy Metrics:")
        print("  • ΔE < 1.0: Not perceptible (perfect match)")
        print("  • ΔE < 3.0: Barely perceptible (excellent match) ✅")
        print("  • ΔE < 6.0: Noticeable (acceptable match) ⚠️")
        print("  • ΔE > 6.0: Obvious difference (poor match) ❌")


if __name__ == "__main__":
    main()
