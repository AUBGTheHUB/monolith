from fastapi import APIRouter, Depends
from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.tournament.group_handlers import GroupHandlers
from src.server.utility.role_checker import RoleChecker
from src.server.schemas.response_schemas.tournament.schemas import (
    GroupsResponse,
    GroupResponse,
)
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.exception import GroupNotFoundError


def register_group_routes(http_handler: GroupHandlers) -> APIRouter:
    """Registers tournament group routes."""

    group_router = APIRouter(prefix="/groups", tags=["tournament"])

    # Public route
    group_router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=http_handler.get_all_groups,
        responses={200: {"model": GroupsResponse}},
    )

    # Protected routes
    group_router.add_api_route(
        path="/generate-bracket",
        methods=["GET"],
        endpoint=http_handler.generate_bracket,
        responses={
            200: {"model": GroupsResponse},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    group_router.add_api_route(
        path="/inactive",
        methods=["GET"],
        endpoint=http_handler.get_inactive_groups,
        responses={
            200: {"model": GroupsResponse},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    group_router.add_api_route(
        path="/active",
        methods=["GET"],
        endpoint=http_handler.get_active_groups,
        responses={
            200: {"model": GroupsResponse},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    group_router.add_api_route(
        path="/{group_id}/declare-winner",
        methods=["POST"],
        endpoint=http_handler.declare_winner,
        responses={
            200: {"model": GroupResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
            404: {"model": GroupNotFoundError},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    group_router.add_api_route(
        path="/{group_id}",
        methods=["GET"],
        endpoint=http_handler.get_group,
        responses={
            200: {"model": GroupResponse},
            401: {"model": ErrResponse},
            403: {"model": ErrResponse},
            404: {"model": GroupNotFoundError},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    return group_router
