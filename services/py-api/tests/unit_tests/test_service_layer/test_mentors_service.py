from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.repository.admin.mentors_repository import MentorsRepository
from src.exception import MentorNotFoundError
from src.server.schemas.request_schemas.admin.mentor_schemas import (
    MentorPostReqData,
    MentorPatchReqData,
)
from src.service.admin.mentors_service import MentorsService
from tests.unit_tests.conftest import MentorsRepoMock


@pytest.fixture
def mentors_service(mentors_repo_mock: MentorsRepoMock) -> MentorsService:
    return MentorsService(cast(MentorsRepository, mentors_repo_mock))


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    mentors_service: MentorsService, mentors_repo_mock: MentorsRepoMock, mentor_mock: Mentor
) -> None:
    mentors = [mentor_mock]
    mentors_repo_mock.fetch_all.return_value = Ok(mentors)

    result = await mentors_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == mentors
    mentors_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    mentors_service: MentorsService, mentors_repo_mock: MentorsRepoMock, mentor_mock: Mentor
) -> None:
    mentors_repo_mock.fetch_by_id.return_value = Ok(mentor_mock)

    result = await mentors_service.get(str(mentor_mock.id))

    assert result.is_ok()
    assert result.unwrap() == mentor_mock
    mentors_repo_mock.fetch_by_id.assert_awaited_once_with(str(mentor_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    mentors_service: MentorsService, mentors_repo_mock: MentorsRepoMock
) -> None:
    mentors_repo_mock.fetch_by_id.return_value = Err(MentorNotFoundError())

    result = await mentors_service.get("missing mentor")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), MentorNotFoundError)
    mentors_repo_mock.fetch_by_id.assert_awaited_once_with("missing mentor")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    mentors_service: MentorsService, mentors_repo_mock: MentorsRepoMock, mentor_mock: Mentor
) -> None:
    req = MentorPostReqData(
        name=mentor_mock.name,
        company=mentor_mock.company,
        job_title=mentor_mock.job_title,
        avatar_url=mentor_mock.avatar_url,
        expertise_areas=mentor_mock.expertise_areas,
        linkedin_url=mentor_mock.linkedin_url,
    )

    mentors_repo_mock.create.return_value = Ok(mentor_mock)

    result = await mentors_service.create(req)

    assert result.is_ok()
    mentors_repo_mock.create.assert_awaited_once()

    assert mentors_repo_mock.create.call_args is not None
    mentor = mentors_repo_mock.create.call_args.args[0]
    assert isinstance(mentor, Mentor)
    assert mentor.name == req.name
    assert mentor.company == req.company
    assert mentor.job_title == req.job_title
    assert mentor.avatar_url == str(req.avatar_url)


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    mentors_service: MentorsService, mentors_repo_mock: MentorsRepoMock, mentor_mock: Mentor
) -> None:
    req = MentorPatchReqData(
        name=mentor_mock.name,
        company=mentor_mock.company,
        job_title=mentor_mock.job_title,
        avatar_url=mentor_mock.avatar_url,
        expertise_areas=mentor_mock.expertise_areas,
        linkedin_url=mentor_mock.linkedin_url,
    )
    updated = Mentor(
        name="New name",
        company=mentor_mock.company,
        job_title=mentor_mock.job_title,
        avatar_url=mentor_mock.avatar_url,
        expertise_areas=mentor_mock.expertise_areas,
        linkedin_url=mentor_mock.linkedin_url,
    )

    mentors_repo_mock.update.return_value = Ok(updated)

    result = await mentors_service.update(mentor_mock.id, req)

    assert result.is_ok()
    mentors_repo_mock.update.assert_awaited_once()

    assert mentors_repo_mock.update.call_args is not None
    assert mentors_repo_mock.update.call_args.args[0] == mentor_mock.id
    updated_params = mentors_repo_mock.update.call_args.args[1]
    assert isinstance(updated_params, UpdateMentorParams)
    assert updated_params.name == req.name
    assert updated_params.company == req.company
    assert updated_params.job_title == req.job_title
    assert updated_params.avatar_url == str(req.avatar_url)


@pytest.mark.asyncio
async def test_delete_calls_repo(
    mentors_service: MentorsService, mentors_repo_mock: MentorsRepoMock, mentor_mock: Mentor
) -> None:
    mentors_repo_mock.delete.return_value = Ok(mentor_mock)

    result = await mentors_service.delete(str(mentor_mock.id))

    assert result.is_ok()
    mentors_repo_mock.delete.assert_awaited_once_with(str(mentor_mock.id))
