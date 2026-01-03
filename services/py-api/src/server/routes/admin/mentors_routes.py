from fastapi import APIRouter, Depends

from src.server.handlers.admin.mentor_handlers import MentorsHandlers
from src.server.routes.route_dependencies import is_auth


def register_mentors_routes(http_handler: MentorsHandlers) -> APIRouter:
    mentors_router = APIRouter(prefix="/mentors", tags=["admin"])

    mentors_router.add_api_route(
        "", endpoint=http_handler.list_mentors, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    mentors_router.add_api_route(
        "/{mentor_id}", endpoint=http_handler.get_mentor, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    mentors_router.add_api_route(
        "", endpoint=http_handler.create_mentor, methods=["POST"], dependencies=[Depends(is_auth)]
    )
    mentors_router.add_api_route(
        "/{mentor_id}", endpoint=http_handler.update_mentor, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    mentors_router.add_api_route(
        "/{mentor_id}", endpoint=http_handler.delete_mentor, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return mentors_router
