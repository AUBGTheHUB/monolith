from fastapi import APIRouter, Depends

from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.routes.route_dependencies import is_registration_open
from src.server.schemas.response_schemas.schemas import ParticipantRegisteredResponse, ErrResponse


def register_hackathon_participants_routes(router: APIRouter, http_handler: ParticipantHandlers) -> None:
    router.add_api_route(
        path="/hackathon/participants",
        methods=["POST"],
        endpoint=http_handler.create_participant,
        status_code=201,
        responses={
            201: {"model": ParticipantRegisteredResponse},
            409: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_registration_open)],
    )
