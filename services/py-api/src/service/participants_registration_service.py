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
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData
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
        decoded_result = JwtUtility.decode_data(token=jwt_token, schema=JwtUserData)
        if is_err(decoded_result):
            return decoded_result

        decoded_data = decoded_result.ok_value

        # Check if the team_name from the token is consistent with the team_name from the request body
        # A missmatch could occur if the frontend passes something different
        if input_data.team_name != decoded_data["team_name"]:
            return Err(TeamNameMissmatchError())

        return await self._hackathon_service.create_invite_link_participant(
            input_data=input_data, decoded_jwt_token=decoded_data
        )
