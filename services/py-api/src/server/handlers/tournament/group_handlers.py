from typing import cast

from result import Err, Ok
from starlette import status

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

        match result:
            case Err(error):
                return self.handle_error(cast(BaseException, error))
            case Ok(groups):
                return Response(
                    AllGroupsResponse(groups=groups),
                    status_code=status.HTTP_200_OK,
                )
        return self.handle_error(RuntimeError("Unexpected result while fetching all groups"))

    async def get_group(self, group_id: str) -> Response:
        result = await self._group_service.fetch_group_by_id(group_id)

        match result:
            case Err(error):
                return self.handle_error(cast(BaseException, error.err_value))
            case Ok(group):
                return Response(
                    GroupResponse(group=group),
                    status_code=status.HTTP_200_OK,
                )
        return self.handle_error(RuntimeError("Unexpected result while fetching group"))

    async def generate_bracket(self) -> Response:
        result = await self._group_service.generate_bracket()

        match result:
            case Err(error):
                return self.handle_error(cast(BaseException, error))
            case Ok(groups):
                return Response(
                    AllGroupsResponse(groups=groups),
                    status_code=status.HTTP_200_OK,
                )
        return self.handle_error(RuntimeError("Unexpected result while generating bracket"))

    async def get_inactive_groups(self) -> Response:
        result = await self._group_service.fetch_inactive_groups()

        match result:
            case Err(error):
                return self.handle_error(cast(BaseException, error))
            case Ok(groups):
                return Response(
                    AllGroupsResponse(groups=groups),
                    status_code=status.HTTP_200_OK,
                )
        return self.handle_error(RuntimeError("Unexpected result while fetching inactive groups"))

    async def get_active_groups(self) -> Response:
        result = await self._group_service.fetch_active_groups()

        match result:
            case Err(error):
                return self.handle_error(cast(BaseException, error))
            case Ok(groups):
                return Response(
                    AllGroupsResponse(groups=groups),
                    status_code=status.HTTP_200_OK,
                )
        return self.handle_error(RuntimeError("Unexpected result while fetching active groups"))

    async def declare_winner(
        self,
        group_id: str,
        winner_id: str,
    ) -> Response:
        result = await self._group_service.declare_winner(
            group_id=group_id,
            winner_id=winner_id,
        )

        match result:
            case Err(error):
                return self.handle_error(cast(BaseException, error))
            case Ok(group):
                return Response(
                    GroupResponse(group=group),
                    status_code=status.HTTP_200_OK,
                )
        return self.handle_error(RuntimeError("Unexpected result while declaring winner"))
