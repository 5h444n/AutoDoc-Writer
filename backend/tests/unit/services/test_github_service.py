"""
Unit tests for GitHub service.

Tests GitHub API integration, error handling, and data transformation.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from fastapi import HTTPException
from app.services.github_service import GitHubService


class TestGitHubServiceGetUserRepos:
    """Tests for GitHubService.get_user_repos method."""

    def test_get_user_repos_success(self):
        """Test successful retrieval of user repositories."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            # Mock the paginated response
            mock_response_1 = Mock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = [{
                "name": "test-repo",
                "html_url": "https://github.com/user/test-repo",
                "updated_at": "2025-01-01T00:00:00Z"
            }]
            
            # The second call will return an empty list to stop pagination loop
            mock_response_2 = Mock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = []
            
            mock_get.side_effect = [mock_response_1, mock_response_2]
            
            # Act
            result = GitHubService.get_user_repos("test_token")
            
            # Assert
            assert len(result) == 1
            assert result[0]["name"] == "test-repo"
            assert result[0]["url"] == "https://github.com/user/test-repo"
            assert result[0]["last_updated"] == "2025-01-01T00:00:00Z"

    def test_get_user_repos_empty_list(self):
        """Test retrieval when user has no repositories."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            
            mock_get.return_value = mock_response
            
            # Act
            result = GitHubService.get_user_repos("test_token")
            
            # Assert
            assert result == []

    def test_get_user_repos_multiple_repos(self):
        """Test retrieval of multiple repositories."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            repos = []
            for i in range(5):
                repos.append({
                    "name": f"repo-{i}",
                    "html_url": f"https://github.com/user/repo-{i}",
                    "updated_at": f"2025-01-0{i+1}T00:00:00Z"
                })
            
            mock_response_1 = Mock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = repos
            
            # Stop pagination
            mock_response_2 = Mock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = []
            
            mock_get.side_effect = [mock_response_1, mock_response_2]
            
            # Act
            result = GitHubService.get_user_repos("test_token")
            
            # Assert
            assert len(result) == 5
            assert all(repo["name"].startswith("repo-") for repo in result)

    def test_get_user_repos_github_exception(self):
        """Test handling of GitHub API exceptions."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response
            
            # Act & Assert
            with pytest.raises(HTTPException):
                GitHubService.get_user_repos("invalid_token")

    def test_get_user_repos_network_error(self):
        """Test handling of network errors."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            import requests
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
            
            # Act & Assert
            with pytest.raises(requests.exceptions.ConnectionError):
               GitHubService.get_user_repos("test_token")

    def test_get_user_repos_unexpected_error(self):
        """Test handling of unexpected errors."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            mock_get.side_effect = ValueError("Unexpected error")
            
            # Act & Assert
            with pytest.raises(ValueError):
                GitHubService.get_user_repos("test_token")

    def test_get_user_repos_creates_correct_auth(self):
        """Test that requests.get is called with the correct token."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_get.return_value = mock_response
            # Act
            GitHubService.get_user_repos("my_secret_token")
            # Assert
            args, kwargs = mock_get.call_args
            assert kwargs['headers']['Authorization'] == "Bearer my_secret_token"

    def test_get_user_repos_data_transformation(self):
        """Test that repository data is correctly transformed."""
        # Arrange
        with patch('app.services.github_service.requests.get') as mock_get:
            mock_response_1 = Mock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = [{
                "name": "my-awesome-repo",
                "html_url": "https://github.com/user/my-awesome-repo",
                "updated_at": "2025-06-15T14:30:00"
            }]
            mock_response_2 = Mock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = []
            mock_get.side_effect = [mock_response_1, mock_response_2]
            
            # Act
            result = GitHubService.get_user_repos("test_token")
            
            # Assert
            assert result[0]["name"] == "my-awesome-repo"
            assert result[0]["url"] == "https://github.com/user/my-awesome-repo"
            assert result[0]["last_updated"] == "2025-06-15T14:30:00"
