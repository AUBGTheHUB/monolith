from dataclasses import field, dataclass
from typing import Dict, Any

from src.database.model.base_model import Base


@dataclass(kw_only=True)
class Team(Base):
    name: str  # unique
    is_verified: bool = field(default=False)

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "name": self.name,
            "is_verified": self.is_verified,
        }

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "is_verified": self.is_verified,
        }
