from pydantic import BaseModel
from typing import List

class RepoBase(BaseModel):
    name: str
    url: str
    last_updated: str
    is_active: bool = False  # <--- NEW: Sprint 2 Feature

    class Config:
        from_attributes = True  # Allows Pydantic to read from SQLAlchemy DB models

class RepoResponse(BaseModel):
    total_repos: int
    repos: List[RepoBase]

class RepoToggleRequest(BaseModel):
    is_active: bool