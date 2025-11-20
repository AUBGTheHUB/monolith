from fastapi import APIRouter, Depends

from src.server.handlers.admin.admin_handlers import AdminHandlers
from src.server.dependencies.admin_auth import require_admin


def register_admin_routes(http_handler: AdminHandlers) -> APIRouter:
    router = APIRouter(prefix="/admin", tags=["admin"])

    # Sponsors
    router.add_api_route(
        "/sponsors", http_handler.list_sponsors, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/sponsors/{sponsor_id}", http_handler.get_sponsor, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/sponsors", http_handler.create_sponsor, methods=["POST"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/sponsors/{sponsor_id}", http_handler.update_sponsor, methods=["PATCH"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/sponsors/{sponsor_id}", http_handler.delete_sponsor, methods=["DELETE"], dependencies=[Depends(require_admin)]
    )

    # Mentors
    router.add_api_route("/mentors", http_handler.list_mentors, methods=["GET"], dependencies=[Depends(require_admin)])
    router.add_api_route(
        "/mentors/{mentor_id}", http_handler.get_mentor, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/mentors", http_handler.create_mentor, methods=["POST"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/mentors/{mentor_id}", http_handler.update_mentor, methods=["PATCH"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/mentors/{mentor_id}", http_handler.delete_mentor, methods=["DELETE"], dependencies=[Depends(require_admin)]
    )

    # Judges
    router.add_api_route("/judges", http_handler.list_judges, methods=["GET"], dependencies=[Depends(require_admin)])
    router.add_api_route(
        "/judges/{judge_id}", http_handler.get_judge, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route("/judges", http_handler.create_judge, methods=["POST"], dependencies=[Depends(require_admin)])
    router.add_api_route(
        "/judges/{judge_id}", http_handler.update_judge, methods=["PATCH"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/judges/{judge_id}", http_handler.delete_judge, methods=["DELETE"], dependencies=[Depends(require_admin)]
    )

    # Team Members
    router.add_api_route(
        "/team-members", http_handler.list_team_members, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/team-members/{member_id}",
        http_handler.get_team_member,
        methods=["GET"],
        dependencies=[Depends(require_admin)],
    )
    router.add_api_route(
        "/team-members", http_handler.create_team_member, methods=["POST"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/team-members/{member_id}",
        http_handler.update_team_member,
        methods=["PATCH"],
        dependencies=[Depends(require_admin)],
    )
    router.add_api_route(
        "/team-members/{member_id}",
        http_handler.delete_team_member,
        methods=["DELETE"],
        dependencies=[Depends(require_admin)],
    )

    # Past Events
    router.add_api_route(
        "/past-events", http_handler.list_past_events, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/past-events/{event_id}", http_handler.get_past_event, methods=["GET"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/past-events", http_handler.create_past_event, methods=["POST"], dependencies=[Depends(require_admin)]
    )
    router.add_api_route(
        "/past-events/{event_id}",
        http_handler.update_past_event,
        methods=["PATCH"],
        dependencies=[Depends(require_admin)],
    )
    router.add_api_route(
        "/past-events/{event_id}",
        http_handler.delete_past_event,
        methods=["DELETE"],
        dependencies=[Depends(require_admin)],
    )

    return router
