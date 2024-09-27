from src.server.schemas.response_schemas.schemas import PongResponse


class UtilityHandlers:

    @staticmethod
    async def ping_service() -> PongResponse:
        return PongResponse(message="pong")
