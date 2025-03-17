# How to Use SciML Hub

This guide provides step-by-step instructions for using SciML Hub's API to access machine learning models for scientific predictions.

## Setup and Authentication

1. **Install the Client Library**
   ```python
   # Python
   from scimlhub import Client
   client = Client(api_key="your_api_key")
   ```
   ```javascript
   // JavaScript
   import { SciMLClient } from '@scimlhub/client';
   const client = new SciMLClient('your_api_key');
   ```

2. **Secure Authentication (Recommended)**
   ```python
   # Using environment variables
   import os
   client = Client(api_key=os.environ["SCIML_API_KEY"])
   ```

## Using the Astrophysics Model

1. **Single Prediction**
   ```python
   stellar_params = {
       "temp": 5778,        # Surface temperature (K)
       "luminosity": 1.0,   # Solar luminosity
       "metallicity": 0.0,  # [Fe/H]
       "radius": 1.0        # Solar radii (optional)
   }
   
   result = client.astro.predict(stellar_params)
   ```

2. **Batch Prediction**
   ```python
   stars = [
       {"temp": 5778, "luminosity": 1.0, "metallicity": 0.0},
       {"temp": 3500, "luminosity": 0.1, "metallicity": -0.5}
   ]
   results = client.astro.predict_batch(stars)
   ```

## Using the Materials GNN Model

1. **Structure Prediction**
   ```python
   # Input structure in POSCAR format
   structure_data = """
   Direct
   1.0
       3.1903000763         0.0000000000         0.0000000000
       0.0000000000         3.1903000763         0.0000000000
       0.0000000000         0.0000000000         3.1903000763
   Si
   2
   Direct
       0.0000000000         0.0000000000         0.0000000000
       0.5000000000         0.5000000000         0.5000000000
   """
   
   result = client.materials.predict(
       structure=structure_data,
       properties=["band_gap", "formation_energy", "elastic_tensor"]
   )
   ```

## Using the Molecular VAE Model

1. **Generate New Molecules**
   ```python
   molecules = client.molecules.generate({
       "constraints": {
           "mol_weight": [300, 500],
           "logP": [-1, 3],
           "synthetic_accessibility": [1, 5],
           "qed": [0.6, 1.0]
       },
       "num_samples": 5
   })
   ```

2. **Predict Molecular Properties**
   ```python
   props = client.molecules.predict(
       smiles="CC1=CC=C(C=C1)NC(=O)CN2CCN(CC2)CC(=O)NC3=CC=C(C=C3)Cl",
       properties=["solubility", "toxicity", "binding_affinity"]
   )
   ```

## Error Handling

```python
from scimlhub.exceptions import (
    InvalidInputError,
    RateLimitError,
    AuthenticationError
)

try:
    result = client.astro.predict({"temp": -100})
except InvalidInputError as e:
    print(f"Invalid input: {e}")
except RateLimitError:
    print("Rate limit exceeded")
except AuthenticationError:
    print("Invalid API key")
```

## Best Practices

1. **Use Batch Processing for Multiple Predictions**
   ```python
   # Good
   results = client.astro.predict_batch(stars)
   
   # Bad
   results = [client.astro.predict(star) for star in stars]
   ```

2. **Filter by Confidence Score**
   ```python
   valid_results = [r for r in results if r["confidence"] > 0.9]
   ```

3. **Implement Caching for Repeated Queries**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def cached_prediction(smiles):
       return client.molecules.predict(smiles)
   ```

4. **Handle Rate Limits**
   ```python
   from time import sleep
   from scimlhub.exceptions import RateLimitError
   
   def retry_with_backoff(func, max_retries=3):
       for i in range(max_retries):
           try:
               return func()
           except RateLimitError:
               if i == max_retries - 1:
                   raise
               sleep(2 ** i)
   ```

## Plan Limitations

| Plan        | Requests/Day | Batch Size | Price/Month |
|-------------|--------------|------------|-------------|
| Free        | 300          | 10         | $0          |
| Premium-1K  | 1,000        | 100        | $50         |
| Premium-5K  | 5,000        | 500        | $35         |
| Premium-10K | 10,000       | 1,000      | $25         |
| Enterprise  | Unlimited    | Custom     | Custom      |

## Getting Support

- Discord Community: [Join](https://discord.gg/ncGnBwR3)
- Enterprise Support: allanw.mk@gmail.com
