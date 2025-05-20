# src/utils/filters.py
from typing import Dict, Any, Optional

def validate_protein_sequence(sequence: str) -> bool:
    """Validate protein sequence contains only valid amino acids"""
    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
    return all(aa in valid_amino_acids for aa in sequence.upper())

def filter_structure_predictions(predictions: list, confidence_threshold: float) -> list:
    """Filter structure predictions based on confidence score"""
    return [pred for pred in predictions if pred["confidence"] >= confidence_threshold]

def filter_material_calculations(results: Dict[str, Any], energy_threshold: Optional[float] = None) -> Dict[str, Any]:
    """Filter DFT calculation results"""
    if energy_threshold and results.get("energy", float("inf")) > energy_threshold:
        return {"status": "rejected", "reason": "Energy above threshold"}
    return results

def filter_quantum_results(results: Dict[str, Any], fidelity_threshold: float = 0.9) -> Dict[str, Any]:
    """Filter quantum results based on fidelity threshold"""
    if results.get("fidelity", 0) < fidelity_threshold:
        return {"status": "low_fidelity", "original_results": results}
    return results