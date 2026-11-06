from fastapi import BackgroundTasks
from result import Result, is_err, Err, Ok

from src.service.mail_service.mail_service import MailService
from src.database.model.event.attendee_model import Attendee, UpdateAttendeeParams, ALLOWED_TICKET_TYPES
from src.database.repository.event.attendees_repository import AttendeesRepository
from src.exception import AttendeeNotFoundError, AttendeeTicketNotFoundException
from src.service.event.tickets_service import TicketsService


class AttendeesService:
    def __init__(self, repo: AttendeesRepository, ticket_service: TicketsService, mail_service: MailService) -> None:
        self._repo = repo
        self._ticket_service = ticket_service
        self._mail_service = mail_service

    async def get_all(self) -> Result[list[Attendee], Exception]:
        return await self._repo.fetch_all()

    async def get(self, attendee_id: str) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        return await self._repo.fetch_by_id(attendee_id)

    async def create(
        self,
        name: str,
        email: str,
        has_paid: bool,
        ticket_type: ALLOWED_TICKET_TYPES,
        background_tasks: BackgroundTasks,
    ) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        ticket_result = await self._ticket_service.create(
            ticket_type=ticket_type,
            barcode_value=email,
            primary_fields={None: "Play Con: Road to the Rift"},
            secondary_fields={
                "Name": name,
                "Email": email,
            },
        )

        if is_err(ticket_result):
            return ticket_result

        result_value: tuple[str, str] = ticket_result.ok_value
        ticket_data = result_value[0]
        ticket_number = result_value[1]

        attendee = Attendee(
            name=name, email=email, has_paid=has_paid, ticket_type=ticket_type, ticket_serial_number=ticket_number
        )

        repo_result = await self._repo.create(attendee)

        if is_err(repo_result):
            return repo_result

        email_result = await self._mail_service.send_email_with_ticket(
            attendee=attendee,
            pass_data=ticket_data,
            background_tasks=background_tasks,
        )

        if is_err(email_result):
            return email_result

        return Ok(repo_result.ok_value)

    async def update(
        self,
        background_tasks: BackgroundTasks,
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

        primary_fields: dict[str | None, str] = {
            None: "Play Con: Road to the Rift",
        }

        ticket_result = await self._ticket_service.update(
            ticket_serial_number=attendee.ok_value.ticket_serial_number,
            ticket_type=ticket_type,
            barcode_value=email,
            primary_fields=primary_fields,
            secondary_fields=secondary_fields if secondary_fields != {} else None,
        )

        if is_err(ticket_result):
            return ticket_result

        result_value: tuple[str, str] = ticket_result.ok_value
        ticket_data = result_value[0]
        ticket_number = result_value[1]

        params = UpdateAttendeeParams(
            name=name,
            email=email,
            has_paid=has_paid,
            ticket_type=ticket_type,
            ticket_serial_number=ticket_number,
        )

        repo_result = await self._repo.update(attendee_id, params)

        if is_err(repo_result):
            return repo_result

        email_result = await self._mail_service.send_email_with_ticket(
            attendee=attendee.ok_value,
            pass_data=ticket_data,
            background_tasks=background_tasks,
        )

        if is_err(email_result):
            return email_result

        return Ok(repo_result.ok_value)

    async def delete(
        self, attendee_id: str
    ) -> Result[Attendee, AttendeeNotFoundError | AttendeeTicketNotFoundException | Exception]:
        attendee = await self._repo.fetch_by_id(attendee_id)

        if is_err(attendee):
            return attendee

        if attendee.ok_value.ticket_serial_number is None:
            return Err(AttendeeTicketNotFoundException())

        ticket_result = await self._ticket_service.delete(attendee.ok_value.ticket_serial_number)

        if is_err(ticket_result):
            return ticket_result

        return await self._repo.delete(attendee_id)
