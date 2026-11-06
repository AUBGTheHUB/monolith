from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from server.schemas.request_schemas.event.attendee_schemas import AttendeePostReqData, AttendeePatchReqData
from src.database.model.event.attendee_model import Attendee
from src.exception import AttendeeNotFoundError
from src.server.handlers.event.attendees_handlers import AttendeesHandlers
from src.server.schemas.response_schemas.schemas import Response
from src.service.event.attendees_service import AttendeesService
from tests.unit_tests.conftest import AttendeesServiceMock, BackgroundTasksMock


@pytest.fixture
def attendees_handlers(attendees_service_mock: AttendeesServiceMock) -> AttendeesHandlers:
    return AttendeesHandlers(cast(AttendeesService, attendees_service_mock))


@pytest.mark.asyncio
async def test_create_attendee_returns_201(
    attendees_handlers: AttendeesHandlers,
    attendees_service_mock: AttendeesServiceMock,
    attendee_mock: Attendee,
    attendee_post_mock: AttendeePostReqData,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    attendees_service_mock.create.return_value = Ok(attendee_mock)

    resp = await attendees_handlers.create_attendee(attendee=attendee_post_mock, background_tasks=background_tasks_mock)

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    attendees_service_mock.create.assert_awaited_once_with(
        name=attendee_mock.name,
        email=attendee_mock.email,
        has_paid=attendee_mock.has_paid,
        ticket_type=attendee_mock.ticket_type,
        background_tasks=background_tasks_mock,
    )


@pytest.mark.asyncio
async def test_get_all_attendees_returns_200(
    attendees_handlers: AttendeesHandlers,
    attendees_service_mock: AttendeesServiceMock,
    attendee_mock: Attendee,
) -> None:
    attendees_service_mock.get_all.return_value = Ok([attendee_mock])

    resp = await attendees_handlers.get_all_attendees()

    assert resp.status_code == 200
    attendees_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_attendee_returns_200(
    attendees_handlers: AttendeesHandlers,
    attendees_service_mock: AttendeesServiceMock,
    attendee_mock: Attendee,
) -> None:
    attendees_service_mock.get.return_value = Ok(attendee_mock)

    resp = await attendees_handlers.get_attendee(str(attendee_mock.id))

    assert resp.status_code == 200
    attendees_service_mock.get.assert_awaited_once_with(str(attendee_mock.id))


@pytest.mark.asyncio
async def test_update_attendee_returns_200(
    attendees_handlers: AttendeesHandlers,
    attendees_service_mock: AttendeesServiceMock,
    attendee_mock: Attendee,
    attendee_patch_mock: AttendeePatchReqData,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    attendees_service_mock.update.return_value = Ok(attendee_mock)

    resp = await attendees_handlers.update_attendee(
        object_id=str(attendee_mock.id), attendee=attendee_patch_mock, background_tasks=background_tasks_mock
    )

    assert resp.status_code == 200
    attendees_service_mock.update.assert_awaited_once_with(
        attendee_id=str(attendee_mock.id),
        name=attendee_mock.name,
        email=attendee_mock.email,
        has_paid=attendee_mock.has_paid,
        ticket_type=attendee_mock.ticket_type,
        background_tasks=background_tasks_mock,
    )


@pytest.mark.asyncio
async def test_delete_attendee_returns_200(
    attendees_handlers: AttendeesHandlers,
    attendees_service_mock: AttendeesServiceMock,
    attendee_mock: Attendee,
) -> None:
    attendees_service_mock.delete.return_value = Ok(attendee_mock)

    resp = await attendees_handlers.delete_attendee(str(attendee_mock.id))

    assert resp.status_code == 200
    attendees_service_mock.delete.assert_awaited_once_with(str(attendee_mock.id))


@pytest.mark.asyncio
async def test_get_attendee_returns_404_when_missing(
    attendees_handlers: AttendeesHandlers, attendees_service_mock: AttendeesServiceMock
) -> None:
    attendees_service_mock.get.return_value = Err(AttendeeNotFoundError())

    resp = await attendees_handlers.get_attendee("missing attendee")

    assert resp.status_code == 404
    attendees_service_mock.get.assert_awaited_once_with("missing attendee")
