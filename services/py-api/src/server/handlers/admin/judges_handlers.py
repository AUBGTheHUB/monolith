from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.judges_service import JudgesService


class JudgesHandlers(BaseHandler):
    def __init__(self, service: JudgesService) -> None:
        self._service = service

    async def create_judge(self) -> Response:
        raise NotImplementedError()

    async def get_all_judges(self) -> Response:
        raise NotImplementedError()

    async def get_judge(self, judge_id: str) -> Response:
        raise NotImplementedError()

    async def update_judge(self, judge_id: str) -> Response:
        raise NotImplementedError()

    async def delete_judge(self, judge_id: str) -> Response:
        raise NotImplementedError()
