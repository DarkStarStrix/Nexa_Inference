from pydantic import BaseModel

class BiologyRequest(BaseModel):
    sequence: str

class AstroRequest(BaseModel):
    temp: float
    luminosity: float
    metallicity: float

class MaterialsRequest(BaseModel):
    structure: str

class PredictionResponse(BaseModel):
    prediction: str | float
    confidence: float

class UserSignup(BaseModel):
    email: str
    plan: str