from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# [Roadmap Step 8] Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "AutoDoc API V1 is running"}

@app.get("/api/v1/github/repos")
async def get_github_repos(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    token = authorization.replace("Bearer ", "")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.github.com/user/repos?sort=updated&per_page=100&type=all",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
        )
        
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch from GitHub")
        
        repos = resp.json()
        
        # Transform for Frontend
        clean_repos = []
        for r in repos:
            clean_repos.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "html_url": r.get("html_url"),
                "description": r.get("description"),
                "language": r.get("language"),
                "size": r.get("size", 0),
                "open_issues_count": r.get("open_issues_count", 0),
                "updated_at": r.get("updated_at")
            })
        return clean_repos

@app.get("/api/v1/github/user")
async def get_github_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Token")
    token = authorization.replace("Bearer ", "")
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.github.com/user", headers={"Authorization": f"Bearer {token}"})
        return resp.json()