import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from github import Github # PyGithub for later

# 1. Load Environment Variables (API Keys)
load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")

# 2. Initialize App
app = FastAPI(title="AutoDoc Writer API")

# 3. CORS Setup (Allow Frontend to talk to us)
# In production, replace "*" with ["http://localhost:5173"] for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---

@app.get("/")
def health_check():
    """Simple check to see if server is running."""
    return {"status": "running", "service": "AutoDoc Backend"}

@app.get("/login")
def login_via_github():
    """
    Step 1: Redirect user to GitHub to approve our app.
    Scope 'repo' is required to read private repositories.
    """
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Server misconfigured: Missing Client ID")
    
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=repo user"
    )
    return RedirectResponse(url=github_auth_url)

@app.get("/auth/callback")
async def github_callback(code: str):
    """
    Step 2: GitHub sends the user back here with a temporary 'code'.
    We exchange this code for a permanent 'access_token'.
    """
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    headers = {"Accept": "application/json"}

    # Talk to GitHub server-to-server
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token", 
            params=params, 
            headers=headers
        )
        
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get token from GitHub")
    
    data = response.json()
    
    # Error handling from GitHub side
    if "error" in data:
        raise HTTPException(status_code=400, detail=f"GitHub Error: {data.get('error_description')}")

    access_token = data.get("access_token")
    
    # FOR SPRINT 1 DEBUGGING ONLY:
    # We return the token directly so you can see it. 
    # In Sprint 2, we will redirect the user to the Frontend Dashboard with this token.
    return {
        "message": "Login Successful!",
        "access_token": access_token,
        "token_type": data.get("token_type")
    }

# --- Card 7: Skeleton for Fetching Repos ---
@app.get("/get-repos")
def get_user_repos(token: str):
    """
    Uses PyGithub to fetch the user's list of repositories.
    """
    try:
        g = Github(token)
        user = g.get_user()
        
        repo_list = []
        # Limit to 10 for performance in Sprint 1
        for repo in user.get_repos(sort="updated", direction="desc")[:10]:
            repo_list.append({
                "id": repo.id,
                "name": repo.name,
                "private": repo.private,
                "url": repo.html_url,
                "description": repo.description,
                "language": repo.language
            })
            
        return {"username": user.login, "repositories": repo_list}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Token or API Error: {str(e)}")