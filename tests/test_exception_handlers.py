import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


class TestExceptionHandlers:
    """Test exception handlers through the API."""
    
    @pytest.fixture
    def client(self):
        from src.main import app
        return TestClient(app)
    
    def test_404_exception_handler(self, client):
        """Test that 404 errors are properly handled."""
        response = client.get("/non-existent-endpoint")
        
        assert response.status_code == 404
        assert "error" in response.json()
        assert response.json()["error"]["status_code"] == 404
        assert "X-Request-ID" in response.headers
    
    def test_validation_exception_handler(self, client):
        """Test validation errors by adding a test endpoint."""
        from src.main import app
        from fastapi import APIRouter
        
        # Create a temporary router with validation
        test_router = APIRouter()
        
        @test_router.get("/test-validation")
        def test_validation(number: int):
            return {"number": number}
        
        # Add the router temporarily
        app.include_router(test_router)
        
        try:
            # Test with invalid input
            response = client.get("/test-validation?number=not-a-number")
            
            assert response.status_code == 422
            assert "error" in response.json()
            assert response.json()["error"]["message"] == "Validation error"
            assert response.json()["error"]["status_code"] == 422
            assert "details" in response.json()["error"]
            assert "X-Request-ID" in response.headers
        finally:
            # Clean up: remove the test router
            app.router.routes = [r for r in app.router.routes if not hasattr(r, 'path') or r.path != "/test-validation"]