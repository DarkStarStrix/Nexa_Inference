# app/core/inference.py
import torch
import logging
from typing import Dict, Any
from app.core.models.helix_synth_mini import HelixSynthMini
from app.config import MODEL_CONFIG

logger = logging.getLogger(__name__)

class ProteinPredictor:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model()
        self.aa_map = {
            'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4,
            'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9,
            'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14,
            'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19,
            'X': 20
        }

    def _load_model(self) -> HelixSynthMini:
        model = HelixSynthMini(
            embedding_dim=MODEL_CONFIG['embedding_dim'],
            hidden_dim=MODEL_CONFIG['hidden_dim'],
            num_layers=MODEL_CONFIG['num_layers']
        )
        model.load_state_dict(torch.load(MODEL_CONFIG['weights_path']))
        model.to(self.device)
        model.eval()
        return model

    async def predict(self, sequence: str) -> Dict[str, Any]:
        try:
            encoded = torch.tensor([
                [self.aa_map.get(aa, self.aa_map['X']) for aa in sequence]
            ], dtype=torch.long).to(self.device)

            with torch.no_grad():
                output = self.model(encoded)
                pred = output.argmax(dim=-1)
                conf = torch.softmax(output, dim=-1).max(dim=-1)[0].mean()

            structure = ''.join(['HEC'[i] for i in pred[0].cpu()])
            return {
                "structure": structure,
                "confidence": float(conf)
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise