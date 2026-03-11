from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err, Ok
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import JUDGES_COLLECTION
from src.database.model.admin.judge_model import Judge, UpdateJudgeParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import JudgeNotFoundError

LOG = get_logger()


class JudgesRepository(CRUDRepository[Judge]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(JUDGES_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Judge, JudgeNotFoundError | Exception]:
        try:
            LOG.info("Fetching judge by ObjectId", sponsor_id=obj_id)

            # Query the db for the sponsor with the given id
            judge = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )

            if judge is None:
                return Err(JudgeNotFoundError())

            return Ok(Judge(id=ObjectId(obj_id), **judge))
        except Exception as e:
            LOG.exception("Failed to fetch judge due to error", judge_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self, session: Optional[AsyncIOMotorClientSession] = None) -> Result[list[Judge], Exception]:
        try:
            LOG.info("Fetching all judges")

            judges_data = await self._collection.find({}, session=session).to_list(length=None)
            judges: list[Judge] = []

            for judge in judges_data:
                judge["id"] = judge.pop("_id")

                judges.append(Judge(**judge))

            LOG.debug(f"Fetched {len(judges)} judges.")
            return Ok(judges)

        except Exception as e:
            LOG.exception(f"Failed to fetch all judges due to err: {e}")
            return Err(e)

    async def create(
        self, judge: Judge, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Judge, JudgeNotFoundError | Exception]:
        try:
            LOG.info("Inserting judge...", judge=judge.dump_as_json())
            await self._collection.insert_one(document=judge.dump_as_mongo_db_document(), session=session)
            return Ok(judge)
        except Exception as e:
            LOG.debug("Judge insertion failed due to...", judge_id=str(judge.id), error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateJudgeParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Judge, JudgeNotFoundError | Exception]:
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
                return Err(JudgeNotFoundError())

            return Ok(Judge(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Could not update judge", judge_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Judge, JudgeNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            projection = {"_id": 0}
            result = await self._collection.find_one_and_delete(filter=filter, projection=projection, session=session)

            if result is None:
                return Err(JudgeNotFoundError())

            return Ok(Judge(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Judge deletion failed due to error", judge_id=obj_id, error=e)
            return Err(e)
