from fastapi import APIRouter, Depends

from src.server.handlers.admin.departments_handlers import DepartmentsHandlers
from src.server.routes.route_dependencies import is_auth, validate_obj_id
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    AdminDepartmentOut,
    AdminDepartmentsListOut,
)


def register_departments_routes(http_handler: DepartmentsHandlers) -> APIRouter:
    departments_router = APIRouter(prefix="/admin/departments")

    departments_router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=http_handler.list_departments,
        responses={200: {"model": AdminDepartmentsListOut}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_auth)],
    )

    departments_router.add_api_route(
        path="/{object_id}",
        methods=["GET"],
        endpoint=http_handler.get_department,
        responses={200: {"model": AdminDepartmentOut}, 404: {"model": ErrResponse}, 401: {"model": ErrResponse}, 400: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    departments_router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=http_handler.create_department,
        responses={201: {"model": AdminDepartmentOut}, 400: {"model": ErrResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_auth)],
    )

    departments_router.add_api_route(
        path="/{object_id}",
        methods=["PATCH"],
        endpoint=http_handler.update_department,
        responses={200: {"model": AdminDepartmentOut}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    departments_router.add_api_route(
        path="/{object_id}",
        methods=["DELETE"],
        endpoint=http_handler.delete_department,
        responses={200: {"model": AdminDepartmentOut}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    return departments_router

