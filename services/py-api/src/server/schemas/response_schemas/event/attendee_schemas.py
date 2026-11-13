from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.event.attendee_model import Attendee


class AttendeeResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    attendee: Attendee

    @field_serializer("attendee")
    def serialize_attendee(self, attendee: Attendee) -> dict[str, Any]:
        return attendee.dump_as_json()


class AttendeesResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    attendees: list[Attendee]

    @field_serializer("attendees")
    def serialize_attendee(self, attendees: list[Attendee]) -> list[dict[str, Any]]:
        return [attendee.dump_as_json() for attendee in attendees]
