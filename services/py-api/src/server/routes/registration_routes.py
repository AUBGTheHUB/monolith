from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.database.model.admin.hub_admin_model import Role
from src.server.utility.role_checker import RoleChecker
from src.server.schemas.request_schemas.event_registration.schemas import (
    AssignSoloMemberRequest,
)

from src.server.schemas.request_schemas.event_registration.schemas import (
    CreateTeamRequest,
    JoinTeamRequest,
    SoloRegistrationRequest,
)


def register_registration_routes(http_handler) -> APIRouter:
    router = APIRouter(
        prefix="/registration",
        tags=["Registration"],
    )

    @router.post(
        "/team/admin",
        status_code=status.HTTP_201_CREATED,
    )
    async def register_team_admin(request: CreateTeamRequest):
        return await http_handler.register_team_admin_handler(request)

    @router.post(
        "/team/member",
        status_code=status.HTTP_201_CREATED,
    )
    async def register_team_member(
        request: JoinTeamRequest,
        background_tasks: BackgroundTasks,
    ):
        return await http_handler.register_team_member_handler(
            request,
            background_tasks,
        )

    @router.post(
        "/solo",
        status_code=status.HTTP_201_CREATED,
    )
    async def register_solo(request: SoloRegistrationRequest):
        return await http_handler.register_solo_handler(request)

    @router.post(
        "/admin/assign-solo",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )
    async def assign_solo(
        request: AssignSoloMemberRequest,
        background_tasks: BackgroundTasks,
    ):
        return await http_handler.assign_solo_handler(
            request,
            background_tasks,
        )

    @router.post(
        "/admin/retry-completion-emails",
        status_code=status.HTTP_202_ACCEPTED,
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )
    async def retry_completion_emails(
        background_tasks: BackgroundTasks,
    ):
        return await http_handler.retry_completion_emails_handler(background_tasks)

    return router
