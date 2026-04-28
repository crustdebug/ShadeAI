"""
FastAPI Routes for ShadeAI
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.pipeline.preprocessor import preprocess_image
from backend.pipeline.face_detector import detect_and_crop
from backend.pipeline.skin_segmentor import segment_skin_rule_based, get_skin_pixels
from backend.pipeline.feature_extractor import extract_all_features
from backend.pipeline.classifier import classify_tone_from_ita, detect_undertone
from backend.pipeline.shade_recommender import recommend_shades
import os
import time

router = APIRouter()

MODEL_DIR = os.getenv("MODEL_DIR", "backend/models")
DATA_DIR = os.getenv("DATA_DIR", "backend/data")


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded image and return skin tone + shade recommendations"""
    start = time.time()
    image_bytes = await file.read()

    # Stage 1: Preprocess
    spaces = preprocess_image(image_bytes)

    # Stage 2: Face Detection
    face_crop, detection = detect_and_crop(spaces['rgb'])
    if face_crop is None:
        raise HTTPException(
            status_code=422,
            detail="No face detected. Please upload a clear, front-facing photo."
        )

    # Stage 3: Skin Segmentation
    mask = segment_skin_rule_based(face_crop)
    skin_pixels = get_skin_pixels(face_crop, mask)
    
    if len(skin_pixels) < 100:
        raise HTTPException(
            status_code=422,
            detail="Could not extract sufficient skin pixels. Try better lighting."
        )

    # Stage 4: Feature Extraction
    features = extract_all_features(face_crop, skin_pixels)

    # Stage 5: Classification
    tone_result = classify_tone_from_ita(features['ita_degrees'])
    undertone_result = detect_undertone(features['ita_degrees'], features['mean_lab'])

    # Stage 6: Shade Recommendation
    db_path = os.path.join(DATA_DIR, "foundation_shades.json")
    recommendations = recommend_shades(
        mean_lab=features['mean_lab'],
        undertone_label=undertone_result['label'],
        db_path=db_path,
        top_k=5
    )

    inference_ms = round((time.time() - start) * 1000, 1)

    return {
        "skin_tone": tone_result,
        "undertone": undertone_result,
        "ita_degrees": round(features['ita_degrees'], 2),
        "mean_lab": {
            "L": round(float(features['mean_lab'][0]), 2),
            "a": round(float(features['mean_lab'][1]), 2),
            "b": round(float(features['mean_lab'][2]), 2)
        },
        "recommendations": recommendations,
        "inference_ms": inference_ms,
        "face_detected": True,
        "face_confidence": round(detection['confidence'], 3)
    }


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "ShadeAI"}
