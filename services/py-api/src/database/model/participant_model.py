from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union


from pydantic import EmailStr
from src.database.model.base_model import BaseDbModel, SerializableObjectId, UpdateParams


@dataclass(kw_only=True)
class Participant(BaseDbModel):
    """A representation of the Participant entity in Mongo. It is also the schema of how the entity should look
    like in Mongo before it is inserted"""

    name: str
    email: str
    is_admin: bool
    email_verified: bool = field(default=False)
    team_id: Optional[SerializableObjectId]

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "email_verified": self.email_verified,
            "team_id": self.team_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "email_verified": self.email_verified,
            "team_id": str(self.team_id) if self.team_id else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateParticipantParams(UpdateParams):
    """This model makes each field of the Participant optional, so that you can
    only set values to the fields that you want to modify and pass to the
    MongoDB find_one_and_update() method.
    Build to be used for updating the Participant document in the database.
    """

    name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    email_verified: Union[bool, None] = None
    is_admin: Union[bool, None] = None
    team_id: Union[str, None] = None
