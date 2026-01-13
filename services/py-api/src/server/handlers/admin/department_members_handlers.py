from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.schemas import AdminDepartmentMemberCreateIn, AdminDepartmentMemberUpdateIn
from src.server.schemas.response_schemas.schemas import (
    Response,
    AdminDepartmentMemberOut,
    AdminDepartmentMembersListOut,
    ErrResponse,
)
from src.service.admin.department_members_service import DepartmentMembersService
from starlette import status


class DepartmentMembersHandlers(BaseHandler):
    def __init__(self, service: DepartmentMembersService) -> None:
        self._service = service

    async def list(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        members = [
            AdminDepartmentMemberOut(
                id=str(member.id),
                name=member.name,
                photo_url=member.photo_url,
                linkedin_url=member.linkedin_url,
                departments=member.departments,
            )
            for member in result.ok_value
        ]

        return Response(
            response_model=AdminDepartmentMembersListOut(members=members),
            status_code=status.HTTP_200_OK,
        )

    async def get(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        member = result.ok_value
        return Response(
            response_model=AdminDepartmentMemberOut(
                id=str(member.id),
                name=member.name,
                photo_url=member.photo_url,
                linkedin_url=member.linkedin_url,
                departments=member.departments,
            ),
            status_code=status.HTTP_200_OK,
        )

    async def create(self, member_in: AdminDepartmentMemberCreateIn) -> Response:
        result = await self._service.create(member_in)

        if is_err(result):
            return self.handle_error(result.err_value)

        member = result.ok_value
        return Response(
            response_model=AdminDepartmentMemberOut(
                id=str(member.id),
                name=member.name,
                photo_url=member.photo_url,
                linkedin_url=member.linkedin_url,
                departments=member.departments,
            ),
            status_code=status.HTTP_201_CREATED,
        )

    async def update(self, object_id: str, member_in: AdminDepartmentMemberUpdateIn) -> Response:
        result = await self._service.update(object_id, member_in)

        if is_err(result):
            return self.handle_error(result.err_value)

        member = result.ok_value
        return Response(
            response_model=AdminDepartmentMemberOut(
                id=str(member.id),
                name=member.name,
                photo_url=member.photo_url,
                linkedin_url=member.linkedin_url,
                departments=member.departments,
            ),
            status_code=status.HTTP_200_OK,
        )

    async def delete(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        member = result.ok_value
        return Response(
            response_model=AdminDepartmentMemberOut(
                id=str(member.id),
                name=member.name,
                photo_url=member.photo_url,
                linkedin_url=member.linkedin_url,
                departments=member.departments,
            ),
            status_code=status.HTTP_200_OK,
        )

