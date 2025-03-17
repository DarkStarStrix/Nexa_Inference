# app/api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Union

class ProteinRequest(BaseModel):
    sequence: str = Field(..., min_length=1, max_length=2000)

class PredictionResponse(BaseModel):
    structure: str
    confidence: float

class AstroInput(BaseModel):
    features: List[float]

class MaterialInput(BaseModel):
    atoms: List[List[float]]
    bonds: List[List[int]]

class PredictionOutput(BaseModel):
    prediction: Union[float, List[float]]
    model_type: str
