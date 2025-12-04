import os
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

router = APIRouter()

# Load configuration from environment
GITHUB_CLIENT_ID = os.getenv("Ov23li8Xv12JtpIeK9TM")
GITHUB_CLIENT_SECRET = os.getenv("fa489d25f69902e484121b825cabbb0db870de4d")
REDIRECT_URI = os.getenv("http://localhost:8000/auth/callback")

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
    GitHub OAuth callback - exchanges code for access token.
    """
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                GITHUB_TOKEN_URL, json=payload, headers=headers
            )
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"GitHub communication error: {exc}")

    token_data = response.json()

    if "error" in token_data:
        raise HTTPException(
            status_code=400,
            detail=f"GitHub OAuth Error: {token_data.get('error_description')}",
        )

    return {
        "message": "Successfully authenticated!",
        "access_token": token_data.get("access_token"),
        "scope": token_data.get("scope"),
        "token_type": token_data.get("token_type"),
    }
