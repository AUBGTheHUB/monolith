from typing import List

from result import Result
from src.database.model.admin.department_model import Department, Member, UpdateDepartmentParams
from src.database.repository.admin.departments_repository import DepartmentsRepository
from src.exception import DepartmentNotFoundError


class DepartmentsService:
    def __init__(self, repository: DepartmentsRepository):
        self._repository = repository

    async def create_department(self, department: Department) -> Result[Department, Exception]:
        return await self._repository.create(department)

    async def list_departments(self) -> Result[List[Department], Exception]:
        return await self._repository.fetch_all()

    async def get_department(self, department_id: str) -> Result[Department, DepartmentNotFoundError | Exception]:
        return await self._repository.fetch_by_id(department_id)

    async def update_department(
        self, department_id: str, update_params: UpdateDepartmentParams
    ) -> Result[Department, DepartmentNotFoundError | Exception]:
        return await self._repository.update(department_id, update_params)

    async def delete_department(
        self, department_id: str
    ) -> Result[Department, DepartmentNotFoundError | Exception]:
        return await self._repository.delete(department_id)

