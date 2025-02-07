from os import environ
from typing import Tuple

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
from src.service.mail_service.resend_service import ResendMailService
from fastapi import BackgroundTasks


class ParticipantRegistrationService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(self, hackathon_service: HackathonService, mailing_service: ResendMailService) -> None:
        self._hackathon_service = hackathon_service
        self._mailing_service = mailing_service

    async def register_admin_participant(self, input_data: AdminParticipantInputData) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 2
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        return await self._hackathon_service.create_participant_and_team_in_transaction(input_data)

    async def register_random_participant(self, input_data: RandomParticipantInputData) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 1
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        return await self._hackathon_service.create_random_participant(input_data)

    async def register_invite_link_participant(
        self, input_data: InviteLinkParticipantInputData, jwt_token: str
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

        return await self._hackathon_service.create_invite_link_participant(
            input_data=input_data, decoded_jwt_token=decoded_data
        )

    async def send_verification_email(
        self, participant: Participant, team: Team, background_tasks: BackgroundTasks
    ) -> None:

        # Send emails only if the env is not tests
        # We don't want to hit the resend limit with test registrations

        if environ["ENV"] != "TEST":
            # Example on how it can be acheived
            if participant.is_admin:
                background_tasks.add_task(
                    self._mailing_service.send_participant_verification_email,
                    participant,
                    team.name,
                    "https://google.com",
                )
