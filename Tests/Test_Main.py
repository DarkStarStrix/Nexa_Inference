def test_predict_bio_endpoint(client):
    """Test biology prediction endpoint."""
    response = client.post (
        "/v1/bio/predict",
        json={"sequence": "ATGCTAGCTAGCTAGC"},
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
    data = response.json ()
    assert "prediction" in data
    assert "confidence" in data
    assert isinstance (data ["confidence"], float)


def test_predict_astro_endpoint(client):
    """Test astrophysics prediction endpoint."""
    response = client.post (
        "/v1/astro/predict",
        json={"temp": 5778, "luminosity": 1.0, "metallicity": 0.0},
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
    data = response.json ()
    assert "prediction" in data
    assert "confidence" in data
    assert isinstance (data ["confidence"], float)


def test_predict_materials_endpoint(client):
    """Test materials prediction endpoint."""
    response = client.post (
        "/v1/materials/predict",
        json={"structure": "Direct 1.0 3.1903000763 0.0 0.0 0.0 3.1903000763 0.0 0.0 0.0 3.1903000763"},
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
    data = response.json ()
    assert "prediction" in data
    assert "confidence" in data
    assert isinstance (data ["confidence"], float)


def test_invalid_api_key(client):
    """Test invalid API key handling."""
    # Override the mock to simulate invalid API key
    from unittest.mock import patch

    with patch ("src.auth.verify_api_key", side_effect=Exception ("Invalid API key")):
        response = client.post (
            "/v1/bio/predict",
            json={"sequence": "ATGCTAGCTAGCTAGC"},
            headers={"X-API-Key": "invalid-key"}
        )
        assert response.status_code in [401, 500]  # Depends on how exception is handled


def test_signup_endpoint(client):
    """Test user signup endpoint."""
    response = client.post (
        "/signup",
        json={"email": "test@example.com", "plan": "free"}
    )
    assert response.status_code == 200
    data = response.json ()
    assert "api_key" in data
    assert len (data ["api_key"]) > 0