from fastapi import APIRouter, Depends

from src.server.handlers.event.attendees_handlers import AttendeesHandlers
from src.server.routes.route_dependencies import validate_obj_id
from src.server.schemas.response_schemas.event.attendee_schemas import AttendeeResponse, AttendeesResponse
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_attendee_routes(http_handler: AttendeesHandlers) -> APIRouter:
    attendees_router = APIRouter(prefix="/attendees", tags=["attendees"])

    attendees_router.add_api_route(
        path="", endpoint=http_handler.get_all_attendees, methods=["GET"], responses={200: {"model": AttendeesResponse}}
    )
    attendees_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.get_attendee,
        methods=["GET"],
        responses={
            200: {"model": AttendeeResponse},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(validate_obj_id)],
    )
    attendees_router.add_api_route(
        path="",
        endpoint=http_handler.create_attendee,
        methods=["POST"],
        responses={
            201: {"model": AttendeeResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
    )
    attendees_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.update_attendee,
        methods=["PATCH"],
        responses={
            200: {"model": AttendeeResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(validate_obj_id)],
    )
    attendees_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.delete_attendee,
        methods=["DELETE"],
        responses={
            200: {"model": AttendeeResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(validate_obj_id)],
    )

    return attendees_router
