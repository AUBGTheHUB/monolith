from dataclasses import dataclass, field
from typing import List, Optional, Any

from src.database.model.admin.base_admin_model import AdminBaseModel, AdminUpdateParams


@dataclass(kw_only=True)
class Mentor(AdminBaseModel):
    name: str
    company: str
    job_title: str
    avatar_url: str
    expertise_areas: List[str] = field(default_factory=list)
    linkedin_url: Optional[str] = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "company": self.company,
            "job_title": self.job_title,
            "avatar_url": self.avatar_url,
            "expertise_areas": self.expertise_areas,
            "linkedin_url": self.linkedin_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "company": self.company,
            "job_title": self.job_title,
            "avatar_url": self.avatar_url,
            "expertise_areas": self.expertise_areas,
            "linkedin_url": self.linkedin_url,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateMentorParams(AdminUpdateParams):
    name: str | None = None
    company: str | None = None
    job_title: str | None = None
    avatar_url: str | None = None
    expertise_areas: List[str] | None = None
    linkedin_url: str | None = None
