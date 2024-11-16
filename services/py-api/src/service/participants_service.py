from math import ceil
from typing import Tuple, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import is_err, Ok, Result

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.handlers.participants_handlers import ParticipantHandlers


class ParticipantService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(
        self, participant_repo: ParticipantsRepository, team_repo: TeamsRepository, tx_manager: TransactionManager
    ) -> None:
        self._participant_repo = participant_repo
        self._team_repo = team_repo
        self._tx_manager = tx_manager

    async def _create_participant_and_team_in_transaction(
        self, input_data: ParticipantRequestBody, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:

        team = await self._team_repo.create(input_data, session)
        if is_err(team):
            return team

        participant = await self._participant_repo.create(input_data, session, team_id=team.ok_value.id)
        if is_err(participant):
            return participant

        return Ok((participant.ok_value, team.ok_value))
    
    async def _create_random_participant_in_transaction(
            self, input_data: ParticipantRequestBody, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Ok[Participant] | Err[DuplicateEmailError | DuplicateTeamNameError | Exception]:
        participant = await self._participant_repo.create(input_data, session, team_id=None)
        if is_err(participant):
            return participant
        
        return Ok(participant.ok_value)

    async def register_admin_participant(
        self, input_data: ParticipantRequestBody
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:
        # TODO: Add Capacity check 2
        result = await self._tx_manager.with_transaction(self._create_participant_and_team_in_transaction, input_data)
        return result
    
    async def capacity_check_one(self):
        random_participants = ParticipantsRepository.get_number_random_participants()
        registered_teams = TeamsRepository.get_number_registered_teams()
        
        hackathon_teams_cap = 20 #change later
        participants_per_team = 5 #change later

        anticipated_total_teams = registered_teams + ceil((random_participants + 1) / participants_per_team)

        if anticipated_total_teams <= hackathon_teams_cap:
            return True
        else:
            #send to participant handler
            return False

    #revise
    async def insert_random_participant(self, input_data: ParticipantRequestBody
    ) -> Ok[Tuple[Participant, Team]] | Err[DuplicateEmailError | DuplicateTeamNameError | Exception]:
        # TODO: Add capacity check 1
        
        if ParticipantsRepository.capacity_check_one():
           result = self._tx_manager.with_transaction(self._create_random_participant_in_transaction, input_data)
           return result; 
        else:
           ParticipantHandlers.capacity_reached()
        

