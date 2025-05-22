from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
import logging
from src.models import BiologyRequest, MaterialsRequest, DatasetRequest
from src.engines import BiologyInferenceEngine, MaterialsInferenceEngine
from src.auth import verify_api_key

app = FastAPI(title="Lambda0 API", version="1.0.0")
logger = logging.getLogger(__name__)

# Initialize model paths
MODEL_PATHS = {
    "bio": {
        "1": "C:/Users/kunya/PycharmProjects/HelixSynth/models/NexaBio_1.pt",
        "2": "C:/Users/kunya/PycharmProjects/HelixSynth/models/NexaBio_2.pt"
    },
    "materials": {
        "1": "C:/Users/kunya/PycharmProjects/HelixSynth/models/NexaMat_1.pt",
        "2": "C:/Users/kunya/PycharmProjects/HelixSynth/models/NexaMat_2.pt"
    }
}

# Initialize engines
engines = {
    "bio_1": BiologyInferenceEngine(MODEL_PATHS["bio"]["1"]),
    "bio_2": BiologyInferenceEngine(MODEL_PATHS["bio"]["2"]),
    "mat_1": MaterialsInferenceEngine(MODEL_PATHS["materials"]["1"]),
    "mat_2": MaterialsInferenceEngine(MODEL_PATHS["materials"]["2"])
}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models": {
            "bio": list(MODEL_PATHS["bio"].keys()),
            "materials": list(MODEL_PATHS["materials"].keys())
        }
    }

@app.post("/api/predict/bio")
async def predict_bio(request: BiologyRequest, _=Depends(verify_api_key)):
    try:
        engine = engines[f"bio_{request.model_version}"]
        result = engine.predict({
            "sequence": request.sequence,
            "confidence_threshold": request.confidence_threshold
        })
        return {
            "model": f"NexaBio_{request.model_version}",
            "predictions": result["predictions"],
            "confidence_scores": result["confidence_scores"]
        }
    except Exception as e:
        logger.error(f"Biology prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict/materials")
async def predict_materials(request: MaterialsRequest, _=Depends(verify_api_key)):
    try:
        engine = engines[f"mat_{request.model_version}"]
        result = engine.predict({
            "structure": request.structure,
            "energy_threshold": request.energy_threshold
        })
        return {
            "model": f"NexaMat_{request.model_version}",
            "predictions": result["predictions"],
            "confidence_scores": result["confidence_scores"]
        }
    except Exception as e:
        logger.error(f"Materials prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
