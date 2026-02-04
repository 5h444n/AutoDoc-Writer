from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base

# Create Tables
Base.metadata.create_all(bind=engine)


def _ensure_repo_columns() -> None:
    if not str(engine.url).startswith("sqlite"):
        return
    with engine.begin() as conn:
        columns = {
            row[1] for row in conn.execute(text("PRAGMA table_info(repositories)")).fetchall()
        }
        if not columns:
            return
        if "full_name" not in columns:
            conn.execute(text("ALTER TABLE repositories ADD COLUMN full_name VARCHAR"))
        if "docs_active" not in columns:
            conn.execute(text("ALTER TABLE repositories ADD COLUMN docs_active BOOLEAN DEFAULT 0"))
        if "docs_style" not in columns:
            conn.execute(text("ALTER TABLE repositories ADD COLUMN docs_style VARCHAR DEFAULT 'plainText'"))
        if "docs_complexity" not in columns:
            conn.execute(text("ALTER TABLE repositories ADD COLUMN docs_complexity INTEGER DEFAULT -1"))


_ensure_repo_columns()

app = FastAPI(title=settings.PROJECT_NAME)

# [Roadmap Step 8] Enable CORS for Frontend
# Use configured BACKEND_CORS_ORIGINS (comma-separated list) from settings for flexibility.
origins = getattr(settings, "BACKEND_CORS_ORIGINS", [
    "http://localhost:3000",
    "http://localhost:5173",
])

# If origins are supplied as a comma-separated env string, normalize to list
if isinstance(origins, str):
    origins = [o.strip() for o in origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Backward-compatible auth routes for REDIRECT_URI configs without /api/v1.
from app.api.v1.endpoints import auth as auth_endpoints
app.include_router(auth_endpoints.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "AutoDoc API V1 is running"}
