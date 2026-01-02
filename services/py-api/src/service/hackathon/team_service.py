from math import ceil
from secrets import token_hex
from typing import Optional, List, TypedDict

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.model.hackathon.team_model import Team
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import (
    DuplicateTeamNameError,
    ParticipantNotFoundError,
    TeamNotFoundError,
)

from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.constants import MAX_NUMBER_OF_TEAM_MEMBERS

LOG = get_logger()


class _RandomTeam(TypedDict):
    team: Team
    participants: list[Participant]


class TeamService:
    """Mid-Level service layer designed to perform crud on teams"""

    def __init__(
        self,
        teams_repo: TeamsRepository,
        participant_service: ParticipantService,
        participant_repo: ParticipantsRepository,
        tx_manager: MongoTransactionManager,
    ):
        self._teams_repo = teams_repo
        self._participant_service = participant_service
        self._participant_repo = participant_repo
        self._tx_manager = tx_manager

    async def fetch_all_teams(self) -> Result[List[Team], Exception]:
        return await self._teams_repo.fetch_all()

    async def delete_team(self, team_id: str) -> Result[Team, TeamNotFoundError | Exception]:
        return await self._teams_repo.delete(obj_id=team_id)

    async def check_team_capacity(self, team_id: str) -> bool:
        """Calculate if there is enough capacity to register a new participant from the invite link for his team."""

        # Fetch number of registered participants in the team
        registered_teammates = await self._participant_repo.get_number_registered_teammates(team_id)

        # Check against team capacity
        return registered_teammates + 1 <= MAX_NUMBER_OF_TEAM_MEMBERS

    async def create_random_participant_teams(self) -> bool:

        result = await self._participant_service.retrieve_and_categorize_random_participants()

        if is_err(result):
            return False

        (prog_participants, non_prog_participants) = result.ok_value

        random_teams = self.form_random_participant_teams(prog_participants, non_prog_participants)

        result = await self.create_random_participant_teams_in_transaction(random_teams)

        if is_err(result):
            return False

        return True

    def form_random_participant_teams(
        self, prog_participants: list[Participant], non_prog_participants: list[Participant]
    ) -> List[_RandomTeam]:
        # Calculate the number of hackathon participants
        number_of_random_participants = len(prog_participants) + len(non_prog_participants)
        # Calculate the number of teams that are going to be needed for the given number of participants
        number_of_teams = ceil(number_of_random_participants / MAX_NUMBER_OF_TEAM_MEMBERS)

        # Create a list for storing the Random Teams
        teams = []

        # Populate the dictionary with the Random Teams named `RandomTeam{i}`
        for i in range(number_of_teams):
            teams.append(_RandomTeam(team=Team(name=f"RT_{token_hex(8)}", is_verified=True), participants=[]))

        # Spread all the programming experienced participants to the teams in a Round Robin (RR) manner
        ctr = 0  # initialize a counter
        while len(prog_participants) > 0:
            teams[ctr % number_of_teams]["participants"].append(prog_participants.pop())
            ctr += 1

        # Spread all the non-programming experienced participants to the teams in a Round Robin (RR) manner
        ctr = 0  # reset counter
        while len(non_prog_participants) > 0:
            teams[ctr % number_of_teams]["participants"].append(non_prog_participants.pop())
            ctr += 1

        return teams

    async def _create_random_participant_teams_in_transaction_callback(
        self, random_teams: List[_RandomTeam], session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[List[_RandomTeam], DuplicateTeamNameError | ParticipantNotFoundError | Exception]:
        # Loop through each RandomTeam in the list. Create the team. Update all the participants with the id of the team
        # created
        for random_team in random_teams:
            # Create the team
            team_result = await self._teams_repo.create(team=random_team["team"], session=session)

            if is_err(team_result):
                return team_result

            # Take out one of the participants and assign them as an admin in the newly created random team
            admin_participant = random_team["participants"].pop()
            admin_result = await self._participant_repo.update(
                obj_id=str(admin_participant.id),
                obj_fields=UpdateParticipantParams(team_id=random_team["team"].id, is_admin=True),
                session=session,
            )

            if is_err(admin_result):
                return admin_result

            # Insert all the participants in the team that was created
            update_result = await self._participant_repo.bulk_update(
                obj_ids=[participant.id for participant in random_team["participants"]],
                obj_fields=UpdateParticipantParams(team_id=random_team["team"].id),
            )

            if is_err(update_result):
                return update_result

        return Ok(random_teams)

    async def create_random_participant_teams_in_transaction(
        self, input_data: List[_RandomTeam]
    ) -> Result[List[_RandomTeam], DuplicateTeamNameError | ParticipantNotFoundError | Exception]:
        return await self._tx_manager.with_transaction(
            self._create_random_participant_teams_in_transaction_callback, input_data
        )
