from fastapi import APIRouter

from src.server.handlers.admin_panel.authentication_handler import AuthenticationHandlers


def register_authentication_routes(http_handler: AuthenticationHandlers) -> APIRouter:
    """Registers all authentication routes for the admin panel under a separate router, along with their respective handler funcs,
    and returns the router"""
    authentication_router = APIRouter(prefix="/admin")
    return authentication_router
