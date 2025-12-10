import os
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from github import Github

# Load environment variables from .env
load_dotenv()

router = APIRouter()

# Environment configuration
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"


@router.get("/login")
async def login():
    """
    Redirects the user to GitHub OAuth authorization page.
    """
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Missing GitHub Client ID")

    auth_url = (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=repo read:user"
    )

    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def callback(code: str):
    """
    GitHub OAuth callback - exchanges code for access token and fetches repos.
    """
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    # Exchange code for access token
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(GITHUB_TOKEN_URL, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"GitHub communication error: {exc}")

    token_data = response.json()

    if "error" in token_data:
        raise HTTPException(
            status_code=400,
            detail=f"GitHub OAuth Error: {token_data.get('error_description')}",
        )

    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token received from GitHub")

    # --- Fetch GitHub Repos ---
    try:
        gh = Github(access_token)
        user = gh.get_user()
        repos = user.get_repos()

        repo_list = [{
            "name": repo.name,
            "url": repo.html_url,
            "last_updated": repo.updated_at.isoformat()
        } for repo in repos]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repositories: {e}")

    return {
        "message": "Successfully authenticated and fetched repositories!",
        "access_token": access_token,
        "user": user.login,
        "total_repos": len(repo_list),
        "repos": repo_list
    }
