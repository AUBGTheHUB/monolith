from __future__ import annotations

from typing import cast

import pytest
from fastapi import UploadFile
from result import Err, Ok

from src.database.model.admin.judge_model import Judge
from src.exception import JudgeNotFoundError
from src.server.handlers.admin.judges_handlers import JudgesHandlers
from src.server.schemas.request_schemas.admin.judge_schemas import (
    JudgePostReqData,
    JudgePatchReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.judges_service import JudgesService
from tests.unit_tests.conftest import JudgesServiceMock


@pytest.fixture
def judges_handlers(judges_service_mock: JudgesServiceMock) -> JudgesHandlers:
    return JudgesHandlers(cast(JudgesService, judges_service_mock))


@pytest.mark.asyncio
async def test_create_judge_returns_201(
    judges_handlers: JudgesHandlers,
    judges_service_mock: JudgesServiceMock,
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

    judges_service_mock.create.return_value = Ok(judge_mock)

    resp = await judges_handlers.create_judge(
        name=judge_mock.name,
        company=judge_mock.company,
        job_title=judge_mock.job_title,
        linkedin_url=judge_mock.linkedin_url,
        avatar=image_mock,
    )

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    judges_service_mock.create.assert_awaited_once_with(
        judge_mock.name,
        judge_mock.company,
        judge_mock.job_title,
        judge_mock.linkedin_url,
        image_mock,
    )


@pytest.mark.asyncio
async def test_get_all_judges_returns_200(
    judges_handlers: JudgesHandlers,
    judges_service_mock: JudgesServiceMock,
    judge_mock: Judge,
) -> None:
    judges_service_mock.get_all.return_value = Ok([judge_mock])

    resp = await judges_handlers.get_all_judges()

    assert resp.status_code == 200
    judges_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_judge_returns_200(
    judges_handlers: JudgesHandlers,
    judges_service_mock: JudgesServiceMock,
    judge_mock: Judge,
) -> None:
    judges_service_mock.get.return_value = Ok(judge_mock)

    resp = await judges_handlers.get_judge(str(judge_mock.id))

    assert resp.status_code == 200
    judges_service_mock.get.assert_awaited_once_with(str(judge_mock.id))


@pytest.mark.asyncio
async def test_update_judge_returns_200(
    judges_handlers: JudgesHandlers,
    judges_service_mock: JudgesServiceMock,
    judge_mock: Judge,
    image_mock: UploadFile,
) -> None:
    req = JudgePatchReqData(
        name=judge_mock.name,
        company=judge_mock.company,
        job_title=judge_mock.job_title,
        linkedin_url=judge_mock.linkedin_url,
        avatar=image_mock,
    )

    judges_service_mock.update.return_value = Ok(judge_mock)

    resp = await judges_handlers.update_judge(
        object_id=str(judge_mock.id),
        name=judge_mock.name,
        company=judge_mock.company,
        job_title=judge_mock.job_title,
        linkedin_url=judge_mock.linkedin_url,
        avatar=image_mock,
    )

    assert resp.status_code == 200
    judges_service_mock.update.assert_awaited_once_with(
        str(judge_mock.id),
        judge_mock.name,
        judge_mock.company,
        judge_mock.job_title,
        judge_mock.linkedin_url,
        image_mock,
    )


@pytest.mark.asyncio
async def test_delete_judge_returns_200(
    judges_handlers: JudgesHandlers,
    judges_service_mock: JudgesServiceMock,
    judge_mock: Judge,
) -> None:
    judges_service_mock.delete.return_value = Ok(judge_mock)

    resp = await judges_handlers.delete_judge(str(judge_mock.id))

    assert resp.status_code == 200
    judges_service_mock.delete.assert_awaited_once_with(str(judge_mock.id))


@pytest.mark.asyncio
async def test_get_judge_returns_404_when_missing(
    judges_handlers: JudgesHandlers, judges_service_mock: JudgesServiceMock
) -> None:
    # Assuming JudgeNotFoundError is the relevant exception
    judges_service_mock.get.return_value = Err(JudgeNotFoundError())

    resp = await judges_handlers.get_judge("missing judge")

    assert resp.status_code == 404
    judges_service_mock.get.assert_awaited_once_with("missing judge")
