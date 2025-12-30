from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, field_validator
from src.server.schemas.common.inputs import NonEmptyStr


class PastEventBase(BaseModel):
    title: NonEmptyStr
    cover_picture: HttpUrl
    tags: List[str] = []

    @field_validator("tags")
    def tags_trim(cls, v: List[str]) -> List[str]:
        return [t.strip() for t in v if t.strip()]


class PastEventCreate(PastEventBase):
    pass


class PastEventUpdate(BaseModel):
    title: Optional[NonEmptyStr] = None
    cover_picture: Optional[HttpUrl] = None
    tags: Optional[List[str]] = None

    @field_validator("tags")
    def tags_trim(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return v
        return [t.strip() for t in v if t.strip()]

    def is_empty(self) -> bool:
        return all(getattr(self, f) is None for f in ("title", "cover_picture", "tags"))


class PastEventRead(PastEventBase):
    id: str
    created_at: datetime
    updated_at: datetime
