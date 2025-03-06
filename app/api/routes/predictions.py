# app/api/routes/predictions.py
from fastapi import APIRouter, HTTPException

from app.api.schemas import ProteinRequest, PredictionResponse
from app.core.inference import ProteinPredictor

router = APIRouter()
predictor = ProteinPredictor()

@router.post("/predict", response_model=PredictionResponse)
async def predict_structure(
    request: ProteinRequest
):
    try:
        result = await predictor.predict(request.sequence)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))