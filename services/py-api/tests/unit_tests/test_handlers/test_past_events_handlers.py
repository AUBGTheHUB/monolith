from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.past_event_model import PastEvent
from src.exception import PastEventNotFoundError
from src.server.handlers.admin.past_events_handlers import PastEventsHandlers
from src.server.schemas.request_schemas.admin.past_event_schemas import (
    PastEventPostReqData,
    PastEventPutReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.past_events_service import PastEventsService
from tests.unit_tests.conftest import PastEventsServiceMock


@pytest.fixture
def past_events_handlers(past_events_service_mock: PastEventsServiceMock) -> PastEventsHandlers:
    return PastEventsHandlers(cast(PastEventsService, past_events_service_mock))


@pytest.mark.asyncio
async def test_create_past_event_returns_201(
    past_events_handlers: PastEventsHandlers, past_events_service_mock: PastEventsServiceMock
) -> None:
    req = PastEventPostReqData(title="t", cover_picture="https://example.com/img.jpg", tags=["x"])
    event = PastEvent(title="t", cover_picture="https://example.com/img.jpg", tags=["x"])

    past_events_service_mock.create.return_value = Ok(event)

    resp = await past_events_handlers.create_past_event(req)

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    past_events_service_mock.create.assert_awaited_once_with(req)


@pytest.mark.asyncio
async def test_get_all_past_events_returns_200(
    past_events_handlers: PastEventsHandlers, past_events_service_mock: PastEventsServiceMock
) -> None:
    events = [PastEvent(title="t", cover_picture="https://example.com/img.jpg", tags=[])]
    past_events_service_mock.get_all.return_value = Ok(events)

    resp = await past_events_handlers.get_all_past_events()

    assert resp.status_code == 200
    past_events_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_past_event_returns_200(
    past_events_handlers: PastEventsHandlers, past_events_service_mock: PastEventsServiceMock
) -> None:
    event_id = "507f1f77bcf86cd799439011"
    event = PastEvent(title="t", cover_picture="https://example.com/img.jpg", tags=[])

    past_events_service_mock.get.return_value = Ok(event)

    resp = await past_events_handlers.get_past_event(event_id)

    assert resp.status_code == 200
    past_events_service_mock.get.assert_awaited_once_with(event_id)


@pytest.mark.asyncio
async def test_update_past_event_returns_200(
    past_events_handlers: PastEventsHandlers, past_events_service_mock: PastEventsServiceMock
) -> None:
    event_id = "507f1f77bcf86cd799439011"
    req = PastEventPutReqData(title="new", cover_picture="https://example.com/img2.jpg", tags=["t2"])
    updated = PastEvent(title="new", cover_picture="https://example.com/img2.jpg", tags=["t2"])

    past_events_service_mock.update.return_value = Ok(updated)

    resp = await past_events_handlers.update_past_event(event_id, req)

    assert resp.status_code == 200
    past_events_service_mock.update.assert_awaited_once_with(event_id, req)


@pytest.mark.asyncio
async def test_delete_past_event_returns_200(
    past_events_handlers: PastEventsHandlers, past_events_service_mock: PastEventsServiceMock
) -> None:
    event_id = "507f1f77bcf86cd799439011"
    deleted = PastEvent(title="t", cover_picture="https://example.com/img.jpg", tags=[])

    past_events_service_mock.delete.return_value = Ok(deleted)

    resp = await past_events_handlers.delete_past_event(event_id)

    assert resp.status_code == 200
    past_events_service_mock.delete.assert_awaited_once_with(event_id)


@pytest.mark.asyncio
async def test_get_past_event_returns_404_when_missing(
    past_events_handlers: PastEventsHandlers, past_events_service_mock: PastEventsServiceMock
) -> None:
    event_id = "507f1f77bcf86cd799439011"
    past_events_service_mock.get.return_value = Err(PastEventNotFoundError())

    resp = await past_events_handlers.get_past_event(event_id)

    assert resp.status_code == 404
    past_events_service_mock.get.assert_awaited_once_with(event_id)
