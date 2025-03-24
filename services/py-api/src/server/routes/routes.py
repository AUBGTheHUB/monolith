from fastapi import APIRouter

from src.server.handlers.http_handlers import HttpHandlersContainer
from src.server.routes.feature_swithces_routes import register_feature_switches_routes
from src.server.routes.utility_routes import register_utility_routes


class Routes:

    @staticmethod
    def register_routes(router: APIRouter, http_handlers: HttpHandlersContainer) -> None:
        """Registers all URL patterns in the router (request multiplexer) and their respective HTTP handlers"""
        register_utility_routes(router=router, http_handler=http_handlers.utility_handlers)
        register_feature_switches_routes(router=router, http_handler=http_handlers.fs_handlers)
