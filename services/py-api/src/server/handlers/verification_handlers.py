from typing import Annotated

from fastapi import BackgroundTasks, Depends
from result import is_err
from src.server.handlers.base_handler import BaseHandler
from src.service.participants_verification_service import (
    ParticipantVerificationService,
    ParticipantVerificationServiceDep,
)
from starlette import status
from src.utils import JwtUtility
from src.server.schemas.response_schemas.schemas import (
    ParticipantVerifiedResponse,
    Response,
    VerificationEmailSentSuccessfullyResponse,
)
from src.server.schemas.jwt_schemas.schemas import JwtParticipantVerificationData


class VerificationHandlers(BaseHandler):

    def __init__(self, service: ParticipantVerificationService) -> None:
        self._service = service

    async def verify_participant(self, jwt_token: str, background_tasks: BackgroundTasks) -> Response:
        # We decode the token here so that we can determine the case of verification that we
        # are dealing with: `admin verification` or `random participant verification`.
        result = JwtUtility.decode_data(token=jwt_token, schema=JwtParticipantVerificationData)

        if is_err(result):
            return self.handle_error(result.err_value)

        jwt_payload = result.ok_value

        if jwt_payload["is_admin"]:
            result = await self._service.verify_admin_participant(
                jwt_data=jwt_payload, background_tasks=background_tasks
            )

        else:
            result = await self._service.verify_random_participant(
                jwt_data=jwt_payload, background_tasks=background_tasks
            )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=ParticipantVerifiedResponse(participant=result.ok_value[0], team=result.ok_value[1]),
            status_code=status.HTTP_200_OK,
        )

    async def resend_verification_email(self, participant_id: str, background_tasks: BackgroundTasks) -> Response:

        result = await self._service.resend_verification_email(
            participant_id=participant_id, background_tasks=background_tasks
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=VerificationEmailSentSuccessfullyResponse(participant=result.ok_value),
            status_code=status.HTTP_200_OK,
        )


def verification_handlers_provider(service: ParticipantVerificationServiceDep) -> VerificationHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "provider" of an
    instance. ``fastapi.Depends`` will automatically inject the VerificationHandlers instance into its intended
    consumers by calling this provider.

    Args:
        service: An automatically injected ParticipantVerificationService instance by FastAPI using ``fastapi.Depends``

    Returns:
        A VerificationHandlers instance
    """
    return VerificationHandlers(service=service)


# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
VerificationHandlersDep = Annotated[VerificationHandlers, Depends(verification_handlers_provider)]
"""FastAPI dependency for automatically injecting a VerificationHandlers instance into consumers"""
