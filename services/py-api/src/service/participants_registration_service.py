from typing import Tuple

from fastapi import BackgroundTasks
from result import Result, Err, is_err

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    TeamNameMissmatchError,
)
from src.server.schemas.jwt_schemas.schemas import JwtParticipantInviteRegistrationData
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.service.hackathon_service import HackathonService
from src.utils import JwtUtility


class ParticipantRegistrationService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def register_admin_participant(
        self, input_data: AdminParticipantInputData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 2
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        result = await self._hackathon_service.create_participant_and_team_in_transaction(input_data)
        if is_err(result):
            return result

        err = await self._hackathon_service.send_verification_email(
            participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
        )

        if err is not None:
            return err

        return result

    async def register_random_participant(
        self, input_data: RandomParticipantInputData, background_tasks: BackgroundTasks
    ) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 1
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        result = await self._hackathon_service.create_random_participant(input_data)
        if is_err(result):
            return result

        err = await self._hackathon_service.send_verification_email(
            participant=result.ok_value[0], background_tasks=background_tasks
        )
        if err is not None:
            return err

        return result

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

    # Returns true if the operation was successful or some shit like that
    async def create_random_participant_teams(self) -> bool:

        result = await self._hackathon_service.retrieve_and_categorize_random_participants()

        if is_err(result):
            return False

        (prog_participants, non_prog_participants) = result.ok_value

        random_teams = self._hackathon_service.form_random_participant_teams(prog_participants, non_prog_participants)

        result = await self._hackathon_service.create_random_participant_teams_in_transaction(random_teams)

        if is_err(result):
            return False

        return True
