from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.past_event_model import PastEvent


class PastEventResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    past_event: PastEvent

    @field_serializer("past_event")
    def serialize_past_event(self, past_event: PastEvent) -> dict[str, Any]:
        return past_event.dump_as_json()


class AllPastEventsResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    past_events: list[PastEvent]

    @field_serializer("past_events")
    def serialize_past_events(self, past_events: list[PastEvent]) -> list[dict[str, Any]]:
        return [past_event.dump_as_json() for past_event in past_events]
