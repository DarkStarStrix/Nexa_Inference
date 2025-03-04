# app/api/schemas.py
from pydantic import BaseModel, Field

class ProteinRequest(BaseModel):
    sequence: str = Field(..., min_length=1, max_length=2000)

class PredictionResponse(BaseModel):
    structure: str
    confidence: float