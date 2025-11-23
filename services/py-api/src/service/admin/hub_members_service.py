from result import Result, Err

from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.repository.admin.hub_members_repository import HubMembersRepository


class HubMembersService:
    def __init__(self, repo: HubMembersRepository) -> None:
        self._repo = repo

    async def list(self) -> Result[list[HubMember], Exception]:
        return Err(NotImplementedError())

    async def get(self, member_id: str) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def create(self, member: HubMember) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def update(self, member_id: str, params: UpdateHubMemberParams) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def delete(self, member_id: str) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())
