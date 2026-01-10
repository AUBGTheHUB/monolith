from typing import Optional

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
        await self._collection.insert_one(obj)
        return Ok()

    async def fetch_by_id(self, obj_id: str) -> Result[Sponsor, Exception]:
        sponsor = await self._collection.find_one({"_id": obj_id})
        if sponsor is None:
            return Err(NotImplementedError()) # TODO: Change with proper exception
        return Ok(sponsor)

    async def fetch_all(self) -> Result[list[Sponsor], Exception]:
        try: 
            sponsors_data = await self._collection.find({}).to_list()

            sponsors: List[Sponsor] = []

            async for sponsor in sponsors_data:
                sponsor["id"] = sponsor.pop("_id")

                sponsor.append(Sponsor(**sponsor))

            return Ok(sponsors)

        except Exception as e:
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateSponsorParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        try:
            query_filter = {'_id': obj_id}
            operation = { '$set' : obj_fields }
            result = await self._collection.update(query_filter, operation)
            
            if result is None:
                return Err(NotImplementedError()) # TODO: Add proper handling

        except Exception as e:
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        try:
            pass
        except Exception as e:
            return Err(e)
