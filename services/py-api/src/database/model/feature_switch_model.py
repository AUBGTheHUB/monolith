from dataclasses import dataclass
from typing import Any, Dict, Union

from src.database.model.base_model import BaseDbModel, UpdateParams


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


class UpdateFeatureSwitchParams(UpdateParams):
    """This model makes each field of the Feature Switch optional, so that you can
    only set values to the fields that you want to modify and pass to the
    MongoDB find_one_and_update() method.
    Build to be used for updating the Feature Switch document in the database.
    """

    name: Union[str, None] = None
    state: Union[bool, None] = None
