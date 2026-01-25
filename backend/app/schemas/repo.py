from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RepoBase(BaseModel):
    id: Optional[int] = None
    name: str
    full_name: Optional[str] = None
    url: str
    description: Optional[str] = ""
    language: Optional[str] = None
    stars: Optional[int] = 0
    commits: Optional[int] = None
    last_updated: Optional[str] = None
    is_active: bool = False

    model_config = ConfigDict(from_attributes=True)

class RepoResponse(BaseModel):
    total_repos: int
    repos: List[RepoBase]

class RepoToggleRequest(BaseModel):
    is_active: bool
