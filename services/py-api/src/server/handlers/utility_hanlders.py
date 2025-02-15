from typing import Annotated

from fastapi import Depends
from starlette import status

from src.database.db_managers import MongoDatabaseManagerDep
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import ErrResponse, PongResponse, Response


class UtilityHandlers(BaseHandler):

    def __init__(self, db_manger: MongoDatabaseManagerDep) -> None:
        self.db_manger = db_manger

    async def ping_services(self) -> Response:
        db_ok = True

        err = await self.db_manger.async_ping_db()
        if err:
            db_ok = False

        if not db_ok:
            return Response(ErrResponse(error="Database not available!"), status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(PongResponse(message="pong"), status_code=status.HTTP_200_OK)


def utility_handlers_provider(db_manger: MongoDatabaseManagerDep) -> UtilityHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "provider" of an
    instance. ``fastapi.Depends`` will automatically inject the UtilityHandlers instance into its intended
    consumers by calling this provider.

    Args:
        db_manger: An automatically injected MongoDatabaseManager instance by FastAPI using ``fastapi.Depends``

    Returns:
        A UtilityHandlers instance
    """
    return UtilityHandlers(db_manger=db_manger)


# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
UtilityHandlersDep = Annotated[UtilityHandlers, Depends(utility_handlers_provider)]
"""FastAPI dependency for automatically injecting a UtilityHandlers instance into consumers"""
