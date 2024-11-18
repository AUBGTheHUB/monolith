from typing import Tuple

from result import Result, Err

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.transaction_manager import TransactionManager
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError, HackathonCapacityExceededError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.service.hackathon_service import HackathonService


class ParticipantRegistrationService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(self, hackathon_service: HackathonService, tx_manager: TransactionManager) -> None:
        self._hackathon_service = hackathon_service
        self._tx_manager = tx_manager

    async def register_admin_participant(self, input_data: ParticipantRequestBody) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 2
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        result = await self._tx_manager.with_transaction(
            self._hackathon_service.create_participant_and_team_in_transaction_callback, input_data
        )

        return result
