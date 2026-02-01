from fastapi import APIRouter
from app.api.v1.endpoints import auth, repos, ai, repo_docs, webhooks

api_router = APIRouter()

# 1. Connect Auth (This creates /api/v1/auth/...)
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# 2. Connect Repos (This creates /api/v1/repos/...)
api_router.include_router(repos.router, prefix="/repos", tags=["Repositories"])

# 3. Connect AI (This creates /api/v1/ai/...)
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])

# 4. Connect Repo Docs
api_router.include_router(repo_docs.router, prefix="/repo-docs", tags=["RepoDocs"])

# 5. Webhooks (no auth)
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
