from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.mentors_service import MentorsService

from result import is_err

from src.server.schemas.request_schemas.admin.mentor_schemas import MentorPostReqData, MentorPatchReqData
from src.server.schemas.response_schemas.admin.mentor_schemas import MentorResponse, MentorsResponse


class MentorsHandlers(BaseHandler):
    def __init__(self, service: MentorsService) -> None:
        self._service = service

    async def create_mentor(self, mentor: MentorPostReqData) -> Response:
        result = await self._service.create(mentor)

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

    async def update_mentor(self, object_id: str, mentor_data: MentorPatchReqData) -> Response:
        result = await self._service.update(object_id, mentor_data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(MentorResponse(mentor=result.ok_value), status_code=200)

    async def delete_mentor(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(MentorResponse(mentor=result.ok_value), status_code=200)
