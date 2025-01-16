from typing import Tuple
from result import Err, Result
from src.database.model.participant_model import Participant
from src.server.exception import HackathonCapacityExceededError, ParticipantNotFoundError
from src.server.schemas.jwt_schemas.schemas import JwtParticipantVerificationData
from src.service.hackathon_service import HackathonService


class ParticipantVerificationService:
    """Service layer responsible for handling the business logic when verifying a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def verify_random_participant(self, jwt_data: JwtParticipantVerificationData) -> Result[
        Tuple[Participant, None],
        HackathonCapacityExceededError | ParticipantNotFoundError | Exception,
    ]:
        has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        return await self._hackathon_service.verify_random_participant(jwt_data=jwt_data)
