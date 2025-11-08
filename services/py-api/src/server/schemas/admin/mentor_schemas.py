from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, field_validator


class MentorBase(BaseModel):
    name: str
    company: str
    job_title: str
    avatar_url: HttpUrl
    expertise_areas: List[str] = []
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("name", "company", "job_title")
    def not_empty(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty")
        return nv

    @field_validator("expertise_areas")
    def areas_trim(cls, v: List[str]) -> List[str]:
        return [a.strip() for a in v if a.strip()]


class MentorCreate(MentorBase):
    pass


class MentorUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    expertise_areas: Optional[List[str]] = None
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("name", "company", "job_title")
    def not_empty_when_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty when provided")
        return nv

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
