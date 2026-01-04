from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.past_event_model import PastEvent


class PastEventResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    past_event: PastEvent

    @field_serializer("past_event")
    def serialize_past_event(self, past_event: PastEvent) -> dict[str, Any]:
        return past_event.dump_as_json()
