from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, field_validator
from src.server.schemas.common.inputs import NonEmptyStr


class MentorBase(BaseModel):
    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar_url: HttpUrl
    expertise_areas: List[str] = []
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("expertise_areas")
    def areas_trim(cls, v: List[str]) -> List[str]:
        return [a.strip() for a in v if a.strip()]


class MentorCreate(MentorBase):
    pass


class MentorUpdate(BaseModel):
    name: Optional[NonEmptyStr] = None
    company: Optional[NonEmptyStr] = None
    job_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    expertise_areas: Optional[List[str]] = None
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("expertise_areas")
    def areas_trim(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return v
        return [a.strip() for a in v if a.strip()]

    def is_empty(self) -> bool:
        return all(
            getattr(self, f) is None
            for f in ("name", "company", "job_title", "avatar_url", "expertise_areas", "linkedin_url")
        )


class MentorRead(MentorBase):
    id: str
    created_at: datetime
    updated_at: datetime
