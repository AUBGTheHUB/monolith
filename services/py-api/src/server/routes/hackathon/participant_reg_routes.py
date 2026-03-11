from fastapi import APIRouter, Depends

from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.routes.route_dependencies import is_registration_open
from src.server.schemas.response_schemas.hackathon.schemas import ParticipantRegisteredResponse
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_participants_reg_routes(http_handler: ParticipantHandlers) -> APIRouter:
    """Registers all participant registration routes under a separate router, along with their respective handler funcs,
    and returns the router"""
    participants_reg_router = APIRouter(prefix="/hackathon/participants", tags=["hackathon"])

    participants_reg_router.add_api_route(
        path="",
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

    return participants_reg_router
