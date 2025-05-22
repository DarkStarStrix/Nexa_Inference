from unittest.mock import Mock

class MockBioEngine:
    def predict(self, data):
        sequence_length = len(data["sequence"]) if "sequence" in data else 100
        return {
            "secondary_structure": "H" * sequence_length,  # Mock helix prediction
            "confidence_scores": [0.95] * sequence_length,
            "processing_time": 0.5
        }

class MockMaterialEngine:
    def predict(self, data):
        return {
            "formation_energy": -5.43,
            "band_gap": 1.1,
            "elastic_constants": {
                "c11": 165.7,
                "c12": 63.9,
                "c44": 79.6
            },
            "magnetic_moment": 0.0,
            "processing_time": 0.3
        }

class MockEngine:
    def predict(self, data):
        if "geometry" in data:  # CFD request
            return {
                "velocity_field": [[0.1, 0.2, 0.3]],
                "pressure_field": [[100.0]],
                "convergence_status": "completed"
            }
        return {
            "prediction": "mock_prediction",
            "confidence": 0.95,
            "processing_time": 0.5
        }

def get_mock_engines():
    """Create mock engines for testing"""
    return {
        "cfd": MockEngine(),
        "bio": MockBioEngine(),
        "mat": MockMaterialEngine(),
        "qst": MockEngine(),
        "astro": MockEngine()
    }

def get_mock_rate_limiter():
    """Create a mock rate limiter for testing"""
    mock_limiter = Mock()
    mock_limiter.allow_request.return_value = True
    return mock_limiter
