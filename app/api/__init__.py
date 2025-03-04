# app/api/__init__.py
from app.api.routes.predictions import router as predictions_router
from app.api.schemas import ProteinRequest, PredictionResponse

__all__ = ["predictions_router", "ProteinRequest", "PredictionResponse"]