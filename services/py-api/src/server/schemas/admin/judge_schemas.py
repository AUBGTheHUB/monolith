from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class JudgeBase(BaseModel):
    name: str
    company: str
    job_title: str
    avatar_url: HttpUrl
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("name", "company", "job_title")
    def not_empty(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty")
        return nv


class JudgeCreate(JudgeBase):
    pass


class JudgeUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("name", "company", "job_title")
    def not_empty_when_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty when provided")
        return nv

    def is_empty(self) -> bool:
        return all(getattr(self, f) is None for f in ("name", "company", "job_title", "avatar_url", "linkedin_url"))


class JudgeRead(JudgeBase):
    id: str
    created_at: datetime
    updated_at: datetime
