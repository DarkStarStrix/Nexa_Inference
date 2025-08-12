# Nexa_Inference: Full Project Documentation (v2.0)

## Overview

**Nexa_Inference** is a unified scientific machine learning (SciML) inference platform providing state-of-the-art models for biology, materials science, astrophysics, and general-purpose language tasks. It exposes a REST API for fast, scalable, and secure predictions, returning results in JSON with detailed performance metrics and confidence scores.

---

## Architecture

- **Backend**: FastAPI (Python)
- **Models**: PyTorch-based, loaded at startup on appropriate hardware (CPU/GPU).
- **Endpoints**: RESTful, with authentication via API key.
- **Core Engines**: Domain-specific engines for Biology, Materials, and a dedicated LLM Inference Engine.
- **Benchmarking**: Integrated suite for measuring latency, throughput, and token generation speed.
- **Dashboard**: HTML dashboard for live monitoring and testing.

---

## Core Models

### 1. Biology: HelixSynth-Pro
- **Type**: Variational Autoencoder (VAE) + Diffusion
- **Task**: Protein secondary/tertiary structure prediction
- **Input**: Amino acid sequence (string)
- **Output**: Structure class (H/E/C), confidence, optionally 3D coordinates
- **Accuracy**: ~70.8% (Q3 score)
- **Latency**: ~78ms

### 2. Astrophysics: Stellar Property Model
- **Type**: Regression/Classification
- **Task**: Predict stellar mass, class, etc.
- **Input**: Temperature, luminosity, metallicity
- **Output**: Mass/class, confidence
- **Latency**: ~60ms

### 3. Materials Science: Materials GNN
- **Type**: Graph Neural Network
- **Task**: Predict band gap, formation energy, etc.
- **Input**: Crystal structure (POSCAR or string)
- **Output**: Property value, confidence
- **Accuracy**: ~98.5%
- **Latency**: ~62ms

### 4. Language: General Purpose LLM
- **Type**: Transformer-based (Mock)
- **Task**: Text generation, summarization, and analysis.
- **Input**: Text prompt (string) and `max_tokens`.
- **Output**: Generated text with detailed performance metrics.
- **Performance Metrics**: `total_latency_ms`, `time_to_first_token_ms`, `tokens_per_second`.

---

## API Endpoints

### Authentication

All endpoints require an API key via the `X-API-Key` header.

### Prediction

#### `/api/predict/bio` (POST)
- **Input**:  
  ```json
  {
    "sequence": "MAKQVKL",
    "model_version": "1",
    "confidence_threshold": 0.8
  }
  ```
- **Output**:  
  ```json
  {
    "model": "NexaBio_1",
    "prediction": "H",
    "confidence": 92.0,
    "tertiary_coordinates": [[1.23, 2.34, 3.45], "..."] 
  }
  ```

#### `/api/predict/materials` (POST)
- **Input**:  
  ```json
  {
    "structure": "POSCAR string",
    "model_version": "1",
    "energy_threshold": 0.5
  }
  ```
- **Output**:  
  ```json
  {
    "model": "NexaMat_1",
    "predicted_band_gap": 2.5,
    "confidence_score": 0.98
  }
  ```

#### `/api/llm/predict` (POST)
- **Description**: Runs inference with the general-purpose LLM.
- **Input**:
  ```json
  {
    "prompt": "Explain the concept of transfer learning in machine learning.",
    "max_tokens": 100
  }
  ```
- **Output**:
  ```json
  {
      "response": "lorem ipsum dolor sit amet...",
      "tokens_generated": 100,
      "metrics": {
          "total_latency_ms": 512.43,
          "time_to_first_token_ms": 85.12,
          "tokens_per_second": 195.15
      }
  }
  ```

### Synthetic Dataset Generation

- `/api/dataset/bio` (POST): Generate random protein dataset (JSON)
- `/api/dataset/materials` (POST): Generate random materials dataset (JSON)
- `/api/dataset/bio/csv` (POST): Download protein dataset (CSV)
- `/api/dataset/materials/csv` (POST): Download materials dataset (CSV)

### Monitoring & Benchmarking

- `/metrics` (GET): Returns average latency and request counts (API key required).
- `/dashboard` (GET): HTML dashboard for live monitoring and testing.
- `/health` (GET): Health check/status.
- `/api/benchmark` (POST): Triggers the performance benchmarking suite.
  - **Description**: Run a high-throughput test on a specified model for a set duration to measure performance.
  - **Input**:
    ```json
    {
        "model_type": "llm",
        "model_version": "1",
        "test_duration_seconds": 15
    }
    ```
  - **Output**:
    ```json
    {
        "benchmark_model": "llm_1",
        "test_duration_seconds": 15,
        "total_requests": 28,
        "avg_latency_ms": 521.5,
        "throughput_req_per_sec": 1.87,
        "total_tokens_generated": 1400,
        "avg_tokens_per_sec": 93.33
    }
    ```

---

## Usage

### Python Example

```python
import requests
response = requests.post(
    "https://api.nexa_inference.com/v1/llm/predict",
    headers={"X-API-Key": "your_api_key"},
    json={"prompt": "What is a Graph Neural Network?"}
)
print(response.json())
```

### Error Handling

- 400: Bad Request (invalid input)
- 401: Unauthorized (missing/invalid API key)
- 429: Too Many Requests (rate limit)
- 500: Internal Server Error

---

## Deployment

### Local Development

1. Clone repository:
   ```bash
   git clone https://github.com/DarkStarStrix/Nexa_Inference.git
   cd Nexa_Inference
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run API:
   ```bash
   python src/main.py
   ```
   Access at `http://localhost:8000`

4. Docker Deployment (Optional):
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

---

## Security

- API key authentication for all endpoints
- No user data stored
- SOC2 Type II compliant (planned)

---

## Performance

- **Average SciML Model Latency**: ~50-80ms
- **LLM Performance**: Measured in tokens/second and time-to-first-token.
- **Scalability**: Architected to support millions of requests per day.
- **Confidence Scores**: Included in all SciML predictions.

---

## Support & Contact

- Discord: [Join](https://discord.gg/ncGnBwR3)
- Email: allanw.mk@gmail.com

---

## License

Commercial license. See [LICENSE](LICENSE).

---

