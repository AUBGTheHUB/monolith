from typing import Any
from fastapi import APIRouter, Response, Depends

from src.server.routes.dependency_factory import _h_service
from src.server.handlers.verification_handlers import VerificationHandlers
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.service.hackathon_service import HackathonService


verification_router = APIRouter(prefix="/hackathon/participants/verify")


def _handler(h_service: HackathonService = Depends(_h_service)) -> VerificationHandlers:
    return VerificationHandlers(h_service)


@verification_router.patch(
    "",
    status_code=200,
    responses={200: {}, 404: {"model": ErrResponse}, 409: {"model": ErrResponse}},
)
async def verify_participant(
    response: Response, jwt_token: str, _handler: VerificationHandlers = Depends(_handler)
) -> Any:
    return await _handler.verify_participant(response=response, jwt_token=jwt_token)
