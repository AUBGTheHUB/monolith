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
        
        update_data = {}
        if data.name is not None:
            update_data["name"] = data.name
        if data.role_title is not None:
            update_data["position"] = data.role_title
        if data.department is not None:
            update_data["department"] = data.department
        if data.avatar_url is not None:
            update_data["avatar_url"] = str(data.avatar_url)
        if data.social_links is not None:
            update_data["social_links"] = data.social_links
        
        update_params = UpdateHubMemberParams(**update_data)
        return await self._repo.update(member_id, update_params)

    async def delete(self, member_id: str) -> Result[HubMember, Exception]:
        return await self._repo.delete(member_id)
