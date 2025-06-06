import pytest
from fastapi.testclient import TestClient


def test_hello_world_endpoint():
    from src.main import app
    client = TestClient(app)
    
    response = client.get("/api/v1/greeting")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}