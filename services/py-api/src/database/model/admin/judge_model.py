from dataclasses import dataclass
from typing import Optional, Any

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class Judge(BaseDbModel):
    name: str
    company: str
    job_title: str
    avatar_url: str
    linkedin_url: Optional[str] = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "company": self.company,
            "job_title": self.job_title,
            "avatar_url": self.avatar_url,
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
            "linkedin_url": self.linkedin_url,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateJudgeParams(UpdateParams):
    name: str | None = None
    company: str | None = None
    job_title: str | None = None
    avatar_url: str | None = None
    linkedin_url: str | None = None
