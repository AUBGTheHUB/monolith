from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import SPONSORS_COLLECTION
from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import SponsorNotFoundError
from datetime import datetime

LOG = get_logger()


class SponsorsRepository(CRUDRepository[Sponsor]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(SPONSORS_COLLECTION)

    async def fetch_by_id(self, obj_id: str) -> Result[Sponsor, Exception]:
        try:
            LOG.info("Fetching sponsor by ObjectId", sponsor_id = obj_id)

            # Query the db for the sponsor with the given id 
            sponsor = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if sponsor is None:
                return Err(SponsorNotFoundError())
            
            return Ok(Sponsor(id=ObjectId(obj_id), **sponsor))
        except Exception as e:
            LOG.exception("Failed to fetch sponsor due to error", sponsor_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self) -> Result[list[Sponsor], Exception]:
        try: 
            LOG.info("Fetching all sponsors")

            sponsors_data = await self._collection.find({}).to_list(length=None)
            sponsors: list[Sponsor] = []

            for sponsor in sponsors_data:
                sponsor["id"] = sponsor.pop("_id")

                sponsors.append(Sponsor(**sponsor))

            LOG.debug(f"Fetched {len(sponsors)} sponsors.")
            return Ok(sponsors)

        except Exception as e:
            LOG.exception(f"Failed to fetch all sponsors due to err: {e}")
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateSponsorParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            update = {"$set": obj_fields.model_dump()}
            print(update)
            projection = {"_id": 0}

            # ReturnDocument.AFTER returns the updated document with the new data
            result = await self._collection.find_one_and_update(
                filter=filter, 
                update=update, 
                projection=projection,
                return_document=ReturnDocument.AFTER,
                session=session
            )
            
            if result is None:
                return Err(SponsorNotFoundError())

            return Ok(Sponsor(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Could not update sponsor", sponsor_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            projection = {"_id": 0}
            result = await self._collection.find_one_and_delete(filter=filter, projection=projection)

            if result is None:
                return Err(SponsorNotFoundError())

            return Ok(Sponsor(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Sponsor deletion failed due to error", sponsor_id=obj_id, error=e)
            return Err(e)

    async def create(
        self, sponsor: Sponsor, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Sponsor, Exception]:
        try:
            LOG.info("Inserting sponsor...", sponsor=sponsor.dump_as_json())
            await self._collection.insert_one(document=sponsor.dump_as_mongo_db_document(), session=session)
            return Ok(sponsor)
        except Exception as e: 
            LOG.debug("Sponsor insertion failed due to...", sponsor_id = str(sponsor.id), error=e)
            return Err(e)