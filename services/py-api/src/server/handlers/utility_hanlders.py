from fastapi import Response, status

from src.database.db_manager import DB_MANAGER
from src.server.schemas.response_schemas.schemas import ErrResponse, PongResponse


class UtilityHandlers:

    def __init__(self, db_manger: DB_MANAGER) -> None:
        self.db_manger = db_manger

    async def ping_services(self, response: Response) -> PongResponse | ErrResponse:
        db_ok = True

        err = await self.db_manger.async_ping_db()
        if err:
            db_ok = False

        if not db_ok:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return ErrResponse(error="Database not available!")

        return PongResponse(message="pong")