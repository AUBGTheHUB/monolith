from typing import Optional

from pymongo.asynchronous.client_session import AsyncClientSession
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument

from src.database.mongo.collections.event_collections import EVENT_ATTENDEE_COLLECTION
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.model.event.attendee_model import Attendee, UpdateAttendeeParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import AttendeeNotFoundError

LOG = get_logger()


class AttendeesRepository(CRUDRepository[Attendee]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(EVENT_ATTENDEE_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        try:
            LOG.info("Fetching attendee by ObjectId", attendee_id=obj_id)

            # Query the db for the attendee with the given id
            attendee = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )

            if attendee is None:
                return Err(AttendeeNotFoundError())

            return Ok(Attendee(id=ObjectId(obj_id), **attendee))
        except Exception as e:
            LOG.exception("Failed to fetch attendee due to error", attendee_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self, session: Optional[AsyncClientSession] = None) -> Result[list[Attendee], Exception]:
        try:
            LOG.info("Fetching all attendees")

            attendees_data = await self._collection.find({}, session=session).to_list(length=None)
            attendees: list[Attendee] = []

            for attendee in attendees_data:
                attendee["id"] = attendee.pop("_id")

                attendees.append(Attendee(**attendee))

            LOG.debug(f"Fetched {len(attendees)} attendees.")
            return Ok(attendees)

        except Exception as e:
            LOG.exception(f"Failed to fetch all attendees due to err: {e}")
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateAttendeeParams, session: Optional[AsyncClientSession] = None
    ) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            update = {"$set": obj_fields.model_dump(exclude_none=True, exclude_unset=True)}
            projection = {"_id": 0}

            # ReturnDocument.AFTER returns the updated document with the new data
            result = await self._collection.find_one_and_update(
                filter=filter,
                update=update,
                projection=projection,
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(AttendeeNotFoundError())

            return Ok(Attendee(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Could not update attendee", attendee_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            projection = {"_id": 0}
            result = await self._collection.find_one_and_delete(filter=filter, projection=projection, session=session)

            if result is None:
                return Err(AttendeeNotFoundError())

            return Ok(Attendee(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Attendee deletion failed due to error", attendee_id=obj_id, error=e)
            return Err(e)

    async def create(
        self, attendee: Attendee, session: Optional[AsyncClientSession] = None
    ) -> Result[Attendee, AttendeeNotFoundError | Exception]:
        try:
            LOG.info("Inserting attendee...", attendee=attendee.dump_as_json())
            await self._collection.insert_one(document=attendee.dump_as_mongo_db_document(), session=session)
            return Ok(attendee)
        except Exception as e:
            LOG.debug("Attendee insertion failed due to...", attendee_id=str(attendee.id), error=e)
            return Err(e)
