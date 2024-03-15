from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers.hackathon.verification_controller import (
    VerificationController as c,
)

router = APIRouter(prefix="/hackathon/verify")


@router.post("/participant")
async def verify_participant(jwt_token: str) -> JSONResponse:
    return c.verify_participants(jwt_token)
