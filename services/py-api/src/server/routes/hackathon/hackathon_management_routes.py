from fastapi import APIRouter, Depends

from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.routes.route_dependencies import is_auth, validate_obj_id
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    TeamDeletedResponse,
    AllTeamsResponse,
    RegistrationClosedSuccessfullyResponse,
    ParticipantDeletedResponse,
)


def register_hackathon_management_routes(router: APIRouter, http_handler: HackathonManagementHandlers) -> None:
    router.add_api_route(
        path="/hackathon/participants/{object_id}",
        methods=["DELETE"],
        endpoint=http_handler.delete_participant,
        responses={
            200: {"model": ParticipantDeletedResponse},
            404: {"model": ErrResponse},
            401: {"model": ErrResponse},
            400: {"model": ErrResponse},
        },
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    router.add_api_route(
        path="/hackathon/teams/{object_id}",
        methods=["DELETE"],
        endpoint=http_handler.delete_team,
        responses={200: {"model": TeamDeletedResponse}, 404: {"model": ErrResponse}},
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    router.add_api_route(
        path="/hackathon/teams",
        methods=["GET"],
        endpoint=http_handler.get_all_teams,
        responses={200: {"model": AllTeamsResponse}},
        dependencies=[Depends(is_auth)],
    )

    router.add_api_route(
        path="/hackathon/close-registration",
        methods=["POST"],
        endpoint=http_handler.close_registration,
        responses={200: {"model": RegistrationClosedSuccessfullyResponse}, 404: {"model": ErrResponse}},
        dependencies=[Depends(is_auth)],
    )
