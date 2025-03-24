from fastapi import APIRouter

from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantVerifiedResponse,
    VerificationEmailSentSuccessfullyResponse,
)


def register_verification_routes(router: APIRouter, http_handler: VerificationHandlers) -> None:
    router.add_api_route(
        path="/hackathon/participants/verify",
        methods=["PATCH"],
        endpoint=http_handler.verify_participant,
        responses={
            200: {"model": ParticipantVerifiedResponse},
            404: {"model": ErrResponse},
            400: {"model": ErrResponse},
        },
    )

    router.add_api_route(
        path="/hackathon/participants/verify/send-email",
        methods=["POST"],
        endpoint=http_handler.resend_verification_email,
        status_code=202,
        responses={
            202: {"model": VerificationEmailSentSuccessfullyResponse},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
            429: {"model": ErrResponse},
        },
    )
