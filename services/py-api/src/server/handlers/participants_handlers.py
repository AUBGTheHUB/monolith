# The HTTP handlers defined here are responsible for accepting requests passed from the routes, and returning responses
# in JSON format. This separation is done in order to improve testability and modularity.
#
# To return a custom type-safe JSON response we recommend using the server.schemas.response_schemas.Response object. By
# doing so you will be returning ResponseModels (aka ResponseSchemas in OpenAPI spec terms), and adhering to the
# OpenAPI spec defined in the routes via `responses` or `response_model` arguments.
#
# For more info: https://fastapi.tiangolo.com/advanced/additional-responses/

from result import is_err
from src.server.handlers.base_handler import BaseHandler
from starlette import status
from src.server.schemas.request_schemas.schemas import (
    ParticipantRequestBody,
    AdminParticipantRequestBody,
    InviteLinkParticipantRequestBody,
)
from src.server.schemas.response_schemas.schemas import (
    ParticipantRegisteredResponse,
    ErrResponse,
    Response,
)
from src.service.participants_registration_service import ParticipantRegistrationService


class ParticipantHandlers(BaseHandler):

    def __init__(self, service: ParticipantRegistrationService) -> None:
        self._service = service

    async def create_participant(
        self,
        input_data: ParticipantRequestBody,
        jwt_token: str | None = None,
    ) -> Response:

        if isinstance(input_data, AdminParticipantRequestBody):
            result = await self._service.register_admin_participant(input_data)

        elif isinstance(input_data, InviteLinkParticipantRequestBody) and jwt_token is not None:
            result = await self._service.register_invite_link_participant(input_data, jwt_token)

        # To provide a better DX for the Frontend.
        elif isinstance(input_data, InviteLinkParticipantRequestBody) and jwt_token is None:
            return Response(
                ErrResponse(error="When `type` is 'invite_link' jwt_token is expected as a query param."),
                status_code=status.HTTP_409_CONFLICT,
            )

        else:
            result = await self._service.register_random_participant(input_data)

        if is_err(result):
            return self.handle_error(err=result.err_value)

        return Response(
            ParticipantRegisteredResponse(participant=result.ok_value[0], team=result.ok_value[1]),
            status_code=status.HTTP_201_CREATED,
        )
