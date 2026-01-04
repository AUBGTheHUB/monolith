from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.mentor_model import Mentor


class MentorResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    mentor: Mentor

    @field_serializer("mentor")
    def serialize_mentor(self, mentor: Mentor) -> dict[str, Any]:
        return mentor.dump_as_json()
