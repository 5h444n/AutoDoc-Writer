from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    username: str
    name: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None
