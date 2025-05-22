from fastapi import status

SAMPLE_PROTEIN_REQUEST = {
    "sequence": "AAAA",
    "confidence_threshold": 0.8,
    "model_version": "NexaBio_2"
}

SAMPLE_PROTEIN_BATCH = {
    "requests": [
        {
            "sequence": "AAAA",
            "model_version": "NexaBio_1"
        },
        {
            "sequence": "AAAA",
            "model_version": "NexaBio_2"
        }
    ]
}

def test_health_check(test_client):
    """Test API health"""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "bio" in data["models"]

def test_protein_structure_prediction(test_client, valid_headers):
    """Test protein structure prediction endpoint"""
    response = test_client.post(
        "/api/bio/predict",
        json=SAMPLE_PROTEIN_REQUEST,
        headers=valid_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "predictions" in data
    assert "confidence_scores" in data
    assert len(data["predictions"]) == len(SAMPLE_PROTEIN_REQUEST["sequence"])

def test_protein_batch_prediction(test_client, valid_headers):
    """Test batch protein structure prediction"""
    response = test_client.post(
        "/api/bio/batch-predict",
        json=SAMPLE_PROTEIN_BATCH,
        headers=valid_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == len(SAMPLE_PROTEIN_BATCH["requests"])

    for result in data["results"]:
        assert "predictions" in result
        assert "confidence_scores" in result

def test_invalid_protein_structure_prediction(test_client, valid_headers):
    """Test invalid protein structure prediction"""
    invalid_request = {
        "sequence": "INVALID_SEQUENCE",
        "confidence_threshold": 0.8,
        "model_version": "NexaBio_2"
    }

    response = test_client.post(
        "/api/bio/predict",
        json=invalid_request,
        headers=valid_headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "Invalid sequence characters" in data["detail"][0]["msg"]

def materials_prediction(test_client, valid_headers):
    """Test materials prediction endpoint"""
    response = test_client.post(
        "/api/materials/predict",
        json={"data": "test_data"},
        headers=valid_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] == "test_prediction"
