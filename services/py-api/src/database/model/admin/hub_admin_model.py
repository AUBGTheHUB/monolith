from typing import Literal, Any, Self
from dataclasses import dataclass

from src.database.model.admin.hub_member_model import HubMember, MEMBER_TYPE

ROLES = Literal["board", "dev", "super_admin"]


@dataclass(kw_only=True)
class HubAdmin(HubMember):
    """Represents a Hub Admin member"""

    username: str
    member_type: MEMBER_TYPE = "admin"
    password_hash: str
    site_role: ROLES

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        doc = super().dump_as_mongo_db_document()
        doc.update(
            {
                "username": self.username,
                "password_hash": self.password_hash,
                "site_role": self.site_role,
            }
        )
        return doc

    def dump_as_json(self) -> dict[str, Any]:
        data = super().dump_as_json()
        data.update(
            {
                "site_role": self.site_role,
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
            site_role=doc["site_role"],
        )
