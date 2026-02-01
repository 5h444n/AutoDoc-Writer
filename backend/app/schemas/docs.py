from typing import Optional

from pydantic import BaseModel


class DocsGenerateRequest(BaseModel):
    repo_full_name: str
    commit_sha: str
    style: Optional[str] = None
    complexity: Optional[int] = None
    force: bool = False


class DocsGenerateResponse(BaseModel):
    commit_sha: str
    commit_short_sha: Optional[str] = None
    repo_name: str
    repo_full_name: str
    generated_at: str
    plain_text: Optional[str] = None
    research_style: Optional[str] = None
    latex: Optional[str] = None
