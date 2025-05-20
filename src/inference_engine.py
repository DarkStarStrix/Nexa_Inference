import torch
from abc import ABC, abstractmethod
import os
import json
from src.logging_utils import log_model_inference, get_logger
from typing import Dict, Optional, List

logger = get_logger(__name__)

class ModelNotFoundError(Exception):
    """Raised when a model file doesn't exist."""
    pass

class InputValidationError(Exception):
    """Raised when input validation fails."""
    pass

class ModelLoadError(Exception):
    """Raised when there's an error loading the model."""
    pass

class VersionNotFoundError(Exception):
    """Raised when a specific model version is not found."""
    pass

class ModelVersionManager:
    """Manages different versions of models."""

    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.version_map = self._load_version_map()

    def _load_version_map(self) -> Dict[str, Dict[str, str]]:
        """Load model version mapping from filesystem.

        Returns:
            Dict[str, Dict[str, str]]: A mapping of model names to their versions
        """
        model_map = {}

        version_file = os.path.join(self.model_dir, "versions.json")
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse {version_file}: {str(e)}")
                logger.info("Falling back to directory scan")
            except Exception as e:
                logger.error(f"Unexpected error reading {version_file}: {str(e)}")

        # Scan model directory and build mapping
        try:
            if os.path.exists(self.model_dir):
                for filename in os.listdir(self.model_dir):
                    if filename.endswith('.pt'):
                        model_name_parts = filename.split('_')
                        if len(model_name_parts) >= 2:
                            model_name = model_name_parts[0]
                            version = model_name_parts[1].replace('.pt', '')

                            if model_name not in model_map:
                                model_map[model_name] = {}

                            model_map[model_name][version] = filename
                            logger.info(f"Discovered model: {model_name} version {version}")

            # Save the discovered mapping
            self._save_version_map(model_map)
            return model_map
        except Exception as e:
            logger.error(f"Error scanning model directory: {str(e)}")
            return {}

    def _save_version_map(self, version_map: Dict[str, Dict[str, str]]) -> None:
        """Save the version mapping to a JSON file."""
        version_file = os.path.join(self.model_dir, "versions.json")
        try:
            with open(version_file, 'w') as f:
                json.dump(version_map, f, indent=4)
            logger.info("Successfully saved version mapping")
        except Exception as e:
            logger.error(f"Failed to save version mapping: {str(e)}")

    def get_model_path(self, model_name: str, version: Optional[str] = None) -> str:
        """Get the path to a specific model version.

        Args:
            model_name: Name of the model
            version: Specific version to load. If None, loads latest version.

        Returns:
            str: Path to the model file

        Raises:
            ModelNotFoundError: If the model or version doesn't exist
        """
        if model_name not in self.version_map:
            raise ModelNotFoundError(f"Model {model_name} not found")

        if version is None:
            # Get latest version
            versions = list(self.version_map[model_name].keys())
            if not versions:
                raise ModelNotFoundError(f"No versions found for model {model_name}")
            version = max(versions)

        if version not in self.version_map[model_name]:
            raise VersionNotFoundError(
                f"Version {version} not found for model {model_name}"
            )

        return os.path.join(self.model_dir, self.version_map[model_name][version])

    def list_available_models(self) -> Dict[str, List[str]]:
        """List all available models and their versions.

        Returns:
            Dict[str, List[str]]: Mapping of model names to their available versions
        """
        return {
            model: list(versions.keys())
            for model, versions in self.version_map.items()
        }

    def validate_model_exists(self, model_name: str, version: Optional[str] = None) -> bool:
        """Validate that a model exists and is accessible.

        Args:
            model_name: Name of the model
            version: Specific version to check. If None, checks latest version.

        Returns:
            bool: True if the model exists and is accessible
        """
        try:
            model_path = self.get_model_path(model_name, version)
            return os.path.exists(model_path)
        except (ModelNotFoundError, VersionNotFoundError):
            return False

