import pytest
from fastapi.testclient import TestClient


def test_personalized_greeting_endpoint():
    from src.main import app
    client = TestClient(app)
    
    # Test with default language
    response = client.post(
        "/api/v1/greeting/personalized",
        json={"name": "Alice"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Hello, Alice!"}
    
    # Test with Japanese
    response = client.post(
        "/api/v1/greeting/personalized",
        json={"name": "Alice", "language": "ja"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "こんにちは、Aliceさん！"}
    
    # Test with Spanish
    response = client.post(
        "/api/v1/greeting/personalized",
        json={"name": "Carlos", "language": "es"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "¡Hola, Carlos!"}
    
    # Test with French
    response = client.post(
        "/api/v1/greeting/personalized",
        json={"name": "Marie", "language": "fr"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Bonjour, Marie!"}


def test_personalized_greeting_validation():
    from src.main import app
    client = TestClient(app)
    
    # Test with empty name
    response = client.post(
        "/api/v1/greeting/personalized",
        json={"name": ""}
    )
    assert response.status_code == 422
    
    # Test with invalid language
    response = client.post(
        "/api/v1/greeting/personalized",
        json={"name": "Test", "language": "invalid"}
    )
    assert response.status_code == 422
    
    # Test with missing name
    response = client.post(
        "/api/v1/greeting/personalized",
        json={}
    )
    assert response.status_code == 422