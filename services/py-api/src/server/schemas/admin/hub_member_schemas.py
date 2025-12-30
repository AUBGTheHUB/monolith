from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, HttpUrl
from src.server.schemas.common.inputs import NonEmptyStr


class HubMemberBase(BaseModel):
    name: NonEmptyStr
    role_title: NonEmptyStr
    avatar_url: HttpUrl
    social_links: Dict[str, HttpUrl] = {}


class HubMemberCreate(HubMemberBase):
    pass


class HubMemberUpdate(BaseModel):
    name: Optional[NonEmptyStr] = None
    role_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, HttpUrl]] = None

    def is_empty(self) -> bool:
        return all(getattr(self, f) is None for f in ("name", "role_title", "avatar_url", "social_links"))


class HubMemberRead(HubMemberBase):
    id: str
    created_at: datetime
    updated_at: datetime
