from pydantic import BaseModel
from datetime import datetime

class RepoBase(BaseModel):
    name: str
    url: str
    last_updated: str

class RepoResponse(BaseModel):
    total_repos: int
    repos: list[RepoBase]