from typing import Tuple
from fastapi import BackgroundTasks
from result import Err, Ok, Result, is_err
from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.schemas.jwt_schemas.schemas import JwtParticipantVerificationData
from src.service.hackathon_service import HackathonService
from src.server.exception import (
    HackathonCapacityExceededError,
    ParticipantNotFoundError,
    TeamNotFoundError,
    ParticipantAlreadyVerifiedError,
    EmailRateLimitExceededError,
)


class ParticipantVerificationService:
    """Service layer responsible for handling the business logic when verifying a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def verify_admin_participant(
        self, jwt_data: JwtParticipantVerificationData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, Team],
        HackathonCapacityExceededError | ParticipantNotFoundError | TeamNotFoundError | ValueError | Exception,
    ]:
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        result = await self._hackathon_service.verify_admin_participant_and_team_in_transaction(jwt_data=jwt_data)
        if is_err(result):
            return result

        err = self._hackathon_service.send_successful_registration_email(
            participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
        )

        if err is not None:
            return err

        return result

    async def verify_random_participant(
        self, jwt_data: JwtParticipantVerificationData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, None], HackathonCapacityExceededError | ParticipantNotFoundError | ValueError | Exception
    ]:
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        result = await self._hackathon_service.verify_random_participant(jwt_data=jwt_data)
        if is_err(result):
            return result

        err = self._hackathon_service.send_successful_registration_email(
            participant=result.ok_value[0], background_tasks=background_tasks
        )
        if err is not None:
            return err

        return result

    async def resend_verification_email(self, participant_id: str, background_tasks: BackgroundTasks) -> Result[
        Participant,
        ParticipantNotFoundError
        | ParticipantAlreadyVerifiedError
        | EmailRateLimitExceededError
        | ValueError
        | Exception,
    ]:

        result = await self._hackathon_service.check_send_verification_email_rate_limit(participant_id=participant_id)
        if is_err(result):
            return result

        err = await self._hackathon_service.send_verification_email(
            participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
        )
        if err is not None:
            return err

        return Ok(result.ok_value[0])
