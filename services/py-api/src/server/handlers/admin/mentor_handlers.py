from typing import Annotated

from fastapi import UploadFile, Form
from pydantic import StringConstraints, HttpUrl

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.mentors_service import MentorsService

from result import is_err

from src.server.schemas.response_schemas.admin.mentor_schemas import MentorResponse, MentorsResponse


class MentorsHandlers(BaseHandler):
    def __init__(self, service: MentorsService) -> None:
        self._service = service

    async def create_mentor(
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

        return Response(MentorResponse(mentor=result.ok_value), status_code=201)

    async def get_all_mentors(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(MentorsResponse(mentors=result.ok_value), status_code=200)

    async def get_mentor(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(MentorResponse(mentor=result.ok_value), status_code=200)

    async def update_mentor(
        self,
        object_id: str,
        name: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        company: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        job_title: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        avatar: Annotated[UploadFile | None, Form()] = None,
        linkedin_url: Annotated[HttpUrl | None, Form()] = None,
    ) -> Response:
        result = await self._service.update(object_id, name, company, job_title, avatar, linkedin_url)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(MentorResponse(mentor=result.ok_value), status_code=200)

    async def delete_mentor(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(MentorResponse(mentor=result.ok_value), status_code=200)
