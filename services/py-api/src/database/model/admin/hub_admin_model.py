from typing import Any, Self
from enum import Enum
from dataclasses import dataclass

from src.database.model.admin.hub_member_model import HubMember, MEMBER_TYPE, UpdateHubMemberParams


class Role(str, Enum):
    BOARD = "board"
    DEV = "dev"
    SUPER = "super_admin"
    MEMBER = "member"


class AssignableRole(str, Enum):
    BOARD = "board"
    DEV = "dev"
    MEMBER = "member"


@dataclass(kw_only=True)
class HubAdmin(HubMember):
    """Represents a Hub Admin member"""

    username: str
    member_type: MEMBER_TYPE = "admin"
    password_hash: str
    site_role: Role

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        doc = super().dump_as_mongo_db_document()
        doc.update(
            {
                "username": self.username,
                "password_hash": self.password_hash,
                "site_role": self.site_role.value,
            }
        )
        return doc

    def dump_as_json(self) -> dict[str, Any]:
        data = super().dump_as_json()
        data.update(
            {
                "site_role": self.site_role.value,
                "username": self.username,
                # intentionally exclude password_hash
            }
        )
        return data

    @classmethod
    def from_mongo_db_document(cls, doc: dict[str, Any]) -> Self:
        base_data = cls._base_from_mongo_db_document(doc)
        return cls(
            **base_data,
            username=doc["username"],
            password_hash=doc["password_hash"],
            site_role=Role(doc["site_role"]),
        )


class UpdateHubAdminParams(UpdateHubMemberParams):
    username: str | None = None
    site_role: AssignableRole | None = None
