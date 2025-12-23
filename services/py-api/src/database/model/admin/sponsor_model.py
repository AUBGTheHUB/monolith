from dataclasses import dataclass
from typing import Optional, Literal, Any

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class Sponsor(BaseDbModel):
    name: str
    # TODO(#admin-sponsors-tier-enum): Replace Literal with Enum once tier list is finalized / needs ordering logic.
    tier: Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]
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


class UpdateSponsorParams(UpdateParams):
    name: str | None = None
    tier: Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"] | None = None
    logo_url: str | None = None
    website_url: str | None = None
