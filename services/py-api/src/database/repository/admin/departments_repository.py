from typing import Optional, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.asynchronous.collection import ReturnDocument
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.model.admin.department_model import Department, Member, UpdateDepartmentParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.base_repository import CRUDRepository
from src.exception import DepartmentNotFoundError

LOG = get_logger()


class DepartmentsRepository(CRUDRepository[Department]):
    def __init__(self, db_manager: MongoDatabaseManager, collection_name: str):
        self._collection = db_manager.get_collection(collection_name)

    def _convert_member_dicts(self, doc: dict) -> None:
        if "members" in doc and doc["members"]:
            for member in doc["members"]:
                member.pop("_id", None)
            doc["members"] = [Member(**member) for member in doc["members"]]

    async def create(
        self, obj: Department, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Department, Exception]:
        try:
            LOG.info("Inserting department...", department=obj.dump_as_json())
            await self._collection.insert_one(document=obj.dump_as_mongo_db_document(), session=session)
            return Ok(obj)

        except Exception as e:
            LOG.exception("Department insertion failed due to error", department_id=str(obj.id), error=e)
            return Err(e)

    async def fetch_all(self) -> Result[List[Department], Exception]:
        try:
            LOG.info("Fetching all departments...")
            departments_data = await self._collection.find({}).to_list(length=None)

            departments = []

            for doc in departments_data:
                doc["id"] = doc.pop("_id")
                self._convert_member_dicts(doc)
                departments.append(Department(**doc))

            LOG.debug("Fetched departments.", count=len(departments))
            return Ok(departments)

        except Exception as e:
            LOG.exception("Failed to fetch all departments due to error", error=e)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[Department, DepartmentNotFoundError | Exception]:
        try:
            LOG.debug("Fetching department by ObjectId...", department_id=obj_id)

            department = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if department is None:
                return Err(DepartmentNotFoundError())

            self._convert_member_dicts(department)

            return Ok(Department(id=ObjectId(obj_id), **department))

        except Exception as e:
            LOG.exception("Failed to fetch department due to error", department_id=obj_id, error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateDepartmentParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Department, DepartmentNotFoundError | Exception]:
        try:
            LOG.info("Updating department...", department_id=obj_id, updated_fields=obj_fields.model_dump())

            result = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(DepartmentNotFoundError())

            self._convert_member_dicts(result)

            return Ok(Department(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Failed to update the department", department_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Department, DepartmentNotFoundError | Exception]:
        try:
            LOG.info("Deleting department...", department_id=obj_id)

            result = await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if result is None:
                return Err(DepartmentNotFoundError())

            self._convert_member_dicts(result)

            return Ok(Department(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Department deletion failed due to error", department_id=obj_id, error=e)
            return Err(e)

