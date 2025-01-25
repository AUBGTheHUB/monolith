from fastapi import APIRouter, Depends
from src.server.handlers.verification_handlers import VerificationHandlers
from src.server.schemas.request_schemas.schemas import ResendEmailParticipantData
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantVerifiedResponse,
    Response,
    VerificationEmailSentSuccessfullyResponse,
)
from src.service.participants_verification_service import ParticipantVerificationService
from src.service.hackathon_service import HackathonService
from src.server.routes.dependency_factory import _h_service


verification_router = APIRouter(prefix="/hackathon/participants/verify")


def _p_verify_service(h_service: HackathonService = Depends(_h_service)) -> ParticipantVerificationService:
    return ParticipantVerificationService(h_service)


def _handler(p_verify_service: ParticipantVerificationService = Depends(_p_verify_service)) -> VerificationHandlers:
    return VerificationHandlers(p_verify_service)


@verification_router.patch(
    "",
    status_code=200,
    responses={200: {"model": ParticipantVerifiedResponse}, 404: {"model": ErrResponse}},
)
async def verify_participant(jwt_token: str, _handler: VerificationHandlers = Depends(_handler)) -> Response:
    return await _handler.verify_participant(jwt_token=jwt_token)


@verification_router.post(
    "/send-email",
    status_code=200,
    responses={
        200: {"model": VerificationEmailSentSuccessfullyResponse},
        400: {"model": ErrResponse},
        404: {"model": ErrResponse},
        409: {"model": ErrResponse},
    },
)
async def send_verification_email(
    email_verification_request_body: ResendEmailParticipantData, _handler: VerificationHandlers = Depends(_handler)
) -> Response:
    return await _handler.send_verification_email(participant_id=email_verification_request_body.participant_id)
