from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument
from result import Err, Result
from structlog.stdlib import get_logger

from src.database.mongo.collections.admin_collections import PAST_EVENTS_COLLECTION
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.model.admin.past_event_model import PastEvent, UpdatePastEventParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import PastEventNotFoundError

LOG = get_logger()


class PastEventsRepository(CRUDRepository[PastEvent]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(PAST_EVENTS_COLLECTION)

    async def create(
        self, obj: PastEvent, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[PastEvent, Exception]:
        try:
            document = obj.dump_as_mongo_db_document()

            if session:
                await self._collection.insert_one(document, session=session)
            else:
                await self._collection.insert_one(document)

            return Result.ok(obj)
        except Exception as exc:
            LOG.exception("Failed to create past event")
            return Err(exc)

    async def fetch_by_id(self, obj_id: str) -> Result[PastEvent, Exception]:
        try:
            document = await self._collection.find_one({"_id": ObjectId(obj_id)})

            if not document:
                return Err(PastEventNotFoundError())

            return Result.ok(PastEvent(**document))
        except Exception as exc:
            LOG.exception("Failed to fetch past event by id")
            return Err(exc)

    async def fetch_all(self) -> Result[list[PastEvent], Exception]:
        try:
            cursor = self._collection.find({})
            documents = await cursor.to_list(length=None)

            past_events = [PastEvent(**doc) for doc in documents]
            return Result.ok(past_events)
        except Exception as exc:
            LOG.exception("Failed to fetch past events")
            return Err(exc)

    async def update(
        self, obj_id: str, obj_fields: UpdatePastEventParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[PastEvent, Exception]:
        try:
            update_data = obj_fields.model_dump(exclude_none=True)

            if not update_data:
                document = await self._collection.find_one({"_id": ObjectId(obj_id)})
                if not document:
                    return Err(PastEventNotFoundError())
                return Result.ok(PastEvent(**document))

            update_data["updated_at"] = datetime.now(tz=timezone.utc)

            if session:
                document = await self._collection.find_one_and_update(
                    {"_id": ObjectId(obj_id)},
                    {"$set": update_data},
                    return_document=ReturnDocument.AFTER,
                    session=session,
                )
            else:
                document = await self._collection.find_one_and_update(
                    {"_id": ObjectId(obj_id)},
                    {"$set": update_data},
                    return_document=ReturnDocument.AFTER,
                )

            if not document:
                return Err(PastEventNotFoundError())

            return Result.ok(PastEvent(**document))
        except Exception as exc:
            LOG.exception("Failed to update past event")
            return Err(exc)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[PastEvent, Exception]:
        try:
            if session:
                document = await self._collection.find_one_and_delete({"_id": ObjectId(obj_id)}, session=session)
            else:
                document = await self._collection.find_one_and_delete({"_id": ObjectId(obj_id)})

            if not document:
                return Err(PastEventNotFoundError())

            return Result.ok(PastEvent(**document))
        except Exception as exc:
            LOG.exception("Failed to delete past event")
            return Err(exc)
