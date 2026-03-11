from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl, ConfigDict

from src.database.model.admin.sponsor_model import ALLOWED_SPONSOR_TIERS
from src.server.schemas.request_schemas.schemas import NonEmptyStr, BasePatchReqData


class SponsorPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    tier: ALLOWED_SPONSOR_TIERS
    logo: UploadFile
    website_url: Optional[HttpUrl] = None


class SponsorPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    tier: Optional[ALLOWED_SPONSOR_TIERS] = None
    logo: Optional[UploadFile] = None
    website_url: Optional[HttpUrl] = None
