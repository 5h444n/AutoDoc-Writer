"""
Unit tests for configuration module.

Tests configuration loading, validation, and defaults.
"""

import os
import pytest
from app.core.config import settings


def test_settings_loaded():
    """Test that settings are loaded successfully."""
    assert settings is not None


def test_project_name():
    """Test that project name is set correctly."""
    assert settings.PROJECT_NAME == "AutoDoc Writer"


def test_api_v1_prefix():
    """Test that API v1 prefix is set correctly."""
    assert settings.API_V1_STR == "/api/v1"


def test_github_client_id_loaded():
    """Test that GitHub client ID is loaded from environment."""
    assert settings.GITHUB_CLIENT_ID == "test_client_id"


def test_github_client_secret_loaded():
    """Test that GitHub client secret is loaded from environment."""
    assert settings.GITHUB_CLIENT_SECRET == "test_client_secret"


def test_redirect_uri_loaded():
    """Test that redirect URI is loaded from environment."""
    assert settings.REDIRECT_URI == "http://localhost:5173/callback"


def test_frontend_url_default():
    """Test that frontend URL has a default value."""
    assert settings.FRONTEND_URL == "http://localhost:5173"


def test_database_url_has_default():
    """Test that database URL has a default value."""
    # In test environment, should be in-memory
    assert settings.DATABASE_URL is not None


def test_secret_key_exists():
    """Test that secret key exists (even if default)."""
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 0


def test_env_is_development():
    """Test that ENV setting defaults to development."""
    assert settings.ENV == "development"


def test_cors_origins_configured():
    """Test that CORS origins are configured."""
    assert isinstance(settings.BACKEND_CORS_ORIGINS, list)
    assert len(settings.BACKEND_CORS_ORIGINS) > 0
    assert "http://localhost:5173" in settings.BACKEND_CORS_ORIGINS


def test_gemini_api_key_loaded():
    """Test that Gemini API key is loaded."""
    # In test environment, should have test value
    assert settings.GEMINI_API_KEY == "test_api_key"


def test_settings_immutable():
    """Test that settings are immutable (Pydantic model)."""
    with pytest.raises(Exception):
        settings.PROJECT_NAME = "Changed"


def test_settings_case_sensitive():
    """Test that settings are case-sensitive."""
    # The Config class should have case_sensitive = True
    assert settings.Config.case_sensitive is True
