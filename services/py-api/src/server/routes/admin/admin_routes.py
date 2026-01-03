from fastapi import APIRouter

from src.server.handlers.admin.admin_handlers import AdminHandlers
from src.server.routes.admin.hub_member_routes import register_hub_members_routes
from src.server.routes.admin.judges_routes import register_judges_routes
from src.server.routes.admin.mentors_routes import register_mentors_routes
from src.server.routes.admin.past_events_routes import register_past_events_routes
from src.server.routes.admin.sponsors_routes import register_sponsor_routes


def register_admin_routes(http_handler: AdminHandlers) -> APIRouter:
    admin_router = APIRouter(prefix="/admin", tags=["admin"])

    sponsors_router = register_sponsor_routes(http_handler=http_handler.sponsors_handlers)
    mentors_router = register_mentors_routes(http_handler=http_handler.mentors_handlers)
    judges_router = register_judges_routes(http_handler=http_handler.judges_handlers)
    hub_members_router = register_hub_members_routes(http_handler=http_handler.hub_members_handlers)
    past_events_router = register_past_events_routes(http_handler=http_handler.past_events_handlers)

    admin_router.include_router(sponsors_router)
    admin_router.include_router(mentors_router)
    admin_router.include_router(judges_router)
    admin_router.include_router(hub_members_router)
    admin_router.include_router(past_events_router)

    return admin_router
