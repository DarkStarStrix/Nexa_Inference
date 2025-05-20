import pytest
import os
import torch
import tempfile
import json
from src.inference_engine import ModelVersionManager

@pytest.fixture
def mock_model():
    """Create a mock PyTorch model for testing."""
    class MockModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = torch.nn.Linear(10, 1)

        def forward(self, x):
            return self.linear(x)

    return MockModel()

@pytest.fixture
def temp_model_dir():
    """Create a temporary directory with mock model files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock model files
        mock_models = {
            "NexaBio_1.pt": None,
            "NexaBio_2.pt": None,
            "NexaAstro_1.pt": None
        }

        for model_name in mock_models:
            model_path = os.path.join(temp_dir, model_name)
            mock_model = torch.nn.Linear(10, 1)
            torch.save(mock_model, model_path)

        # Create versions.json
        versions = {
            "NexaBio": {
                "1": "NexaBio_1.pt",
                "2": "NexaBio_2.pt"
            },
            "NexaAstro": {
                "1": "NexaAstro_1.pt"
            }
        }

        with open(os.path.join(temp_dir, "versions.json"), "w") as f:
            json.dump(versions, f)

        yield temp_dir

@pytest.fixture
def model_manager(temp_model_dir):
    """Create a ModelVersionManager instance with the temporary directory."""
    return ModelVersionManager(model_dir=temp_model_dir)

@pytest.fixture
def mock_bio_data():
    """Create mock biology input data."""
    return "ATGCATGC"

@pytest.fixture
def mock_astro_data():
    """Create mock astrophysics input data."""
    return {
        "temp": 5000,
        "luminosity": 1.0,
        "metallicity": -0.5
    }

@pytest.fixture
def mock_materials_data():
    """Create mock materials science input data."""
    return """Material Structure
    Direct
    1.0 0.0 0.0
    0.0 1.0 0.0
    0.0 0.0 1.0
    """
