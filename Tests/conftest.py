import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

class MockSupabaseResponse:
    def __init__(self, data):
        self.data = data

@pytest.fixture(autouse=True)
def mock_supabase():
    mock = MagicMock()
    mock_response = MockSupabaseResponse([{'key': 'test_key', 'tier': 'free'}])
    mock.table.return_value = MagicMock()
    mock.table.return_value.select.return_value = MagicMock()
    mock.table.return_value.select.return_value.eq.return_value = MagicMock()
    mock.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
    
    with patch('src.config.supabase', mock), \
         patch('src.auth.supabase', mock):
        yield mock

@pytest.fixture
def test_client(mock_supabase):
    from src.main import app
    return TestClient(app)

@pytest.fixture
def valid_headers():
    return {"X-API-Key": "test_key"}
