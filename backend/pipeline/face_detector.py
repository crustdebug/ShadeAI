"""
Module 2a: Face Detection using MTCNN or Haar Cascade fallback
"""
import numpy as np
import cv2
from typing import Optional, Tuple, Dict

# Try to import MTCNN, fall back to Haar cascade if not available
try:
    from mtcnn import MTCNN
    _mtcnn_detector = None
    MTCNN_AVAILABLE = True
except ImportError:
    MTCNN_AVAILABLE = False
    _mtcnn_detector = None

_haar_cascade = None


def get_mtcnn():
    global _mtcnn_detector
    if _mtcnn_detector is None and MTCNN_AVAILABLE:
        _mtcnn_detector = MTCNN()
    return _mtcnn_detector


def get_haar_cascade():
    global _haar_cascade
    if _haar_cascade is None:
        _haar_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    return _haar_cascade


def detect_face_mtcnn(img_rgb: np.ndarray) -> Optional[Dict]:
    """
    Detect the largest face in img_rgb using MTCNN.
    Returns dict with 'box' [x, y, w, h], 'keypoints', 'confidence'
    or None if no face found.
    """
    if not MTCNN_AVAILABLE:
        return None
    
    detector = get_mtcnn()
    if detector is None:
        return None
    
    results = detector.detect_faces(img_rgb)
    if not results:
        return None
    # Pick face with highest confidence
    best = max(results, key=lambda r: r['confidence'])
    return best


def detect_face_haar(img_rgb: np.ndarray) -> Optional[Dict]:
    """
    Detect face using Haar cascade (fallback method).
    Returns dict with 'box' [x, y, w, h], 'confidence'
    """
    cascade = get_haar_cascade()
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None
    
    # Pick largest face
    largest = max(faces, key=lambda f: f[2] * f[3])
    x, y, w, h = largest
    return {
        'box': [int(x), int(y), int(w), int(h)],
        'confidence': 0.9,  # Haar doesn't provide confidence
        'keypoints': None
    }


def crop_face(img_rgb: np.ndarray, box: list, padding: float = 0.15) -> np.ndarray:
    """
    Crop face region from image with optional padding.
    box = [x, y, w, h]
    """
    x, y, w, h = box
    H, W = img_rgb.shape[:2]

    pad_x = int(w * padding)
    pad_y = int(h * padding)

    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)
    x2 = min(W, x + w + pad_x)
    y2 = min(H, y + h + pad_y)

    return img_rgb[y1:y2, x1:x2]


def detect_and_crop(img_rgb: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[Dict]]:
    """
    Full detection + crop pipeline.
    Returns (cropped_face_rgb, detection_result) or (None, None).
    """
    # Try MTCNN first
    detection = detect_face_mtcnn(img_rgb)
    
    # Fall back to Haar cascade
    if detection is None:
        detection = detect_face_haar(img_rgb)
    
    if detection is None:
        return None, None
    
    face_crop = crop_face(img_rgb, detection['box'])
    return face_crop, detection
