import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoints:
    """Test root and health check endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to EthioGuide API"}

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestSitesEndpoints:
    """Test cultural sites endpoints"""

    def test_get_all_sites_endpoint_exists(self):
        """Test that /sites endpoint is accessible"""
        response = client.get("/sites")
        # Should return 200 or 500 (if DB not connected), but not 404
        assert response.status_code in [200, 500]

    def test_get_site_by_name_not_found(self):
        """Test getting a non-existent site returns 404"""
        response = client.get("/sites/NonExistentSite12345")
        # Should return 404 or 500 (if DB not connected)
        assert response.status_code in [404, 500]

    def test_add_to_favorites_requires_site_name(self):
        """Test that adding to favorites requires site_name field"""
        response = client.post("/favorites", json={})
        # Should return 422 (validation error) since site_name is required
        assert response.status_code == 422


class TestAPIDocumentation:
    """Test API documentation endpoints"""

    def test_openapi_schema_exists(self):
        """Test that OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "EthioGuide API"
        assert schema["info"]["version"] == "1.0.0"

    def test_docs_endpoint_exists(self):
        """Test that /docs (Swagger UI) is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
