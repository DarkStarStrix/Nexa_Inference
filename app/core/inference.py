# app/core/inference.py
from typing import Dict, Any, List

import torch


class BasePredictor:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class AstroPredictor(BasePredictor):
    def __init__(self):
        super().__init__()
        self.model = torch.load('app/core/models/Catboost_nn_model.pt')
        self.model.to(self.device)
        self.model.eval()

    async def predict_stellar(self, features: List[float]) -> Dict[str, Any]:
        features_tensor = torch.FloatTensor(features).reshape(1, -1).to(self.device)
        with torch.no_grad():
            prediction = self.model(features_tensor)
        return {
            "prediction": prediction.cpu().numpy().tolist()[0],
            "model_type": "stellar_properties"
        }

class MaterialPredictor(BasePredictor):
    def __init__(self):
        super().__init__()
        self.gnn_model = torch.load("app/models/material/gnn_model.pt")
        self.vae_model = torch.load("app/models/material/vae_model.pt")
        self.gnn_model.to(self.device)
        self.vae_model.to(self.device)
        self.gnn_model.eval()
        self.vae_model.eval()

    async def predict_gnn(self, atoms: List[List[float]], bonds: List[List[int]]) -> Dict[str, Any]:
        atoms_tensor = torch.FloatTensor(atoms).to(self.device)
        bonds_tensor = torch.LongTensor(bonds).to(self.device)
        with torch.no_grad():
            prediction = self.gnn_model(atoms_tensor, bonds_tensor)
        return {
            "prediction": prediction.cpu().numpy().tolist(),
            "model_type": "material_properties"
        }

    async def predict_vae(self, atoms: List[List[float]], bonds: List[List[int]]) -> Dict[str, Any]:
        atoms_tensor = torch.FloatTensor(atoms).to(self.device)
        bonds_tensor = torch.LongTensor(bonds).to(self.device)
        with torch.no_grad():
            latent = self.vae_model.encode(atoms_tensor, bonds_tensor)
        return {
            "embedding": latent.cpu().numpy().tolist(),
            "model_type": "material_embedding"
        }
