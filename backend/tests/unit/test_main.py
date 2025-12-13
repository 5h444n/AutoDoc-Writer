"""
Unit tests for the main application module.

Tests the FastAPI application initialization, middleware configuration,
and root endpoint.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_app_is_fastapi_instance(client):
    """Test that the app is a FastAPI instance."""
    from app.main import app
    assert isinstance(app, FastAPI)


def test_app_has_correct_title(client):
    """Test that the app has the correct title."""
    from app.main import app
    assert app.title == "AutoDoc Writer"


def test_root_endpoint_returns_success(client):
    """Test that the root endpoint returns a success message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "AutoDoc API" in response.json()["message"]


def test_cors_middleware_configured(client):
    """Test that CORS middleware is properly configured."""
    # Make a preflight request
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    # CORS should allow the origin
    assert response.status_code in [200, 204]


def test_api_v1_prefix_configured(client):
    """Test that API v1 prefix is configured."""
    # Try to access a v1 endpoint (repos should exist)
    response = client.get("/api/v1/repos/")
    # Should not return 404 for the base path structure
    assert response.status_code != 404 or "not found" not in response.text.lower()


def test_database_tables_created(test_db):
    """Test that database tables are created on startup."""
    from app.db.base import Base
    # Check that tables exist
    assert len(Base.metadata.tables) > 0


def test_health_check_endpoint(client):
    """Test that the application responds to basic health check."""
    response = client.get("/")
    assert response.status_code == 200


def test_openapi_docs_available(client):
    """Test that OpenAPI documentation is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    assert "openapi" in openapi_spec
    assert "info" in openapi_spec
