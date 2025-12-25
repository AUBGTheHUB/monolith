from typing import Tuple

from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.base_model import SerializableObjectId
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import (
    DuplicateEmailError,
    TeamNameMissmatchError,
    TeamNotFoundError,
    ParticipantNotFoundError
)
from src.server.schemas.request_schemas.schemas import (
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData

LOG = get_logger()


class ParticipantService:
    def __init__(
            self,
            participants_repo: ParticipantsRepository,
            teams_repo: TeamsRepository,
    ) -> None:
        self._participant_repo = participants_repo
        self._teams_repo = teams_repo

    async def create_random_participant(
            self, input_data: RandomParticipantInputData
    ) -> Result[Tuple[Participant, None], DuplicateEmailError | Exception]:

        result = await self._participant_repo.create(
            Participant(**input_data.model_dump(), is_admin=False, team_id=None)
        )
        if is_err(result):
            return result

        # As when first created, the random participant is not assigned to a team we return the team as None
        return Ok((result.ok_value, None))

    async def create_invite_link_participant(
            self, input_data: InviteLinkParticipantInputData, decoded_jwt_token: JwtParticipantInviteRegistrationData
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | TeamNotFoundError | TeamNameMissmatchError | Exception]:

        # Check if team still exists - Returns an error when it doesn't
        team_result = await self._teams_repo.fetch_by_id(decoded_jwt_token.team_id)
        if is_err(team_result):
            return team_result

        # Check if the team_name from the token is consistent with the team_name from the request body
        # A missmatch could occur if the frontend passes something different
        if input_data.team_name != team_result.ok_value.name:
            return Err(TeamNameMissmatchError())

        participant_result = await self._participant_repo.create(
            Participant(
                **input_data.model_dump(),
                team_id=SerializableObjectId(decoded_jwt_token.team_id),
                email_verified=True,
            )
        )
        if is_err(participant_result):
            return participant_result

        # Return the new participant
        return Ok((participant_result.ok_value, team_result.ok_value))

    async def delete_participant(
            self, participant_id: str
    ) -> Result[Participant, ParticipantNotFoundError | Exception]:
        return await self._participant_repo.delete(obj_id=participant_id)
