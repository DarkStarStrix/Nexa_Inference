# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import predictions
from app.utils.monitoring import setup_monitoring

app = FastAPI(title="HelixSynth API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(predictions.router, prefix="/api/v1")

# Startup event
@app.on_event("startup")
async def startup_event():
    setup_monitoring(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)