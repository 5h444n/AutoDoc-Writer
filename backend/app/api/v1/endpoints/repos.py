from fastapi import APIRouter, Depends, HTTPException
from app.services.github_service import GitHubService
from app.schemas.repo import RepoResponse

router = APIRouter()

@router.get("/", response_model=RepoResponse)
def read_repos(access_token: str):
    try:
        repos = GitHubService.get_user_repos(access_token)
        return {"total_repos": len(repos), "repos": repos}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))