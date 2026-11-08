from typing import Optional, cast

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.asynchronous.client_session import AsyncClientSession
from pydantic import BaseModel
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.tournament_collections import GROUPS_COLLECTION
from src.database.model.tournament.group_model import Group
from src.database.repository.base_repository import CRUDRepository
from src.exception import GroupNotFoundError

LOG = get_logger()


class GroupsRepository(CRUDRepository[Group]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(GROUPS_COLLECTION)

    async def fetch_by_id(self, obj_id: str, session: Optional[AsyncClientSession] = None) -> Result[Group, Err]:
        try:
            LOG.info("Fetching group by ObjectId", group_id=obj_id)

            group = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)},
                projection={"_id": 0},
                session=session,
            )

            if group is None:
                return cast(
                    Result[Group, Err],
                    cast(object, Err(GroupNotFoundError())),
                )

            return Ok(Group(id=ObjectId(obj_id), **group))

        except Exception as e:
            LOG.exception("Failed to fetch group", group_id=obj_id, error=e)
            return cast(
                Result[Group, Err],
                cast(object, Err(e)),
            )

    async def fetch_all(self, session: Optional[AsyncClientSession] = None) -> Result[list[Group], Exception]:
        try:
            LOG.info("Fetching all groups")

            groups_data = await self._collection.find({}, session=session).to_list(length=None)

            groups: list[Group] = []

            for group in groups_data:
                group["id"] = group.pop("_id")
                groups.append(Group(**group))

            return Ok(groups)

        except Exception as e:
            LOG.exception("Failed to fetch all groups", error=e)
            return Err(e)

    async def create(self, obj: Group, session: Optional[AsyncClientSession] = None) -> Result[Group, Exception]:
        try:
            LOG.info("Creating group", group_id=str(obj.id))

            await self._collection.insert_one(
                document=obj.dump_as_mongo_db_document(),
                session=session,
            )

            return Ok(obj)

        except Exception as e:
            LOG.exception("Failed to create group", group_id=str(obj.id), error=e)
            return Err(e)

    async def update(
        self,
        obj_id: str,
        obj_fields: BaseModel,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Group, GroupNotFoundError | Exception]:
        try:
            filter_query = {"_id": ObjectId(obj_id)}
            update_query = {"$set": obj_fields.model_dump()}

            result = await self._collection.find_one_and_update(
                filter=filter_query,
                update=update_query,
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(GroupNotFoundError())

            return Ok(Group(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Failed to update group", group_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[Group, GroupNotFoundError | Exception]:
        try:
            result = await self._collection.find_one_and_delete(
                filter={"_id": ObjectId(obj_id)},
                projection={"_id": 0},
                session=session,
            )

            if result is None:
                return Err(GroupNotFoundError())

            return Ok(Group(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Failed to delete group", group_id=obj_id, error=e)
            return Err(e)
