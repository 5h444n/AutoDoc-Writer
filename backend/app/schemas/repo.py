from pydantic import BaseModel, ConfigDict
from typing import List

class RepoBase(BaseModel):
    name: str
    url: str
    last_updated: str
    is_active: bool = False  # <--- NEW: Sprint 2 Feature

    model_config = ConfigDict(from_attributes=True)

class RepoResponse(BaseModel):
    total_repos: int
    repos: List[RepoBase]

class RepoToggleRequest(BaseModel):
    is_active: bool