from result import is_err
from starlette import status

from src.database.model.admin.department_model import Department, Member, UpdateDepartmentParams
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.schemas import AdminDepartmentCreateIn, AdminDepartmentUpdateIn
from src.server.schemas.response_schemas.schemas import (
    Response,
    AdminDepartmentOut,
    AdminDepartmentsListOut,
    AdminTeamMemberOut,
)
from src.service.admin.departments_service import DepartmentsService


class DepartmentsHandlers(BaseHandler):

    def __init__(self, service: DepartmentsService) -> None:
        self._service = service

    async def list_departments(self) -> Response:
        result = await self._service.list_departments()

        if is_err(result):
            return self.handle_error(result.err_value)

        departments = [
            AdminDepartmentOut(
                id=str(dept.id),
                name=dept.name,
                members=[AdminTeamMemberOut(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in dept.members],
            )
            for dept in result.ok_value
        ]

        return Response(
            response_model=AdminDepartmentsListOut(departments=departments),
            status_code=status.HTTP_200_OK,
        )

    async def get_department(self, object_id: str) -> Response:
        result = await self._service.get_department(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        dept = result.ok_value
        return Response(
            response_model=AdminDepartmentOut(
                id=str(dept.id),
                name=dept.name,
                members=[AdminTeamMemberOut(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in dept.members],
            ),
            status_code=status.HTTP_200_OK,
        )

    async def create_department(self, department_in: AdminDepartmentCreateIn) -> Response:
        members = [Member(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in department_in.members]
        department = Department(name=department_in.name, members=members)

        result = await self._service.create_department(department)

        if is_err(result):
            return self.handle_error(result.err_value)

        dept = result.ok_value
        return Response(
            response_model=AdminDepartmentOut(
                id=str(dept.id),
                name=dept.name,
                members=[AdminTeamMemberOut(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in dept.members],
            ),
            status_code=status.HTTP_201_CREATED,
        )

    async def update_department(self, object_id: str, department_in: AdminDepartmentUpdateIn) -> Response:
        members = [Member(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in department_in.members]
        update_params = UpdateDepartmentParams(name=department_in.name, members=members)

        result = await self._service.update_department(object_id, update_params)

        if is_err(result):
            return self.handle_error(result.err_value)

        dept = result.ok_value
        return Response(
            response_model=AdminDepartmentOut(
                id=str(dept.id),
                name=dept.name,
                members=[AdminTeamMemberOut(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in dept.members],
            ),
            status_code=status.HTTP_200_OK,
        )

    async def delete_department(self, object_id: str) -> Response:
        result = await self._service.delete_department(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        dept = result.ok_value
        return Response(
            response_model=AdminDepartmentOut(
                id=str(dept.id),
                name=dept.name,
                members=[AdminTeamMemberOut(name=m.name, photo_url=m.photo_url, linkedin_url=m.linkedin_url) for m in dept.members],
            ),
            status_code=status.HTTP_200_OK,
        )

