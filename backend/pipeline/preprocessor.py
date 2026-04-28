"""
Module 1: Image Acquisition & Preprocessing
"""
import cv2
import numpy as np
from skimage import color as skcolor
from typing import Tuple, Dict


def gray_world_white_balance(img_rgb: np.ndarray) -> np.ndarray:
    """
    Apply Gray World white balance correction.
    Input:  img_rgb  — H×W×3 uint8 array in RGB
    Output: corrected H×W×3 uint8 array in RGB
    """
    img_float = img_rgb.astype(np.float32)
    mu_r = img_float[:, :, 0].mean()
    mu_g = img_float[:, :, 1].mean()
    mu_b = img_float[:, :, 2].mean()
    mu_gray = (mu_r + mu_g + mu_b) / 3.0

    img_float[:, :, 0] = np.clip(img_float[:, :, 0] * (mu_gray / (mu_r + 1e-6)), 0, 255)
    img_float[:, :, 1] = np.clip(img_float[:, :, 1] * (mu_gray / (mu_g + 1e-6)), 0, 255)
    img_float[:, :, 2] = np.clip(img_float[:, :, 2] * (mu_gray / (mu_b + 1e-6)), 0, 255)
    return img_float.astype(np.uint8)


def convert_color_spaces(img_rgb: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Convert RGB image to CIELAB, HSV, and YCbCr.
    Returns dict with keys: 'lab', 'hsv', 'ycbcr', 'rgb'
    """
    # CIELAB: scikit-image expects float [0,1] RGB
    img_float_01 = img_rgb.astype(np.float32) / 255.0
    lab = skcolor.rgb2lab(img_float_01)

    # HSV: OpenCV expects BGR uint8
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 0] /= 179.0
    hsv[:, :, 1] /= 255.0
    hsv[:, :, 2] /= 255.0

    # YCbCr
    ycbcr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    ycbcr /= 255.0

    return {'rgb': img_rgb, 'lab': lab, 'hsv': hsv, 'ycbcr': ycbcr}


def preprocess_image(
    image_bytes: bytes,
    target_size: Tuple[int, int] = (224, 224)
) -> Dict[str, np.ndarray]:
    """
    Full preprocessing pipeline.
    Input:  raw image bytes
    Output: dict containing all color space representations at target_size
    """
    # Decode bytes → numpy RGB
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError("Could not decode image. Ensure it is a valid JPEG/PNG/WEBP.")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 1. White balance correction
    img_wb = gray_world_white_balance(img_rgb)

    # 2. Resize to model input size
    img_resized = cv2.resize(img_wb, target_size, interpolation=cv2.INTER_LANCZOS4)

    # 3. Multi-space conversion
    spaces = convert_color_spaces(img_resized)

    # 4. Store original full-res for display
    spaces['original_rgb'] = img_rgb
    spaces['original_wb'] = img_wb

    return spaces
