from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response, ErrResponse
from src.server.schemas.response_schemas.admin.hub_member_schemas import HubMemberResponse, HubMembersListResponse
from src.server.schemas.request_schemas.admin.hub_member_schemas import HubMemberPostReqData, HubMemberPatchReqData
from src.service.admin.hub_members_service import HubMembersService
from starlette import status


class HubMembersHandlers(BaseHandler):
    def __init__(self, service: HubMembersService) -> None:
        self._service = service

    async def create_hub_member(self, data: HubMemberPostReqData) -> Response:
        result = await self._service.create(data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_201_CREATED,
        )

    async def get_all_hub_members(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        members_data = [member.dump_as_json() for member in result.ok_value]
        return Response(
            response_model=HubMembersListResponse(members=members_data),
            status_code=status.HTTP_200_OK,
        )

    async def get_hub_member(self, member_id: str) -> Response:
        result = await self._service.get(member_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_200_OK,
        )

    async def update_hub_member(self, member_id: str, data: HubMemberPatchReqData) -> Response:
        result = await self._service.update(member_id, data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_200_OK,
        )

    async def delete_hub_member(self, member_id: str) -> Response:
        result = await self._service.delete(member_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_200_OK,
        )
