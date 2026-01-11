from dataclasses import dataclass, field
from typing import Any, Literal, NotRequired, TypedDict, cast

from pydantic import HttpUrl

from src.database.model.base_model import BaseDbModel, UpdateParams

DEPARTMENTS_LIST = Literal["Development", "Marketing", "Logistics", "PR", "Design"]
MEMBER_TYPE = Literal["member", "admin"]
"""This is to distinguish between ordinary club members with NO access to the admin panel
    and admins with specific access based on their role defined in the hub_admin_model"""


class SocialLinks(TypedDict):
    linkedin: NotRequired[HttpUrl]
    github: NotRequired[HttpUrl]
    website: NotRequired[HttpUrl]


@dataclass(kw_only=True)
class HubMember(BaseDbModel):
    """Represents a Hub club member"""

    name: str
    member_type: MEMBER_TYPE = "member"
    position: str
    department: DEPARTMENTS_LIST
    avatar_url: str
    social_links: SocialLinks = field(default_factory=lambda: cast(SocialLinks, cast(object, {})))

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "member_type": self.member_type,
            "position": self.position,
            "avatar_url": self.avatar_url,
            "social_links": self.social_links,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "member_type": self.member_type,
            "position": self.position,
            "avatar_url": self.avatar_url,
            "social_links": self.social_links,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateHubMemberParams(UpdateParams):
    name: str | None = None
    position: str | None = None
    avatar_url: str | None = None
    social_links: SocialLinks | None = None
