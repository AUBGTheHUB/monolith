from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import MENTORS_COLLECTION
from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import MentorNotFoundError

LOG = get_logger()


class MentorsRepository(CRUDRepository[Mentor]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(MENTORS_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, MentorNotFoundError | Exception]:
        try:
            LOG.info("Fetching mentor by ObjectId", mentor_id=obj_id)

            # Query the db for the mentor with the given id
            mentor = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )

            if mentor is None:
                return Err(MentorNotFoundError())

            return Ok(Mentor(id=ObjectId(obj_id), **mentor))
        except Exception as e:
            LOG.exception("Failed to fetch mentor due to error", mentor_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self) -> Result[list[Mentor], Exception]:
        try:
            LOG.info("Fetching all mentors")

            mentors_data = await self._collection.find({}).to_list(length=None)
            mentors: list[Mentor] = []

            for mentor in mentors_data:
                mentor["id"] = mentor.pop("_id")

                mentors.append(Mentor(**mentor))

            LOG.debug(f"Fetched {len(mentors)} mentors.")
            return Ok(mentors)

        except Exception as e:
            LOG.exception("Failed to fetch mentors due to error", error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateMentorParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, MentorNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            update = {"$set": obj_fields.model_dump(exclude_none=True, exclude_unset=True)}
            projection = {"_id": 0}

            result = await self._collection.find_one_and_update(
                filter=filter,
                update=update,
                projection=projection,
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(MentorNotFoundError())

            return Ok(Mentor(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Could not update mentor", mentor_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, MentorNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            projection = {"_id": 0}
            result = await self._collection.find_one_and_delete(filter=filter, projection=projection, session=session)

            if result is None:
                return Err(MentorNotFoundError())

            return Ok(Mentor(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Mentor deletion failed due to error", mentor_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def create(
        self, mentor: Mentor, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Mentor, MentorNotFoundError | Exception]:
        try:
            LOG.info("Inserting mentor...", mentor=mentor.dump_as_json())
            await self._collection.insert_one(document=mentor.dump_as_mongo_db_document(), session=session)
            return Ok(mentor)
        except Exception as e:
            LOG.exception("Mentor insertion failed due to...", mentor_id=str(mentor.id), error=e)
            return Err(e)
