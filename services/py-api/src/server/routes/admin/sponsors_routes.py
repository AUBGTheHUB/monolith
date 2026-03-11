from fastapi import APIRouter, Depends
from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.admin.sponsors_handlers import SponsorsHandlers
from src.server.utility.role_checker import RoleChecker
from src.server.routes.route_dependencies import validate_obj_id
from src.server.schemas.response_schemas.admin.sponsor_schemas import SponsorResponse, SponsorsResponse
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_sponsor_routes(http_handler: SponsorsHandlers) -> APIRouter:
    sponsors_router = APIRouter(prefix="/sponsors", tags=["sponsors"])

    sponsors_router.add_api_route(
        path="", endpoint=http_handler.get_all_sponsors, methods=["GET"], responses={200: {"model": SponsorsResponse}}
    )
    sponsors_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.get_sponsor,
        methods=["GET"],
        responses={
            200: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(validate_obj_id)],
    )
    sponsors_router.add_api_route(
        path="",
        endpoint=http_handler.create_sponsor,
        methods=["POST"],
        responses={
            201: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )
    sponsors_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.update_sponsor,
        methods=["PATCH"],
        responses={
            200: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )
    sponsors_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.delete_sponsor,
        methods=["DELETE"],
        responses={
            200: {"model": SponsorResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )

    return sponsors_router
