"""
Photo Quality Checker
Analyzes uploaded photos and provides real-time feedback on quality
"""
import cv2
import numpy as np
from typing import Dict, List, Tuple


class PhotoQualityChecker:
    """Checks photo quality for skin tone analysis"""
    
    def __init__(self):
        # Relaxed thresholds for better real-world performance
        self.min_brightness = 60  # Was 80 - now more lenient
        self.max_brightness = 235  # Was 220 - now more lenient
        self.min_face_size = 80  # Was 100 - now more lenient
        self.max_blur_threshold = 50  # Was 100 - now more strict on actual blur
        
    def check_quality(self, image: np.ndarray) -> Dict:
        """
        Comprehensive photo quality check
        
        Returns:
            dict with:
                - overall_score: 0-100
                - is_acceptable: bool
                - issues: list of problems
                - warnings: list of warnings
                - suggestions: list of improvements
        """
        issues = []
        warnings = []
        suggestions = []
        scores = []
        
        # 1. Check brightness
        brightness_score, brightness_issues = self._check_brightness(image)
        scores.append(brightness_score)
        issues.extend(brightness_issues)
        
        # 2. Check blur
        blur_score, blur_issues = self._check_blur(image)
        scores.append(blur_score)
        issues.extend(blur_issues)
        
        # 3. Check color cast
        cast_score, cast_issues = self._check_color_cast(image)
        scores.append(cast_score)
        warnings.extend(cast_issues)
        
        # 4. Check face detection
        face_score, face_issues = self._check_face(image)
        scores.append(face_score)
        issues.extend(face_issues)
        
        # 5. Check resolution
        res_score, res_issues = self._check_resolution(image)
        scores.append(res_score)
        warnings.extend(res_issues)
        
        # 6. Check overexposure/underexposure
        exposure_score, exposure_issues = self._check_exposure(image)
        scores.append(exposure_score)
        issues.extend(exposure_issues)
        
        # Calculate overall score
        overall_score = int(np.mean(scores))
        
        # ALWAYS accept - never block analysis, only warn
        is_acceptable = True  # Always allow analysis
        
        # Generate suggestions
        if overall_score < 50:
            suggestions.append("Consider retaking the photo with better conditions")
        if brightness_score < 60:
            suggestions.append("Use natural window light or soft indoor lighting")
        if blur_score < 60:
            suggestions.append("Hold camera steady or use a tripod")
        if face_score < 60:
            suggestions.append("Face camera directly, ensure face is clearly visible")
        if cast_score < 60:
            suggestions.append("Avoid colored lighting or strong filters")
        
        return {
            "overall_score": overall_score,
            "is_acceptable": is_acceptable,
            "quality_level": self._get_quality_level(overall_score),
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions,
            "detailed_scores": {
                "brightness": brightness_score,
                "sharpness": blur_score,
                "color_accuracy": cast_score,
                "face_detection": face_score,
                "resolution": res_score,
                "exposure": exposure_score
            }
        }
    
    def _check_brightness(self, image: np.ndarray) -> Tuple[int, List[str]]:
        """Check if image brightness is acceptable"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        
        issues = []
        # More lenient brightness check
        if mean_brightness < self.min_brightness:
            issues.append("Image is too dark - increase lighting")
            score = int((mean_brightness / self.min_brightness) * 100)
        elif mean_brightness > self.max_brightness:
            issues.append("Image is too bright - reduce lighting or move away from direct light")
            score = int((255 - mean_brightness) / (255 - self.max_brightness) * 100)
        else:
            # Optimal range - give high score even if not perfect
            score = 100
        
        # Don't penalize slightly dim/bright photos
        if score > 50:
            issues = []  # Clear issues if score is acceptable
        
        return max(0, min(100, score)), issues
    
    def _check_blur(self, image: np.ndarray) -> Tuple[int, List[str]]:
        """Check image sharpness using Laplacian variance"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        warnings = []  # Changed from issues to warnings
        # More lenient blur threshold
        if laplacian_var < self.max_blur_threshold:
            warnings.append("Image is blurry - hold camera steady")
            score = int((laplacian_var / self.max_blur_threshold) * 100)
        else:
            score = 100
        
        # Only flag as blocking issue if VERY blurry (score < 30)
        issues = []
        if score < 30:
            issues = warnings
            warnings = []
        
        return max(0, min(100, score)), issues
    
    def _check_color_cast(self, image: np.ndarray) -> Tuple[int, List[str]]:
        """Check for strong color casts (warm/cool lighting)"""
        mean_color = np.mean(image, axis=(0, 1))
        b, g, r = mean_color
        
        issues = []
        score = 100
        
        # More lenient color cast detection - only flag extreme cases
        # Check for strong blue cast (cool lighting)
        if b > r + 30 and b > g + 30:
            issues.append("Strong blue/cool color cast detected - use warmer lighting")
            score = 60
        
        # Check for strong red/yellow cast (warm lighting)
        elif r > b + 40 or (r > b + 25 and g > b + 25):
            issues.append("Strong warm/yellow color cast detected - use neutral lighting")
            score = 60
        
        # Check for green cast
        elif g > r + 30 and g > b + 30:
            issues.append("Green color cast detected - avoid fluorescent lighting")
            score = 50
        
        return score, issues
    
    def _check_face(self, image: np.ndarray) -> Tuple[int, List[str]]:
        """Check if face is detected and properly sized"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        issues = []
        if len(faces) == 0:
            issues.append("No face detected - ensure face is clearly visible and facing camera")
            return 0, issues
        
        warnings = []  # Changed from issues
        if len(faces) > 1:
            # Multiple faces is a warning, not a blocker
            warnings.append("Multiple faces detected - ensure only one person in frame")
            # Don't add to issues, just return lower score
            return 70, []  # No blocking issues
        
        # Check face size - more lenient
        x, y, w, h = faces[0]
        face_area = w * h
        image_area = image.shape[0] * image.shape[1]
        face_ratio = face_area / image_area
        
        if face_ratio < 0.03:  # Was 0.05, now more lenient
            warnings.append("Face is too small - move closer to camera")
            return 50, []  # Warning only, not blocking
        elif face_ratio > 0.8:  # Was 0.7, now more lenient
            warnings.append("Face is too close - move back from camera")
            return 75, []  # Warning only, not blocking
        
        return 100, issues
    
    def _check_resolution(self, image: np.ndarray) -> Tuple[int, List[str]]:
        """Check image resolution"""
        height, width = image.shape[:2]
        
        issues = []
        # More lenient resolution check
        if width < 300 or height < 300:
            issues.append("Image resolution is too low - use higher quality camera")
            score = 30
        elif width < 400 or height < 400:
            issues.append("Image resolution is low - consider using higher quality")
            score = 60  # Was 40, now more lenient
        elif width < 640 or height < 480:
            # Don't flag as issue, just lower score slightly
            score = 85  # Was 70
        else:
            score = 100
        
        return score, issues
    
    def _check_exposure(self, image: np.ndarray) -> Tuple[int, List[str]]:
        """Check for overexposure or underexposure"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Check histogram
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        # Overexposure: too many pixels near 255
        overexposed_pixels = np.sum(hist[245:])  # Was 240, now more lenient
        total_pixels = gray.shape[0] * gray.shape[1]
        overexposure_ratio = overexposed_pixels / total_pixels
        
        # Underexposure: too many pixels near 0
        underexposed_pixels = np.sum(hist[:10])  # Was :15, now more lenient
        underexposure_ratio = underexposed_pixels / total_pixels
        
        issues = []
        score = 100
        
        # More lenient thresholds
        if overexposure_ratio > 0.15:  # Was 0.1
            issues.append("Image is overexposed - reduce lighting or use diffused light")
            score = 60
        elif underexposure_ratio > 0.15:  # Was 0.1
            issues.append("Image is underexposed - increase lighting")
            score = 60
        
        return score, issues
    
    def _get_quality_level(self, score: int) -> str:
        """Convert score to quality level"""
        if score >= 85:  # Was 90
            return "Excellent"
        elif score >= 70:  # Was 75
            return "Good"
        elif score >= 50:  # Was 60
            return "Acceptable"
        elif score >= 35:  # Was 40
            return "Poor"
        else:
            return "Unacceptable"
    
    def get_quality_badge(self, score: int) -> str:
        """Get emoji badge for quality level"""
        if score >= 85:  # Was 90
            return "✅ Excellent"
        elif score >= 70:  # Was 75
            return "👍 Good"
        elif score >= 50:  # Was 60
            return "⚠️ Acceptable"
        elif score >= 35:  # Was 40
            return "❌ Poor"
        else:
            return "🚫 Unacceptable"


def check_photo_quality(image_path: str) -> Dict:
    """
    Convenience function to check photo quality from file path
    
    Args:
        image_path: Path to image file
        
    Returns:
        Quality report dictionary
    """
    image = cv2.imread(image_path)
    if image is None:
        return {
            "overall_score": 0,
            "is_acceptable": False,
            "quality_level": "Unacceptable",
            "issues": ["Could not read image file"],
            "warnings": [],
            "suggestions": ["Ensure image file is valid and not corrupted"]
        }
    
    checker = PhotoQualityChecker()
    return checker.check_quality(image)
