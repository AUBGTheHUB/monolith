from fastapi import APIRouter

from src.server.handlers.auth.auth_handlers import AuthHandlers


def register_auth_routes(http_handler: AuthHandlers) -> APIRouter:
    """Registers all auth routes for the admin panel under a separate router, along with their respective handler funcs,
    and returns the router"""

    # TODO ADD responses to each path according to prior project structure
    auth_router = APIRouter(prefix="/auth", tags=["auth"])
    auth_router.add_api_route(
        path="/login",
        methods=["POST"],
        endpoint=http_handler.login,
    )
    auth_router.add_api_route(
        path="/register",
        methods=["POST"],
        endpoint=http_handler.register,
    )
    auth_router.add_api_route(path="/refresh", methods=["POST"], endpoint=http_handler.refresh_token)

    return auth_router
