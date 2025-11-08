from dataclasses import dataclass
from src.database.model.base_model import BaseDbModel

class SponsorTier(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    # CUSTOM = 5

@dataclass()
class Sponsor(BaseDbModel):
    name: str
    logo_url: str
    website_url: str
    tier: SponsorTier
