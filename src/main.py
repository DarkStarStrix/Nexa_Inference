from fastapi import FastAPI, Depends, HTTPException
import hashlib
import json
from src.schemas import BiologyRequest, AstroRequest, MaterialsRequest, PredictionResponse, UserSignup
from src.auth import verify_api_key
from src.config import redis_client
from src.inference_engine import BiologyInferenceEngine, AstrophysicsInferenceEngine, MaterialsInferenceEngine
import secrets

app = FastAPI()

bio_engine = BiologyInferenceEngine("models/biology.pt")
astro_engine = AstrophysicsInferenceEngine("models/astrophysics.pt")
mat_engine = MaterialsInferenceEngine("models/materials.pt")
# Initialize other engines (QST, HEP, CFD) similarly

@app.post("/v1/bio/predict", response_model=PredictionResponse)
async def predict_bio(request: BiologyRequest, _=Depends(verify_api_key)):
    cache_key = hashlib.sha256(request.sequence.encode()).hexdigest()
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    result = bio_engine.predict(request.sequence)
    redis_client.set(cache_key, json.dumps(result), ex=3600)
    return result

@app.post("/v1/astro/predict", response_model=PredictionResponse)
async def predict_astro(request: AstroRequest, _=Depends(verify_api_key)):
    input_str = f"{request.temp}{request.luminosity}{request.metallicity}"
    cache_key = hashlib.sha256(input_str.encode()).hexdigest()
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    result = astro_engine.predict(request.dict())
    redis_client.set(cache_key, json.dumps(result), ex=3600)
    return result

@app.post("/v1/materials/predict", response_model=PredictionResponse)
async def predict_materials(request: MaterialsRequest, _=Depends(verify_api_key)):
    cache_key = hashlib.sha256(request.structure.encode()).hexdigest()
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    result = mat_engine.predict(request.structure)
    redis_client.set(cache_key, json.dumps(result), ex=3600)
    return result

@app.post("/signup")
async def signup(user: UserSignup):
    existing = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User already exists")
    api_key = secrets.token_urlsafe(32)
    supabase.table("users").insert({
        "email": user.email,
        "tier": user.plan,
        "api_key": api_key,
        "requests_used": 0
    }).execute()
    return {"api_key": api_key}
