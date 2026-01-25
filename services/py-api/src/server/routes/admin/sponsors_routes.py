from fastapi import APIRouter, Depends

from src.server.handlers.admin.sponsors_handlers import SponsorsHandlers
from src.server.routes.route_dependencies import is_authorized, validate_obj_id
from src.server.schemas.response_schemas.admin.sponsor_schemas import SponsorResponse, SponsorsResponse
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_sponsor_routes(http_handler: SponsorsHandlers) -> APIRouter:
    sponsors_router = APIRouter(prefix="/sponsors", tags=["sponsors"])

    sponsors_router.add_api_route(
        path="", 
        endpoint=http_handler.get_all_sponsors, 
        methods=["GET"], 
        responses={
            200: {"model": SponsorsResponse}
        },
        dependencies=[Depends(is_authorized)]
    )
    sponsors_router.add_api_route(
        path="/{object_id}", 
        endpoint=http_handler.get_sponsor, 
        methods=["GET"], 
        responses={
            200: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse}
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)]
    )
    sponsors_router.add_api_route(
        path="", 
        endpoint=http_handler.create_sponsor, 
        methods=["POST"], 
        responses={
            201: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse}
        },
        dependencies=[Depends(is_authorized)]
    )
    sponsors_router.add_api_route(
        path="/{object_id}", 
        endpoint=http_handler.update_sponsor, 
        methods=["PATCH"],
        responses={
            200: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse}
        }, 
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)]
    )
    sponsors_router.add_api_route(
        path="/{object_id}", 
        endpoint=http_handler.delete_sponsor, 
        methods=["DELETE"], 
        responses={
            200: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse}
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)]
    )

    return sponsors_router
