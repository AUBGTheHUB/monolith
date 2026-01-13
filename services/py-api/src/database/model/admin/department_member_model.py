from dataclasses import dataclass
from typing import Any, Dict, List, Union

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class DepartmentMember(BaseDbModel):
    name: str
    photo_url: str
    linkedin_url: str
    departments: List[str]

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "photo_url": self.photo_url,
            "linkedin_url": self.linkedin_url,
            "departments": self.departments,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "photo_url": self.photo_url,
            "linkedin_url": self.linkedin_url,
            "departments": self.departments,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class UpdateDepartmentMemberParams(UpdateParams):
    name: Union[str, None] = None
    photo_url: Union[str, None] = None
    linkedin_url: Union[str, None] = None
    departments: Union[List[str], None] = None

