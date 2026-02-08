from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.admin.judge_schemas import JudgePostReqData, JudgePatchReqData
from src.server.schemas.response_schemas.admin.judge_schemas import JudgeResponse, JudgesResponse
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.judges_service import JudgesService


class JudgesHandlers(BaseHandler):
    def __init__(self, service: JudgesService) -> None:
        self._service = service

    async def create_judge(self, judge: JudgePostReqData) -> Response:
        result = await self._service.create(judge)

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

    async def update_judge(self, object_id: str, data: JudgePatchReqData) -> Response:
        result = await self._service.update(object_id, data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgeResponse(judge=result.ok_value), status_code=200)

    async def delete_judge(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(JudgeResponse(judge=result.ok_value), status_code=200)
