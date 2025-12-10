from fastapi import APIRouter
from app.api.v1.endpoints import repos, auth
# Note: You'll need to move your auth logic to endpoints/auth.py similarly

api_router = APIRouter()
api_router.include_router(repos.router, prefix="/repos", tags=["repos"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])