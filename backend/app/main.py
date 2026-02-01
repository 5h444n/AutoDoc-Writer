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
# We explicitly add localhost:3000 (React) and localhost:5173 (Vite/Next.js)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Explicit list is safer for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "AutoDoc API V1 is running"}
