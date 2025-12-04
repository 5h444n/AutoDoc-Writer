from fastapi import FastAPI
from .auth import router as auth_router
from .github_repos import router as repo_router

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

# Register routers
app.include_router(auth_router, prefix="/auth")
app.include_router(repo_router)

@app.get("/")
def read_root():
    return {"message": "AutoDoc Backend is running!"}
