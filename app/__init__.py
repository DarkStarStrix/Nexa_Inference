# app/__init__.py
from app.core import ProteinPredictor
from app.config import MODEL_CONFIG, TIER_LIMITS

__version__ = "1.0.0"
__all__ = ["ProteinPredictor", "MODEL_CONFIG", "TIER_LIMITS"]


def monitoring():
    return "OK"
