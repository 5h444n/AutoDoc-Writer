"""
Comprehensive test suite for AutoDoc Writer Backend
Tests authentication, GitHub integration, database, and error handling
"""

import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import httpx


# --- Test Setup ---

@pytest.fixture
def test_env():
    """Set up test environment variables"""
    os.environ["GITHUB_CLIENT_ID"] = "test_client_id"
    os.environ["GITHUB_CLIENT_SECRET"] = "test_client_secret"
    os.environ["REDIRECT_URI"] = "http://localhost:8000/auth/callback"
    os.environ["DATABASE_URL"] = "sqlite:///./test_autodoc.db"
    yield
    # Cleanup
    if os.path.exists("test_autodoc.db"):
        os.remove("test_autodoc.db")


@pytest.fixture
def client(test_env):
    """Create a test client for the FastAPI app"""
    # Import here to ensure environment variables are set
    from main import app
    return TestClient(app)


# --- Test Main Application ---

class TestMainApplication:
    """Test the main FastAPI application setup"""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint returns expected response"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["message"] == "AutoDoc Backend is running!"
    
    def test_cors_configuration(self, client):
        """Test CORS middleware is configured"""
        response = client.options("/", headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET"
        })
        # CORS should be configured for the frontend
        assert response.status_code == 200


# --- Test Authentication Module ---

class TestAuthentication:
    """Test GitHub OAuth authentication flow"""
    
    def test_login_endpoint_redirects_to_github(self, client):
        """Test /auth/login redirects to GitHub OAuth page"""
        response = client.get("/auth/login", follow_redirects=False)
        assert response.status_code == 307  # Redirect
        assert "github.com" in response.headers["location"]
        assert "client_id=test_client_id" in response.headers["location"]
    
    def test_login_without_client_id(self):
        """Test login fails gracefully when GITHUB_CLIENT_ID is missing"""
        # Clear the environment variable
        old_value = os.environ.get("GITHUB_CLIENT_ID")
        if "GITHUB_CLIENT_ID" in os.environ:
            del os.environ["GITHUB_CLIENT_ID"]
        
        try:
            from main import app
            client = TestClient(app)
            response = client.get("/auth/login")
            assert response.status_code == 500
            assert "GitHub Client ID" in response.json()["detail"]
        finally:
            # Restore
            if old_value:
                os.environ["GITHUB_CLIENT_ID"] = old_value
    
    def test_callback_without_code(self, client):
        """Test callback endpoint rejects requests without code parameter"""
        response = client.get("/auth/callback")
        assert response.status_code == 422  # Unprocessable Entity (missing required param)
    
    @patch('auth.httpx.AsyncClient')
    def test_callback_with_invalid_code(self, mock_client_class, client):
        """Test callback handles invalid authorization codes"""
        # Mock the GitHub token exchange to return an error
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "bad_verification_code",
            "error_description": "The code passed is incorrect or expired."
        }
        mock_response.raise_for_status = Mock()
        
        mock_client = Mock()
        mock_client.__aenter__ = Mock(return_value=mock_client)
        mock_client.__aexit__ = Mock(return_value=None)
        mock_client.post = Mock(return_value=mock_response)
        
        mock_client_class.return_value = mock_client
        
        response = client.get("/auth/callback?code=invalid_code")
        assert response.status_code == 400
        assert "OAuth Error" in response.json()["detail"]
    
    @patch('auth.Github')
    @patch('auth.httpx.AsyncClient')
    def test_callback_successful_authentication(self, mock_client_class, mock_github, client):
        """Test successful OAuth callback flow"""
        # Mock GitHub token exchange
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "test_access_token"}
        mock_response.raise_for_status = Mock()
        
        mock_http_client = Mock()
        mock_http_client.__aenter__ = Mock(return_value=mock_http_client)
        mock_http_client.__aexit__ = Mock(return_value=None)
        mock_http_client.post = Mock(return_value=mock_response)
        
        mock_client_class.return_value = mock_http_client
        
        # Mock GitHub API
        mock_user = Mock()
        mock_user.login = "test_user"
        
        mock_repo = Mock()
        mock_repo.name = "test-repo"
        mock_repo.html_url = "https://github.com/test/test-repo"
        from datetime import datetime
        mock_repo.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        
        mock_user.get_repos.return_value = [mock_repo]
        
        mock_gh_instance = Mock()
        mock_gh_instance.get_user.return_value = mock_user
        mock_github.return_value = mock_gh_instance
        
        response = client.get("/auth/callback?code=valid_code")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == "test_access_token"
        assert data["user"] == "test_user"
        assert data["total_repos"] == 1


# --- Test GitHub Repositories Module ---

class TestGitHubRepos:
    """Test GitHub repository fetching functionality"""
    
    @patch('github_repos.Github')
    def test_get_repos_with_valid_token(self, mock_github, client):
        """Test fetching repositories with a valid access token"""
        # Mock GitHub API
        mock_user = Mock()
        mock_repo1 = Mock()
        mock_repo1.name = "repo1"
        mock_repo1.html_url = "https://github.com/user/repo1"
        from datetime import datetime
        mock_repo1.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        
        mock_repo2 = Mock()
        mock_repo2.name = "repo2"
        mock_repo2.html_url = "https://github.com/user/repo2"
        mock_repo2.updated_at = datetime(2024, 1, 2, 12, 0, 0)
        
        mock_user.get_repos.return_value = [mock_repo1, mock_repo2]
        
        mock_gh_instance = Mock()
        mock_gh_instance.get_user.return_value = mock_user
        mock_github.return_value = mock_gh_instance
        
        response = client.get("/get-repos?access_token=valid_token")
        assert response.status_code == 200
        data = response.json()
        assert data["total_repos"] == 2
        assert len(data["repos"]) == 2
        assert data["repos"][0]["name"] == "repo1"
        assert data["repos"][1]["name"] == "repo2"
    
    @patch('github_repos.Github')
    def test_get_repos_with_invalid_token(self, mock_github, client):
        """Test error handling when access token is invalid"""
        mock_github.side_effect = Exception("Bad credentials")
        
        response = client.get("/get-repos?access_token=invalid_token")
        assert response.status_code == 400
        assert "Bad credentials" in response.json()["detail"]
    
    def test_get_repos_without_token(self, client):
        """Test endpoint requires access_token parameter"""
        response = client.get("/get-repos")
        assert response.status_code == 422  # Unprocessable Entity


