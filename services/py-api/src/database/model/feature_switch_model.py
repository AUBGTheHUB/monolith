from dataclasses import dataclass
from typing import Any, Dict

from src.database.model.base_model import BaseDbModel

@dataclass(kw_only=True)
class FeatureSwitch(BaseDbModel):
    name: str
    state: bool
    

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "state": self.state,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }