from typing import Tuple, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import is_err, Err, Ok

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody


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
    ) -> Ok[Tuple[Participant, Team]] | Err[DuplicateEmailError | DuplicateTeamNameError | Exception]:

        team = await self._team_repo.create(input_data, session)
        if is_err(team):
            return team

        participant = await self._participant_repo.create(input_data, session, team_id=team.ok_value.id)
        if is_err(participant):
            return participant

        return Ok((participant.ok_value, team.ok_value))

  #  async def capacity_check_one(self, db_manager: DatabaseManager, collection_name: str):
       
    #    _collection =   db_manager.get_collection(collection_name)
   #     N = _collection.count_documents({"team_id":  ""})  # Number of already verified random participants
    #    R = _collection.count_documents({})



    async def register_admin_participant(
        self, input_data: ParticipantRequestBody
    ) -> Ok[Tuple[Participant, Team]] | Err[DuplicateEmailError  | DuplicateTeamNameError | Exception]:
        # TODO: Add Capacity check 2
        result = await self._tx_manager.with_transaction(self._create_participant_and_team_in_transaction, input_data)
        return result
