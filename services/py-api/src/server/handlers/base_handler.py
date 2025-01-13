from abc import ABC

from src.server.custom_types import ERROR_MAPPING
from src.server.schemas.response_schemas.schemas import ErrResponse, Response
from starlette import status


class BaseHandler(ABC): 
    def handle_error(err: BaseException):
        """Add all know custom errors that could occur during participant registration with a custom message and
        If any new Custom errors regarding the participant registration are introduced, update the
        ParticipantRegistrationErrors type alias"""

        # Check if the error is a known type
        for error_type, (message, code) in ERROR_MAPPING.items():
            if isinstance(err, error_type):
                return Response(ErrResponse(error=message), status_code=code)

        # Default error response
        return Response(
            ErrResponse(error="An unexpected error occurred during the creation of Participant"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )