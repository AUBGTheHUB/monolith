from fastapi import APIRouter, Depends

from src.server.routes.route_dependencies import is_authorized, validate_obj_id

from src.server.handlers.admin.hub_members_handlers import HubMembersHandlers
from src.server.schemas.response_schemas.admin.hub_member_schemas import HubMembersListResponse, HubMemberResponse
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_hub_members_routes(http_handler: HubMembersHandlers) -> APIRouter:
    hub_members_router = APIRouter(prefix="/hub-members", tags=["hub-members"])

    hub_members_router.add_api_route(
        "",
        endpoint=http_handler.get_all_hub_members,
        methods=["GET"],
        responses={200: {"model": HubMembersListResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_authorized)],
    )
    hub_members_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.get_hub_member,
        methods=["GET"],
        responses={
            200: {"model": HubMemberResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )
    hub_members_router.add_api_route(
        "",
        endpoint=http_handler.create_hub_member,
        methods=["POST"],
        responses={201: {"model": HubMemberResponse}, 401: {"model": ErrResponse}},
        dependencies=[Depends(is_authorized)],
    )
    hub_members_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.update_hub_member,
        methods=["PATCH"],
        responses={
            200: {"model": HubMemberResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )
    hub_members_router.add_api_route(
        "/{object_id}",
        endpoint=http_handler.delete_hub_member,
        methods=["DELETE"],
        responses={
            200: {"model": HubMemberResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized), Depends(validate_obj_id)],
    )

    return hub_members_router
