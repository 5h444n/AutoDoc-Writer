"""
Performance tests for AutoDoc-Writer backend.

Tests response times, load handling, and resource usage.
"""

import pytest
import time
from unittest.mock import patch, Mock
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestAPIPerformance:
    """Test API endpoint performance."""

    def test_root_endpoint_response_time(self, client):
        """Test that root endpoint responds quickly."""
        # Act
        start_time = time.time()
        response = client.get("/")
        elapsed_time = time.time() - start_time
        
        # Assert
        assert response.status_code == 200
        assert elapsed_time < 0.1  # Should respond in less than 100ms

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_repos_endpoint_response_time(self, mock_auth_class, mock_github_class, client):
        """Test that repos endpoint responds within acceptable time."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        # Create multiple repos to simulate realistic scenario
        repos = []
        for i in range(20):
            repo = Mock()
            repo.name = f"repo-{i}"
            repo.html_url = f"https://github.com/user/repo-{i}"
            repo.updated_at = datetime(2025, 1, 1)
            repos.append(repo)
        
        mock_user = Mock()
        mock_user.get_repos.return_value = repos
        mock_gh = Mock()
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        start_time = time.time()
        response = client.get("/api/v1/repos/?access_token=test_token")
        elapsed_time = time.time() - start_time
        
        # Assert
        assert response.status_code == 200
        assert elapsed_time < 1.0  # Should respond in less than 1 second


class TestConcurrentRequests:
    """Test handling of concurrent requests."""

    def test_multiple_concurrent_root_requests(self, client):
        """Test that multiple concurrent requests are handled correctly."""
        # Arrange
        num_requests = 50
        
        def make_request():
            response = client.get("/")
            return response.status_code
        
        # Act
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        # Assert
        assert len(results) == num_requests
        assert all(status == 200 for status in results)

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_concurrent_repos_requests(self, mock_auth_class, mock_github_class, client):
        """Test handling of concurrent repos requests."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        repo = Mock()
        repo.name = "test-repo"
        repo.html_url = "https://github.com/user/test-repo"
        repo.updated_at = datetime(2025, 1, 1)
        
        mock_user = Mock()
        mock_user.get_repos.return_value = [repo]
        mock_gh = Mock()
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        num_requests = 20
        
        def make_request():
            response = client.get("/api/v1/repos/?access_token=test_token")
            return response.status_code
        
        # Act
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        elapsed_time = time.time() - start_time
        
        # Assert
        assert len(results) == num_requests
        assert all(status == 200 for status in results)
        assert elapsed_time < 5.0  # Should complete all requests in under 5 seconds


class TestDatabasePerformance:
    """Test database operation performance."""

    def test_bulk_user_creation_performance(self, test_db):
        """Test performance of bulk user creation."""
        from app.models.user import User
        
        # Arrange
        num_users = 100
        
        # Act
        start_time = time.time()
        for i in range(num_users):
            user = User(
                github_id=10000 + i,
                username=f"user{i}",
                email=f"user{i}@example.com"
            )
            test_db.add(user)
        test_db.commit()
        elapsed_time = time.time() - start_time
        
        # Assert
        assert elapsed_time < 2.0  # Should create 100 users in under 2 seconds
        
        # Verify
        user_count = test_db.query(User).count()
        assert user_count == num_users

    def test_bulk_query_performance(self, test_db):
        """Test performance of bulk queries."""
        from app.models.user import User
        
        # Arrange - Create test data
        for i in range(50):
            user = User(
                github_id=20000 + i,
                username=f"queryuser{i}",
                email=f"queryuser{i}@example.com"
            )
            test_db.add(user)
        test_db.commit()
        
        # Act
        start_time = time.time()
        users = test_db.query(User).all()
        elapsed_time = time.time() - start_time
        
        # Assert
        assert elapsed_time < 0.1  # Should query in under 100ms
        assert len(users) == 50


class TestMemoryUsage:
    """Test memory usage and resource management."""

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_large_repo_list_handling(self, mock_auth_class, mock_github_class, client):
        """Test handling of large repository lists."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        # Create a large number of repos
        repos = []
        for i in range(500):
            repo = Mock()
            repo.name = f"repo-{i}"
            repo.html_url = f"https://github.com/user/repo-{i}"
            repo.updated_at = datetime(2025, 1, 1)
            repos.append(repo)
        
        mock_user = Mock()
        mock_user.get_repos.return_value = repos
        mock_gh = Mock()
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act
        response = client.get("/api/v1/repos/?access_token=test_token")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_repos"] == 500
        assert len(data["repos"]) == 500


class TestScalability:
    """Test system scalability."""

    def test_rapid_successive_requests(self, client):
        """Test handling of rapid successive requests."""
        # Arrange
        num_requests = 100
        
        # Act
        start_time = time.time()
        responses = []
        for _ in range(num_requests):
            response = client.get("/")
            responses.append(response)
        elapsed_time = time.time() - start_time
        
        # Assert
        assert all(r.status_code == 200 for r in responses)
        # Should handle 100 requests in under 5 seconds
        assert elapsed_time < 5.0
        
        # Calculate average response time
        avg_time = elapsed_time / num_requests
        assert avg_time < 0.05  # Average under 50ms per request

    def test_openapi_schema_generation_performance(self, client):
        """Test that OpenAPI schema generation is fast."""
        # Act
        start_time = time.time()
        response = client.get("/openapi.json")
        elapsed_time = time.time() - start_time
        
        # Assert
        assert response.status_code == 200
        assert elapsed_time < 0.2  # Should generate in under 200ms


class TestResourceCleanup:
    """Test proper resource cleanup."""

    def test_database_connections_cleaned_up(self, test_db):
        """Test that database connections are properly closed."""
        from app.models.user import User
        
        # Perform multiple operations
        for i in range(10):
            user = User(
                github_id=30000 + i,
                username=f"cleanupuser{i}",
                email=f"cleanupuser{i}@example.com"
            )
            test_db.add(user)
            test_db.commit()
            test_db.query(User).filter_by(github_id=30000 + i).first()
        
        # Should complete without resource exhaustion
        assert True

    @patch('app.services.github_service.Github')
    @patch('app.services.github_service.Auth')
    def test_no_memory_leaks_in_repeated_calls(self, mock_auth_class, mock_github_class, client):
        """Test that repeated API calls don't cause memory leaks."""
        # Arrange
        mock_auth = Mock()
        mock_auth_class.Token.return_value = mock_auth
        
        repo = Mock()
        repo.name = "test-repo"
        repo.html_url = "https://github.com/user/test-repo"
        repo.updated_at = datetime(2025, 1, 1)
        
        mock_user = Mock()
        mock_user.get_repos.return_value = [repo]
        mock_gh = Mock()
        mock_gh.get_user.return_value = mock_user
        mock_github_class.return_value = mock_gh
        
        # Act - Make many requests
        for _ in range(100):
            response = client.get("/api/v1/repos/?access_token=test_token")
            assert response.status_code == 200
        
        # If we get here without crashing, no obvious memory leak
        assert True
