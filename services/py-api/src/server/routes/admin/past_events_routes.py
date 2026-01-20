from fastapi import APIRouter, Depends

from src.server.handlers.admin.past_events_handlers import PastEventsHandlers
from src.server.routes.route_dependencies import is_auth, validate_obj_id


def register_past_events_routes(http_handler: PastEventsHandlers) -> APIRouter:
    events_router = APIRouter(prefix="/events", tags=["events"])

    # List all past events
    events_router.add_api_route(
        "",
        endpoint=http_handler.get_all_past_events,
        methods=["GET"],
        dependencies=[Depends(is_auth)],
    )

    # Create a past event
    events_router.add_api_route(
        "",
        endpoint=http_handler.create_past_event,
        methods=["POST"],
        dependencies=[Depends(is_auth)],
    )

    # Get a single past event by id
    events_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.get_past_event,
        methods=["GET"],
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    # Update a past event
    events_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.update_past_event,
        methods=["PATCH"],
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    # Delete a past event
    events_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.delete_past_event,
        methods=["DELETE"],
        dependencies=[Depends(is_auth), Depends(validate_obj_id)],
    )

    return events_router
