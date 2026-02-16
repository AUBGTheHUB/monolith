from __future__ import annotations

from typing import cast

import pytest
from fastapi import UploadFile
from result import Err, Ok

from src.database.model.admin.judge_model import Judge
from src.database.repository.admin.judges_repository import JudgesRepository
from src.exception import JudgeNotFoundError
from src.server.schemas.request_schemas.admin.judge_schemas import (
    JudgePostReqData,
)
from src.service.admin.judges_service import JudgesService
from src.service.utility.image_storing.image_storing_service import ImageStoringService
from tests.unit_tests.conftest import JudgesRepoMock, ImageStoringServiceMock


@pytest.fixture
def judges_service(
    judges_repo_mock: JudgesRepoMock, image_storing_service_mock: ImageStoringServiceMock
) -> JudgesService:
    return JudgesService(
        cast(JudgesRepository, judges_repo_mock), cast(ImageStoringService, image_storing_service_mock)
    )


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    judges_service: JudgesService, judges_repo_mock: JudgesRepoMock, judge_mock: Judge
) -> None:
    judges = [judge_mock]
    judges_repo_mock.fetch_all.return_value = Ok(judges)

    result = await judges_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == judges
    judges_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    judges_service: JudgesService,
    judges_repo_mock: JudgesRepoMock,
    judge_mock: Judge,
) -> None:
    judges_repo_mock.fetch_by_id.return_value = Ok(judge_mock)

    result = await judges_service.get(str(judge_mock.id))

    assert result.is_ok()
    assert result.unwrap() == judge_mock
    judges_repo_mock.fetch_by_id.assert_awaited_once_with(str(judge_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(judges_service: JudgesService, judges_repo_mock: JudgesRepoMock) -> None:
    judges_repo_mock.fetch_by_id.return_value = Err(JudgeNotFoundError())

    result = await judges_service.get("missing judge")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), JudgeNotFoundError)
    judges_repo_mock.fetch_by_id.assert_awaited_once_with("missing judge")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    judges_service: JudgesService,
    judges_repo_mock: JudgesRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    judge_mock: Judge,
    image_mock: UploadFile,
) -> None:
    req = JudgePostReqData(
        name=judge_mock.name,
        company=judge_mock.company,
        job_title=judge_mock.job_title,
        linkedin_url=judge_mock.linkedin_url,
        avatar=image_mock,
    )

    judges_repo_mock.create.return_value = Ok(judge_mock)
    image_storing_service_mock.upload_image.return_value = judge_mock.avatar_url

    result = await judges_service.create(
        name=judge_mock.name,
        company=judge_mock.company,
        job_title=judge_mock.job_title,
        linkedin_url=judge_mock.linkedin_url,
        avatar=image_mock,
    )

    assert result.is_ok()
    judges_repo_mock.create.assert_awaited_once()

    assert judges_repo_mock.create.call_args is not None
    judge = judges_repo_mock.create.call_args.args[0]
    assert isinstance(judge, Judge)
    assert judge.name == req.name
    assert judge.company == req.company
    assert judge.job_title == req.job_title
    assert judge.linkedin_url == str(req.linkedin_url)
    assert judge.avatar_url == judge_mock.avatar_url


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    judges_service: JudgesService, judges_repo_mock: JudgesRepoMock, judge_mock: Judge, image_mock: UploadFile
) -> None:
    updated = Judge(
        id=judge_mock.id,
        name="Updated Name",
        company=judge_mock.company,
        job_title="Updated Title",
        linkedin_url=judge_mock.linkedin_url,
        avatar_url=str(judge_mock.avatar_url),
    )

    judges_repo_mock.update.return_value = Ok(updated)

    result = await judges_service.update(
        judge_id=str(judge_mock.id),
        name="Updated Name",
        company=judge_mock.company,
        job_title="Updated Title",
        linkedin_url=judge_mock.linkedin_url,
        avatar=image_mock,
    )

    assert result.is_ok()
    judges_repo_mock.update.assert_awaited_once()

    assert judges_repo_mock.update.call_args is not None
    assert judges_repo_mock.update.call_args.args[0] == judge_mock.id

    body = result.ok_value
    assert body.name == updated.name
    assert body.company == updated.company
    assert body.job_title == updated.job_title
    assert body.linkedin_url == updated.linkedin_url


@pytest.mark.asyncio
async def test_delete_calls_repo(
    judges_service: JudgesService,
    judges_repo_mock: JudgesRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    judge_mock: Judge,
) -> None:
    judges_repo_mock.delete.return_value = Ok(judge_mock)

    result = await judges_service.delete(str(judge_mock.id))

    assert result.is_ok()
    judges_repo_mock.delete.assert_awaited_once_with(str(judge_mock.id))
    image_storing_service_mock.delete_image.assert_called_once_with(f"judges/{str(judge_mock.id)}")
