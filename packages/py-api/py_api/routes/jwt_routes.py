from typing import Dict, Tuple

from fastapi import APIRouter, Request
from py_api.controllers import VerificationController as c

router = APIRouter(prefix="/hackathon/verify")


@router.get("", response_model=Tuple[Dict[str, str], int])
def verify_user_route(request: Request) -> Tuple[Dict[str, str], int]:
    verification_token = request.query_params.get("token")
    print(verification_token)
    return c.verify_participant(verification_token)
