from typing import Tuple
from result import Err, Result
from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import HackathonCapacityExceededError, ParticipantNotFoundError, TeamNotFoundError
from src.server.schemas.jwt_schemas.schemas import JwtParticipantVerificationData
from src.service.hackathon_service import HackathonService


class ParticipantVerificationService:
    """Service layer responsible for handling the business logic when verifying a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def verify_admin_participant(self, jwt_data: JwtParticipantVerificationData) -> Result[
        Tuple[Participant, Team],
        HackathonCapacityExceededError | ParticipantNotFoundError | TeamNotFoundError | Exception,
    ]:
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        return await self._hackathon_service.verify_admin_participant_and_team_in_transaction(jwt_data=jwt_data)

    async def verify_random_participant(self, jwt_data: JwtParticipantVerificationData) -> Result[
        Tuple[Participant, None],
        HackathonCapacityExceededError | ParticipantNotFoundError | Exception,
    ]:
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        return await self._hackathon_service.verify_random_participant(jwt_data=jwt_data)

    # TODO: Create a method send_verification_email that checks if the rate limit is not exceeded and passes the control
    # to the hackathon servcie. The hackathon service should implement a method called or something along these lines
    # check_send_verification_email_rate_limit() that checks the if the rate limit is exceeded or not.
    # if the check passes you pass the control to the HackathonService.send_verification_email() that should send the email
    # like a background task and update the participant with the last_email_sent.
