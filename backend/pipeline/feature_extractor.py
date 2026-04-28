"""
Module 3: Color Feature Extraction
"""
import numpy as np
import cv2
from skimage import color as skcolor
from typing import Dict


def extract_handcrafted_features(skin_pixels_rgb: np.ndarray) -> np.ndarray:
    """
    Compute 18-dim handcrafted color feature vector from skin pixels.
    Input:  N×3 RGB uint8 skin pixel array
    Output: (18,) float32 feature vector
    """
    if len(skin_pixels_rgb) == 0:
        return np.zeros(18, dtype=np.float32)

    # CIELAB
    skin_float = skin_pixels_rgb.astype(np.float32) / 255.0
    skin_lab = skcolor.rgb2lab(skin_float.reshape(-1, 1, 3)).reshape(-1, 3)

    # HSV
    skin_bgr = cv2.cvtColor(
        skin_pixels_rgb.reshape(-1, 1, 3),
        cv2.COLOR_RGB2BGR
    )
    skin_hsv = cv2.cvtColor(skin_bgr, cv2.COLOR_BGR2HSV).reshape(-1, 3).astype(np.float32)
    skin_hsv[:, 0] /= 179.0
    skin_hsv[:, 1] /= 255.0
    skin_hsv[:, 2] /= 255.0

    # YCbCr
    skin_ycbcr = cv2.cvtColor(
        skin_pixels_rgb.reshape(-1, 1, 3),
        cv2.COLOR_RGB2YCrCb
    ).reshape(-1, 3).astype(np.float32) / 255.0

    features = []
    for channels in [skin_lab, skin_hsv, skin_ycbcr]:
        for c in range(3):
            features.append(channels[:, c].mean())
            features.append(channels[:, c].std())

    return np.array(features, dtype=np.float32)


def compute_ita(skin_pixels_rgb: np.ndarray) -> float:
    """
    Compute Individual Typology Angle from mean CIELAB values.
    ITA° = arctan((L* - 50) / b*) × (180/π)
    """
    if len(skin_pixels_rgb) == 0:
        return 0.0
    skin_float = skin_pixels_rgb.astype(np.float32) / 255.0
    skin_lab = skcolor.rgb2lab(skin_float.reshape(-1, 1, 3)).reshape(-1, 3)
    L_mean = skin_lab[:, 0].mean()
    b_mean = skin_lab[:, 2].mean()
    if abs(b_mean) < 1e-6:
        b_mean = 1e-6
    ita = np.degrees(np.arctan((L_mean - 50.0) / b_mean))
    return float(ita)


def extract_all_features(
    face_rgb: np.ndarray,
    skin_pixels_rgb: np.ndarray
) -> Dict:
    """
    Run full feature extraction.
    Returns dict with 'handcrafted' (18,), 'ita_degrees', 'mean_lab'
    """
    h_features = extract_handcrafted_features(skin_pixels_rgb)
    ita = compute_ita(skin_pixels_rgb)

    # Mean LAB for shade matching
    if len(skin_pixels_rgb) > 0:
        skin_float = skin_pixels_rgb.astype(np.float32) / 255.0
        lab = skcolor.rgb2lab(skin_float.reshape(-1, 1, 3)).reshape(-1, 3)
        mean_lab = lab.mean(axis=0)
    else:
        mean_lab = np.array([50.0, 0.0, 0.0])

    return {
        'handcrafted': h_features,
        'ita_degrees': ita,
        'mean_lab': mean_lab
    }
