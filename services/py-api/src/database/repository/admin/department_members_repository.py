from typing import Optional, cast, Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.asynchronous.collection import ReturnDocument
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.model.admin.department_member_model import DepartmentMember, UpdateDepartmentMemberParams
from src.database.mongo.db_manager import MongoDatabaseManager, DEPARTMENT_MEMBERS_COLLECTION
from src.database.repository.base_repository import CRUDRepository
from src.exception import DepartmentMemberNotFoundError

LOG = get_logger()


class DepartmentMembersRepository(CRUDRepository[DepartmentMember]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(DEPARTMENT_MEMBERS_COLLECTION)

    async def create(
        self, obj: DepartmentMember, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[DepartmentMember, Exception]:
        try:
            LOG.debug("Creating department member...", member_name=obj.name)
            doc = obj.dump_as_mongo_db_document()
            await self._collection.insert_one(doc, session=session)
            LOG.debug("Department member created successfully.", member_id=str(obj.id))
            return Ok(obj)

        except Exception as e:
            LOG.exception("Failed to create department member due to error", error=e, member_name=obj.name)
            return Err(e)

    async def fetch_all(self) -> Result[list[DepartmentMember], Exception]:
        try:
            LOG.debug("Fetching all department members...")
            members_data = await self._collection.find({}).to_list(length=None)

            members = []
            for doc in members_data:
                doc["id"] = doc.pop("_id")
                members.append(DepartmentMember(**doc))

            LOG.debug("Fetched department members.", count=len(members))
            return Ok(members)

        except Exception as e:
            LOG.exception("Failed to fetch all department members due to error", error=e)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[DepartmentMember, DepartmentMemberNotFoundError | Exception]:
        try:
            LOG.debug("Fetching department member by ObjectId...", member_id=obj_id)
            member = cast(dict[str, Any], await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}))

            if member is None:
                return Err(DepartmentMemberNotFoundError())

            return Ok(DepartmentMember(id=ObjectId(obj_id), **member))

        except Exception as e:
            LOG.exception("Failed to fetch department member due to error", member_id=obj_id, error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateDepartmentMemberParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[DepartmentMember, DepartmentMemberNotFoundError | Exception]:
        try:
            LOG.debug("Updating department member...", member_id=obj_id, updated_fields=obj_fields.model_dump())

            result = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(DepartmentMemberNotFoundError())

            return Ok(DepartmentMember(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Failed to update department member", member_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[DepartmentMember, DepartmentMemberNotFoundError | Exception]:
        try:
            LOG.debug("Deleting department member...", member_id=obj_id)
            member = cast(dict[str, Any], await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)}, session=session))

            if member is None:
                return Err(DepartmentMemberNotFoundError())

            member["id"] = member.pop("_id")
            return Ok(DepartmentMember(**member))

        except Exception as e:
            LOG.exception("Failed to delete department member due to error", member_id=obj_id, error=e)
            return Err(e)

