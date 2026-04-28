"""
Module 5: Cosmetic Shade Recommendation using CIEDE2000
"""
import json
import os
import numpy as np
from typing import List, Dict
from backend.utils.ciede2000 import ciede2000


def load_shade_database(db_path: str) -> List[Dict]:
    """Load foundation shade database from JSON"""
    with open(db_path, 'r') as f:
        return json.load(f)


def undertone_compatible(shade_undertone: str, detected_undertone: str) -> bool:
    """
    Check undertone compatibility between shade and detected undertone.
    Neutral is compatible with everything.
    """
    if detected_undertone == "Neutral":
        return True
    return shade_undertone == detected_undertone


def recommend_shades(
    mean_lab: np.ndarray,
    undertone_label: str,
    db_path: str,
    top_k: int = 5,
    delta_e_threshold: float = 8.0
) -> List[Dict]:
    """
    Match skin tone LAB to foundation shade database using CIEDE2000.
    Returns top_k shades sorted by ΔE, filtered by undertone compatibility.
    """
    shades = load_shade_database(db_path)
    results = []

    for shade in shades:
        shade_lab = np.array([shade['L'], shade['a'], shade['b']], dtype=np.float32)
        delta_e = ciede2000(mean_lab, shade_lab)
        compatible = undertone_compatible(shade.get('undertone', 'Neutral'), undertone_label)
        results.append({
            **shade,
            'delta_e': round(delta_e, 3),
            'undertone_match': compatible,
            'within_threshold': delta_e < 3.0
        })

    # Sort: undertone-compatible first, then by ΔE
    compatible_results = sorted(
        [r for r in results if r['undertone_match']],
        key=lambda x: x['delta_e']
    )
    incompatible_results = sorted(
        [r for r in results if not r['undertone_match']],
        key=lambda x: x['delta_e']
    )

    # Return top_k from compatible, fill remainder from incompatible if needed
    final = compatible_results[:top_k]
    if len(final) < top_k:
        final += incompatible_results[:top_k - len(final)]

    return final[:top_k]
