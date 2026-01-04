from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from src.database.model.base_model import BaseDbModel

class SponsorTier(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    # CUSTOM = 5

@dataclass()
class Sponsor(BaseDbModel):
    def dump_as_json(self) -> Dict[str, Any]:
        pass

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        pass

    name: str
    logo_url: str
    website_url: str
    tier: SponsorTier
