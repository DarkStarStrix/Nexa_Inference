# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server
import uvicorn
from contextlib import contextmanager
import time

from app.api.routes import ModelPredictor
from app.services.auth import verify_api_key
from app.api.schemas.schemas import (
    AstroInput,
    MaterialInput,
    PredictionOutput
)
from app.monitoring import LATENCY

app = FastAPI(title="Science ML API")
predictor = ModelPredictor()

@contextmanager
def track_latency(endpoint):
    start_time = time.time()
    try:
        yield
    finally:
        LATENCY.labels(endpoint=endpoint).observe(time.time() - start_time)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/astro/predict", response_model=PredictionOutput)
async def predict_astro(data: AstroInput, _=Depends(verify_api_key)):
    with track_latency("astro_prediction"):
        try:
            result = await predictor.predict_astro(data.features)
            return PredictionOutput(**result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/material/gnn", response_model=PredictionOutput)
async def predict_material_gnn(data: MaterialInput, _=Depends(verify_api_key)):
    with track_latency("material_gnn"):
        try:
            result = await predictor.predict_material_gnn(data.atoms, data.bonds)
            return PredictionOutput(**result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/material/vae", response_model=PredictionOutput)
async def predict_material_vae(data: MaterialInput, _=Depends(verify_api_key)):
    with track_latency("material_vae"):
        try:
            result = await predictor.predict_material_vae(data.atoms, data.bonds)
            return PredictionOutput(**result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

async def startup_event():
    start_http_server(9090)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
