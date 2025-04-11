# app/routers/model_router.py
from app.api.schemas.schemas import AstroInput, MaterialInput, PredictionOutput
from fastapi import APIRouter, Depends, HTTPException

from app.core.inference import AstroPredictor, MaterialPredictor
from app.services.auth import verify_api_key

router = APIRouter()

astro_predictor = AstroPredictor()
material_predictor = MaterialPredictor()

@router.post("/astro/stellar", response_model=PredictionOutput)
async def predict_astro(input_data: AstroInput, _=Depends(verify_api_key)):
    try:
        result = await astro_predictor.predict_stellar(input_data.features)
        return PredictionOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/material/gnn", response_model=PredictionOutput)
async def predict_material_gnn(input_data: MaterialInput, _=Depends(verify_api_key)):
    try:
        result = await material_predictor.predict_gnn(input_data.atoms, input_data.bonds)
        return PredictionOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/material/vae", response_model=PredictionOutput)
async def predict_material_vae(input_data: MaterialInput, _=Depends(verify_api_key)):
    try:
        result = await material_predictor.predict_vae(input_data.atoms, input_data.bonds)
        return PredictionOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))