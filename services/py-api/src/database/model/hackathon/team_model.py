from dataclasses import field, dataclass
from typing import Dict, Any, Union

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class Team(BaseDbModel):
    """A representation of the Team entity in Mongo. It is also the schema of how the entity should look
    like in Mongo before it is inserted"""

    name: str  # unique
    is_verified: bool = field(default=False)

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "is_verified": self.is_verified,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "is_verified": self.is_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class UpdateTeamParams(UpdateParams):
    """This model makes each field of the Team optional, so that you can
    only set values to the fields that you want to modify and pass to the
    MongoDB find_one_and_update() method.
    Build to be used for updating the Team document in the database.

    The ``updated_at`` filed us set for you, so you should not set it explicitly
    """

    name: Union[str, None] = None
    is_verified: Union[bool, None] = None
