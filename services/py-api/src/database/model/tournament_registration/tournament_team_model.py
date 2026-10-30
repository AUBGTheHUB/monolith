from dataclasses import dataclass
from datetime import datetime
from typing import Any, Union

from pydantic import ConfigDict
from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class TournamentTeam(BaseDbModel):
    name: str
    code: str

    completion_email_sent_at: datetime | None = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "code": self.code,
            "completion_email_sent_at": self.completion_email_sent_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "completion_email_sent_at": (
                self.completion_email_sent_at.isoformat() if self.completion_email_sent_at else None
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class UpdateTournamentTeamParams(UpdateParams):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Union[str | None] = None
    code: Union[str | None] = None
    completion_email_sent_at: datetime | None
