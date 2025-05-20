import pytest
from fastapi.testclient import TestClient
import torch
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.append (os.path.dirname (os.path.dirname (os.path.abspath (__file__))))


# Mock Redis
@pytest.fixture
def mock_redis():
    with patch ("src.config.redis_client") as mock_client:
        mock_client.get.return_value = None
        mock_client.set.return_value = True
        yield mock_client


# Mock Supabase
@pytest.fixture
def mock_supabase():
    with patch ("src.config.supabase") as mock_client:
        mock_table = MagicMock ()
        mock_select = MagicMock ()
        mock_eq = MagicMock ()
        mock_execute = MagicMock ()
        mock_update = MagicMock ()
        mock_insert = MagicMock ()

        # Mocking the chain of methods
        mock_execute.execute.return_value.data = [{"tier": "free", "requests_used": 0}]
        mock_eq.eq.return_value = mock_execute
        mock_select.select.return_value = mock_eq
        mock_table.table.return_value = mock_select
        mock_update.update.return_value = mock_eq
        mock_table.table.return_value = mock_update
        mock_insert.insert.return_value = mock_execute
        mock_table.table.return_value = mock_insert

        mock_client.table.return_value = mock_table
        yield mock_client


# Mock models
@pytest.fixture
def mock_models():
    with patch ("torch.load") as mock_load:
        mock_model = MagicMock ()
        mock_model.eval.return_value = None
        mock_model.return_value = torch.tensor ([0.8, 0.1, 0.1])
        mock_load.return_value = mock_model
        yield mock_load


# Test client
@pytest.fixture
def client(mock_redis, mock_supabase, mock_models):
    from src.main import app

    with patch ("src.auth.verify_api_key", return_value={"tier": "free"}):
        client = TestClient (app)
        yield client
        