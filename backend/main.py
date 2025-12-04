from fastapi import FastAPI
from .auth import router as auth_router
from .github_repos import router as repo_router

app = FastAPI()

# Register routers
app.include_router(auth_router, prefix="/auth")
app.include_router(repo_router)

@app.get("/")
def read_root():
    return {"message": "AutoDoc Backend is running!"}
