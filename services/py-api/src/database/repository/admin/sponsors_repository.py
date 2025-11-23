from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import SPONSORS_COLLECTION
from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class SponsorsRepository(CRUDRepository[Sponsor]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(SPONSORS_COLLECTION)

    async def create(
        self, obj: Sponsor, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[List[Sponsor], Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj_fields: UpdateSponsorParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())
