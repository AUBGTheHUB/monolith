from result import Result, Err

from src.database.model.admin.team_member_model import TeamMember, UpdateTeamMemberParams
from src.database.repository.admin.team_members_repository import TeamMembersRepository


class TeamMembersService:
    def __init__(self, repo: TeamMembersRepository) -> None:
        self._repo = repo

    async def list(self) -> Result[list[TeamMember], Exception]:
        return Err(NotImplementedError())

    async def get(self, member_id: str) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())

    async def create(self, member: TeamMember) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())

    async def update(self, member_id: str, params: UpdateTeamMemberParams) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())

    async def delete(self, member_id: str) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())
