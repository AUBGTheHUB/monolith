from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl, ConfigDict

from src.server.schemas.request_schemas.schemas import BasePatchReqData, NonEmptyStr


class MentorPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar: UploadFile
    linkedin_url: Optional[HttpUrl] = None


class MentorPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    company: Optional[NonEmptyStr] = None
    job_title: Optional[NonEmptyStr] = None
    avatar: Optional[UploadFile] = None
    linkedin_url: Optional[HttpUrl] = None
