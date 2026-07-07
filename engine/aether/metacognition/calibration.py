from typing import Dict, Any

class ConfidenceCalibrator:
    """
    Confidence calibration to reduce overconfidence and improve uncertainty estimates.
    Adjusts raw LLM confidence scores based on historical accuracy.
    """
    def __init__(self):
        self.calibration_factor = 1.0
        
    def calibrate(self, raw_confidence: float, historical_accuracy: float) -> float:
        """
        Adjust raw confidence based on how accurate the system actually is.
        """
        # If system is highly accurate, trust its confidence
        # If system is historically inaccurate, penalize high confidence
        
        error_margin = abs(raw_confidence - historical_accuracy)
        
        # Simple exponential penalty based on error margin
        penalty = error_margin * 0.5
        
        calibrated = raw_confidence - penalty
        return max(0.0, min(1.0, calibrated))
        
    def update_calibration(self, expected_confidence: float, actual_score: float):
        """Update internal calibration metrics over time"""
        error = actual_score - expected_confidence
        # Adjust internal factor slightly towards the error direction
        self.calibration_factor += (error * 0.1)
