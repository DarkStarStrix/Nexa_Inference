# app/api/routes/predictions.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import ProteinRequest, PredictionResponse
from app.core.inference import ProteinPredictor
from app.services.auth import verify_api_key

router = APIRouter()
predictor = ProteinPredictor()

@router.post("/predict", response_model=PredictionResponse)
async def predict_structure(
    request: ProteinRequest,
    user = Depends(verify_api_key)
):
    try:
        result = await predictor.predict(request.sequence)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))