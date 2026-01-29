from dataclasses import field
from typing import cast

from pydantic import BaseModel, ConfigDict, model_validator
from src.server.schemas.request_schemas.schemas import NonEmptyStr

from src.database.model.admin.hub_admin_model import HubAdmin
from src.database.model.admin.hub_member_model import MEMBER_TYPE, DEPARTMENTS_LIST, SocialLinks


class BaseHubMemberData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    member_type: MEMBER_TYPE = "admin"
    position: str
    department: DEPARTMENTS_LIST
    avatar_url: str
    social_links: SocialLinks = field(default_factory=lambda: cast(SocialLinks, cast(object, {})))


class RegisterHubAdminData(BaseHubMemberData):

    password: str
    repeat_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "RegisterHubAdminData":
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")
        return self

    def convert_to_hub_admin(self) -> HubAdmin:
        return HubAdmin(
            name=self.name,
            member_type=self.member_type,
            position=self.position,
            avatar_url=self.avatar_url,
            social_links=self.social_links,
            department=self.department,
            password_hash="",
            # TODO change site roles
            site_role="dev",
        )


class LoginHubAdminData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    password: str
