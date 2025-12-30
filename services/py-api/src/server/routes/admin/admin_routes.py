from fastapi import APIRouter, Depends

from src.server.handlers.admin.admin_handlers import AdminHandlers
from src.server.routes.route_dependencies import is_auth


def register_sponsor_routes(admin_router: APIRouter, http_handler: AdminHandlers) -> APIRouter:
    sponsors_router = APIRouter(prefix="/sponsors", tags=["admin"])

    sponsors_router.add_api_route("", http_handler.list_sponsors, methods=["GET"], dependencies=[Depends(is_auth)])
    sponsors_router.add_api_route(
        "/{sponsor_id}", http_handler.get_sponsor, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    sponsors_router.add_api_route("", http_handler.create_sponsor, methods=["POST"], dependencies=[Depends(is_auth)])
    sponsors_router.add_api_route(
        "/{sponsor_id}", http_handler.update_sponsor, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    sponsors_router.add_api_route(
        "/{sponsor_id}", http_handler.delete_sponsor, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return sponsors_router


def register_mentors_routes(admin_router: APIRouter, http_handler: AdminHandlers) -> APIRouter:
    mentors_router = APIRouter(prefix="/mentors", tags=["admin"])

    mentors_router.add_api_route("", http_handler.list_mentors, methods=["GET"], dependencies=[Depends(is_auth)])
    mentors_router.add_api_route(
        "/{mentor_id}", http_handler.get_mentor, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    mentors_router.add_api_route("", http_handler.create_mentor, methods=["POST"], dependencies=[Depends(is_auth)])
    mentors_router.add_api_route(
        "/{mentor_id}", http_handler.update_mentor, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    mentors_router.add_api_route(
        "/{mentor_id}", http_handler.delete_mentor, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return mentors_router


def register_judges_routes(admin_router: APIRouter, http_handler: AdminHandlers) -> APIRouter:
    judges_router = APIRouter(prefix="/judges", tags=["admin"])

    judges_router.add_api_route("", http_handler.list_judges, methods=["GET"], dependencies=[Depends(is_auth)])
    judges_router.add_api_route("/{judge_id}", http_handler.get_judge, methods=["GET"], dependencies=[Depends(is_auth)])
    judges_router.add_api_route("", http_handler.create_judge, methods=["POST"], dependencies=[Depends(is_auth)])
    judges_router.add_api_route(
        "/{judge_id}", http_handler.update_judge, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    judges_router.add_api_route(
        "/{judge_id}", http_handler.delete_judge, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return judges_router


def register_hub_members_routes(admin_router: APIRouter, http_handler: AdminHandlers) -> APIRouter:
    hub_members_router = APIRouter(prefix="/hub-members", tags=["admin"])

    hub_members_router.add_api_route(
        "", http_handler.list_hub_members, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "/{member_id}", http_handler.get_hub_member, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "", http_handler.create_hub_member, methods=["POST"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "/{member_id}", http_handler.update_hub_member, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    hub_members_router.add_api_route(
        "/{member_id}", http_handler.delete_hub_member, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return hub_members_router


def register_past_events_routes(admin_router: APIRouter, http_handler: AdminHandlers) -> APIRouter:
    past_events_router = APIRouter(prefix="/past-events", tags=["admin"])

    past_events_router.add_api_route(
        "", http_handler.list_past_events, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "/{event_id}", http_handler.get_past_event, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "", http_handler.create_past_event, methods=["POST"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "/{event_id}", http_handler.update_past_event, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    past_events_router.add_api_route(
        "/{event_id}", http_handler.delete_past_event, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return past_events_router


def register_admin_routes(http_handler: AdminHandlers) -> APIRouter:
    admin_router = APIRouter(prefix="/admin", tags=["admin"])

    sponsors_router = register_sponsor_routes(admin_router=admin_router, http_handler=http_handler)
    mentors_router = register_mentors_routes(admin_router=admin_router, http_handler=http_handler)
    judges_router = register_judges_routes(admin_router=admin_router, http_handler=http_handler)
    hub_members_router = register_hub_members_routes(admin_router=admin_router, http_handler=http_handler)
    past_events_router = register_past_events_routes(admin_router=admin_router, http_handler=http_handler)

    admin_router.include_router(sponsors_router)
    admin_router.include_router(mentors_router)
    admin_router.include_router(judges_router)
    admin_router.include_router(hub_members_router)
    admin_router.include_router(past_events_router)

    return admin_router
