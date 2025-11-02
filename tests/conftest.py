import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_activity():
    return {
        "description": "Test activity description",
        "schedule": "Test schedule",
        "max_participants": 10,
        "participants": ["test@mergington.edu"]
    }