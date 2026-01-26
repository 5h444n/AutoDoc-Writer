from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base

# Create Tables
Base.metadata.create_all(bind=engine)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title=settings.PROJECT_NAME)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# [Roadmap Step 8] Enable CORS for Frontend
# We explicitly add localhost:3000 (React) and localhost:5173 (Vite/Next.js)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Explicit list is safer for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],  # Explicitly list required headers
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
@limiter.limit("100/minute")
def root(request: Request):
    return {"message": "AutoDoc API V1 is running"}