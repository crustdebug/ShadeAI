"""
Module 4: Skin Tone Classification & Undertone Detection
"""
import numpy as np
from typing import Dict

MST_LABELS = {
    0: "MST-01 Porcelain", 1: "MST-02 Fair", 2: "MST-03 Light",
    3: "MST-04 Light-Medium", 4: "MST-05 Medium", 5: "MST-06 Medium-Dark",
    6: "MST-07 Tan", 7: "MST-08 Brown", 8: "MST-09 Deep Brown", 9: "MST-10 Deep"
}

MST_GROUP = {
    0: "Light", 1: "Light", 2: "Light",
    3: "Medium", 4: "Medium", 5: "Medium",
    6: "Dark", 7: "Dark", 8: "Dark", 9: "Dark"
}


def classify_tone_from_ita(ita_degrees: float) -> Dict:
    """
    ITA-based skin tone classification (no model required).
    """
    if ita_degrees > 55:
        idx = 0
    elif ita_degrees > 41:
        idx = 1
    elif ita_degrees > 28:
        idx = 2
    elif ita_degrees > 19:
        idx = 3
    elif ita_degrees > 10:
        idx = 4
    elif ita_degrees > 0:
        idx = 5
    elif ita_degrees > -10:
        idx = 6
    elif ita_degrees > -20:
        idx = 7
    elif ita_degrees > -30:
        idx = 8
    else:
        idx = 9

    return {
        'class_index': idx,
        'label': MST_LABELS[idx],
        'group': MST_GROUP[idx],
        'confidence': None,
        'probabilities': None,
        'method': 'ITA_based'
    }


def detect_undertone(ita_degrees: float, mean_lab: np.ndarray) -> Dict:
    """
    Detect undertone using ITA heuristic and LAB values.
    Returns: {'score': float, 'label': str, 'description': str}
    """
    # Use ITA and b* channel (yellow-blue axis)
    b_star = float(mean_lab[2])
    a_star = float(mean_lab[1])
    
    # Heuristic: b* > 15 tends warm (yellow), b* < 10 tends cool (blue)
    # a* > 12 tends warm (red), a* < 8 tends cool (pink)
    score = 0.0
    
    if b_star > 15:
        score += 0.4
    elif b_star < 10:
        score -= 0.4
    
    if a_star > 12:
        score += 0.3
    elif a_star < 8:
        score -= 0.3
    
    # ITA contribution
    if ita_degrees > 28:
        score += 0.2
    elif ita_degrees < 10:
        score -= 0.2
    
    score = float(np.clip(score, -1.0, 1.0))

    if score > 0.3:
        label, desc = "Warm", "Golden, peachy, or yellow undertones"
    elif score < -0.3:
        label, desc = "Cool", "Pink, red, or bluish undertones"
    else:
        label, desc = "Neutral", "Balanced mix of warm and cool undertones"

    return {'score': score, 'label': label, 'description': desc}
