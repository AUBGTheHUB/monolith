from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Union

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class Member:
    name: str
    photo_url: str
    linkedin_url: str

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "photo_url": self.photo_url, "linkedin_url": self.linkedin_url}


@dataclass(kw_only=True)
class Department(BaseDbModel):
    name: str
    members: List[Member]

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "members": [member.to_dict() for member in self.members],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "members": [member.to_dict() for member in self.members],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class UpdateDepartmentParams(UpdateParams):
    name: Union[str, None] = None
    members: Union[List[Member], None] = None

    def _member_to_dict(self, member: Any) -> dict[str, Any]:
        if isinstance(member, Member):
            return member.to_dict()
        if isinstance(member, (dict, Mapping)):
            return dict(member)
        raise TypeError(f"Unexpected member type: {type(member)}")

    def model_dump(self, *, exclude_none: bool = True, **kwargs: dict[str, Any]) -> dict[str, Any]:
        data = super().model_dump(exclude_none=exclude_none, **kwargs)
        if "members" in data and data["members"] is not None:
            data["members"] = [self._member_to_dict(member) for member in data["members"]]
        return data

