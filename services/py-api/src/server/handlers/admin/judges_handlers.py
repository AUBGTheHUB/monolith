from typing import Annotated

from fastapi import Form, UploadFile
from pydantic import StringConstraints, HttpUrl
from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.admin.judge_schemas import JudgeResponse, JudgesResponse
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.judges_service import JudgesService


class JudgesHandlers(BaseHandler):
    def __init__(self, service: JudgesService) -> None:
        self._service = service

    async def create_judge(
        self,
        name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Form(...)],
        company: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Form(...)],
        job_title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Form(...)],
        avatar: Annotated[UploadFile, Form()],
        linkedin_url: Annotated[HttpUrl | None, Form()] = None,
    ) -> Response:

        result = await self._service.create(name, company, job_title, avatar, linkedin_url)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgeResponse(judge=result.ok_value), status_code=201)

    async def get_all_judges(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgesResponse(judges=result.ok_value), status_code=200)

    async def get_judge(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgeResponse(judge=result.ok_value), status_code=200)

    async def update_judge(
        self,
        object_id: str,
        name: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        company: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        job_title: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        avatar: Annotated[UploadFile | None, Form()] = None,
        linkedin_url: Annotated[HttpUrl | None, Form()] = None,
    ) -> Response:
        result = await self._service.update(
            judge_id=object_id,
            name=name,
            company=company,
            job_title=job_title,
            avatar=avatar,
            linkedin_url=linkedin_url,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgeResponse(judge=result.ok_value), status_code=200)

    async def delete_judge(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgeResponse(judge=result.ok_value), status_code=200)
