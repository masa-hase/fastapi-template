import pytest
from fastapi.testclient import TestClient


def test_request_id_in_response_header():
    from src.main import app
    client = TestClient(app)
    
    response = client.get("/api/v1/greeting")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) == 36  # UUID format