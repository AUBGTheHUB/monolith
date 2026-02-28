from dataclasses import field
from typing import cast, Self

from fastapi import Form
from pydantic import BaseModel, ConfigDict, model_validator
from src.server.schemas.request_schemas.schemas import NonEmptyStr
from src.database.model.admin.hub_admin_model import HubAdmin, Role
from src.database.model.admin.hub_member_model import MEMBER_TYPE, DEPARTMENTS_LIST, SocialLinks


class BaseHubMemberData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    member_type: MEMBER_TYPE = "admin"
    position: str
    departments: list[DEPARTMENTS_LIST]
    social_links: SocialLinks = field(default_factory=lambda: cast(SocialLinks, cast(object, {})))


class RegisterHubAdminData(BaseHubMemberData):
    username: str
    password: str
    repeat_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")
        return self

    def convert_to_hub_admin(self, password_hash: str, avatar_url: str) -> HubAdmin:
        return HubAdmin(
            name=self.name,
            username=self.username,
            member_type=self.member_type,
            position=self.position,
            social_links=self.social_links,
            departments=self.departments,
            password_hash=password_hash,
            site_role=Role.BOARD,
            avatar_url=avatar_url,
        )

    # Helper method to handle Form data mapping
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        repeat_password: str = Form(...),
        position: str = Form(...),
        departments: list[DEPARTMENTS_LIST] = Form(...),
        member_type: MEMBER_TYPE = Form("admin"),
    ) -> "RegisterHubAdminData":
        return cls(
            name=name,
            username=username,
            password=password,
            repeat_password=repeat_password,
            position=position,
            departments=departments,
            member_type=member_type,
        )


class LoginHubAdminData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    username: NonEmptyStr
    password: str
