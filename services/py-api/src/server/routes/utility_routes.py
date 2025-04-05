from fastapi import APIRouter

from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import (
    PongResponse,
    ErrResponse,
)


def register_utility_routes(http_handler: UtilityHandlers) -> APIRouter:
    """Registers all utility routes under a separate router, along with their respective handler funcs, and returns the
    router"""
    utility_router = APIRouter()

    utility_router.add_api_route(
        path="/ping",
        methods=["GET"],
        endpoint=http_handler.ping_services,
        responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}},
    )

    return utility_router
