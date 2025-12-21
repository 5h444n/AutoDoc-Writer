"""
Unit tests for GitHub service.

Tests GitHub API integration, error handling, and data transformation.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.services.github_service import GitHubService


class TestGitHubServiceGetUserRepos:
    """Tests for GitHubService.get_user_repos method."""

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_success(self, mock_get):
        """Test successful retrieval of user repositories."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "name": "test-repo",
                "html_url": "https://github.com/user/test-repo",
                "updated_at": "2025-01-01T00:00:00Z"
            }
        ]
        mock_get.return_value = mock_response
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert len(result) == 1
        assert result[0]["name"] == "test-repo"
        assert result[0]["url"] == "https://github.com/user/test-repo"
        mock_get.assert_called()

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_empty_list(self, mock_get):
        """Test retrieval when user has no repositories."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert result == []

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_multiple_repos(self, mock_get):
        """Test retrieval of multiple repositories."""
        # Arrange
        repos_data = [
            {
                "name": f"repo-{i}",
                "html_url": f"https://github.com/user/repo-{i}",
                "updated_at": f"2025-01-0{i+1}T00:00:00Z"
            }
            for i in range(5)
        ]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = repos_data
        mock_get.return_value = mock_response
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert len(result) == 5
        assert all(repo["name"].startswith("repo-") for repo in result)

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_github_exception(self, mock_get):
        """Test handling of GitHub API exceptions."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Bad credentials"}
        mock_get.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(Exception):
            GitHubService.get_user_repos("invalid_token")

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_network_error(self, mock_get):
        """Test handling of network errors."""
        # Arrange
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        # Act & Assert
        with pytest.raises(Exception):
            GitHubService.get_user_repos("test_token")

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_unexpected_error(self, mock_get):
        """Test handling of unexpected errors."""
        # Arrange
        mock_get.side_effect = ValueError("Unexpected error")
        
        # Act & Assert
        with pytest.raises(Exception):
            GitHubService.get_user_repos("test_token")

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_creates_correct_auth(self, mock_get):
        """Test that Authorization header is set with the correct token."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Act
        GitHubService.get_user_repos("my_secret_token")
        
        # Assert
        call_kwargs = mock_get.call_args[1]
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["Authorization"] == "Bearer my_secret_token"

    @patch('app.services.github_service.requests.get')
    def test_get_user_repos_data_transformation(self, mock_get):
        """Test that repository data is correctly transformed."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "name": "my-awesome-repo",
                "html_url": "https://github.com/user/my-awesome-repo",
                "updated_at": "2025-06-15T14:30:00Z"
            }
        ]
        mock_get.return_value = mock_response
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert result[0]["name"] == "my-awesome-repo"
        assert result[0]["url"] == "https://github.com/user/my-awesome-repo"
        assert result[0]["last_updated"] == "2025-06-15T14:30:00Z"
