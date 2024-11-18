from math import ceil
from typing import Optional, Tuple

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import is_err, Ok, Result

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.exception import DuplicateTeamNameError, DuplicateEmailError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody


class HackathonService:
    """Service layer designed to hold all business logic related to hackathon management"""

    def __init__(
        self,
        participant_repo: ParticipantsRepository,
        team_repo: TeamsRepository,
        tx_manager: TransactionManager,
    ) -> None:
        self._participant_repo = participant_repo
        self._team_repo = team_repo
        self._tx_manager = tx_manager

    async def create_participant_and_team_in_transaction_callback(
        self, input_data: ParticipantRequestBody, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:
        """Creates a participant and team in a transactional manner. The participant is added to the team created.
        This method is intended be passed as the `callback` argument to the `TransactionManager.with_transaction(...)`
        function. If any of the db operations: creation of a Team obj, creation of a Participant obj fail, the whole
        operation fails, and no permanent changes are made to the database. (The transaction is roll backed by the
        `with_transaction` method).
        """
        team = await self._team_repo.create(input_data, session)
        if is_err(team):
            return team

        participant = await self._participant_repo.create(input_data, session, team_id=team.ok_value.id)
        if is_err(participant):
            return participant

        return Ok((participant.ok_value, team.ok_value))

    async def check_capacity_register_admin_participant_case(self) -> bool:
        """Calculate if there is enough capacity to register a new team. Capacity is measured in max number of verified
        teams in the hackathon. This is the Capacity Check 2 from the Excalidraw 'Adding a participant workflow'"""

        # Fetch number of verified random participants
        verified_random_participants = await self._participant_repo.get_verified_random_participants_count()

        # Fetch number of verified registered teams
        verified_registered_teams = await self._team_repo.get_verified_registered_teams_count()

        # Calculate the anticipated number of teams
        number_ant_teams = verified_registered_teams + ceil(
            verified_random_participants / self._team_repo.MAX_NUMBER_OF_TEAM_MEMBERS
        )

        # Check against the hackathon capacity
        return number_ant_teams < self._team_repo.MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON
