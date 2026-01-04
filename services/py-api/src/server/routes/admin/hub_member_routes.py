from fastapi import APIRouter, Depends
from src.server.routes.route_dependencies import is_auth

from src.server.handlers.admin.hub_members_handlers import HubMembersHandlers


def register_hub_members_routes(http_handler: HubMembersHandlers) -> APIRouter:
    hub_members_router = APIRouter(prefix="/hub-members", tags=["hub-members"])

    hub_members_router.add_api_route(
        "", endpoint=http_handler.get_all_hub_members, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "/{member_id}", endpoint=http_handler.get_hub_member, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "", endpoint=http_handler.create_hub_member, methods=["POST"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "/{member_id}", endpoint=http_handler.update_hub_member, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "/{member_id}", endpoint=http_handler.delete_hub_member, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return hub_members_router
