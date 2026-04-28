"""
Module 2b: Skin Segmentation
"""
import numpy as np
import cv2
from typing import Optional


def segment_skin_rule_based(face_rgb: np.ndarray) -> np.ndarray:
    """
    Rule-based skin segmentation using HSV + YCbCr thresholds.
    Returns: mask H×W uint8 {0, 1}
    """
    face_bgr = cv2.cvtColor(face_rgb, cv2.COLOR_RGB2BGR)

    # HSV skin range
    hsv = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 15, 60], dtype=np.uint8)
    upper_hsv = np.array([25, 180, 255], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # YCbCr skin range
    ycbcr = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2YCrCb)
    lower_ycbcr = np.array([0, 133, 77], dtype=np.uint8)
    upper_ycbcr = np.array([255, 173, 127], dtype=np.uint8)
    mask_ycbcr = cv2.inRange(ycbcr, lower_ycbcr, upper_ycbcr)

    # Combine masks
    combined = cv2.bitwise_and(mask_hsv, mask_ycbcr)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel)
    combined = cv2.morphologyEx(combined, cv2.MORPH_DILATE, kernel)

    return (combined > 0).astype(np.uint8)


def get_skin_pixels(face_rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Extract skin-only pixels using segmentation mask.
    Returns: N×3 array of RGB skin pixels
    """
    face_resized = cv2.resize(face_rgb, (mask.shape[1], mask.shape[0]))
    skin_pixels = face_resized[mask == 1]
    return skin_pixels
