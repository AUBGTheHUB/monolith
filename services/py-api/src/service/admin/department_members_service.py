from result import Result

from src.database.model.admin.department_member_model import DepartmentMember, UpdateDepartmentMemberParams
from src.database.repository.admin.department_members_repository import DepartmentMembersRepository
from src.server.schemas.request_schemas.schemas import AdminDepartmentMemberCreateIn, AdminDepartmentMemberUpdateIn


class DepartmentMembersService:
    def __init__(self, repository: DepartmentMembersRepository) -> None:
        self._repository = repository

    async def create(self, member_in: AdminDepartmentMemberCreateIn) -> Result[DepartmentMember, Exception]:
        member = DepartmentMember(
            name=member_in.name,
            photo_url=member_in.photo_url,
            linkedin_url=member_in.linkedin_url,
            departments=member_in.departments,
        )
        return await self._repository.create(member)

    async def get_all(self) -> Result[list[DepartmentMember], Exception]:
        return await self._repository.fetch_all()

    async def get(self, member_id: str) -> Result[DepartmentMember, Exception]:
        return await self._repository.fetch_by_id(member_id)

    async def update(self, member_id: str, member_in: AdminDepartmentMemberUpdateIn) -> Result[DepartmentMember, Exception]:
        update_params = UpdateDepartmentMemberParams(**member_in.model_dump(exclude_none=True))
        return await self._repository.update(member_id, update_params)

    async def delete(self, member_id: str) -> Result[DepartmentMember, Exception]:
        return await self._repository.delete(member_id)

