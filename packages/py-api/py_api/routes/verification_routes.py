from typing import Dict, Tuple

from fastapi import APIRouter, Request
from py_api.functionality.hackathon.verification.jwt_verification import (
    JWTVerification as c,
)

router = APIRouter(prefix="/hackathon")


@router.get("/verify")
def verify_participant_route(verification_token: str) -> Tuple[Dict[str, str], int]:
    # TODO: use verify func when ready
    return c.verify_participant(verification_token)

# TODO: Use functions from controler


@router.get("/invite")
def invite_participant_route(invite_token: str) -> Tuple[Dict[str, str], int]:
    return c.invite_participant(invite_token)
