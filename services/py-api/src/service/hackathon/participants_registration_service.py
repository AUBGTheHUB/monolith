from typing import Tuple

from fastapi import BackgroundTasks
from result import Result, Err, is_err, Ok

from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    TeamNameMissmatchError,
    ParticipantNotFoundError,
)
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.service.hackathon.hackathon_service import HackathonService


class ParticipantRegistrationService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def register_admin_participant(
        self, input_data: AdminParticipantInputData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError
        | DuplicateTeamNameError
        | HackathonCapacityExceededError
        | ParticipantNotFoundError
        | Exception,
    ]:
        # Capacity Check 2
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        create_result = await self._hackathon_service.create_participant_and_team_in_transaction(input_data)
        if is_err(create_result):
            return create_result

        # Send verification email
        update_result = await self._hackathon_service.send_verification_email(
            participant=create_result.ok_value[0], team=create_result.ok_value[1], background_tasks=background_tasks
        )
        # Update result could be None if we are in Test ENV, and we should not send emails
        if update_result is not None and is_err(update_result):
            return update_result

        # If we are in Test env we should return the original created participant as update_result is None
        return Ok((update_result.ok_value if update_result else create_result.ok_value[0], create_result.ok_value[1]))

    async def register_random_participant(
        self, input_data: RandomParticipantInputData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, None],
        DuplicateEmailError | HackathonCapacityExceededError | ParticipantNotFoundError | Exception,
    ]:
        # Capacity Check 1
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        create_result = await self._hackathon_service.create_random_participant(input_data)
        if is_err(create_result):
            return create_result

        # Send verification email
        update_result = await self._hackathon_service.send_verification_email(
            participant=create_result.ok_value[0], background_tasks=background_tasks
        )
        # Update result could be None if we are in Test ENV, and we should not send emails
        if update_result is not None and is_err(update_result):
            return update_result

        # If we are in Test env we should return the original created participant as update_result is None
        return Ok((update_result.ok_value if update_result else create_result.ok_value[0], None))

    async def register_invite_link_participant(
        self, input_data: InviteLinkParticipantInputData, jwt_token: str, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | TeamCapacityExceededError | TeamNameMissmatchError | Exception,
    ]:
        # Decode the token
        decoded_result = JwtUtility.decode_data(token=jwt_token, schema=JwtParticipantInviteRegistrationData)
        if is_err(decoded_result):
            return decoded_result

        decoded_data = decoded_result.ok_value

        # Check Team Capacity
        has_capacity = await self._hackathon_service.check_team_capacity(decoded_data["team_id"])
        if not has_capacity:
            return Err(TeamCapacityExceededError())

        result = await self._hackathon_service.create_invite_link_participant(
            input_data=input_data, decoded_jwt_token=decoded_data
        )
        if is_err(result):
            return result

        # Invite link participants are automatically verified, that's why we don't send a verification email
        err = self._hackathon_service.send_successful_registration_email(
            participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
        )
        if err is not None:
            return err

        return result


def participant_reg_service_provider(hackathon_service: HackathonService) -> ParticipantRegistrationService:
    """
    Args:
        hackathon_service: A HackathonService instance

    Returns:
        A ParticipantRegistrationService instance
    """
    return ParticipantRegistrationService(hackathon_service)
