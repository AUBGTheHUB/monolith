from result import Result

from src.database.model.admin.hub_member_model import HubMember
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.server.schemas.request_schemas.admin.hub_member_schemas import HubMemberPostReqData, HubMemberPatchReqData


class HubMembersService:
    def __init__(self, repo: HubMembersRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[HubMember], Exception]:
        return await self._repo.fetch_all()

    async def get(self, member_id: str) -> Result[HubMember, Exception]:
        return await self._repo.fetch_by_id(member_id)

    async def create(self, data: HubMemberPostReqData) -> Result[HubMember, Exception]:
        member = HubMember(
            name=data.name,
            position=data.role_title,
            department=data.department,
            avatar_url=str(data.avatar_url),
            social_links=data.social_links,
        )
        return await self._repo.create(member)

    async def update(self, member_id: str, data: HubMemberPatchReqData) -> Result[HubMember, Exception]:
        from src.database.model.admin.hub_member_model import UpdateHubMemberParams
        
        update_data = data.model_dump(exclude_none=True)
        if "role_title" in update_data:
            update_data["position"] = update_data.pop("role_title")
        if "avatar_url" in update_data:
            update_data["avatar_url"] = str(update_data["avatar_url"])
        
        update_params = UpdateHubMemberParams(**update_data)
        return await self._repo.update(member_id, update_params)

    async def delete(self, member_id: str) -> Result[HubMember, Exception]:
        return await self._repo.delete(member_id)
