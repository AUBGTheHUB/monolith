from typing import Annotated

from fastapi import Form, UploadFile
from pydantic import StringConstraints
from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.schemas import NonEmptyStr
from src.server.schemas.response_schemas.admin.past_event_schemas import (
    AllPastEventsResponse,
    PastEventResponse,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.past_events_service import PastEventsService


class PastEventsHandlers(BaseHandler):
    def __init__(self, service: PastEventsService) -> None:
        self._service = service

    async def create_past_event(
        self,
        title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Form(...)],
        cover_picture: Annotated[UploadFile, Form()],
        tags: Annotated[list[NonEmptyStr], Form()] = [],
    ) -> Response:
        result = await self._service.create(title, cover_picture, tags)

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

    async def get_past_event(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=200,
        )

    async def update_past_event(
        self,
        object_id: str,
        title: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        cover_picture: Annotated[UploadFile | None, Form()] = None,
        tags: Annotated[list[NonEmptyStr] | None, Form()] = None,
    ) -> Response:
        result = await self._service.update(object_id, title, cover_picture, tags)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=200,
        )

    async def delete_past_event(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=PastEventResponse(past_event=result.ok_value),
            status_code=200,
        )
