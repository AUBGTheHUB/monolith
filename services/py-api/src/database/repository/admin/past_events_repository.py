from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import PAST_EVENTS_COLLECTION
from src.database.model.admin.past_event_model import PastEvent, UpdatePastEventParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class PastEventsRepository(CRUDRepository[PastEvent]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(PAST_EVENTS_COLLECTION)

    async def create(
        self, obj: PastEvent, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[list[PastEvent], Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj_fields: UpdatePastEventParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())
