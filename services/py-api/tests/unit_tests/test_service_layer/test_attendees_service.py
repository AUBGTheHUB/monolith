from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.service.event.tickets_service import TicketsService
from src.service.mail_service.mail_service import MailService
from src.database.model.event.attendee_model import Attendee
from src.database.repository.event.attendees_repository import AttendeesRepository
from src.exception import AttendeeNotFoundError
from src.server.schemas.request_schemas.event.attendee_schemas import (
    AttendeePostReqData,
)
from src.service.event.attendees_service import AttendeesService
from tests.unit_tests.conftest import AttendeesRepoMock, TicketsServiceMock, MailServiceMock, BackgroundTasksMock

SERIAL = "serial-123"
PASS_DATA = "ZmFrZS1wYXNzLWJhc2U2NA=="
GOOGLE_URL = "https://pay.google.com/gp/v/save/fi3nofiwnf"


@pytest.fixture
def attendees_service(
    attendees_repo_mock: AttendeesRepoMock, tickets_service_mock: TicketsServiceMock, mail_service_mock: MailServiceMock
) -> AttendeesService:
    return AttendeesService(
        repo=cast(AttendeesRepository, attendees_repo_mock),
        ticket_service=cast(TicketsService, tickets_service_mock),
        mail_service=cast(MailService, mail_service_mock),
    )


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    attendees_service: AttendeesService, attendees_repo_mock: AttendeesRepoMock, attendee_mock: Attendee
) -> None:
    attendees = [attendee_mock]
    attendees_repo_mock.fetch_all.return_value = Ok(attendees)

    result = await attendees_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == attendees
    attendees_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    attendees_service: AttendeesService,
    attendees_repo_mock: AttendeesRepoMock,
    attendee_mock: Attendee,
) -> None:
    attendees_repo_mock.fetch_by_id.return_value = Ok(attendee_mock)

    result = await attendees_service.get(str(attendee_mock.id))

    assert result.is_ok()
    assert result.unwrap() == attendee_mock
    attendees_repo_mock.fetch_by_id.assert_awaited_once_with(str(attendee_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    attendees_service: AttendeesService, attendees_repo_mock: AttendeesRepoMock
) -> None:
    attendees_repo_mock.fetch_by_id.return_value = Err(AttendeeNotFoundError())

    result = await attendees_service.get("missing attendee")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), AttendeeNotFoundError)
    attendees_repo_mock.fetch_by_id.assert_awaited_once_with("missing attendee")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    attendees_service: AttendeesService,
    attendees_repo_mock: AttendeesRepoMock,
    attendee_mock: Attendee,
    background_tasks_mock: BackgroundTasksMock,
    tickets_service_mock: TicketsServiceMock,
) -> None:
    req = AttendeePostReqData(
        name=attendee_mock.name,
        email=attendee_mock.email,
        has_paid=attendee_mock.has_paid,
        ticket_type=attendee_mock.ticket_type,
    )

    tickets_service_mock.create.return_value = Ok((PASS_DATA, SERIAL, GOOGLE_URL))
    attendees_repo_mock.create.return_value = Ok(attendee_mock)

    result = await attendees_service.create(
        name=attendee_mock.name,
        email=attendee_mock.email,
        has_paid=attendee_mock.has_paid,
        ticket_type=attendee_mock.ticket_type,
        background_tasks=background_tasks_mock,
    )

    assert result.is_ok()
    attendees_repo_mock.create.assert_awaited_once()
    tickets_service_mock.create.assert_awaited_once()

    assert attendees_repo_mock.create.call_args is not None
    attendee = attendees_repo_mock.create.call_args.args[0]
    assert isinstance(attendee, Attendee)
    assert attendee.name == req.name
    assert attendee.email == req.email
    assert attendee.has_paid == req.has_paid
    assert attendee.ticket_type == req.ticket_type


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    attendees_service: AttendeesService,
    attendees_repo_mock: AttendeesRepoMock,
    attendee_mock: Attendee,
    tickets_service_mock: TicketsServiceMock,
    mail_service_mock: MailServiceMock,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    updated = Attendee(
        name="New name",
        email=attendee_mock.email,
        has_paid=attendee_mock.has_paid,
        ticket_type=attendee_mock.ticket_type,
    )

    tickets_service_mock.update.return_value = Ok(None)
    attendees_repo_mock.fetch_by_id.return_value = Ok(attendee_mock)
    attendees_repo_mock.update.return_value = Ok(updated)
    mail_service_mock.send_update_email_with_ticket.return_value = Ok(attendee_mock.ticket_serial_number)

    result = await attendees_service.update(
        attendee_id=str(attendee_mock.id),
        name=attendee_mock.name,
        email=attendee_mock.email,
        has_paid=attendee_mock.has_paid,
        ticket_type=attendee_mock.ticket_type,
        background_tasks=background_tasks_mock,
    )

    assert result.is_ok()
    attendees_repo_mock.update.assert_awaited_once()
    tickets_service_mock.update.assert_awaited_once()

    assert attendees_repo_mock.update.call_args is not None
    assert attendees_repo_mock.update.call_args.args[0] == str(attendee_mock.id)

    body = result.ok_value
    assert body.name == updated.name
    assert body.email == updated.email
    assert body.has_paid == updated.has_paid
    assert body.ticket_type == updated.ticket_type


@pytest.mark.asyncio
async def test_delete_calls_repo(
    attendees_service: AttendeesService,
    attendees_repo_mock: AttendeesRepoMock,
    attendee_mock: Attendee,
    tickets_service_mock: TicketsServiceMock,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    attendees_repo_mock.fetch_by_id.return_value = Ok(attendee_mock)
    attendees_repo_mock.delete.return_value = Ok(attendee_mock)
    tickets_service_mock.delete.return_value = Ok(None)

    result = await attendees_service.delete(str(attendee_mock.id))

    assert result.is_ok()

    attendees_repo_mock.delete.assert_awaited_once_with(str(attendee_mock.id))
    tickets_service_mock.delete.assert_awaited_once()
