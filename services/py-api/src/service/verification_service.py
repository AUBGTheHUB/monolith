from fastapi import HTTPException
from src.service.hackathon_service import HackathonService


class VerificationService:
    def __init__(self, hackathon_service: HackathonService):
        self._hackathon_service = hackathon_service

    async def verify_random_participant(self, participant_id: str, team_id: str) -> None:
        """
        Verify a random participant using the participant_id and team_id from the JWT token.
        """

        # If the participant has no team assigned, perform Capacity Check 1
        if not team_id:
            has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
            if not has_capacity:
                raise HTTPException(status_code=409, detail="The hackathon capacity is full.")

        # Simulate marking the participant as verified
        # (Assume actual verification logic will go here if needed)
        print("Participant {participant_id} verified successfully.")  # Log for debugging
