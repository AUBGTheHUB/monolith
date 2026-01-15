from fastapi import APIRouter, Depends

from src.server.handlers.admin.past_events_handlers import PastEventsHandlers
from src.server.routes.route_dependencies import is_authorized, validate_obj_id
from src.server.schemas.response_schemas.admin.past_event_schemas import (
    AllPastEventsResponse,
    PastEventResponse,
)
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_past_events_routes(http_handler: PastEventsHandlers) -> APIRouter:
    events_router = APIRouter(prefix="/events", tags=["events"])

    events_router.add_api_route(
        "",
        endpoint=http_handler.create_past_event,
        methods=["POST"],
        status_code=201,
        responses={201: {"model": PastEventResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_authorized)],
    )

    events_router.add_api_route(
        "",
        endpoint=http_handler.get_all_past_events,
        methods=["GET"],
        responses={200: {"model": AllPastEventsResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_authorized)],
    )

    events_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.get_past_event,
        methods=["GET"],
        responses={
            200: {"model": PastEventResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )

    events_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.update_past_event,
        methods=["PUT"],
        responses={
            200: {"model": PastEventResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )

    events_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.delete_past_event,
        methods=["DELETE"],
        responses={
            200: {"model": PastEventResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )

    return events_router
