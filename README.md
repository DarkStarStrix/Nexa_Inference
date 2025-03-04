I'll create example documentation for open-sourcing this project, including usage examples and use cases.

```python
# docs/README.md
# HelixSynth: Protein Secondary Structure Prediction API

HelixSynth is an open-source API for predicting protein secondary structures using deep learning. It provides fast and accurate predictions for helices (H), beta sheets (E), and coils (C).

## Quick Start

```python
import requests

API_KEY = "your_api_key"
API_URL = "https://api.helixsynth.com/api/v1/predict"

def predict_structure(sequence):
    response = requests.post(
        API_URL,
        headers={"X-API-Key": API_KEY},
        json={"sequence": sequence}
    )
    return response.json()

# Example usage
sequence = "MLSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF"
result = predict_structure(sequence)
print(f"Structure: {result['structure']}")
print(f"Confidence: {result['confidence']:.2f}")
```

## Use Cases

### Academic Research
```python
from Bio import SeqIO
from helixsynth.client import HelixSynthClient

client = HelixSynthClient(api_key="your_api_key")

# Batch processing of protein sequences
for record in SeqIO.parse("proteins.fasta", "fasta"):
    prediction = client.predict(str(record.seq))
    print(f">{record.id}")
    print(f"Sequence: {record.seq}")
    print(f"Structure: {prediction['structure']}")
```

### Pharmaceutical Companies
```python
from helixsynth.client import HelixSynthClient
import pandas as pd

class DrugScreening:
    def __init__(self, api_key):
        self.client = HelixSynthClient(api_key=api_key)
    
    def analyze_candidates(self, sequences):
        results = []
        for seq in sequences:
            pred = self.client.predict(seq)
            helix_content = pred['structure'].count('H') / len(pred['structure'])
            results.append({
                'sequence': seq,
                'structure': pred['structure'],
                'helix_content': helix_content,
                'confidence': pred['confidence']
            })
        return pd.DataFrame(results)

# Usage
screener = DrugScreening(api_key="your_api_key")
candidates = ["MKKLLVVL...", "ASDFGHKL..."]  # Your protein candidates
results = screener.analyze_candidates(candidates)
```

## API Plans

| Plan | Requests/Month | Price | Best For |
|------|---------------|--------|----------|
| Free | 100 | $0 | Academic Research |
| Pro | 1,000 | $49 | Small Labs |
| Enterprise | Unlimited | Custom | Companies |

## Features

- Fast predictions (<100ms per sequence)
- 85%+ accuracy on benchmark datasets
- Batch processing support
- Confidence scores
- REST API
- Python client library
- Docker support

## Installation

```bash
# Install using pip
pip install helixsynth-client

# Or build from source
git clone https://github.com/yourusername/helixsynth.git
cd helixsynth
pip install -e .
```

## Contributing

We welcome contributions! Please check our [CONTRIBUTING.md](CONTRIBUTING.md) guide.

## Citation

If you use HelixSynth in your research, please cite:

```bibtex
@software{helixsynth2024,
  author = {Your Name},
  title = {HelixSynth: Fast Protein Secondary Structure Prediction},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/yourusername/helixsynth}
}
```

## License

MIT License
```

wget https://models.helixsynth.org/weights/helixsynth_mini.pt
