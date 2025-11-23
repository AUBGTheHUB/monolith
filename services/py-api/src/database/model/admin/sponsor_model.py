from dataclasses import dataclass
from typing import Optional, Any

from src.database.model.admin.base_admin_model import AdminBaseModel, AdminUpdateParams


@dataclass(kw_only=True)
class Sponsor(AdminBaseModel):
    name: str
    tier: str  # PLATINUM | GOLD | SILVER | BRONZE | CUSTOM (free text for now)
    logo_url: str
    website_url: Optional[str] = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "tier": self.tier,
            "logo_url": self.logo_url,
            "website_url": self.website_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "tier": self.tier,
            "logo_url": self.logo_url,
            "website_url": self.website_url,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateSponsorParams(AdminUpdateParams):
    name: str | None = None
    tier: str | None = None
    logo_url: str | None = None
    website_url: str | None = None
