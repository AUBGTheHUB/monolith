from fastapi import APIRouter

from src.server.handlers.http_handlers import HttpHandlersContainer
from src.server.routes.admin_panel.authentication_routes import register_authentication_routes
from src.server.routes.feature_swithces_routes import register_feature_switches_routes
from src.server.routes.hackathon.hackathon_management_routes import register_hackathon_management_routes
from src.server.routes.hackathon.participant_reg_routes import register_participants_reg_routes
from src.server.routes.hackathon.verification_routes import register_verification_routes
from src.server.routes.utility_routes import register_utility_routes
from src.server.routes.admin.admin_routes import register_admin_routes


class Routes:

    @staticmethod
    def register_routes(main_router: APIRouter, http_handlers: HttpHandlersContainer) -> None:
        """Registers all URL patterns in the main_router (request multiplexer) and their respective HTTP handlers"""
        utility_router = register_utility_routes(http_handler=http_handlers.utility_handlers)
        fs_router = register_feature_switches_routes(http_handler=http_handlers.fs_handlers)
        participant_reg_router = register_participants_reg_routes(
            http_handler=http_handlers.hackathon_handlers.participant_handlers
        )
        hackathon_reg_router = register_hackathon_management_routes(
            http_handler=http_handlers.hackathon_handlers.hackathon_management_handlers
        )
        authentication_router = register_authentication_routes(http_handler=http_handlers.authentication_handlers)
        verification_router = register_verification_routes(
            http_handler=http_handlers.hackathon_handlers.verification_handlers
        )
        admin_router = register_admin_routes(http_handler=http_handlers.admin_handlers)
        # Bind all routers to the main one
        main_router.include_router(utility_router)
        main_router.include_router(fs_router)
        main_router.include_router(participant_reg_router)
        main_router.include_router(hackathon_reg_router)
        main_router.include_router(verification_router)
        main_router.include_router(authentication_router)
        main_router.include_router(admin_router)
