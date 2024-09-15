from pymongo.errors import ConnectionFailure

from fastapi import Response, status
from result import is_err

from src.database.db_manager import ping_db
from src.server.response_schemas.schemas import ErrResponse, PongResponse


class UtilityHandlers:
    @staticmethod
    async def ping_services(response: Response) -> PongResponse | ErrResponse:
        db_ok = True

        err = ping_db()
        if err:
            db_ok = False

        if not db_ok:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return ErrResponse(error="Database not available!")

        return PongResponse(message="pong")
