from fastapi import APIRouter
from fastapi.params import Depends

from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.user_handlers import UserHandlers
from src.server.routes.route_dependencies import validate_obj_id
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.utility.role_checker import RoleChecker


def register_user_routes(http_handler: UserHandlers) -> APIRouter:
    """Registers all routes related to user/role management"""

    user_router = APIRouter(prefix="/users", tags=["users"])
    user_router.add_api_route(
        path="/{object_id}/role",
        endpoint=http_handler.change_role,
        methods=["PATCH"],
        responses={
            204: {"description": "Role change successful"},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.SUPER])), Depends(validate_obj_id)],
    )
    return user_router
