from typing import Dict, Tuple

from fastapi import APIRouter, Request
from py_api.controllers import VerificationController as c

router = APIRouter(prefix="/hackathon/verify")


@router.put("", response_model=Tuple[Dict[str, str], int])
def verify_participant_route(verification_token: str) -> Tuple[Dict[str, str], int]:
    # TODO: use verify func when ready
    return c.verify_participant(verification_token)

# TODO: Add a route to handle the inviting of participants to a team
