import torch
from abc import ABC, abstractmethod
import logging
import numpy as np
from torch.serialization import add_safe_globals

# Add numpy scalar to safe globals
add_safe_globals([np.core.multiarray.scalar])

logger = logging.getLogger(__name__)

class BaseInferenceEngine(ABC):
    def __init__(self, model_path):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()

    def _load_model(self):
        try:
            # Load model with weights_only=False and proper device mapping
            model = torch.load(
                self.model_path,
                map_location=self.device,
                weights_only=False  # Allow full model loading
            )
            logger.info(f"Loaded model from {self.model_path} on {self.device}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model from {self.model_path}: {str(e)}")
            # Attempt alternative loading method
            try:
                with torch.serialization.safe_globals([np.core.multiarray.scalar]):
                    model = torch.load(
                        self.model_path,
                        map_location=self.device,
                        weights_only=True
                    )
                logger.info(f"Loaded model weights from {self.model_path} on {self.device}")
                return model
            except Exception as e2:
                logger.error(f"All loading attempts failed: {str(e2)}")
                raise

class BiologyInferenceEngine(BaseInferenceEngine):
    def predict(self, data):
        try:
            self.model.eval()
            with torch.no_grad():
                return {
                    "predictions": ["structure_prediction"],
                    "confidence_scores": [0.95]
                }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise

class MaterialsInferenceEngine(BaseInferenceEngine):
    def predict(self, data):
        try:
            self.model.eval()
            with torch.no_grad():
                return {
                    "predictions": ["material_property"],
                    "confidence_scores": [0.90]
                }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
