from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.asynchronous.collection import ReturnDocument
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import HUB_MEMBERS_COLLECTION
from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import HubMemberNotFoundError

LOG = get_logger()


class HubMembersRepository(CRUDRepository[HubMember]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(HUB_MEMBERS_COLLECTION)

    async def create(
        self, obj: HubMember, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember, Exception]:
        try:
            LOG.debug("Creating hub member...", member_name=obj.name)
            doc = obj.dump_as_mongo_db_document()
            await self._collection.insert_one(doc, session=session)
            LOG.debug("Hub member created successfully.", member_id=str(obj.id))
            return Ok(obj)
        except Exception as e:
            LOG.exception("Failed to create hub member due to error", error=e, member_name=obj.name)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[HubMember, HubMemberNotFoundError | Exception]:
        try:
            LOG.debug("Fetching hub member by ObjectId...", member_id=obj_id)

            member = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if member is None:
                return Err(HubMemberNotFoundError())

            return Ok(HubMember(id=ObjectId(obj_id), **member))
        except Exception as e:
            LOG.exception("Failed to fetch hub member due to error", member_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self) -> Result[list[HubMember], Exception]:
        try:
            LOG.debug("Fetching all hub members...")

            members_data = await self._collection.find({}).to_list(length=None)

            members = []
            for doc in members_data:
                doc["id"] = doc.pop("_id")
                members.append(HubMember(**doc))

            LOG.debug("Fetched hub members.", count=len(members))
            return Ok(members)

        except Exception as e:
            LOG.exception("Failed to fetch all hub members due to error", error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateHubMemberParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember, HubMemberNotFoundError | Exception]:
        try:
            LOG.debug("Updating hub member...", member_id=obj_id, updated_fields=obj_fields.model_dump())

            result = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(HubMemberNotFoundError())

            return Ok(HubMember(id=ObjectId(obj_id), **result))
        except Exception as e:
            LOG.exception("Failed to update hub member", member_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember, HubMemberNotFoundError | Exception]:
        try:
            LOG.debug("Deleting hub member...", member_id=obj_id)

            member = await self._collection.find_one_and_delete(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )
            if member is None:
                return Err(HubMemberNotFoundError())

            return Ok(HubMember(id=ObjectId(obj_id), **member))
        except Exception as e:
            LOG.exception("Failed to delete hub member due to error", member_id=obj_id, error=e)
            return Err(e)
