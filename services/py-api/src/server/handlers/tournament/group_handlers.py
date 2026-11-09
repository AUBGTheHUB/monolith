from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.server.schemas.response_schemas.tournament.schemas import (
    AllGroupsResponse,
    GroupResponse,
)
from src.service.tournament.group_service import GroupService


class GroupHandlers(BaseHandler):

    def __init__(self, group_service: GroupService) -> None:
        self._group_service = group_service

    async def get_all_groups(self) -> Response:
        result = await self._group_service.fetch_all_groups()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=AllGroupsResponse(groups=result.ok_value),
            status_code=200,
        )

    async def get_group(self, group_id: str) -> Response:
        result = await self._group_service.fetch_group_by_id(group_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=GroupResponse(group=result.ok_value),
            status_code=200,
        )

    async def generate_bracket(self) -> Response:
        result = await self._group_service.generate_bracket()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            AllGroupsResponse(groups=result.ok_value),
            status_code=200,
        )

    async def get_inactive_groups(self) -> Response:
        result = await self._group_service.fetch_inactive_groups()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            AllGroupsResponse(groups=result.ok_value),
            status_code=200,
        )

    async def get_active_groups(self) -> Response:
        result = await self._group_service.fetch_active_groups()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            AllGroupsResponse(groups=result.ok_value),
            status_code=200,
        )

    async def declare_winner(
        self,
        group_id: str,
        winner_id: str,
    ) -> Response:
        result = await self._group_service.declare_winner(
            group_id=group_id,
            winner_id=winner_id,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            GroupResponse(group=result.ok_value),
            status_code=200,
        )
