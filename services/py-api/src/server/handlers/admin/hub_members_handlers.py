from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.hub_members_service import HubMembersService


class HubMembersHandlers(BaseHandler):
    def __init__(self, service: HubMembersService) -> None:
        self._service = service

    async def create_hub_member(self) -> Response:
        raise NotImplementedError()

    async def get_all_hub_members(self) -> Response:
        raise NotImplementedError()

    async def get_hub_member(self, member_id: str) -> Response:
        raise NotImplementedError()

    async def update_hub_member(self, member_id: str) -> Response:
        raise NotImplementedError()

    async def delete_hub_member(self, member_id: str) -> Response:
        raise NotImplementedError()
