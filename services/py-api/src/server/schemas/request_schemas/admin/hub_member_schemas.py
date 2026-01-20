from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

from src.database.model.admin.hub_member_model import SocialLinks, DEPARTMENTS_LIST
from src.server.schemas.request_schemas.schemas import NonEmptyStr, BasePatchReqData


class HubMemberPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    role_title: NonEmptyStr
    department: DEPARTMENTS_LIST
    avatar_url: HttpUrl
    social_links: SocialLinks


class HubMemberPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    role_title: Optional[NonEmptyStr] = None
    department: Optional[DEPARTMENTS_LIST] = None
    avatar_url: Optional[HttpUrl] = None
    social_links: Optional[SocialLinks] = None
