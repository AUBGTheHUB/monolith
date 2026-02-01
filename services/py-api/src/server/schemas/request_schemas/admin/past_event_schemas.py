from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

from src.server.schemas.request_schemas.schemas import NonEmptyStr, BasePatchReqData


class PastEventPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: NonEmptyStr
    cover_picture: HttpUrl
    tags: list[NonEmptyStr] = []


class PastEventPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    title: Optional[NonEmptyStr] = None
    cover_picture: Optional[HttpUrl] = None
    tags: Optional[list[NonEmptyStr]] = None


class PastEventPutReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: NonEmptyStr
    cover_picture: HttpUrl
    tags: list[NonEmptyStr] = []
