from __future__ import annotations

from typing import cast

import pytest
from fastapi import UploadFile
from result import Err, Ok

from src.database.model.admin.past_event_model import PastEvent
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.exception import PastEventNotFoundError
from src.service.admin.past_events_service import PastEventsService
from src.service.utility.image_storing.image_storing_service import ImageStoringService
from tests.unit_tests.conftest import PastEventsRepoMock, ImageStoringServiceMock


@pytest.fixture
def past_events_service(
    past_events_repo_mock: PastEventsRepoMock, image_storing_service_mock: ImageStoringServiceMock
) -> PastEventsService:
    return PastEventsService(
        cast(PastEventsRepository, past_events_repo_mock), cast(ImageStoringService, image_storing_service_mock)
    )


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    past_events_service: PastEventsService,
    past_events_repo_mock: PastEventsRepoMock,
    past_event_mock: PastEvent,
) -> None:
    events = [past_event_mock]
    past_events_repo_mock.fetch_all.return_value = Ok(events)

    result = await past_events_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == events
    past_events_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    past_events_service: PastEventsService,
    past_events_repo_mock: PastEventsRepoMock,
    past_event_mock: PastEvent,
) -> None:
    past_events_repo_mock.fetch_by_id.return_value = Ok(past_event_mock)

    result = await past_events_service.get(str(past_event_mock.id))

    assert result.is_ok()
    assert result.unwrap() == past_event_mock
    past_events_repo_mock.fetch_by_id.assert_awaited_once_with(str(past_event_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    past_events_service: PastEventsService, past_events_repo_mock: PastEventsRepoMock
) -> None:
    past_events_repo_mock.fetch_by_id.return_value = Err(PastEventNotFoundError())

    result = await past_events_service.get("mii")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), PastEventNotFoundError)
    past_events_repo_mock.fetch_by_id.assert_awaited_once_with("mii")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    past_events_service: PastEventsService,
    past_events_repo_mock: PastEventsRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    past_event_mock: PastEvent,
    image_mock: UploadFile,
) -> None:

    past_events_repo_mock.create.return_value = Ok(past_event_mock)
    image_storing_service_mock.upload_image.return_value = past_event_mock.cover_picture

    result = await past_events_service.create(
        title=past_event_mock.title, cover_picture=image_mock, tags=past_event_mock.tags
    )

    assert result.is_ok()
    past_events_repo_mock.create.assert_awaited_once()

    assert past_events_repo_mock.create.call_args is not None
    passed_event = past_events_repo_mock.create.call_args.args[0]
    assert isinstance(passed_event, PastEvent)
    assert passed_event.title == past_event_mock.title
    assert passed_event.cover_picture == past_event_mock.cover_picture
    assert passed_event.tags == past_event_mock.tags


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    past_events_service: PastEventsService,
    past_events_repo_mock: PastEventsRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    past_event_mock: PastEvent,
    image_mock: UploadFile,
) -> None:
    updated = PastEvent(title="new", cover_picture=str(past_event_mock.cover_picture), tags=past_event_mock.tags)

    past_events_repo_mock.update.return_value = Ok(updated)
    image_storing_service_mock.upload_image.return_value = past_event_mock.cover_picture

    result = await past_events_service.update(
        event_id=str(past_event_mock.id), title=updated.title, cover_picture=image_mock, tags=updated.tags
    )

    assert result.is_ok()
    past_events_repo_mock.update.assert_awaited_once()

    assert past_events_repo_mock.update.call_args is not None
    assert past_events_repo_mock.update.call_args.args[0] == past_event_mock.id

    body = result.ok_value
    assert body.title == updated.title
    assert body.cover_picture == updated.cover_picture
    assert body.tags == updated.tags


@pytest.mark.asyncio
async def test_delete_calls_repo(
    past_events_service: PastEventsService,
    past_events_repo_mock: PastEventsRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    past_event_mock: PastEvent,
) -> None:
    past_events_repo_mock.delete.return_value = Ok(past_event_mock)

    result = await past_events_service.delete(str(past_event_mock.id))

    assert result.is_ok()
    past_events_repo_mock.delete.assert_awaited_once_with(str(past_event_mock.id))
    image_storing_service_mock.delete_image.assert_called_once_with(f"past_events/{str(past_event_mock.id)}")
