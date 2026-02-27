class AnswerCalibrator:
    """Simple confidence-based calibrator."""

    def __init__(self, threshold=2.0):
        self.threshold = threshold

    def is_valid(self, score):
        # Currently uses a simple threshold; can replace with ML-based calibration later
        return score > self.threshold