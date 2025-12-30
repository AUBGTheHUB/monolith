from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl
from src.server.schemas.common.inputs import NonEmptyStr

ALLOWED_SPONSOR_TIERS = ["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]


class SponsorBase(BaseModel):
    name: NonEmptyStr
    tier: Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]
    logo_url: HttpUrl
    website_url: Optional[HttpUrl] = None


class SponsorCreate(SponsorBase):
    pass


class SponsorUpdate(BaseModel):
    name: Optional[NonEmptyStr] = None
    tier: Optional[Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]] = None
    logo_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None

    def is_empty(self) -> bool:
        return all(getattr(self, f) is None for f in ("name", "tier", "logo_url", "website_url"))


class SponsorRead(SponsorBase):
    id: str
    created_at: datetime
    updated_at: datetime
