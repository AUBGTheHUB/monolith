from typing import Any
from result import Err
from src.server.exception import HackathonCapacityExceededError
from src.service.hackathon_service import HackathonService


class VerificationService:
    def __init__(self, hackaton_service: HackathonService):
        self._hackaton_service = hackaton_service

    async def verify_participant_exists(self, id: str) -> bool:
        return await self._hackaton_service.check_if_participant_exists_in_by_id(object_id=id)

    async def verify_admin_participant(self, id: str) -> Any:
        has_capacity = await self._hackaton_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())
        return await self._hackaton_service.verify_admin_participant_and_team_in_transaction(admin_id=id)
