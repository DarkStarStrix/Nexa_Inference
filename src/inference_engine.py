import torch
from abc import ABC, abstractmethod

class BaseInferenceEngine(ABC):
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(model_path, map_location=self.device)
        self.model.eval()

    @abstractmethod
    def preprocess(self, input_data):
        pass

    @abstractmethod
    def postprocess(self, output):
        pass

    def predict(self, input_data):
        with torch.no_grad():
            preprocessed = self.preprocess(input_data)
            output = self.model(preprocessed.to(self.device))
            result = self.postprocess(output)
        return result

class BiologyInferenceEngine(BaseInferenceEngine):
    def preprocess(self, sequence):
        # Convert FASTA sequence to tensor (placeholder)
        return torch.tensor([ord(c) for c in sequence], dtype=torch.float32).unsqueeze(0)

    def postprocess(self, output):
        pred = torch.argmax(output, dim=1).item()
        conf = torch.softmax(output, dim=1).max().item() * 100
        return {"prediction": "HEC"[pred], "confidence": conf}

class AstrophysicsInferenceEngine(BaseInferenceEngine):
    def preprocess(self, data):
        # Convert {temp, luminosity, metallicity} to tensor
        return torch.tensor([data["temp"], data["luminosity"], data["metallicity"]],
                          dtype=torch.float32).unsqueeze(0)

    def postprocess(self, output):
        return {"prediction": output.item(), "confidence": 97.49}  # Placeholder confidence

class MaterialsInferenceEngine(BaseInferenceEngine):
    def preprocess(self, structure):
        # Convert POSCAR string to tensor (placeholder)
        return torch.tensor([float(x) for x in structure.split()[:10]],
                          dtype=torch.float32).unsqueeze(0)

    def postprocess(self, output):
        return {"prediction": output.item(), "confidence": 98.5}  # Placeholder confidence
