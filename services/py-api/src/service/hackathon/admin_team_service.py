from typing import Optional, Tuple

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.model.hackathon.team_model import Team, UpdateTeamParams
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import (
    DuplicateTeamNameError,
    DuplicateEmailError,
    ParticipantAlreadyVerifiedError,
    ParticipantNotFoundError,
    TeamNotFoundError,
)
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
)
from src.service.jwt_utils.schemas import JwtParticipantVerificationData

LOG = get_logger()


class AdminTeamService:
    """Mid-Level service layer designed to register new admins and their teams"""

    def __init__(
        self,
        teams_repo: TeamsRepository,
        participant_repo: ParticipantsRepository,
        tx_manager: MongoTransactionManager,
    ):
        self._teams_repo = teams_repo
        self._participant_repo = participant_repo
        self._tx_manager = tx_manager

    async def _create_participant_and_team_in_transaction_callback(
        self, input_data: AdminParticipantInputData, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:
        """
        This method is intended to be passed as the `callback` argument to the `TransactionManager.with_transaction(...)`
        function.
        """
        team = await self._teams_repo.create(Team(name=input_data.team_name), session)

        if is_err(team):
            return team

        participant = await self._participant_repo.create(
            Participant(
                **input_data.model_dump(),
                team_id=team.ok_value.id,
            ),
            session,
        )
        if is_err(participant):
            return participant

        return Ok((participant.ok_value, team.ok_value))

    async def create_participant_and_team_in_transaction(
        self, input_data: AdminParticipantInputData
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:
        """Creates a participant and team in a transactional manner. The participant is added to the team created. If
        any of the db operations: creation of a Team obj, creation of a Participant obj fails, the whole operation
        fails, and no permanent changes are made to the database."""

        return await self._tx_manager.with_transaction(
            self._create_participant_and_team_in_transaction_callback, input_data
        )

    async def verify_admin_participant_and_team_in_transaction(
        self, jwt_data: JwtParticipantVerificationData
    ) -> Result[
        Tuple[Participant, Team],
        ParticipantNotFoundError | TeamNotFoundError | Exception,
    ]:
        return await self._tx_manager.with_transaction(self._verify_admin_participant_and_team_callback, jwt_data)

    async def _verify_admin_participant_and_team_callback(
        self,
        jwt_data: JwtParticipantVerificationData,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[
        Tuple[Participant, Team],
        ParticipantNotFoundError | TeamNotFoundError | ParticipantAlreadyVerifiedError | Exception,
    ]:
        # This step is taken to ensure that we are not verifying an already verified participant
        result = await self._participant_repo.fetch_by_id(jwt_data.sub)

        if is_err(result):
            return result

        if result.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        result_verified_admin = await self._participant_repo.update(
            obj_id=jwt_data.sub, obj_fields=UpdateParticipantParams(email_verified=True), session=session
        )

        if is_err(result_verified_admin):
            return result_verified_admin

        result_verified_team = await self._teams_repo.update(
            obj_id=str(result_verified_admin.ok_value.team_id),
            obj_fields=UpdateTeamParams(is_verified=True),
            session=session,
        )

        if is_err(result_verified_team):
            return result_verified_team

        return Ok((result_verified_admin.ok_value, result_verified_team.ok_value))
