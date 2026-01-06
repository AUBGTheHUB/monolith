from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.admin.past_event_schemas import (
    PastEventPostReqData,
    PastEventPutReqData,
)
from src.server.schemas.response_schemas.admin.past_event_schemas import (
    AllPastEventsResponse,
    PastEventResponse,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.past_events_service import PastEventsService


class PastEventsHandlers(BaseHandler):
    def __init__(self, service: PastEventsService) -> None:
        self._service = service

    async def create_past_event(self, req_data: PastEventPostReqData) -> Response:
        result = await self._service.create(req_data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=201,
        )

    async def get_all_past_events(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=AllPastEventsResponse(past_events=result.ok_value),
            status_code=200,
        )

    async def get_past_event(self, id: str) -> Response:
        result = await self._service.get(id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=200,
        )

    async def update_past_event(self, id: str, req_data: PastEventPutReqData) -> Response:
        result = await self._service.update(id, req_data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=200,
        )

    async def delete_past_event(self, id: str) -> Response:
        result = await self._service.delete(id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=200,
        )
