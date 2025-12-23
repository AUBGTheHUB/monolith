from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import JUDGES_COLLECTION
from src.database.model.admin.judge_model import Judge, UpdateJudgeParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class JudgesRepository(CRUDRepository[Judge]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(JUDGES_COLLECTION)

    async def create(self, obj: Judge, session: Optional[AsyncIOMotorClientSession] = None) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[list[Judge], Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj_fields: UpdateJudgeParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Judge, Exception]:
        return Err(NotImplementedError())
