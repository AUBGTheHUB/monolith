from abc import ABC

from src.exception import ERROR_MAPPING
from src.server.schemas.response_schemas.schemas import ErrResponse, Response
from starlette import status


class BaseHandler(ABC):
    @staticmethod
    def handle_error(err: BaseException) -> Response:
        """
        Accepts an Exception (custom or not) and returns an appropriate response with error message and status code
        """
        # Check if the error is a known type
        for error_type, (message, code) in ERROR_MAPPING.items():
            if isinstance(err, error_type):
                return Response(ErrResponse(error=message), status_code=code)

        # Default error response
        return Response(
            ErrResponse(error="An unexpected error occurred"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
