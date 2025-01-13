# The HTTP handlers defined here are responsible for accepting requests passed from the routes, and returning responses
# in JSON format. This separation is done in order to improve testability and modularity.
#
# To return a custom type-safe JSON response we recommend using the server.schemas.response_schemas.Response object. By
# doing so you will be returning ResponseModels (aka ResponseSchemas in OpenAPI spec terms), and adhering to the
# OpenAPI spec defined in the routes via `responses` or `response_model` arguments.
#
# For more info: https://fastapi.tiangolo.com/advanced/additional-responses/

from result import is_err
from starlette import status
from src.server.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    TeamNotFoundError,
    TeamNameMissmatchError,
)
from src.server.custom_types import DispatchResult, ParticipantRegistrationErrors
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


class ParticipantHandlers:

    def __init__(self, service: ParticipantRegistrationService) -> None:
        self._service = service

    async def create_participant(
        self,
        input_data: ParticipantRequestBody,
        jwt_token: str | None = None,
    ) -> Response:

        # To provide a better DX for the Frontend.
        if isinstance(input_data, InviteLinkParticipantRequestBody) and jwt_token is None:
            return Response(
                ErrResponse(error="When `type` is 'invite_link' jwt_token is expected as a query param."),
                status_code=status.HTTP_409_CONFLICT,
            )

        result = await self._dispatch_request_based_on_input_data(input_data, jwt_token)
        if is_err(result):
            return self._handle_error(err=result.err_value)

        return Response(
            ParticipantRegisteredResponse(participant=result.ok_value[0], team=result.ok_value[1]),
            status_code=status.HTTP_201_CREATED,
        )

    def _dispatch_request_based_on_input_data(
        self, input_data: ParticipantRequestBody, jwt_token: str | None = None
    ) -> DispatchResult:
        if isinstance(input_data, AdminParticipantRequestBody):
            return self._service.register_admin_participant(input_data)

        elif isinstance(input_data, InviteLinkParticipantRequestBody) and jwt_token is not None:
            return self._service.register_invite_link_participant(input_data, jwt_token)

        return self._service.register_random_participant(input_data)

    @staticmethod
    def _handle_error(err: ParticipantRegistrationErrors) -> Response:
        error_mapping = {
            DuplicateEmailError: ("Participant with this email already exists", status.HTTP_409_CONFLICT),
            DuplicateTeamNameError: ("Team with this name already exists", status.HTTP_409_CONFLICT),
            HackathonCapacityExceededError: ("Max hackathon capacity has been reached", status.HTTP_409_CONFLICT),
            TeamCapacityExceededError: ("Max team capacity has been reached", status.HTTP_409_CONFLICT),
            TeamNotFoundError: ("The specified team was not found", status.HTTP_404_NOT_FOUND),
            TeamNameMissmatchError: (
                "team_name passed in the request body is different from the team_name in the" "decoded JWT token",
                status.HTTP_400_BAD_REQUEST,
            ),
        }
        """Add all know custom errors that could occur during participant registration with a custom message and
        If any new Custom errors regarding the participant registration are introduced, update the
        ParticipantRegistrationErrors type alias"""

        # Check if the error is a known type
        for error_type, (message, code) in error_mapping.items():
            if isinstance(err, error_type):
                return Response(ErrResponse(error=message), status_code=code)

        # If the error is a string, use it as the message directly
        if isinstance(err, str):
            return Response(ErrResponse(error=err), status_code=status.HTTP_400_BAD_REQUEST)

        # Default error response
        return Response(
            ErrResponse(error="An unexpected error occurred during the creation of Participant"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
