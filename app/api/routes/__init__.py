# app/api/routes/__init__.py
from fastapi import APIRouter, HTTPException, Depends
from app.api.routes.predictions import router
from app.services.auth import verify_api_key
from app.api.routes.predictions import ModelPredictor
from app.monitoring import track_latency

__all__ = [
    "router",
    "APIRouter",
    "HTTPException",
    "Depends",
    "verify_api_key",
    "ModelPredictor",
    "track_latency"
]
