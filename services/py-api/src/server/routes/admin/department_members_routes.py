from fastapi import APIRouter, Depends

from src.server.handlers.admin.department_members_handlers import DepartmentMembersHandlers
from src.server.routes.route_dependencies import is_auth, validate_obj_id
from src.server.schemas.request_schemas.schemas import AdminDepartmentMemberCreateIn, AdminDepartmentMemberUpdateIn
from src.server.schemas.response_schemas.schemas import (
    AdminDepartmentMemberOut,
    AdminDepartmentMembersListOut,
    ErrResponse,
)


def register_department_members_routes(http_handler: DepartmentMembersHandlers) -> APIRouter:
    dept_members_router = APIRouter(prefix="/admin/department-members", tags=["department-members"])

    dept_members_router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=http_handler.list,
        responses={200: {"model": AdminDepartmentMembersListOut}},
        dependencies=[Depends(is_auth)],
    )

    dept_members_router.add_api_route(
        path="/{object_id}",
        methods=["GET"],
        endpoint=http_handler.get,
        responses={200: {"model": AdminDepartmentMemberOut}, 404: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    dept_members_router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=http_handler.create,
        responses={201: {"model": AdminDepartmentMemberOut}, 400: {"model": ErrResponse}},
        dependencies=[Depends(is_auth)],
    )

    dept_members_router.add_api_route(
        path="/{object_id}",
        methods=["PATCH"],
        endpoint=http_handler.update,
        responses={200: {"model": AdminDepartmentMemberOut}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    dept_members_router.add_api_route(
        path="/{object_id}",
        methods=["DELETE"],
        endpoint=http_handler.delete,
        responses={200: {"model": AdminDepartmentMemberOut}, 404: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    return dept_members_router

