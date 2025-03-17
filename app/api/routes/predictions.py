# app/api/routes/predictions.py
from typing import Dict, Any, List

import torch


class ModelPredictor:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.astro_model = self._load_astro_model()
        self.gnn_model = self._load_gnn_model()
        self.vae_model = self._load_vae_model()

    def _load_astro_model(self):
        model = torch.load('app/core/models/Catboost_nn_model.pt')
        model.to(self.device)
        model.eval()
        return model

    def _load_gnn_model(self):
        model = torch.load("app/models/material/gnn_model.pt")
        model.to(self.device)
        model.eval()
        return model

    def _load_vae_model(self):
        model = torch.load("app/models/material/vae_model.pt")
        model.to(self.device)
        model.eval()
        return model

    async def predict_astro(self, features: List[float]) -> Dict[str, Any]:
        features_tensor = torch.FloatTensor(features).reshape(1, -1).to(self.device)
        with torch.no_grad():
            prediction = self.astro_model(features_tensor)
            confidence = torch.softmax(prediction, dim=1).max().item()

        return {
            "prediction": prediction.cpu().numpy().tolist()[0],
            "confidence": confidence,
            "model_type": "astro"
        }

    async def predict_material_gnn(self, atoms: List[List[float]], bonds: List[List[int]]) -> Dict[str, Any]:
        atoms_tensor = torch.FloatTensor(atoms).to(self.device)
        bonds_tensor = torch.LongTensor(bonds).to(self.device)

        with torch.no_grad():
            prediction = self.gnn_model(atoms_tensor, bonds_tensor)

        return {
            "prediction": prediction.cpu().numpy().tolist(),
            "model_type": "material_gnn"
        }

    async def predict_material_vae(self, atoms: List[List[float]], bonds: List[List[int]]) -> Dict[str, Any]:
        atoms_tensor = torch.FloatTensor(atoms).to(self.device)
        bonds_tensor = torch.LongTensor(bonds).to(self.device)

        with torch.no_grad():
            latent = self.vae_model.encode(atoms_tensor, bonds_tensor)

        return {
            "embedding": latent.cpu().numpy().tolist(),
            "model_type": "material_vae"
        }


def router():
    return ModelPredictor()
