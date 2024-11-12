from typing import Tuple, Optional
import math
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import is_err, Err, Ok

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError, CapacityExceededError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody


class ParticipantService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(
        self, participant_repo: ParticipantsRepository, team_repo: TeamsRepository, tx_manager: TransactionManager,
        hackathon_cap: int, team_capacity: int 
    ) -> None:
        self._participant_repo = participant_repo
        self._team_repo = team_repo
        self._tx_manager = tx_manager
        self.hackathon_cap = hackathon_cap
        self.team_capacity = team_capacity

    async def _create_participant_and_team_in_transaction(
        self, input_data: ParticipantRequestBody, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Ok[Tuple[Participant, Team]] | Err[DuplicateEmailError | DuplicateTeamNameError | Exception]:

        team = await self._team_repo.create(input_data, session)
        if is_err(team):
            return team

        participant = await self._participant_repo.create(input_data, session, team_id=team.ok_value.id)
        if is_err(participant):
            return participant

        return Ok((participant.ok_value, team.ok_value))
    
    async def _check_capacity(self) -> bool:
        """Calculate if there is enough capacity to register a new team"""
        # Fetch number of verified random participants
        verified_random_participants = await self._participant_repo.get_verified_random_participants_count()

        # Fetch number of verified registered teams
        verified_registered_teams = await self._team_repo.get_verified_registered_teams_count()

        # Calculate the anticipated number of teams
        number_ant_teams = verified_registered_teams + math.ceil(verified_random_participants / self.team_capacity)

        # Check against the hackathon capacity
        return number_ant_teams < self.hackathon_cap

    async def register_admin_participant(
        self, input_data: ParticipantRequestBody
    ) -> Ok[Tuple[Participant, Team]] | Err[DuplicateEmailError | DuplicateTeamNameError| CapacityExceededError | Exception]:
        # Capacity Check 2
        has_capacity = await self._check_capacity()
        if not has_capacity:
            return Err(CapacityExceededError("Hackathon capacity exceeded, cannot register new team"))

        # Proceed with registration if there is capacity
        result = await self._tx_manager.with_transaction(self._create_participant_and_team_in_transaction, input_data)
        return result
