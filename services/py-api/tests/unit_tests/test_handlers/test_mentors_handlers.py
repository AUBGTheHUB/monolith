from __future__ import annotations

from typing import cast

import pytest
from fastapi import UploadFile
from result import Err, Ok

from src.database.model.admin.mentor_model import Mentor
from src.exception import MentorNotFoundError
from src.server.handlers.admin.mentor_handlers import MentorsHandlers
from src.server.schemas.request_schemas.admin.mentor_schemas import (
    MentorPatchReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.mentors_service import MentorsService


class MentorsServiceMock:
    """Protocol mock for MentorsService"""

    def __init__(self) -> None:
        from unittest.mock import AsyncMock

        self.get_all = AsyncMock()
        self.get = AsyncMock()
        self.create = AsyncMock()
        self.update = AsyncMock()
        self.delete = AsyncMock()


@pytest.fixture
def mentors_service_mock() -> MentorsServiceMock:
    return MentorsServiceMock()


@pytest.fixture
def mentors_handlers(mentors_service_mock: MentorsServiceMock) -> MentorsHandlers:
    return MentorsHandlers(cast(MentorsService, mentors_service_mock))


@pytest.mark.asyncio
async def test_create_mentor_returns_201(
    mentors_handlers: MentorsHandlers,
    mentors_service_mock: MentorsServiceMock,
    mentor_mock: Mentor,
    image_mock: UploadFile,
) -> None:

    mentors_service_mock.create.return_value = Ok(mentor_mock)

    resp = await mentors_handlers.create_mentor(
        name=mentor_mock.name,
        company=mentor_mock.company,
        job_title=mentor_mock.job_title,
        avatar=image_mock,
        linkedin_url=mentor_mock.linkedin_url,
    )

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    mentors_service_mock.create.assert_awaited_once_with(
        mentor_mock.name, mentor_mock.company, mentor_mock.job_title, image_mock, mentor_mock.linkedin_url
    )


@pytest.mark.asyncio
async def test_get_all_mentors_returns_200(
    mentors_handlers: MentorsHandlers,
    mentors_service_mock: MentorsServiceMock,
    mentor_mock: Mentor,
) -> None:
    mentors_service_mock.get_all.return_value = Ok([mentor_mock])

    resp = await mentors_handlers.get_all_mentors()

    assert resp.status_code == 200
    mentors_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_mentor_returns_200(
    mentors_handlers: MentorsHandlers,
    mentors_service_mock: MentorsServiceMock,
    mentor_mock: Mentor,
) -> None:
    mentors_service_mock.get.return_value = Ok(mentor_mock)

    resp = await mentors_handlers.get_mentor(str(mentor_mock.id))

    assert resp.status_code == 200
    mentors_service_mock.get.assert_awaited_once_with(str(mentor_mock.id))


@pytest.mark.asyncio
async def test_update_mentor_returns_200(
    mentors_handlers: MentorsHandlers,
    mentors_service_mock: MentorsServiceMock,
    mentor_mock: Mentor,
    image_mock: UploadFile,
) -> None:
    req = MentorPatchReqData(
        name=mentor_mock.name,
        company=mentor_mock.company,
        job_title=mentor_mock.job_title,
        avatar=image_mock,
        linkedin_url=mentor_mock.linkedin_url,
    )

    mentors_service_mock.update.return_value = Ok(mentor_mock)

    resp = await mentors_handlers.update_mentor(
        object_id=str(mentor_mock.id),
        name=mentor_mock.name,
        company=mentor_mock.company,
        job_title=mentor_mock.job_title,
        avatar=image_mock,
        linkedin_url=mentor_mock.linkedin_url,
    )

    assert resp.status_code == 200
    mentors_service_mock.update.assert_awaited_once_with(
        str(mentor_mock.id),
        mentor_mock.name,
        mentor_mock.company,
        mentor_mock.job_title,
        image_mock,
        mentor_mock.linkedin_url,
    )


@pytest.mark.asyncio
async def test_delete_mentor_returns_200(
    mentors_handlers: MentorsHandlers,
    mentors_service_mock: MentorsServiceMock,
    mentor_mock: Mentor,
) -> None:
    mentors_service_mock.delete.return_value = Ok(mentor_mock)

    resp = await mentors_handlers.delete_mentor(str(mentor_mock.id))

    assert resp.status_code == 200
    mentors_service_mock.delete.assert_awaited_once_with(str(mentor_mock.id))


@pytest.mark.asyncio
async def test_get_mentor_returns_404_when_missing(
    mentors_handlers: MentorsHandlers, mentors_service_mock: MentorsServiceMock
) -> None:
    mentors_service_mock.get.return_value = Err(MentorNotFoundError())

    resp = await mentors_handlers.get_mentor("missing mentor")

    assert resp.status_code == 404
    mentors_service_mock.get.assert_awaited_once_with("missing mentor")


@pytest.mark.asyncio
async def test_update_mentor_returns_404_when_not_found(
    mentors_handlers: MentorsHandlers, mentors_service_mock: MentorsServiceMock
) -> None:
    mentors_service_mock.update.return_value = Err(MentorNotFoundError())

    resp = await mentors_handlers.update_mentor(object_id="missing mentor", name="Jane Updated")

    assert resp.status_code == 404
    mentors_service_mock.update.assert_awaited_once_with("missing mentor", "Jane Updated")


@pytest.mark.asyncio
async def test_delete_mentor_returns_404_when_not_found(
    mentors_handlers: MentorsHandlers, mentors_service_mock: MentorsServiceMock
) -> None:
    mentors_service_mock.delete.return_value = Err(MentorNotFoundError())

    resp = await mentors_handlers.delete_mentor("missing mentor")

    assert resp.status_code == 404
    mentors_service_mock.delete.assert_awaited_once_with("missing mentor")
