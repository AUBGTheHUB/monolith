from fastapi import BackgroundTasks, HTTPException

from src.database.mongo.transaction_manager import MongoTransactionManager

from src.database.repository.event_registration.participants_repository import (
    ParticipantsRepository,
)

from src.database.repository.event_registration.teams_repository import (
    TeamsRepository,
)

from src.server.schemas.request_schemas.event_registration.schemas import (
    CreateTeamRequest,
    JoinTeamRequest,
    SoloRegistrationRequest,
)

from src.service.registration_services import (
    register_team_admin,
    register_team_member,
    register_solo_member,
)

from src.service.event_registration_mail_service import (
    EventRegistrationMailService,
)
from fastapi import BackgroundTasks, HTTPException
from result import is_err

from src.service.registration_services import assign_solo_member_to_team
from src.server.schemas.request_schemas.event_registration.schemas import (
    AssignSoloMemberRequest,
)


def unwrap_registration_result(result):
    if result.is_err():
        error = result.err_value

        if isinstance(error, (ValueError, LookupError)):
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

        raise HTTPException(
            status_code=500,
            detail="Registration failed",
        )

    return result.ok_value


class RegistrationHandlers:

    def __init__(
        self,
        participants_repository: ParticipantsRepository,
        teams_repository: TeamsRepository,
        transaction_manager: MongoTransactionManager,
        mail_service: EventRegistrationMailService,
    ):
        self._participants_repository = participants_repository
        self._teams_repository = teams_repository
        self._transaction_manager = transaction_manager
        self._mail_service = mail_service

    async def register_team_admin_handler(
        self,
        request: CreateTeamRequest,
    ):
        result = await register_team_admin(
            participant_data=request.participant.model_dump(),
            team_name=request.team_name,
            participants_repository=self._participants_repository,
            teams_repository=self._teams_repository,
            transaction_manager=self._transaction_manager,
        )

        team = unwrap_registration_result(result)

        return {
            "message": "Team created successfully",
            "team_code": team.code,
            "team": team.dump_as_json(),
        }

    async def register_team_member_handler(
        self,
        request: JoinTeamRequest,
        background_tasks: BackgroundTasks,
    ):
        result = await register_team_member(
            participant_data=request.participant.model_dump(),
            team_code=request.team_code,
            participants_repository=self._participants_repository,
            teams_repository=self._teams_repository,
            transaction_manager=self._transaction_manager,
            on_team_completed=lambda email, name, code: (
                self._mail_service.queue_team_completion_email(
                    leader_email=email,
                    team_name=name,
                    team_code=code,
                    background_tasks=background_tasks,
                )
            ),
        )

        participant = unwrap_registration_result(result)

        return {
            "message": "Successfully joined team",
            "participant": participant.dump_as_json(),
        }

    async def register_solo_handler(
        self,
        request: SoloRegistrationRequest,
    ):
        result = await register_solo_member(
            participant_data=request.participant.model_dump(),
            participants_repository=self._participants_repository,
        )

        participant = unwrap_registration_result(result)

        return {
            "message": "Solo registration successful",
            "participant": participant.dump_as_json(),
        }

    async def assign_solo_handler(
        self,
        request: AssignSoloMemberRequest,
        background_tasks: BackgroundTasks,
    ):
        result = await assign_solo_member_to_team(
            participant_id=request.participant_id,
            team_code=request.team_code,
            assigned_role=request.assigned_role,
            participants_repository=self._participants_repository,
            teams_repository=self._teams_repository,
            transaction_manager=self._transaction_manager,
            on_team_completed=lambda email, name, code: (
                self._mail_service.queue_team_completion_email(
                    leader_email=email,
                    team_name=name,
                    team_code=code,
                    background_tasks=background_tasks,
                )
            ),
        )

        if is_err(result):
            if isinstance(result.err_value, ValueError):
                raise HTTPException(
                    status_code=400,
                    detail=str(result.err_value),
                )

            raise HTTPException(
                status_code=500,
                detail="Could not assign participant",
            )

        participant = result.ok_value

        return {
            "participant_id": str(participant["_id"]),
            "team_id": str(participant["team_id"]),
            "assigned_role": participant["assigned_role"],
        }

    async def retry_completion_emails_handler(
        self,
        background_tasks: BackgroundTasks,
    ):
        try:
            queued_count = await self._mail_service.queue_pending_completion_emails(
                participants_repository=self._participants_repository,
                background_tasks=background_tasks,
                limit=50,
            )

            return {
                "message": "Pending completion emails queued",
                "queued": queued_count,
            }

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Could not queue pending completion emails",
            )
