from typing import Tuple
from fastapi import BackgroundTasks
from result import Err, Ok, Result, is_err
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.service.hackathon.admin_team_service import AdminTeamService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.team_service import TeamService
from src.service.jwt_utils.schemas import JwtParticipantVerificationData
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.exception import (
    HackathonCapacityExceededError,
    ParticipantNotFoundError,
    TeamNotFoundError,
    ParticipantAlreadyVerifiedError,
    EmailRateLimitExceededError,
)


class VerificationService:
    """High-Level Service layer responsible for handling the business logic when verifying a participant"""

    def __init__(
        self,
        hackathon_utility_service: HackathonUtilityService,
        team_service: TeamService,
        participant_service: ParticipantService,
        admin_team_service: AdminTeamService,
    ) -> None:
        self._hackathon_utility_service = hackathon_utility_service
        self._team_service = team_service
        self._participant_service = participant_service
        self._admin_team_service = admin_team_service

    async def verify_admin_participant(
        self, jwt_data: JwtParticipantVerificationData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, Team],
        HackathonCapacityExceededError | ParticipantNotFoundError | TeamNotFoundError | ValueError | Exception,
    ]:
        has_capacity = await self._hackathon_utility_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        result = await self._admin_team_service.verify_admin_participant_and_team_in_transaction(jwt_data=jwt_data)
        if is_err(result):
            return result

        err = self._participant_service.send_successful_registration_email(
            participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
        )

        if err is not None:
            return err

        # Check if the current registration of the participant reached the capacity of the hackathon
        # and take the necessary steps to finalize it
        # This will be executed only after we return a response from the route
        background_tasks.add_task(self.finalize_verification)

        return result

    async def verify_random_participant(
        self, jwt_data: JwtParticipantVerificationData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, None], HackathonCapacityExceededError | ParticipantNotFoundError | ValueError | Exception
    ]:
        has_capacity = await self._hackathon_utility_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        result = await self._participant_service.verify_random_participant(jwt_data=jwt_data)
        if is_err(result):
            return result

        err = self._participant_service.send_successful_registration_email(
            participant=result.ok_value[0], background_tasks=background_tasks
        )
        if err is not None:
            return err

        # Check if the current registration of the participant reached the capacity of the hackathon
        # and take the necessary steps to finalize it
        # This will be executed only after we return a response from the route
        background_tasks.add_task(self.finalize_verification)

        return result

    async def resend_verification_email(self, participant_id: str, background_tasks: BackgroundTasks) -> Result[
        Participant,
        ParticipantNotFoundError
        | TeamNotFoundError
        | ParticipantAlreadyVerifiedError
        | EmailRateLimitExceededError
        | ValueError
        | Exception,
    ]:

        result = await self._participant_service.check_send_verification_email_rate_limit(participant_id=participant_id)
        if is_err(result):
            return result

        err = await self._participant_service.send_verification_email(
            participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
        )
        if err is not None:
            return err

        return Ok(result.ok_value[0])

    async def finalize_verification(self) -> None:
        # The registration form is considered closed when the last random participant cannot enter the hackathon
        has_capacity = await self._hackathon_utility_service.check_capacity_register_random_participant_case()

        if not has_capacity:
            # Flip the new team registration switch to false
            result = await self._hackathon_utility_service.close_reg_for_random_and_admin_participants()

            # If the registration switch was flipped successfully create the random participant teams
            if not is_err(result):
                await self._team_service.create_random_participant_teams()
