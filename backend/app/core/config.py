import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoDoc Writer"
    API_V1_STR: str = "/api/v1"

    # --- Environment & AI ---
    # We add these here so Pydantic doesn't complain about "Extra inputs"
    ENV: str = "development"
    GEMINI_API_KEY: Optional[str] = None

    # --- Security ---
    SECRET_KEY: str  # Required - no default value for security

    # --- GitHub URLs -----------------ADDED THIS PART TANIM
    GITHUB_AUTH_URL: str = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL: str = "https://github.com/login/oauth/access_token"

    # --- GitHub OAuth ---
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    REDIRECT_URI: str

    # --- CORS (Frontend Connection) ---
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./autodoc.db"

    # Pydantic v2 configuration
    model_config = ConfigDict(
        # 1. Get the directory of THIS file (backend/app/core/config.py)
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env"
        ),
        env_file_encoding="utf-8",
        # Ensure variable names match exactly (e.g., GITHUB_CLIENT_ID, not github_client_id)
        case_sensitive=True,
        # Make settings immutable
        frozen=True,
    )

settings = Settings()