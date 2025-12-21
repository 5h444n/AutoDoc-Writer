import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoDoc Writer"
    API_V1_STR: str = "/api/v1"

    # --- Environment & AI ---
    # We add these here so Pydantic doesn't complain about "Extra inputs"
    ENV: str = "development"
    GEMINI_API_KEY: Optional[str] = None

    # --- Security ---
    SECRET_KEY: str = "change_this_in_production"

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

    class Config:
        # 1. Get the directory of THIS file (backend/app/core/config.py)
        _current_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. Go up 3 levels to get to the project root (AutoDoc-Writer/)
        _root_dir = os.path.join(_current_dir, "..", "..", "..")

        # 3. Point to the .env file in the root
        env_file = os.path.join(_root_dir, ".env")
        env_file_encoding = "utf-8"

        # Ensure variable names match exactly (e.g., GITHUB_CLIENT_ID, not github_client_id)
        case_sensitive = True

settings = Settings()