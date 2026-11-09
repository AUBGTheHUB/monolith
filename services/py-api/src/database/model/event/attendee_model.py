from dataclasses import dataclass
from typing import Optional, Literal, Any

from src.database.model.base_model import BaseDbModel, UpdateParams

ALLOWED_TICKET_TYPES = Literal["GUEST", "PARTICIPANT"]


@dataclass(kw_only=True)
class Attendee(BaseDbModel):
    name: str
    email: str
    has_paid: bool
    ticket_type: ALLOWED_TICKET_TYPES
    ticket_serial_number: Optional[str] = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "email": self.email,
            "has_paid": self.has_paid,
            "ticket_type": self.ticket_type,
            "ticket_serial_number": self.ticket_serial_number,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "has_paid": self.has_paid,
            "ticket_type": self.ticket_type,
            "ticket_serial_number": self.ticket_serial_number,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateAttendeeParams(UpdateParams):
    name: str | None = None
    email: str | None = None
    has_paid: bool | None = None
    ticket_type: ALLOWED_TICKET_TYPES | None = None
    ticket_serial_number: str | None = None
