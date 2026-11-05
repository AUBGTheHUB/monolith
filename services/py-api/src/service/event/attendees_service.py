from result import Result, is_err, Err

from src.database.model.event.attendee_model import Attendee, UpdateAttendeeParams, ALLOWED_TICKET_TYPES
from src.database.repository.event.attendees_repository import AttendeesRepository
from src.exception import AttendeeNotFoundError, AttendeeTicketNotFoundException
from src.service.event.tickets_service import TicketsService


class AttendeesService:
    def __init__(self, repo: AttendeesRepository, ticket_service: TicketsService) -> None:
        self._repo = repo
        self._ticket_service = ticket_service

    async def get_all(self) -> Result[list[Attendee], Exception]:
        return await self._repo.fetch_all()

    async def get(self, attendee_id: str) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        return await self._repo.fetch_by_id(attendee_id)

    async def create(
        self, name: str, email: str, has_paid: bool, ticket_type: ALLOWED_TICKET_TYPES
    ) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        result = await self._ticket_service.create(
            ticket_type=ticket_type,
            barcode_value=email,
            primary_fields={None: "Play Con: Road to the Rift"},
            secondary_fields={
                "Name": name,
                "Email": email,
            },
        )

        if is_err(result):
            return result

        attendee = Attendee(
            name=name, email=email, has_paid=has_paid, ticket_type=ticket_type, ticket_serial_number=result.ok_value[1]
        )
        return await self._repo.create(attendee)

    async def update(
        self,
        attendee_id: str,
        name: str | None = None,
        email: str | None = None,
        has_paid: bool | None = None,
        ticket_type: ALLOWED_TICKET_TYPES | None = None,
    ) -> Result[Attendee, AttendeeNotFoundError | AttendeeTicketNotFoundException | Exception]:
        attendee = await self._repo.fetch_by_id(attendee_id)

        if is_err(attendee):
            return attendee

        if attendee.ok_value.ticket_serial_number is None:
            return Err(AttendeeTicketNotFoundException())

        secondary_fields: dict[str | None, str] = {}

        if name is not None:
            secondary_fields["Name"] = name

        if email is not None:
            secondary_fields["Email"] = email

        result = await self._ticket_service.update(
            ticket_serial_number=attendee.ok_value.ticket_serial_number,
            ticket_type=ticket_type,
            barcode_value=email,
            primary_fields={None: "Play Con: Road to the Rift"},
            secondary_fields=secondary_fields if secondary_fields != {} else None,
        )
        if is_err(result):
            return result

        params = UpdateAttendeeParams(
            name=name,
            email=email,
            has_paid=has_paid,
            ticket_type=ticket_type,
            ticket_serial_number=attendee.ok_value.ticket_serial_number,
        )
        return await self._repo.update(attendee_id, params)

    async def delete(self, attendee_id: str) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        # TODO: Add ticket revoke
        return await self._repo.delete(attendee_id)
