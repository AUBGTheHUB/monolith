from fastapi import APIRouter
from starlette import status
from src.server.handlers.auth.auth_handlers import AuthHandlers
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.response_schemas.auth.schemas import AuthTokensSuccessfullyIssued


def register_auth_routes(http_handler: AuthHandlers) -> APIRouter:
    """Registers all auth routes for the admin panel under a separate router, along with their respective handler funcs,
    and returns the router"""

    auth_router = APIRouter(prefix="/auth", tags=["auth"])
    auth_router.add_api_route(
        path="/login",
        methods=["POST"],
        endpoint=http_handler.login,
        responses={
            200: {"model": AuthTokensSuccessfullyIssued},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
    )
    auth_router.add_api_route(
        path="/register",
        methods=["POST"],
        endpoint=http_handler.register,
        status_code=status.HTTP_204_NO_CONTENT,
        responses={204: {"description": "Registration successful"}, 409: {"model": ErrResponse}},
    )
    auth_router.add_api_route(
        path="/refresh",
        methods=["POST"],
        endpoint=http_handler.refresh_token_pair,
        responses={
            200: {"model": AuthTokensSuccessfullyIssued},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
    )

    return auth_router
