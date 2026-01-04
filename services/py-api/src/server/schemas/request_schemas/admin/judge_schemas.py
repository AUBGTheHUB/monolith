from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

from src.server.schemas.request_schemas.schemas import NonEmptyStr, BasePatchReqData


class JudgePostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar_url: HttpUrl
    linkedin_url: Optional[HttpUrl] = None


class JudgePatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    company: Optional[NonEmptyStr] = None
    job_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None
