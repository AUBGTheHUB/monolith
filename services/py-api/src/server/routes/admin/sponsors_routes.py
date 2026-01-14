from fastapi import APIRouter, Depends

from src.server.handlers.admin.sponsors_handlers import SponsorsHandlers
from src.server.routes.route_dependencies import is_authorized


def register_sponsor_routes(http_handler: SponsorsHandlers) -> APIRouter:
    sponsors_router = APIRouter(prefix="/sponsors", tags=["sponsors"])

    sponsors_router.add_api_route(
        "", endpoint=http_handler.get_all_sponsors, methods=["GET"] , dependencies=[Depends(is_authorized)]
    )
    sponsors_router.add_api_route(
        "/{sponsor_id}", endpoint=http_handler.get_sponsor, methods=["GET"] , dependencies=[Depends(is_authorized)]
    )
    sponsors_router.add_api_route(
        "", endpoint=http_handler.create_sponsor, methods=["POST"] , dependencies=[Depends(is_authorized)]
    )
    sponsors_router.add_api_route(
        "/{sponsor_id}", endpoint=http_handler.update_sponsor, methods=["PATCH"] , dependencies=[Depends(is_authorized)]
    )
    sponsors_router.add_api_route(
        "/{sponsor_id}", endpoint=http_handler.delete_sponsor, methods=["DELETE"] , dependencies=[Depends(is_authorized)]
    )

    return sponsors_router
