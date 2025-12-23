from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, HttpUrl, field_validator


class HubMemberBase(BaseModel):
    name: str
    role_title: str
    avatar_url: HttpUrl
    social_links: Dict[str, HttpUrl] = {}

    @field_validator("name", "role_title")
    def not_empty(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty")
        return nv


class HubMemberCreate(HubMemberBase):
    pass


class HubMemberUpdate(BaseModel):
    name: Optional[str] = None
    role_title: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, HttpUrl]] = None

    @field_validator("name", "role_title")
    def not_empty_when_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty when provided")
        return nv

    def is_empty(self) -> bool:
        return all(getattr(self, f) is None for f in ("name", "role_title", "avatar_url", "social_links"))


class HubMemberRead(HubMemberBase):
    id: str
    created_at: datetime
    updated_at: datetime
