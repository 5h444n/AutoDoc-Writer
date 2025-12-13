"""
Shared pytest fixtures for all tests.

This module provides common fixtures used across the test suite including:
- Test database setup
- Mock clients
- Test data factories
- Authentication helpers
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables before importing app
os.environ["GITHUB_CLIENT_ID"] = "test_client_id"
os.environ["GITHUB_CLIENT_SECRET"] = "test_client_secret"
os.environ["REDIRECT_URI"] = "http://localhost:5173/callback"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GEMINI_API_KEY"] = "test_api_key"

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    # Create an in-memory SQLite database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with a test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def mock_github_token():
    """Provide a mock GitHub access token."""
    return "gho_test_token_1234567890"


@pytest.fixture
def mock_github_user():
    """Provide mock GitHub user data."""
    return {
        "login": "testuser",
        "id": 12345,
        "avatar_url": "https://avatars.githubusercontent.com/u/12345",
        "html_url": "https://github.com/testuser",
        "name": "Test User",
        "email": "test@example.com",
    }


@pytest.fixture
def mock_github_repos():
    """Provide mock GitHub repository data."""
    return [
        {
            "name": "test-repo-1",
            "full_name": "testuser/test-repo-1",
            "html_url": "https://github.com/testuser/test-repo-1",
            "description": "Test repository 1",
            "private": False,
            "updated_at": "2025-01-01T00:00:00Z",
        },
        {
            "name": "test-repo-2",
            "full_name": "testuser/test-repo-2",
            "html_url": "https://github.com/testuser/test-repo-2",
            "description": "Test repository 2",
            "private": True,
            "updated_at": "2025-01-02T00:00:00Z",
        },
    ]


@pytest.fixture
def sample_code_python():
    """Provide sample Python code for testing."""
    return '''
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    """Main function."""
    print(fibonacci(10))

if __name__ == "__main__":
    main()
'''


@pytest.fixture
def sample_code_javascript():
    """Provide sample JavaScript code for testing."""
    return '''
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5));
'''
