from src.database.model.admin.hub_admin_model import HubAdmin, UpdateHubAdminParams, AssignableRole
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.exception import HubMemberNotFoundError
from result import Result


class UserService:
    def __init__(
        self,
        hub_members_repo: HubMembersRepository,
    ) -> None:
        self._hub_members_repo = hub_members_repo

    async def change_role(
        self, user_id: str, new_role: AssignableRole
    ) -> Result[HubAdmin, HubMemberNotFoundError | Exception]:
        update_params = UpdateHubAdminParams(site_role=new_role)
        return await self._hub_members_repo.update(user_id, update_params)
