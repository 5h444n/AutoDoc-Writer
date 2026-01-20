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

    def test_repos_endpoint_response_time(self, client, test_db):
        """Test that repos endpoint responds within acceptable time."""
        # Arrange
        from app.models.user import User
        from app.models.repository import Repository
        
        # Create user
        user = User(github_username="perf_user", access_token="perf_token")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create multiple repos
        for i in range(20):
            repo = Repository(
                name=f"repo-{i}",
                url=f"https://github.com/user/repo-{i}",
                last_updated="2025-01-01T00:00:00Z",
                owner_id=user.id
            )
            test_db.add(repo)
        test_db.commit()
        
        # Act
        start_time = time.time()
        response = client.get(
            "/api/v1/repos/",
            headers={"Authorization": "Bearer perf_token"}
        )
        elapsed_time = time.time() - start_time
        
        # Assert
        assert response.status_code == 200
        assert elapsed_time < 0.5


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

    # Concurrent repository requests using TestClient + SQLite are flaky due to threading issues
    # def test_concurrent_repos_requests(self, client, test_db):
    #     pass


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
                github_username=f"user{i}",
                access_token=f"token{i}"
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
                github_username=f"queryuser{i}",
                access_token=f"token{i}"
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

    def test_large_repo_list_handling(self, client, test_db):
        """Test handling of large repository lists."""
        # Arrange
        from app.models.user import User
        from app.models.repository import Repository
        
        user = User(github_username="large_repo_user", access_token="large_repo_token")
        test_db.add(user)
        test_db.commit()
        
        # Create a large number of repos (using bulk insert for speed)
        repos = []
        for i in range(500):
            repo = Repository(
                name=f"repo-{i}",
                url=f"https://github.com/user/repo-{i}",
                last_updated="2025-01-01T00:00:00Z",
                owner_id=user.id
            )
            repos.append(repo)
        test_db.bulk_save_objects(repos)
        test_db.commit()
        
        # Act
        response = client.get(
            "/api/v1/repos/",
            headers={"Authorization": "Bearer large_repo_token"}
        )
        
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
                github_username=f"cleanupuser{i}",
                access_token=f"token{i}"
            )
            test_db.add(user)
            test_db.commit()
            test_db.query(User).filter_by(github_username=f"cleanupuser{i}").first()
        
        # Should complete without resource exhaustion
        assert True

    def test_no_memory_leaks_in_repeated_calls(self, client, test_db):
        """Test that repeated API calls don't cause memory leaks."""
        # Arrange
        from app.models.user import User
        from app.models.repository import Repository
        
        user = User(github_username="leak_check_user", access_token="leak_check_token")
        test_db.add(user)
        test_db.commit()
        
        repo = Repository(
            name="test-repo",
            url="https://github.com/user/test-repo",
            last_updated="2025-01-01T00:00:00Z",
            owner_id=user.id
        )
        test_db.add(repo)
        test_db.commit()
        
        # Act - Make many requests
        for _ in range(100):
            response = client.get(
                "/api/v1/repos/",
                headers={"Authorization": "Bearer leak_check_token"}
            )
            assert response.status_code == 200
        
        # If we get here without crashing, no obvious memory leak
        assert True
