from fastapi import APIRouter

from src.server.handlers.tournament.tournament_registration_handlers import TournamentRegistrationHandlers
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.response_schemas.tournament.schemas import (
    TournamentSoloParticipantResponse,
    TournamentTeamAndParticipantResponse,
)


def register_tournament_registration_routes(http_handler: TournamentRegistrationHandlers) -> APIRouter:
    tournament_registration_router = APIRouter(prefix="/tournament/register")

    tournament_registration_router.add_api_route(
        path="/team",
        methods=["POST"],
        endpoint=http_handler.register_team_and_admin_handler,
        responses={
            201: {"model": TournamentTeamAndParticipantResponse},
            400: {"model": ErrResponse},
            409: {"model": ErrResponse},
        },
    )

    # check again for background tasks
    tournament_registration_router.add_api_route(
        path="/member",
        methods=["POST"],
        endpoint=http_handler.register_team_member_handler,
        responses={
            201: {"model": TournamentTeamAndParticipantResponse},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
            409: {"model": ErrResponse},
        },
    )

    tournament_registration_router.add_api_route(
        path="/solo",
        methods=["POST"],
        endpoint=http_handler.register_solo_handler,
        responses={
            201: {"model": TournamentSoloParticipantResponse},
            400: {"model": ErrResponse},
            409: {"model": ErrResponse},
        },
    )

    return tournament_registration_router
