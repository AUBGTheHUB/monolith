from starlette import status

from src.database.db_manager import DB_MANAGER
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import ErrResponse, PongResponse, Response


class UtilityHandlers(BaseHandler):

    def __init__(self, db_manger: DB_MANAGER) -> None:
        self.db_manger = db_manger

    async def ping_services(self) -> Response:
        db_ok = True

        err = await self.db_manger.async_ping_db()
        if err:
            db_ok = False

        if not db_ok:
            return Response(ErrResponse(error="Database not available!"), status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(PongResponse(message="pong"), status_code=status.HTTP_200_OK)
