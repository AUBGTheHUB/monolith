from fastapi import APIRouter

from src.server.handlers.http_handlers import HttpHandlersContainer
from src.server.routes.feature_swithces_routes import register_feature_switches_routes
from src.server.routes.hackathon.hackathon_management_routes import register_hackathon_management_routes
from src.server.routes.hackathon.participant_reg_routes import register_hackathon_participants_routes
from src.server.routes.hackathon.verification_routes import register_verification_routes
from src.server.routes.utility_routes import register_utility_routes


class Routes:

    @staticmethod
    def register_routes(router: APIRouter, http_handlers: HttpHandlersContainer) -> None:
        """Registers all URL patterns in the router (request multiplexer) and their respective HTTP handlers"""
        register_utility_routes(router=router, http_handler=http_handlers.utility_handlers)
        register_feature_switches_routes(router=router, http_handler=http_handlers.fs_handlers)
        register_hackathon_participants_routes(router=router, http_handler=http_handlers.participant_handlers)
        register_hackathon_management_routes(router=router, http_handler=http_handlers.hackathon_management_handlers)
        register_verification_routes(router=router, http_handler=http_handlers.verification_handlers)
