from dataclasses import dataclass, field
from typing import Any, Literal, NotRequired, TypedDict, cast

from src.database.model.base_model import BaseDbModel, UpdateParams

DEPARTMENTS_LIST = Literal["Development", "Marketing", "Logistics", "PR", "Design"]


class SocialLinks(TypedDict):
    linkedin: NotRequired[str]
    github: NotRequired[str]
    website: NotRequired[str]


@dataclass(kw_only=True)
class HubMember(BaseDbModel):
    """Represents a Hub club member"""

    name: str
    role_title: str
    department: DEPARTMENTS_LIST
    avatar_url: str
    social_links: SocialLinks = field(default_factory=lambda: cast(SocialLinks, {}))

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "role_title": self.role_title,
            "avatar_url": self.avatar_url,
            "social_links": self.social_links,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "role_title": self.role_title,
            "avatar_url": self.avatar_url,
            "social_links": self.social_links,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateHubMemberParams(UpdateParams):
    name: str | None = None
    role_title: str | None = None
    avatar_url: str | None = None
    social_links: SocialLinks | None = None
