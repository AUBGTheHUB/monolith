from typing import Tuple, List

from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.base_model import SerializableObjectId
from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.model.hackathon.team_model import Team
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import (
    DuplicateEmailError,
    TeamNameMissmatchError,
    TeamNotFoundError,
    ParticipantNotFoundError,
    ParticipantAlreadyVerifiedError,
)
from src.server.schemas.request_schemas.schemas import (
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData

LOG = get_logger()


class ParticipantService:
    """Service layer designed to perform crud on participants"""

    def __init__(
        self,
        participants_repo: ParticipantsRepository,
        teams_repo: TeamsRepository,
    ) -> None:
        self._participant_repo = participants_repo
        self._teams_repo = teams_repo

    async def retrieve_and_categorize_random_participants(
        self,
    ) -> Result[Tuple[List[Participant], List[Participant]], Exception]:
        programming_oriented = []
        non_programming_oriented = []
        # Fetch all the verified random participants
        result = await self._participant_repo.get_verified_random_participants()

        # Return the result to the upper layer in case of an Exception
        if is_err(result):
            return result

        # Group the into categories programming oriented, non-programming oriented
        for participant in result.ok_value:
            if participant.programming_level == "I am not participating as a programmer":
                non_programming_oriented.append(participant)
            else:
                programming_oriented.append(participant)

        return Ok((programming_oriented, non_programming_oriented))

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

    async def verify_random_participant(
        self, jwt_data: JwtParticipantVerificationData
    ) -> Result[Tuple[Participant, None], ParticipantNotFoundError | ParticipantAlreadyVerifiedError | Exception]:

        # This step is taken to ensure that we are not verifying an already verified participant
        result = await self._participant_repo.fetch_by_id(jwt_data.sub)

        if is_err(result):
            return result

        if result.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        # Updates the random participant if it exists
        result = await self._participant_repo.update(
            obj_id=jwt_data.sub, obj_fields=UpdateParticipantParams(email_verified=True)
        )

        if is_err(result):
            return result

        # As when first created, the random participant is not assigned to a team we return the team as None
        return Ok((result.ok_value, None))