class BaseInferenceEngine(ABC):
    def __init__(self, model_path):
        logger.info(f"Initializing inference engine with model: {model_path}")

        if not os.path.exists(model_path):
            raise ModelNotFoundError(f"Model file not found: {model_path}")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

        try:
            self.model = torch.load(model_path, map_location=self.device)
            self.model.eval()
        except Exception as e:
            logger.error(f"Failed to load model {model_path}: {str(e)}")
            raise

        self.model_path = model_path

    @abstractmethod
    def preprocess(self, input_data):
        pass

    @abstractmethod
    def postprocess(self, output):
        pass

    @abstractmethod
    def validate_input(self, input_data):
        """Validate input data."""
        pass

    @log_model_inference(model_name="base")
    def predict(self, input_data):
        try:
            # Validate input
            self.validate_input(input_data)

            # Process data
            with torch.no_grad():
                preprocessed = self.preprocess(input_data)
                output = self.model(preprocessed.to(self.device))
                result = self.postprocess(output)

            return result
        except InputValidationError as e:
            logger.warning(f"Input validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

class BiologyInferenceEngine(BaseInferenceEngine):
    def __init__(self, model_path):
        super().__init__(model_path)
        self._log_model_info("Biology")

    def _log_model_info(self, model_type):
        """Log information about the loaded model."""
        logger.info(f"Loaded {model_type} inference engine")
        logger.info(f"Model file: {self.model_path}")

    def validate_input(self, sequence):
        if not sequence:
            raise InputValidationError("Sequence cannot be empty")

        # Validate that sequence contains only valid characters (ATGC for DNA)
        valid_chars = set("ATGCUN-")
        if not all(c in valid_chars for c in sequence.upper()):
            raise InputValidationError(
                "Sequence contains invalid characters. For DNA, use only A, T, G, C, U, N, and -."
            )

    def preprocess(self, sequence):
        # Convert FASTA sequence to tensor (placeholder)
        sequence = sequence.upper()
        return torch.tensor([ord(c) for c in sequence], dtype=torch.float32).unsqueeze(0)

    def postprocess(self, output):
        pred = torch.argmax(output, dim=1).item()
        conf = torch.softmax(output, dim=1).max().item() * 100
        return {"prediction": "HEC"[pred], "confidence": conf}

class AstrophysicsInferenceEngine(BaseInferenceEngine):
    def __init__(self, model_path):
        super().__init__(model_path)
        self._log_model_info("Astrophysics")

    def _log_model_info(self, model_type):
        """Log information about the loaded model."""
        logger.info(f"Loaded {model_type} inference engine")
        logger.info(f"Model file: {self.model_path}")

    def validate_input(self, data):
        """Validate astrophysics input data."""
        required_fields = ["temp", "luminosity", "metallicity"]
        for field in required_fields:
            if field not in data:
                raise InputValidationError(f"Missing required field: {field}")

        # Validate temperature
        if data["temp"] <= 0:
            raise InputValidationError("Temperature must be positive")

        # Validate luminosity
        if data["luminosity"] <= 0:
            raise InputValidationError("Luminosity must be positive")

        # Metallicity typically ranges from -4 to +1 in [Fe/H]
        if data["metallicity"] < -4 or data["metallicity"] > 1:
            logger.warning(f"Unusual metallicity value: {data['metallicity']}")

    def preprocess(self, data):
        # Convert {temp, luminosity, metallicity} to tensor
        return torch.tensor([data["temp"], data["luminosity"], data["metallicity"]],
                             dtype=torch.float32).unsqueeze(0)

    def postprocess(self, output):
        return {"prediction": output.item(), "confidence": 97.49}  # Placeholder confidence

class MaterialsInferenceEngine(BaseInferenceEngine):
    def __init__(self, model_path):
        super().__init__(model_path)
        self._log_model_info("Materials")

    def _log_model_info(self, model_type):
        """Log information about the loaded model."""
        logger.info(f"Loaded {model_type} inference engine")
        logger.info(f"Model file: {self.model_path}")

    def validate_input(self, structure):
        """Validate materials structure input."""
        if not structure or len(structure) < 10:
            raise InputValidationError("Structure data is too short or empty")

        # Check if it looks like a POSCAR format
        if "Direct" not in structure and "Cartesian" not in structure:
            logger.warning("Structure may not be in POSCAR format")

    def preprocess(self, structure):
        # Convert POSCAR string to tensor (placeholder)
        # Get first 10 numeric values, or pad with zeros
        numbers = []
        for word in structure.split():
            try:
                numbers.append(float(word))
                if len(numbers) >= 10:
                    break
            except ValueError:
                continue

        # Pad if needed
        while len(numbers) < 10:
            numbers.append(0.0)

        return torch.tensor(numbers, dtype=torch.float32).unsqueeze(0)

    def postprocess(self, output):
        return {"prediction": output.item(), "confidence": 98.5}  # Placeholder confidence

