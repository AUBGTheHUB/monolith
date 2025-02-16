from fastapi import APIRouter, BackgroundTasks, Depends
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
from src.server.routes.dependency_factory import _h_service, registration_open

verification_router = APIRouter(prefix="/hackathon/participants/verify")


def _p_verify_service(h_service: HackathonService = Depends(_h_service)) -> ParticipantVerificationService:
    return ParticipantVerificationService(h_service)


def _handler(p_verify_service: ParticipantVerificationService = Depends(_p_verify_service)) -> VerificationHandlers:
    return VerificationHandlers(p_verify_service)


@verification_router.patch(
    "",
    status_code=200,
    responses={200: {"model": ParticipantVerifiedResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
    dependencies=[Depends(registration_open)],
)
async def verify_participant(
    jwt_token: str, background_tasks: BackgroundTasks, _handler: VerificationHandlers = Depends(_handler)
) -> Response:
    return await _handler.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks)


@verification_router.post(
    "/send-email",
    status_code=202,
    responses={
        202: {"model": VerificationEmailSentSuccessfullyResponse},
        400: {"model": ErrResponse},
        404: {"model": ErrResponse},
        429: {"model": ErrResponse},
    },
    dependencies=[Depends(registration_open)],
)
async def send_verification_email(
    email_verification_request_body: ResendEmailParticipantData,
    background_tasks: BackgroundTasks,
    _handler: VerificationHandlers = Depends(_handler),
) -> Response:
    return await _handler.resend_verification_email(
        participant_id=email_verification_request_body.participant_id, background_tasks=background_tasks
    )
