from result import Result, Err

from src.database.model.admin.hub_member_model import HubMember
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.server.schemas.admin.request_schemas.schemas import HubMemberPostReqData
from src.server.schemas.admin.request_schemas.schemas import HubMemberPatchReqData


class HubMembersService:
    def __init__(self, repo: HubMembersRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[HubMember], Exception]:
        return Err(NotImplementedError())

    async def get(self, member_id: str) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def create(self, data: HubMemberPostReqData) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def update(self, member_id: str, data: HubMemberPatchReqData) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def delete(self, member_id: str) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())
