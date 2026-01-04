from src.database.model.sponsor_model import Sponsor, SponsorTier
from src.database.repository.base_repository import CRUDRepository

from motor.motor_asyncio import AsyncIOMotorClientSession
from src.database.mongo.db_manager import MongoDatabaseManager
from structlog.stdlib import get_logger

from result import Result, Err, Ok

from typing import List, Optional

LOG = get_logger()

class SponsorRepository(CRUDRepository[Sponsor]):
    def __init__(self, db_manager: MongoDatabaseManager, collection_name: str):
        self._collection = db_manager.get_collection(collection_name)

    async def create(self, obj: Sponsor, session: Optional[AsyncIOMotorClientSession] = None) -> Result[Sponsor, Exception]:
        await self._collection.insert_one(obj)
        return Ok()

    async def fetch_by_id(self, obj_id: str) -> Result[Sponsor, Err]:
        sponsor = await self._collection.find_one({"_id": obj_id})
        if sponsor is None:
            return Err(NotImplementedError()) # TODO: Change with proper exception
        return Ok(sponsor)

    async def fetch_all(self) -> Result[List[Sponsor], Exception]:
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
        self,
        obj_id: str,
        obj_fields: Sponsor,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Sponsor, Exception]:
        try:
            query_filter = {'_id': obj_id}
            operation = { '$set' : obj_fields }
            result = await self._collection.update(query_filter, operation)
            
            if result is None:
                return Err(NotImplementedError()) # TODO: Add proper handling

        except Exception as e:
            return Err(e)

    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result[Sponsor, Exception]:
        try:
            pass
        except Exception as e:
            return Err(e)