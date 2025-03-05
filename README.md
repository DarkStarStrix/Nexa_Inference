
# HelixSynth 🧬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://helixsynth.readthedocs.io/)

HelixSynth is a state-of-the-art API for protein secondary structure prediction, leveraging deep learning to provide rapid and accurate predictions of helices (H), beta sheets (E), and coils (C).

## 🚀 Quick Start

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

## 🎯 Key Features

- ⚡ **Ultra-Fast Processing**: <100ms per sequence prediction
- 🎯 **High Accuracy**: >85% accuracy on standard benchmark datasets
- 🔄 **Batch Processing**: Support for multiple sequences
- 📊 **Confidence Scoring**: Reliability metrics for predictions
- 🐳 **Docker Support**: Easy deployment and scaling
- 📚 **Python Client Library**: Simple integration

## 💻 Installation

```bash
# Via pip
pip install helixsynth-client

# From source
git clone https://github.com/yourusername/helixsynth.git
cd helixsynth
pip install -e .
```

## 🎓 Use Cases

### Academic Research
```python
from Bio import SeqIO
from helixsynth.client import HelixSynthClient

client = HelixSynthClient(api_key="your_api_key")

# Batch processing
for record in SeqIO.parse("proteins.fasta", "fasta"):
    prediction = client.predict(str(record.seq))
    print(f">{record.id}")
    print(f"Sequence: {record.seq}")
    print(f"Structure: {prediction['structure']}")
```

### Pharmaceutical Applications
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
```

## 💎 API Plans

| Plan | Requests/Month | Price | Best For |
|------|---------------|--------|----------|
| Free | 100 | $0 | Academic Research |
| Pro | 1,000 | $49 | Small Labs |
| Enterprise | Unlimited | Custom | Companies |

## 🤝 Contributing

We welcome contributions from the community! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide for details.

## 📚 Citation

If you use HelixSynth in your research, please cite:

```bibtex
@software{helixsynth2024,
  author = {Allan},
  title = {HelixSynth: Fast Protein Secondary Structure Prediction},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/DarkStarStrix/helixsynth}
}
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 Email: allanw.mk@gmail.com
- 💬 Discord: [Join our community](https://discord.gg/helixsynth)
- 🐦 Twitter: [@HelixSynth](https://twitter.com/helixsynth)

## 📦 Model Weights

Download the latest model weights:

```bash
wget https://models.helixsynth.org/weights/helixsynth_mini.pt
```

