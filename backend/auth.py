import os
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a router instead of an app
router = APIRouter()

# --- Configuration ---
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

@router.get("/login")
async def login():
    """
    Redirects the user to the GitHub OAuth authorization page.
    """
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Server configuration error: Missing GitHub credentials in .env file.")

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "scope": "repo read:user",
        "redirect_uri": "http://localhost:8000/callback"
    }
    
    auth_url = f"{GITHUB_AUTH_URL}?client_id={params['client_id']}&scope={params['scope']}&redirect_uri={params['redirect_uri']}"
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def callback(code: str):
    """
    Handles the callback from GitHub, exchanges the code for an access token.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found.")

    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8000/callback"
    }

    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(GITHUB_TOKEN_URL, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.RequestError as exc:
             raise HTTPException(status_code=500, detail=f"Failed to communicate with GitHub: {exc}")

    data = response.json()
    
    if "error" in data:
        raise HTTPException(status_code=400, detail=f"GitHub Error: {data.get('error_description')}")

    return {
        "access_token": data.get("access_token"),
        "token_type": data.get("token_type"),
        "scope": data.get("scope"),
        "message": "Successfully logged in via GitHub!"
    }