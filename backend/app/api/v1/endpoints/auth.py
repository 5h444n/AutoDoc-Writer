from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "Ov23liarD6NyPCrJjvMG")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "7dfe8c4d77365e903696d9cbbe21bfe64befeddf")

@router.get("/login")
def login():
    """
    Redirects the user to GitHub's OAuth login page.
    """
    return RedirectResponse(url=f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=repo")

@router.get("/callback")
async def callback(code: str):
    """
    Exchanges code for token and redirects to frontend.
    """
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            json={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code
            }
        )
        data = response.json()
        access_token = data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token from GitHub")

        # Redirect to frontend with token
        return RedirectResponse(url=f"http://localhost:5173?github_token={access_token}")

@router.get("/github/repos")
async def get_github_repos(authorization: str = None):
    """
    Fetches the user's repositories from GitHub.
    Accepts 'Authorization: Bearer <token>' header.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.split(" ")[1]
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos?sort=updated&per_page=100&type=all",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch repositories from GitHub")
            
        return response.json()