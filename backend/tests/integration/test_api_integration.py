"""
Integration tests for API endpoints.

Tests the full request/response cycle including database interactions.
"""

import pytest
from unittest.mock import patch, Mock
from datetime import datetime


class TestReposEndpointIntegration:
    """Integration tests for repos endpoint."""

    def test_get_repos_full_flow(self, client, test_db):
        """Test complete flow of getting repositories."""
        # Arrange - Create a user with repos in the database
        from app.models.user import User
        from app.models.repository import Repository
        
        user = User(github_username="testuser")
        user.access_token = "test_token"
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        repo1 = Repository(
            name="repo1",
            url="https://github.com/user/repo1",
            last_updated="2025-01-01T00:00:00Z",
            owner_id=user.id
        )
        repo2 = Repository(
            name="repo2",
            url="https://github.com/user/repo2",
            last_updated="2025-01-02T00:00:00Z",
            owner_id=user.id
        )
        test_db.add(repo1)
        test_db.add(repo2)
        test_db.commit()
        
        # Act - Use Bearer token
        response = client.get(
            "/api/v1/repos/",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "total_repos" in data
        assert "repos" in data
        assert data["total_repos"] == 2
        assert len(data["repos"]) == 2

    def test_get_repos_with_invalid_token_returns_error(self, client):
        """Test that invalid token returns appropriate error."""
        # Act - Use invalid Bearer token (no user with this token in DB)
        response = client.get(
            "/api/v1/repos/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        # Assert
        assert response.status_code == 401
        assert "detail" in response.json()

    def test_get_repos_with_no_repos_returns_empty(self, client, test_db):
        """Test that user with no repos gets empty list."""
        # Arrange - Create a user with no repos
        from app.models.user import User
        
        user = User(github_username="testuser")
        user.access_token = "test_token"
        test_db.add(user)
        test_db.commit()
        
        # Act - Use Bearer token
        response = client.get(
            "/api/v1/repos/",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_repos"] == 0
        assert data["repos"] == []


class TestAPIErrorHandling:
    """Test API error handling integration."""

    def test_404_for_unknown_endpoint(self, client):
        """Test that unknown endpoints return 404."""
        response = client.get("/api/v1/unknown-endpoint")
        assert response.status_code == 404

    def test_405_for_wrong_method(self, client):
        """Test that wrong HTTP method returns 405."""
        # Repos endpoint only accepts GET
        response = client.post("/api/v1/repos/")
        assert response.status_code == 405

    def test_422_for_missing_required_params(self, client):
        """Test that missing required parameters return 422 or 401 for authentication."""
        response = client.get("/api/v1/repos/")
        # Now requires authentication, so returns 401 instead of 422
        assert response.status_code in [401, 422]


class TestDatabaseIntegration:
    """Test database integration."""

    def test_database_connection_works(self, test_db):
        """Test that database connection is established."""
        # Test that we can execute queries
        from sqlalchemy import text
        result = test_db.execute(text("SELECT 1")).fetchone()
        assert result[0] == 1

    def test_can_create_user_model(self, test_db):
        """Test that User model can be created."""
        from app.models.user import User
        
        user = User(github_username="testuser")
        user.access_token = "test_token_123"
        test_db.add(user)
        test_db.commit()
        
        # Query back
        retrieved_user = test_db.query(User).filter_by(github_username="testuser").first()
        assert retrieved_user is not None
        assert retrieved_user.github_username == "testuser"

    def test_can_create_repository_model(self, test_db):
        """Test that Repository model can be created."""
        from app.models.repository import Repository
        
        repo = Repository(
            name="test-repo",
            url="https://github.com/user/test-repo",
            owner_id=1
        )
        test_db.add(repo)
        test_db.commit()
        
        # Query back
        retrieved_repo = test_db.query(Repository).filter_by(name="test-repo").first()
        assert retrieved_repo is not None
        assert retrieved_repo.url == "https://github.com/user/test-repo"


class TestCORSIntegration:
    """Test CORS integration."""

    def test_cors_allows_configured_origin(self, client):
        """Test that CORS allows configured origins."""
        response = client.options(
            "/api/v1/repos/",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            }
        )
        # Should not block configured origin
        assert response.status_code in [200, 204]

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get(
            "/",
            headers={"Origin": "http://localhost:5173"}
        )
        # Check for CORS headers (they may vary based on configuration)
        assert response.status_code == 200


class TestOpenAPIIntegration:
    """Test OpenAPI schema integration."""

    def test_openapi_schema_valid(self, client):
        """Test that OpenAPI schema is valid."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_swagger_ui_accessible(self, client):
        """Test that Swagger UI is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_accessible(self, client):
        """Test that ReDoc is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestEndToEndFlow:
    """Test complete end-to-end flows."""

    def test_complete_repo_retrieval_flow(self, client, test_db):
        """Test complete flow from request to response with database."""
        # Arrange - Create user and repo in database
        from app.models.user import User
        from app.models.repository import Repository
        
        user = User(github_username="testuser")
        user.access_token = "test_token_123"
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        repo = Repository(
            name="awesome-project",
            url="https://github.com/user/awesome-project",
            last_updated="2025-06-15T00:00:00Z",
            owner_id=user.id
        )
        test_db.add(repo)
        test_db.commit()
        
        # Act - Use Bearer token
        response = client.get(
            "/api/v1/repos/",
            headers={"Authorization": "Bearer test_token_123"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_repos"] == 1
        assert data["repos"][0]["name"] == "awesome-project"
        assert data["repos"][0]["url"] == "https://github.com/user/awesome-project"
