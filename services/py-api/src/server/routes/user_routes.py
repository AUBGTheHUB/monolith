from fastapi import APIRouter
from fastapi.params import Depends

from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.user_handlers import UserHandlers
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.response_schemas.auth.schemas import (
    UserResponse,
)
from src.server.utility.role_checker import RoleChecker


def register_user_routes(http_handler: UserHandlers) -> APIRouter:
    """Registers all routes related to user/role management"""

    user_router = APIRouter(prefix="/users", tags=["users"])
    user_router.add_api_route(
        path="/{user_id}/role",
        endpoint=http_handler.change_role,
        methods=["PATCH"],
        responses={
            200: {"model": UserResponse},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.SUPER]))],
    )
    return user_router
