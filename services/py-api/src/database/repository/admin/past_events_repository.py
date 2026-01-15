from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument
from result import Err, Ok, Result
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
        self,
        obj: PastEvent,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[PastEvent, Exception]:
        try:
            document = obj.dump_as_mongo_db_document()
            await self._collection.insert_one(document, session=session)
            return Ok(obj)
        except Exception as exc:
            LOG.exception("Failed to create past event")
            return Err(exc)

    async def fetch_by_id(
        self,
        obj_id: str,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[PastEvent, Exception]:
        try:
            document = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)},
                projection={"_id": 0},
                session=session,
            )

            if document is None:
                return Err(PastEventNotFoundError())

            return Ok(PastEvent(id=ObjectId(obj_id), **document))
        except Exception as exc:
            LOG.exception("Failed to fetch past event by id")
            return Err(exc)

    async def fetch_all(
        self,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[list[PastEvent], Exception]:
        try:
            cursor = self._collection.find(
                {},
                projection={
                    "_id": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "title": 1,
                    "cover_picture": 1,
                    "tags": 1,
                },
                session=session,
            )
            documents = await cursor.to_list(length=None)

            past_events: list[PastEvent] = []
            for doc in documents:
                doc_id = doc.get("_id")
                if doc_id is None:
                    continue

                doc.pop("_id", None)
                past_events.append(PastEvent(id=doc_id, **doc))

            return Ok(past_events)
        except Exception as exc:
            LOG.exception("Failed to fetch past events")
            return Err(exc)

    async def update(
        self,
        obj_id: str,
        obj_fields: UpdatePastEventParams,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[PastEvent, Exception]:
        try:
            update_data = obj_fields.model_dump()
            LOG.info("Updating past event...", past_event_id=obj_id, updated_fields=update_data)

            # If no fields are provided, return the current document (single DB call).
            if not update_data:
                document = await self._collection.find_one(
                    filter={"_id": ObjectId(obj_id)},
                    projection={"_id": 0},
                    session=session,
                )

                if document is None:
                    return Err(PastEventNotFoundError())

                return Ok(PastEvent(id=ObjectId(obj_id), **document))

            document = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": update_data},
                return_document=ReturnDocument.AFTER,
                projection={"_id": 0},
                session=session,
            )

            if document is None:
                return Err(PastEventNotFoundError())

            return Ok(PastEvent(id=ObjectId(obj_id), **document))
        except Exception as exc:
            LOG.exception("Failed to update past event")
            return Err(exc)

    async def delete(
        self,
        obj_id: str,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[PastEvent, Exception]:
        try:
            document = await self._collection.find_one_and_delete(
                filter={"_id": ObjectId(obj_id)},
                projection={"_id": 0},
                session=session,
            )

            if document is None:
                return Err(PastEventNotFoundError())

            return Ok(PastEvent(id=ObjectId(obj_id), **document))
        except Exception as exc:
            LOG.exception("Failed to delete past event")
            return Err(exc)
