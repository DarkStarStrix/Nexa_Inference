# app/core/utils/__init__.py
from typing import Dict, Any

def process_sequence(sequence: str) -> Dict[str, Any]:
    return {
        "processed": sequence.upper(),
        "length": len(sequence)
    }

__all__ = ["process_sequence"]