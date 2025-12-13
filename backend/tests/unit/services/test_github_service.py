"""
Unit tests for GitHub service.

Tests GitHub API integration, error handling, and data transformation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from app.services.github_service import GitHubService
from github.GithubException import GithubException


@pytest.fixture
def mock_github_instance():
    """Create a mock GitHub instance."""
    mock_gh = Mock()
    mock_user = Mock()
    mock_gh.get_user.return_value = mock_user
    return mock_gh, mock_user


@pytest.fixture
def mock_repo():
    """Create a mock repository."""
    repo = Mock()
    repo.name = "test-repo"
    repo.html_url = "https://github.com/user/test-repo"
    repo.updated_at = datetime(2025, 1, 1, 0, 0, 0)
    return repo


class TestGitHubServiceGetUserRepos:
    """Tests for GitHubService.get_user_repos method."""

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_success(self, mock_auth_class, mock_github_class, mock_repo):
        """Test successful retrieval of user repositories."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        mock_gh = Mock()
        mock_user = Mock()
        mock_user.get_repos.return_value = [mock_repo]
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert len(result) == 1
        assert result[0].name == "test-repo"
        assert result[0].url == "https://github.com/user/test-repo"
        mock_auth_class.Token.assert_called_once_with("test_token")
        mock_github_class.assert_called_once_with(auth=mock_auth)

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_empty_list(self, mock_auth_class, mock_github_class):
        """Test retrieval when user has no repositories."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        mock_gh = Mock()
        mock_user = Mock()
        mock_user.get_repos.return_value = []
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert result == []

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_multiple_repos(self, mock_auth_class, mock_github_class):
        """Test retrieval of multiple repositories."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        repos = []
        for i in range(5):
            repo = Mock()
            repo.name = f"repo-{i}"
            repo.html_url = f"https://github.com/user/repo-{i}"
            repo.updated_at = datetime(2025, 1, i + 1, 0, 0, 0)
            repos.append(repo)
        
        mock_gh = Mock()
        mock_user = Mock()
        mock_user.get_repos.return_value = repos
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert len(result) == 5
        assert all(repo.name.startswith("repo-") for repo in result)

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_github_exception(self, mock_auth_class, mock_github_class):
        """Test handling of GitHub API exceptions."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        mock_gh = Mock()
        github_error = GithubException(401, {"message": "Bad credentials"})
        mock_gh.get_user.side_effect = github_error
        mock_github_class.return_value = mock_gh
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            GitHubService.get_user_repos("invalid_token")
        
        assert "GitHub API error" in str(exc_info.value)

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_network_error(self, mock_auth_class, mock_github_class):
        """Test handling of network errors."""
        # Arrange
        import requests
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        mock_gh = Mock()
        mock_gh.get_user.side_effect = requests.exceptions.ConnectionError("Network error")
        mock_github_class.return_value = mock_gh
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            GitHubService.get_user_repos("test_token")
        
        assert "Network error" in str(exc_info.value)

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_unexpected_error(self, mock_auth_class, mock_github_class):
        """Test handling of unexpected errors."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        mock_gh = Mock()
        mock_gh.get_user.side_effect = ValueError("Unexpected error")
        mock_github_class.return_value = mock_gh
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            GitHubService.get_user_repos("test_token")
        
        assert "Unexpected error" in str(exc_info.value)

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_creates_correct_auth(self, mock_auth_class, mock_github_class):
        """Test that Auth.Token is called with the correct token."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        mock_gh = Mock()
        mock_user = Mock()
        mock_user.get_repos.return_value = []
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        GitHubService.get_user_repos("my_secret_token")
        
        # Assert
        mock_auth_class.Token.assert_called_once_with("my_secret_token")

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_get_user_repos_data_transformation(self, mock_auth_class, mock_github_class):
        """Test that repository data is correctly transformed."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        repo = Mock()
        repo.name = "my-awesome-repo"
        repo.html_url = "https://github.com/user/my-awesome-repo"
        repo.updated_at = datetime(2025, 6, 15, 14, 30, 0)
        
        mock_gh = Mock()
        mock_user = Mock()
        mock_user.get_repos.return_value = [repo]
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        result = GitHubService.get_user_repos("test_token")
        
        # Assert
        assert result[0].name == "my-awesome-repo"
        assert result[0].url == "https://github.com/user/my-awesome-repo"
        assert result[0].last_updated == "2025-06-15T14:30:00"
