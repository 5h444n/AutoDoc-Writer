"""
Unit tests for GitHub service.

Tests GitHub API integration, error handling, and data transformation.
"""

import pytest
from unittest.mock import Mock, patch
import base64
import requests
from fastapi import HTTPException
from app.services.github_service import GitHubService


class TestGitHubService:
    """Tests for GitHubService methods."""

    def test_get_user_repos_success(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response_1 = Mock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = [{
                "name": "test-repo",
                "html_url": "https://github.com/user/test-repo",
                "updated_at": "2025-01-01T00:00:00Z"
            }]

            mock_response_2 = Mock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = []

            mock_req.side_effect = [mock_response_1, mock_response_2]

            result = GitHubService.get_user_repos("test_token")

            assert len(result) == 1
            assert result[0]["name"] == "test-repo"

    def test_get_user_repos_empty_list(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_req.return_value = mock_response

            result = GitHubService.get_user_repos("test_token")
            assert result == []

    def test_get_user_repos_multiple_repos(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            repos = [{
                "name": f"repo-{i}",
                "html_url": f"https://github.com/user/repo-{i}",
                "updated_at": f"2025-01-0{i+1}T00:00:00Z"
            } for i in range(5)]

            mock_response_1 = Mock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = repos

            mock_response_2 = Mock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = []

            mock_req.side_effect = [mock_response_1, mock_response_2]

            result = GitHubService.get_user_repos("test_token")
            assert len(result) == 5

    def test_get_user_repos_github_exception(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_req.return_value = mock_response

            with pytest.raises(HTTPException):
                GitHubService.get_user_repos("invalid_token")

    def test_get_user_repos_network_error(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_req.side_effect = requests.exceptions.ConnectionError("Network error")

            with pytest.raises(HTTPException):
                GitHubService.get_user_repos("test_token")

    def test_get_user_repos_unexpected_error(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_req.side_effect = ValueError("Unexpected error")

            with pytest.raises(ValueError):
                GitHubService.get_user_repos("test_token")

    def test_get_user_repos_creates_correct_auth(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_req.return_value = mock_response

            GitHubService.get_user_repos("my_secret_token")
            args, kwargs = mock_req.call_args
            assert kwargs['headers']['Authorization'] == "Bearer my_secret_token"

    def test_get_user_repos_data_transformation(self):
        with patch('app.services.github_service.requests.request') as mock_req:
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
            mock_req.side_effect = [mock_response_1, mock_response_2]

            result = GitHubService.get_user_repos("test_token")
            assert result[0]["name"] == "my-awesome-repo"

    def test_exchange_code_for_token_success(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"access_token": "abc123"}
            mock_req.return_value = mock_response

            token = GitHubService.exchange_code_for_token("code123")
            assert token == "abc123"

    def test_exchange_code_for_token_error(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {"error": "bad", "error_description": "desc"}
            mock_req.return_value = mock_response

            with pytest.raises(HTTPException):
                GitHubService.exchange_code_for_token("code123")

    def test_get_repo_commit_count_with_link(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"Link": "<https://api.github.com/?page=5>; rel=\"last\""}       
            mock_response.json.return_value = [1]
            mock_req.return_value = mock_response

            count = GitHubService.get_repo_commit_count("token", "owner/repo")
            assert count == 5

    def test_get_repo_commit_count_no_link(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {}
            mock_response.json.return_value = [1,2,3]
            mock_req.return_value = mock_response

            count = GitHubService.get_repo_commit_count("token", "owner/repo")
            assert count == 3

    def test_get_file_content_base64(self):
        with patch('app.services.github_service.requests.request') as mock_req:
            b64 = base64.b64encode(b"hello").decode()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"content": b64, "encoding": "base64", "sha": "abc"}   
            mock_req.return_value = mock_response

            content, sha = GitHubService.get_file_content("token", "owner/repo", "README.md")        
            assert content.strip() == "hello"
            assert sha == "abc"
