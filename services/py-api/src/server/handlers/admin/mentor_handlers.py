from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.mentors_service import MentorsService


class MentorsHandlers(BaseHandler):
    def __init__(self, service: MentorsService) -> None:
        self._service = service

    async def create_mentor(self) -> Response:
        raise NotImplementedError()

    async def get_all_mentors(self) -> Response:
        raise NotImplementedError()

    async def get_mentor(self, mentor_id: str) -> Response:
        raise NotImplementedError()

    async def update_mentor(self, mentor_id: str) -> Response:
        raise NotImplementedError()

    async def delete_mentor(self, mentor_id: str) -> Response:
        raise NotImplementedError()
