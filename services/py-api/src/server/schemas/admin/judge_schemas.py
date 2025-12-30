from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl
from src.server.schemas.common.inputs import NonEmptyStr


class JudgeBase(BaseModel):
    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar_url: HttpUrl
    linkedin_url: Optional[HttpUrl] = None


class JudgeCreate(JudgeBase):
    pass


class JudgeUpdate(BaseModel):
    name: Optional[NonEmptyStr] = None
    company: Optional[NonEmptyStr] = None
    job_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None


class JudgeRead(JudgeBase):
    id: str
    created_at: datetime
    updated_at: datetime
