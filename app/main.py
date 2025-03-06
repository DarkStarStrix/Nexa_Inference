# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server
import uvicorn
from app.api.routes import predictions
from app.services.auth import verify_api_key
from app.monitoring import LATENCY
from contextlib import contextmanager
import time

app = FastAPI(title="HelixSynth API")

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

app.include_router(predictions.router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])

@app.on_event("startup")
async def startup_event():
    # Start Prometheus metrics server
    start_http_server(9090)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
