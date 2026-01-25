from typing import Literal, Any
from dataclasses import dataclass

from src.database.model.admin.hub_member_model import HubMember, MEMBER_TYPE

ROLES = Literal["board", "dev", "super_admin"]


@dataclass(kw_only=True)
class HubAdmin(HubMember):
    """Represents a Hub Admin member"""

    member_type: MEMBER_TYPE = "admin"
    password_hash: str
    site_role: ROLES

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        doc = super().dump_as_mongo_db_document()
        doc.update(
            {
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
                # intentionally exclude password_hash
            }
        )
        return data
