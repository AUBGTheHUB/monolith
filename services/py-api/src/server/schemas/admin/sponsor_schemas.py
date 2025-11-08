from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, field_validator

ALLOWED_SPONSOR_TIERS = ["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]


class SponsorBase(BaseModel):
    name: str
    tier: Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]
    logo_url: HttpUrl
    website_url: Optional[HttpUrl] = None

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("name cannot be empty")
        return nv


class SponsorCreate(SponsorBase):
    pass


class SponsorUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]] = None
    logo_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None

    @field_validator("name")
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        nv = v.strip()
        if not nv:
            raise ValueError("name cannot be empty when provided")
        return nv

    def is_empty(self) -> bool:
        return all(getattr(self, f) is None for f in ("name", "tier", "logo_url", "website_url"))


class SponsorRead(SponsorBase):
    id: str
    created_at: datetime
    updated_at: datetime
