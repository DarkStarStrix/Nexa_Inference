import pytest
from src.inference_engine import (
    ModelVersionManager,
    BiologyInferenceEngine,
    AstrophysicsInferenceEngine,
    MaterialsInferenceEngine,
    ModelNotFoundError,
    InputValidationError,
    VersionNotFoundError
)
import torch
import os

class TestModelVersionManager:
    def test_initialization(self, model_manager):
        """Test that ModelVersionManager initializes correctly."""
        assert model_manager is not None
        assert isinstance(model_manager.version_map, dict)
        assert len(model_manager.version_map) > 0

    def test_list_available_models(self, model_manager):
        """Test listing available models."""
        models = model_manager.list_available_models()
        assert "NexaBio" in models
        assert "NexaAstro" in models
        assert len(models["NexaBio"]) == 2
        assert len(models["NexaAstro"]) == 1

    def test_get_model_path(self, model_manager, temp_model_dir):
        """Test getting model path."""
        path = model_manager.get_model_path("NexaBio", "1")
        assert path == os.path.join(temp_model_dir, "NexaBio_1.pt")
        assert os.path.exists(path)

    def test_get_latest_version(self, model_manager):
        """Test getting latest version of a model."""
        path = model_manager.get_model_path("NexaBio")  # No version specified
        assert "NexaBio_2.pt" in path  # Should get version 2 as it's latest

    def test_nonexistent_model(self, model_manager):
        """Test handling of nonexistent model."""
        with pytest.raises(ModelNotFoundError):
            model_manager.get_model_path("NonexistentModel")

    def test_nonexistent_version(self, model_manager):
        """Test handling of nonexistent version."""
        with pytest.raises(VersionNotFoundError):
            model_manager.get_model_path("NexaBio", "999")

class TestBiologyInferenceEngine:
    def test_initialization(self, temp_model_dir):
        """Test that BiologyInferenceEngine initializes correctly."""
        model_path = os.path.join(temp_model_dir, "NexaBio_1.pt")
        engine = BiologyInferenceEngine(model_path)
        assert engine is not None
        assert isinstance(engine.model, torch.nn.Module)

    def test_input_validation(self, temp_model_dir, mock_bio_data):
        """Test input validation for biology data."""
        engine = BiologyInferenceEngine(os.path.join(temp_model_dir, "NexaBio_1.pt"))

        # Valid input
        engine.validate_input(mock_bio_data)

        # Invalid input
        with pytest.raises(InputValidationError):
            engine.validate_input("ATGX")  # X is not valid

        with pytest.raises(InputValidationError):
            engine.validate_input("")  # Empty sequence

class TestAstrophysicsInferenceEngine:
    def test_initialization(self, temp_model_dir):
        """Test that AstrophysicsInferenceEngine initializes correctly."""
        model_path = os.path.join(temp_model_dir, "NexaAstro_1.pt")
        engine = AstrophysicsInferenceEngine(model_path)
        assert engine is not None
        assert isinstance(engine.model, torch.nn.Module)

    def test_input_validation(self, temp_model_dir, mock_astro_data):
        """Test input validation for astrophysics data."""
        engine = AstrophysicsInferenceEngine(os.path.join(temp_model_dir, "NexaAstro_1.pt"))

        # Valid input
        engine.validate_input(mock_astro_data)

        # Invalid input
        with pytest.raises(InputValidationError):
            engine.validate_input({"temp": -1, "luminosity": 1.0, "metallicity": -0.5})

        with pytest.raises(InputValidationError):
            engine.validate_input({})  # Missing fields

class TestMaterialsInferenceEngine:
    def test_initialization(self, temp_model_dir):
        """Test that MaterialsInferenceEngine initializes correctly."""
        model_path = os.path.join(temp_model_dir, "NexaMat_1.pt")
        engine = MaterialsInferenceEngine(model_path)
        assert engine is not None
        assert isinstance(engine.model, torch.nn.Module)

    def test_input_validation(self, temp_model_dir, mock_materials_data):
        """Test input validation for materials science data."""
        engine = MaterialsInferenceEngine(os.path.join(temp_model_dir, "NexaMat_1.pt"))

        # Valid input
        engine.validate_input(mock_materials_data)

        # Invalid input
        with pytest.raises(InputValidationError):
            engine.validate_input("")  # Empty structure

        with pytest.raises(InputValidationError):
            engine.validate_input("Invalid structure")  # Invalid format
