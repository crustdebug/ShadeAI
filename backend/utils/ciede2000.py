"""
CIEDE2000 Color Difference Implementation
"""
import numpy as np

def ciede2000(lab1: np.ndarray, lab2: np.ndarray) -> float:
    """
    Compute CIEDE2000 color difference between two CIELAB colors.
    lab1, lab2: arrays of shape (3,) → [L*, a*, b*]
    Returns: ΔE*00 scalar
    """
    L1, a1, b1 = float(lab1[0]), float(lab1[1]), float(lab1[2])
    L2, a2, b2 = float(lab2[0]), float(lab2[1]), float(lab2[2])

    # Step 1: Compute C*ab
    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)
    C_avg = (C1 + C2) / 2.0
    C_avg7 = C_avg ** 7
    G = 0.5 * (1 - np.sqrt(C_avg7 / (C_avg7 + 25**7)))
    a1p = a1 * (1 + G)
    a2p = a2 * (1 + G)
    C1p = np.sqrt(a1p**2 + b1**2)
    C2p = np.sqrt(a2p**2 + b2**2)

    # Step 2: Compute h'
    def hprime(a, b):
        if a == 0 and b == 0:
            return 0.0
        angle = np.degrees(np.arctan2(b, a))
        return angle + 360 if angle < 0 else angle

    h1p = hprime(a1p, b1)
    h2p = hprime(a2p, b2)

    # Step 3: Compute ΔL', ΔC', ΔH'
    dLp = L2 - L1
    dCp = C2p - C1p

    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360

    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))

    # Step 4: CIEDE2000 weighting functions
    Lp_avg = (L1 + L2) / 2.0
    Cp_avg = (C1p + C2p) / 2.0

    if C1p * C2p == 0:
        Hp_avg = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        Hp_avg = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        Hp_avg = (h1p + h2p + 360) / 2
    else:
        Hp_avg = (h1p + h2p - 360) / 2

    T = (1
         - 0.17 * np.cos(np.radians(Hp_avg - 30))
         + 0.24 * np.cos(np.radians(2 * Hp_avg))
         + 0.32 * np.cos(np.radians(3 * Hp_avg + 6))
         - 0.20 * np.cos(np.radians(4 * Hp_avg - 63)))

    SL = 1 + 0.015 * (Lp_avg - 50)**2 / np.sqrt(20 + (Lp_avg - 50)**2)
    SC = 1 + 0.045 * Cp_avg
    SH = 1 + 0.015 * Cp_avg * T

    Cp_avg7 = Cp_avg ** 7
    RC = 2 * np.sqrt(Cp_avg7 / (Cp_avg7 + 25**7))
    d_theta = 30 * np.exp(-((Hp_avg - 275) / 25)**2)
    RT = -np.sin(np.radians(2 * d_theta)) * RC

    kL = kC = kH = 1.0
    dE = np.sqrt(
        (dLp / (kL * SL))**2 +
        (dCp / (kC * SC))**2 +
        (dHp / (kH * SH))**2 +
        RT * (dCp / (kC * SC)) * (dHp / (kH * SH))
    )
    return float(dE)
