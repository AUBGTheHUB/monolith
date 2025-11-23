from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import MENTORS_COLLECTION
from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class MentorsRepository(CRUDRepository[Mentor]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(MENTORS_COLLECTION)

    async def create(
        self, obj: Mentor, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[List[Mentor], Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj_fields: UpdateMentorParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())
