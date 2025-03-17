# app/api/__init__.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from app.api.routes.predictions import router as predictions_router
from app.api.schemas.schemas import (
    ProteinRequest,
    PredictionResponse,
    AstroInput,
    MaterialInput,
    PredictionOutput
)

__all__ = [
    "FastAPI", "HTTPException", "Depends",
    "CORSMiddleware", "BaseModel",
    "List", "Dict", "Any",
    "predictions_router",
    "ProteinRequest", "PredictionResponse",
    "AstroInput", "MaterialInput", "PredictionOutput"
]

