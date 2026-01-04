from fastapi import APIRouter, Depends
from src.server.routes.route_dependencies import is_auth

from src.server.handlers.admin.past_events_handlers import PastEventsHandlers


def register_past_events_routes(http_handler: PastEventsHandlers) -> APIRouter:
    past_events_router = APIRouter(prefix="/past-events", tags=["admin"])

    past_events_router.add_api_route(
        "", endpoint=http_handler.get_all_past_events, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "/{event_id}", endpoint=http_handler.get_past_event, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "", endpoint=http_handler.create_past_event, methods=["POST"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "/{event_id}", endpoint=http_handler.update_past_event, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "/{event_id}", endpoint=http_handler.delete_past_event, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return past_events_router
