"""
Color space conversion utilities
"""
import cv2
import numpy as np
from skimage import color as skcolor

def rgb_to_lab(rgb_array: np.ndarray) -> np.ndarray:
    """Convert RGB to CIELAB. Input: uint8 RGB, Output: float LAB"""
    rgb_float = rgb_array.astype(np.float32) / 255.0
    return skcolor.rgb2lab(rgb_float.reshape(-1, 1, 3)).reshape(-1, 3)

def rgb_to_hsv(rgb_array: np.ndarray) -> np.ndarray:
    """Convert RGB to HSV. Input: uint8 RGB, Output: normalized float HSV"""
    bgr = cv2.cvtColor(rgb_array.reshape(-1, 1, 3), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).reshape(-1, 3).astype(np.float32)
    hsv[:, 0] /= 179.0
    hsv[:, 1] /= 255.0
    hsv[:, 2] /= 255.0
    return hsv

def rgb_to_ycbcr(rgb_array: np.ndarray) -> np.ndarray:
    """Convert RGB to YCbCr. Input: uint8 RGB, Output: normalized float YCbCr"""
    bgr = cv2.cvtColor(rgb_array.reshape(-1, 1, 3), cv2.COLOR_RGB2BGR)
    ycbcr = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb).reshape(-1, 3).astype(np.float32)
    return ycbcr / 255.0
