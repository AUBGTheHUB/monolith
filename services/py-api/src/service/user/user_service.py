from src.database.model.admin.hub_admin_model import HubAdmin, UpdateHubAdminParams, AssignableRole
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import HubMemberNotFoundError
from result import Result, is_err
from structlog.stdlib import get_logger

LOG = get_logger()


class UserService:
    def __init__(
        self,
        hub_members_repo: HubMembersRepository,
        refresh_token_repo: RefreshTokenRepository,
    ) -> None:
        self._hub_members_repo = hub_members_repo
        self._refresh_token_repo = refresh_token_repo

    async def change_role(
        self, user_id: str, new_role: AssignableRole
    ) -> Result[HubAdmin, HubMemberNotFoundError | Exception]:
        update_params = UpdateHubAdminParams(site_role=new_role)
        result = await self._hub_members_repo.update(user_id, update_params)
        if is_err(result):
            return result

        invalidation_result = await self._refresh_token_repo.invalidate_all_tokens_by_hub_member_id(user_id)
        if is_err(invalidation_result):
            LOG.error(
                "Failed to invalidate sessions after role change", user_id=user_id, error=invalidation_result.err_value
            )

        return result
