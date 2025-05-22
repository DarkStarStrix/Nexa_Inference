from pydantic import BaseModel
from typing import List, Dict, Any

class CFDRequest(BaseModel):
    geometry: Dict[str, Any]
    fluid_properties: Dict[str, Any]
    mesh_resolution: Dict[str, Any]

class BatchRequest(BaseModel):
    requests: List[Dict[str, Any]]

class ProteinRequest(BaseModel):
    sequence: str
    model_version: str = "NexaBio_1"

class MaterialRequest(BaseModel):
    structure: Dict[str, Any]
    properties: List[str]
    model_version: str = "NexaMat_1"

# Sample test data
SAMPLE_CFD_REQUEST = {
    "geometry": {
        "type": "channel",
        "dimensions": {
            "length": 1.0,
            "width": 0.1,
            "height": 0.1
        }
    },
    "fluid_properties": {
        "density": 1.0,
        "viscosity": 1e-3,
        "velocity": 1.0
    },
    "mesh_resolution": {
        "x": 100,
        "y": 20,
        "z": 20
    }
}

SAMPLE_BATCH_REQUEST = {
    "requests": [
        SAMPLE_CFD_REQUEST,
        {
            "geometry": {
                "type": "pipe",
                "dimensions": {
                    "length": 2.0,
                    "diameter": 0.1
                }
            },
            "fluid_properties": {
                "density": 1.0,
                "viscosity": 1e-3,
                "velocity": 2.0
            },
            "mesh_resolution": {
                "x": 200,
                "y": 20,
                "z": 20
            }
        }
    ]
}

# Sample test data for Bio
SAMPLE_PROTEIN_REQUEST = {
    "sequence": "MVKVGVNGFGRIGRLVTRAAFNSGKVDIVAINDPFIDLNYMVYMFQYDSTHGKFHGTVKAENGKLVINGNPITIFQERDPSKIKWGDAGAEYVVESTGVFTTMEKAGAHLQGGAKRVIISAPSADAPMFVMGVNHEKYDNSLKIISNASCTTNCLAPLAKVIHDNFGIVEGLMTTVHAITATQKTVDGPSGKLWRDGRGALQNIIPASTGAAKAVGKVIPELDGKLTGMAFRVPTANVSVVDLTCRLEKPAKYDDIKKVVKQASEGPLKGILGYTEHQVVSSDFNSDTHSSTFDAGAGIALNDHFVKLISWYDNEFGYSNRVVDLMAHMASKE",
    "model_version": "NexaBio_1"
}

SAMPLE_PROTEIN_BATCH = {
    "sequences": [
        "MVKVGVNGFGRIGRLVTRAAFNSGKVDIVAINDPFIDLNYMVYMFQYDSTHGKFHGTV",
        "MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNCVV"
    ],
    "model_version": "NexaBio_2"
}

# Sample test data for Material Science
SAMPLE_MATERIAL_REQUEST = {
    "structure": {
        "lattice": {
            "a": 3.867,
            "b": 3.867,
            "c": 3.867,
            "alpha": 90.0,
            "beta": 90.0,
            "gamma": 90.0
        },
        "species": ["Si", "Si", "Si", "Si", "Si", "Si", "Si", "Si"],
        "coords": [
            [0.0, 0.0, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
            [0.25, 0.25, 0.25],
            [0.75, 0.75, 0.25],
            [0.75, 0.25, 0.75],
            [0.25, 0.75, 0.75]
        ]
    },
    "properties": ["formation_energy", "band_gap", "elastic_constants"],
    "model_version": "NexaMat_1"
}

SAMPLE_MATERIAL_BATCH = {
    "structures": [
        SAMPLE_MATERIAL_REQUEST["structure"],
        {
            "lattice": {
                "a": 4.08,
                "b": 4.08,
                "c": 4.08,
                "alpha": 90.0,
                "beta": 90.0,
                "gamma": 90.0
            },
            "species": ["Ge", "Ge", "Ge", "Ge", "Ge", "Ge", "Ge", "Ge"],
            "coords": [
                [0.0, 0.0, 0.0],
                [0.0, 0.5, 0.5],
                [0.5, 0.0, 0.5],
                [0.5, 0.5, 0.0],
                [0.25, 0.25, 0.25],
                [0.75, 0.75, 0.25],
                [0.75, 0.25, 0.75],
                [0.25, 0.75, 0.75]
            ]
        }
    ],
    "properties": ["formation_energy", "band_gap"],
    "model_version": "NexaMat_2"
}

