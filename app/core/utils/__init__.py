# app/core/utils/__init__.py
from typing import Dict, Any, List, Tuple
import torch
import numpy as np
import pandas as pd
from Bio import SeqIO
from datetime import datetime
import os
import yaml
from tqdm import tqdm
import logging

def process_sequence(sequence: str) -> Dict[str, Any]:
    return {
        "processed": sequence.upper(),
        "length": len(sequence)
    }

__all__ = [
    "process_sequence",
    "Dict", "Any", "List", "Tuple",
    "torch", "np", "pd",
    "SeqIO", "datetime", "os",
    "yaml", "tqdm", "logging"
]
