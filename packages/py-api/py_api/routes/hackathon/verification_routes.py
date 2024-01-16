from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from py_api.controllers.hackathon.verification_controller import (
    VerificationController as c,
)

router = APIRouter(prefix="/hackathon/verify")


@router.get("/admin")
def verify_admin(jwt_token: str) -> JSONResponse:
    return c.verify_admin(jwt_token)


@router.get("/test")
def verify_url(team_name: str) -> Any:
    return c.test_controller(team_name=team_name)
