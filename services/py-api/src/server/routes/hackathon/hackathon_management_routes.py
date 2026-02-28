from fastapi import APIRouter, Depends
from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.utility.role_checker import RoleChecker
from src.server.routes.route_dependencies import validate_obj_id
from src.server.schemas.response_schemas.hackathon.schemas import (
    TeamDeletedResponse,
    AllTeamsResponse,
    RegistrationClosedSuccessfullyResponse,
    ParticipantDeletedResponse,
)
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_hackathon_management_routes(http_handler: HackathonManagementHandlers) -> APIRouter:
    """Registers all hackathon_management routes under a separate router, along with their respective handler funcs,
    and returns the router"""

    hackathon_management_router = APIRouter(prefix="/hackathon", tags=["hackathon"])

    hackathon_management_router.add_api_route(
        path="/participants/{object_id}",
        methods=["DELETE"],
        endpoint=http_handler.delete_participant,
        responses={
            200: {"model": ParticipantDeletedResponse},
            404: {"model": ErrResponse},
            401: {"model": ErrResponse},
            400: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )

    hackathon_management_router.add_api_route(
        path="/teams/{object_id}",
        methods=["DELETE"],
        endpoint=http_handler.delete_team,
        responses={200: {"model": TeamDeletedResponse}, 401: {"model": ErrResponse}, 404: {"model": ErrResponse}},
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )

    hackathon_management_router.add_api_route(
        path="/teams",
        methods=["GET"],
        endpoint=http_handler.get_all_teams,
        responses={200: {"model": AllTeamsResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    hackathon_management_router.add_api_route(
        path="/close-registration",
        methods=["POST"],
        endpoint=http_handler.close_registration,
        responses={
            200: {"model": RegistrationClosedSuccessfullyResponse},
            404: {"model": ErrResponse},
            401: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )

    return hackathon_management_router
