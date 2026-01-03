from src.service.admin.hub_members_service import HubMembersService


# Hub Members Handlers
class HubMembersHandlers(BaseException):
    def __init__(self, service: HubMembersService) -> None:
        self._service = service

    async def create_hub_member(self) -> None:
        raise NotImplementedError()

    async def list_hub_members(self) -> None:
        raise NotImplementedError()

    async def get_hub_member(self, member_id: str) -> None:
        raise NotImplementedError()

    async def update_hub_member(self, member_id: str) -> None:
        raise NotImplementedError()

    async def delete_hub_member(self, member_id: str) -> None:
        raise NotImplementedError()
