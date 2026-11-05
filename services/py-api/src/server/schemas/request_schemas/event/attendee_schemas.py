from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.database.model.event.attendee_model import ALLOWED_TICKET_TYPES
from src.server.schemas.request_schemas.schemas import BasePatchReqData, NonEmptyStr


class AttendeePostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    email: NonEmptyStr
    has_paid: bool
    ticket_type: ALLOWED_TICKET_TYPES
    ticket_serial_number: NonEmptyStr


class AttendeePatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    email: Optional[NonEmptyStr] = None
    has_paid: Optional[bool] = None
    ticket_type: Optional[ALLOWED_TICKET_TYPES] = None
    ticket_serial_number: Optional[NonEmptyStr] = None
