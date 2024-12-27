from typing import Tuple

from result import Result, Err

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError, HackathonCapacityExceededError, TeamCapacityExceededError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.service.hackathon_service import HackathonService


class ParticipantRegistrationService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def register_admin_participant(self, input_data: ParticipantRequestBody) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 2
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        return await self._hackathon_service.create_participant_and_team_in_transaction(input_data)

    async def register_random_participant(self, input_data: ParticipantRequestBody) -> Result[
        Participant,
        DuplicateEmailError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 1
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        return await self._hackathon_service.create_random_participant(input_data)
    
    async def register_invite_link_participant(self, input_data: ParticipantRequestBody) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | HackathonCapacityExceededError | Exception,
    ]:
        # Check Team Capacity
        has_capacity = await self._hackathon_service.check_team_capacity(input_data.team_name)
        if not has_capacity:
            return Err(TeamCapacityExceededError())

        # Proceed with registration if there is capacity
        return await self._hackathon_service.create_invite_link_participant(input_data)