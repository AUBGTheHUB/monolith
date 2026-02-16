from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

from src.database.model.admin.hub_member_model import SocialLinks, DEPARTMENTS_LIST
from src.server.schemas.request_schemas.schemas import NonEmptyStr, BasePatchReqData


class HubMemberPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    position: NonEmptyStr
    department: DEPARTMENTS_LIST
    avatar: UploadFile
    social_links: SocialLinks


class HubMemberPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    position: Optional[NonEmptyStr] = None
    department: Optional[DEPARTMENTS_LIST] = None
    avatar: Optional[UploadFile] = None
    social_links: Optional[SocialLinks] = None
