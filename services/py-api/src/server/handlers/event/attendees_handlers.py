from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.event.attendee_schemas import AttendeePostReqData, AttendeePatchReqData
from src.server.schemas.response_schemas.event.attendee_schemas import AttendeeResponse, AttendeesResponse
from src.server.schemas.response_schemas.schemas import Response
from src.service.event.attendees_service import AttendeesService


# Attendees Handlers
class AttendeesHandlers(BaseHandler):
    def __init__(self, service: AttendeesService) -> None:
        self._service = service

    async def create_attendee(self, attendee: AttendeePostReqData) -> Response:
        result = await self._service.create(
            name=attendee.name,
            email=attendee.email,
            has_paid=attendee.has_paid,
            ticket_type=attendee.ticket_type,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(AttendeeResponse(attendee=result.ok_value), status_code=201)

    async def get_all_attendees(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(AttendeesResponse(attendees=result.ok_value), status_code=200)

    async def get_attendee(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(AttendeeResponse(attendee=result.ok_value), status_code=200)

    async def update_attendee(self, attendee_id: str, attendee: AttendeePatchReqData) -> Response:
        result = await self._service.update(
            attendee_id=attendee_id,
            name=attendee.name,
            email=attendee.email,
            has_paid=attendee.has_paid,
            ticket_type=attendee.ticket_type,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(AttendeeResponse(attendee=result.ok_value), status_code=200)

    async def delete_attendee(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(AttendeeResponse(attendee=result.ok_value), status_code=200)
