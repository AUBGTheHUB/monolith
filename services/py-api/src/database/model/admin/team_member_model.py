from dataclasses import dataclass, field
from typing import Dict

from src.database.model.admin.base_admin_model import AdminBaseModel, AdminUpdateParams


@dataclass(kw_only=True)
class TeamMember(AdminBaseModel):
    name: str
    role_title: str
    avatar_url: str
    social_links: Dict[str, str] = field(default_factory=dict)

    def dump_as_mongo_db_document(self) -> dict[str, object]:
        return {
            "_id": self.id,
            "name": self.name,
            "role_title": self.role_title,
            "avatar_url": self.avatar_url,
            "social_links": self.social_links,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, object]:
        return {
            "id": str(self.id),
            "name": self.name,
            "role_title": self.role_title,
            "avatar_url": self.avatar_url,
            "social_links": self.social_links,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateTeamMemberParams(AdminUpdateParams):
    name: str | None = None
    role_title: str | None = None
    avatar_url: str | None = None
    social_links: Dict[str, str] | None = None
