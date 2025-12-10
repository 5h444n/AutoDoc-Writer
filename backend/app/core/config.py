from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoDoc Writer"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "change_this_in_production"

    # GitHub
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    REDIRECT_URI: str

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./autodoc.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()