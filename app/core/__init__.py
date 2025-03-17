# app/__init__.py
from app.api.routes.predictions import ModelPredictor
from app.api.routes import router
from app.api.schemas.schemas import (
    ProteinRequest,
    PredictionResponse,
    AstroInput,
    MaterialInput,
    PredictionOutput
)
from app.monitoring import track_latency, LATENCY
from app.services.auth import verify_api_key

__all__ = [
    "ModelPredictor",
    "router",
    "ProteinRequest",
    "PredictionResponse",
    "AstroInput",
    "MaterialInput",
    "PredictionOutput",
    "track_latency",
    "LATENCY",
    "verify_api_key"
]