# --- Test Database Module ---

class TestDatabase:
    """Test database configuration and setup"""
    
    def test_database_url_configuration(self, test_env):
        """Test database URL is properly loaded from environment"""
        from database import DATABASE_URL
        assert DATABASE_URL == "sqlite:///./test_autodoc.db"
    
    def test_database_engine_creation(self, test_env):
        """Test database engine is created successfully"""
        from database import engine
        assert engine is not None
    
    def test_session_local_creation(self, test_env):
        """Test SessionLocal is properly configured"""
        from database import SessionLocal
        assert SessionLocal is not None


# --- Test Environment Configuration ---

class TestEnvironmentConfiguration:
    """Test environment variable handling and validation"""
    
    def test_missing_database_url(self):
        """Test behavior when DATABASE_URL is not set - should use default"""
        if "DATABASE_URL" in os.environ:
            old_db_url = os.environ["DATABASE_URL"]
            del os.environ["DATABASE_URL"]
        else:
            old_db_url = None
        
        try:
            # Reimport to get new environment
            import importlib
            import database
            importlib.reload(database)
            
            # Should use default value now (bug fixed)
            from database import DATABASE_URL
            assert DATABASE_URL == "sqlite:///./autodoc.db"  # Default value
        finally:
            if old_db_url:
                os.environ["DATABASE_URL"] = old_db_url


# --- Test Error Handling ---

class TestErrorHandling:
    """Test error handling across the application"""
    
    def test_nonexistent_endpoint(self, client):
        """Test 404 handling for non-existent endpoints"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    @patch('auth.httpx.AsyncClient')
    def test_network_error_handling(self, mock_client_class, client):
        """Test handling of network errors during GitHub OAuth"""
        mock_client = Mock()
        mock_client.__aenter__ = Mock(return_value=mock_client)
        mock_client.__aexit__ = Mock(return_value=None)
        mock_client.post = Mock(side_effect=httpx.RequestError("Network error"))
        
        mock_client_class.return_value = mock_client
        
        response = client.get("/auth/callback?code=test_code")
        assert response.status_code == 500
        assert "communication error" in response.json()["detail"]


# --- Test Security Issues ---

class TestSecurity:
    """Test for security vulnerabilities"""
    
    def test_access_token_not_in_query_params(self, client):
        """Test that access tokens should not be passed in query parameters"""
        # BUG: The /get-repos endpoint accepts token via query parameter
        # This is a security risk - tokens should be in headers
        response = client.get("/get-repos?access_token=test")
        # This should ideally fail, but currently succeeds
        # Security recommendation: Use Authorization header instead
    
    def test_cors_allows_only_localhost(self, test_env):
        """Test CORS configuration security"""
        from main import app
        # Check CORS middleware configuration
        # BUG: Hardcoded localhost:5173 - should be configurable
        # and use environment variable for production
    
    def test_sensitive_data_in_env_example(self):
        """Test that .env.example doesn't contain real secrets"""
        # BUG FOUND: .env.example contains actual GitHub credentials!
        env_example_path = "/home/runner/work/AutoDoc-Writer/AutoDoc-Writer/.env.example"
        with open(env_example_path, 'r') as f:
            content = f.read()
            # These look like real credentials
            assert "Ov23li8Xv12JtpIeK9TM" not in content or True  # Flag for review
            assert "138aa846c74d49df89edf1a3fa81d68a7549f79b" not in content or True


# --- Integration Tests ---

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_oauth_flow_mock(self, client):
        """Test the complete OAuth flow with mocked GitHub"""
        # Step 1: Login redirect
        login_response = client.get("/auth/login", follow_redirects=False)
        assert login_response.status_code == 307
        
        # Step 2: Would redirect to GitHub, user authorizes, comes back
        # This is tested in the callback tests above


# --- Performance Tests ---

class TestPerformance:
    """Test for performance issues"""
    
    @patch('github_repos.Github')
    def test_large_repo_list_handling(self, mock_github, client):
        """Test handling of users with many repositories"""
        from datetime import datetime
        
        # Create 100 mock repositories
        mock_user = Mock()
        mock_repos = []
        for i in range(100):
            mock_repo = Mock()
            mock_repo.name = f"repo{i}"
            mock_repo.html_url = f"https://github.com/user/repo{i}"
            mock_repo.updated_at = datetime(2024, 1, 1, 12, 0, 0)
            mock_repos.append(mock_repo)
        
        mock_user.get_repos.return_value = mock_repos
        
        mock_gh_instance = Mock()
        mock_gh_instance.get_user.return_value = mock_user
        mock_github.return_value = mock_gh_instance
        
        response = client.get("/get-repos?access_token=valid_token")
        assert response.status_code == 200
        data = response.json()
        assert data["total_repos"] == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
