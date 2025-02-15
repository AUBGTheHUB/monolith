from fastapi import APIRouter, BackgroundTasks

from src.server.handlers.verification_handlers import VerificationHandlersDep
from src.server.schemas.request_schemas.schemas import ResendEmailParticipantData
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantVerifiedResponse,
    Response,
    VerificationEmailSentSuccessfullyResponse,
)

verification_router = APIRouter(prefix="/hackathon/participants/verify")


@verification_router.patch(
    "",
    status_code=200,
    responses={200: {"model": ParticipantVerifiedResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
)
async def verify_participant(
    jwt_token: str, background_tasks: BackgroundTasks, handler: VerificationHandlersDep
) -> Response:
    return await handler.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks)


@verification_router.post(
    "/send-email",
    status_code=202,
    responses={
        202: {"model": VerificationEmailSentSuccessfullyResponse},
        400: {"model": ErrResponse},
        404: {"model": ErrResponse},
        429: {"model": ErrResponse},
    },
)
async def send_verification_email(
    email_verification_request_body: ResendEmailParticipantData,
    background_tasks: BackgroundTasks,
    handler: VerificationHandlersDep,
) -> Response:
    return await handler.resend_verification_email(
        participant_id=email_verification_request_body.participant_id, background_tasks=background_tasks
    )
