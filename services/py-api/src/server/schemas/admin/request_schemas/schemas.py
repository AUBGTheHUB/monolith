from typing import Annotated, Optional
from pydantic import BaseModel, HttpUrl, ConfigDict, field_validator, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class JudgeBaseInputData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar_url: HttpUrl
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("name", "company", "job_title")
    @classmethod
    def not_empty(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty")
        return nv


class JudgePostReqData(JudgeBaseInputData):
    pass


class JudgeUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None

    @field_validator("name", "company", "job_title")
    @classmethod
    def not_empty_when_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        nv = v.strip()
        if not nv:
            raise ValueError("field cannot be empty when provided")
        return nv

    def is_empty(self) -> bool:
        return all(
            getattr(self, field) is None for field in ("name", "company", "job_title", "avatar_url", "linkedin_url")
        )
