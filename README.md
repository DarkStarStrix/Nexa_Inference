# Nexa_Inference 
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![API Status](https://img.shields.io/badge/API-Live-green.svg)](https://scimlhub.com/status)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.scimlhub.com)

**Nexa_Inference** is a unified platform for scientific machine learning, providing the newest Nexa models for predictions in biology (protein structure), astrophysics (stellar properties), and material science (material properties). Access these models via a simple REST API, with results returned in JSON format including predictions and confidence scores (0-100%).

## Quick Start

### Prerequisites
- Python 3.9+
- An API key (still in dev coming soon)
- `requests` library (`pip install requests`)

### Example: Protein Structure Prediction
Predict the secondary structure of a protein sequence:
```python
import requests

response = requests.post(
    "https://api.Nexa_inference.com/v1/bio/predict",
    headers={"X-API-Key": "your_api_key"},
    json={"sequence": "MAKQVKL"}
)

result = response.json()
print(result)
# Output: {"prediction": "H", "confidence": 80.56}
```

### Example: Stellar Property Prediction
Estimate a star's mass:
```python
response = requests.post(
    "https://api.Nexa_inference.com/v1/astro/predict",
    headers={"X-API-Key": "your_api_key"},
    json={
        "temp": 5778,  # Kelvin
        "luminosity": 1.0,  # Solar luminosity
        "metallicity": 0.0  # [Fe/H]
    }
)

result = response.json()
print(f"Stellar Mass: {result['prediction']} Solar masses")
print(f"Confidence: {result['confidence']}%")
# Output: {"prediction": 1.0, "confidence": 97.49}
```

### Example: Material Property Prediction
Predict a material's band gap:
```python
response = requests.post(
    "https://api.Nexa_inference.com/v1/materials/predict",
    headers={"X-API-Key": "your_api_key"},
    json={"structure": "POSCAR data string"}
)

result = response.json()
print(f"Band Gap: {result['prediction']} eV")
print(f"Confidence: {result['confidence']}%")
# Output: {"prediction": 2.5, "confidence": 98.5}
```

## Core Models

### Biology: HelixSynth-Pro (Protein Structure Prediction)
- **Model**: Variational Autoencoder (VAE) with diffusion
- **Purpose**: Predicts protein secondary structures (H: Helix, E: Sheet, C: Coil)
- **Accuracy**: 70.82% overall (Q3 score)
- **Latency**: ~78ms
- **Details**: See https://github.com/DarkStarStrix/CSE-Repo-of-Advanced-Computation-ML-and-Systems-Engineering/blob/main/Papers/Computer_Science/Machine_Learning/Protein_Structure_Prediction.pdf

### Materials Science: Materials GNN
- **Model**: Graph Neural Network (GNN)
- **Purpose**: Predicts material properties (band gap, formation energy)
- **Accuracy**: 98.5% on crystal structures
- **Latency**: ~62ms
- **Details**: See https://github.com/DarkStarStrix/CSE-Repo-of-Advanced-Computation-ML-and-Systems-Engineering/blob/main/Papers/Computer_Science/Machine_Learning/Material_Scince_battery_ion_prediction.pdf

## API Usage

The API endpoints return predictions and confidence scores in JSON format: `{"prediction": value, "confidence": percentage}`.

### Endpoints

#### 1. `/v1/bio/predict` - Protein Structure Prediction
- **Method**: POST
- **Input**:
  ```json
  {
    "sequence": "MAKQVKL" 
  }
  ```
- **Output**:
  ```json
  {
    "prediction": "H",  
    "confidence": 80.56  
  }
  ```

#### 3. `/v1/materials/predict` - Material Property Prediction
- **Method**: POST
- **Input**:
  ```json
  {
    "structure": "POSCAR data string"  
  }
  ```
- **Output**:
  ```json
  {
    "prediction": 2.5,  
    "confidence": 98.5   
  }
  ```

### Authentication
Include your API key in the request header:
```bash
X-API-Key: your_api_key
```

### Error Responses
- **400 Bad Request**: Invalid input format
- **401 Unauthorized**: Missing or invalid API key
- **429 Too Many Requests**: Rate limit exceeded
- **500 Server Error**: Internal issue (contact support)

## Installation (Local Development)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DarkStarStrix/Nexa_Inference.git
   ```
   cd Lambda_Zero
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API Locally**:
   ```bash
   python app/main.py
   ```
   The API will be available at `http://localhost:8000`.

4. **Docker Deployment** (Optional):
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

## Key Features
- **Fast**: Average response time ~50ms
- **Accurate**: >95% accuracy across domains
- **Reliable**: Confidence scores with every prediction
- **Scalable**: Supports millions of requests daily
- **Secure**: SOC2 Type II compliant

## Example Outputs

### Protein Structure
```json
{
  "prediction": "H",
  "confidence": 80.56
}
```

### Astrophysics
```json
{
  "prediction": "GALAXY",
  "confidence": 97.29
}
```

### Materials Science
```json
{
  "prediction": 2.5,
  "confidence": 98.5
}
```

## Use Cases
- **Biology**: Protein design, drug discovery
- **Astrophysics**: Stellar classification, exoplanet research
- **Materials Science**: Material discovery, energy applications

## Resources
- [How to Use](how_to_use.md)
- [Changelog](CHANGELOG.md)

## Enterprise Support
For custom models, on-premise deployment, or integration help, email: [allanw.mk@gmail.com](mailto:allanw.mk@gmail.com).


## License
Commercial license - see [LICENSE](LICENSE)
