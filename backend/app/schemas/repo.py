from pydantic import BaseModel
from typing import List
from datetime import datetime

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

class CommitInfo(BaseModel):
    sha: str
    message: str
    author_name: str
    date: datetime
    url: str
