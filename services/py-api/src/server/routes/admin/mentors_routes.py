from fastapi import APIRouter, Depends

from src.server.handlers.admin.mentor_handlers import MentorsHandlers
from src.server.routes.route_dependencies import is_authorized, validate_obj_id
from src.server.schemas.response_schemas.admin.mentor_schemas import MentorResponse, MentorsResponse
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.routes.route_dependencies import is_authorized


def register_mentors_routes(http_handler: MentorsHandlers) -> APIRouter:
    mentors_router = APIRouter(prefix="/mentors", tags=["mentors"])

    mentors_router.add_api_route(
        path="",
        endpoint=http_handler.get_all_mentors,
        methods=["GET"],
        responses={200: {"model": MentorsResponse}},
        dependencies=[Depends(is_authorized)],
    )
    mentors_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.get_mentor,
        methods=["GET"],
        responses={
            200: {"model": MentorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )
    mentors_router.add_api_route(
        path="",
        endpoint=http_handler.create_mentor,
        methods=["POST"],
        responses={201: {"model": MentorResponse}, 400: {"model": ErrResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_authorized)],
    )
    mentors_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.update_mentor,
        methods=["PATCH"],
        responses={
            200: {"model": MentorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )
    mentors_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.delete_mentor,
        methods=["DELETE"],
        responses={
            200: {"model": MentorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )

    return mentors_router
