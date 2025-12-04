from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI(
    title="AutoDoc Writer Backend",
    version="1.0.0",
)

# include auth router with prefix
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "AutoDoc Backend is running!"}
