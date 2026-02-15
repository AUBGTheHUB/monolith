from typing import Any, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument
from result import Ok, Result, Err
from src.database.model.admin.hub_admin_model import HubAdmin
from src.exception import DuplicateHubMemberUsernameError, HubMemberNotFoundError
from pymongo.asynchronous.collection import ReturnDocument
from result import Result, Err, Ok
from structlog.stdlib import get_logger
from pymongo.errors import DuplicateKeyError

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import HUB_MEMBERS_COLLECTION
from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import HubMemberNotFoundError

LOG = get_logger()


class HubMembersRepository(CRUDRepository[HubMember]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(HUB_MEMBERS_COLLECTION)

    def _hub_member_from_mongo(self, doc: dict[str, Any]) -> HubMember | HubAdmin:
        member_type = doc.get("member_type")

        if member_type == "admin":
            return HubAdmin.from_mongo_db_document(doc)

        return HubMember.from_mongo_db_document(doc)

    async def create(
        self, hub_member: HubMember | HubAdmin, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember | HubAdmin, DuplicateHubMemberUsernameError | Exception]:
        try:
            LOG.info("Inserting HUB member...", hub_member=hub_member.dump_as_json())
            await self._collection.insert_one(
                document=hub_member.dump_as_mongo_db_document(),
                session=session,
            )
            LOG.info("Successfully inserted HUB member", hub_member=hub_member.dump_as_json())
            return Ok(hub_member)

        except DuplicateKeyError:
            if isinstance(hub_member, HubAdmin):
                LOG.warning("HUB member insertion failed due to a duplicate username")
                return Err(DuplicateHubMemberUsernameError(hub_member.username))
            # no actual other valid case

        except Exception as e:
            LOG.exception("HUB member insertion failed due to error", error=e)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[HubMember | HubAdmin, HubMemberNotFoundError | Exception]:
        try:
            LOG.info("Fetching hub_member by ObjectID...", hub_member_id=obj_id)

            hub_member = await self._collection.find_one(filter={"_id": ObjectId(obj_id)})

            if hub_member is None:
                return Err(HubMemberNotFoundError())

            return Ok(self._hub_member_from_mongo(doc=hub_member))

        except Exception as e:
            LOG.exception("Failed to fetch hub member due to error", hub_member_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self) -> Result[list[HubMember | HubAdmin], Exception]:
        try:
            LOG.info("Fetching all HUB members...")

            hub_members_info = await self._collection.find({}).to_list(length=None)

            hub_members = []
            for hub_member in hub_members_info:
                hub_members.append(self._hub_member_from_mongo(hub_member))

            LOG.debug(f"Fetched {len(hub_members)} hub members")
            return Ok(hub_members)

        except Exception as e:
            LOG.exception(f"Failed to fetch all HUB members due to err {e}")
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateHubMemberParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember | HubAdmin, HubMemberNotFoundError | Exception]:
        try:
            LOG.info(f"Updating HUB member...", hub_member_id=obj_id, updated_fields=obj_fields.model_dump())
            hub_member = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if hub_member is None:
                return Err(HubMemberNotFoundError())

            return Ok(self._hub_member_from_mongo(doc=hub_member))

        except Exception as e:
            LOG.exception("Failed to update HUB member", hub_member_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember | HubAdmin, HubMemberNotFoundError | Exception]:
        try:
            LOG.info("Deleting HUB member...", hub_member_id=obj_id)

            hub_member = await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)}, session=session)

            if hub_member is None:
                return Err(HubMemberNotFoundError())

            return Ok(self._hub_member_from_mongo(doc=hub_member))

        except Exception as e:
            LOG.exception("HUB member deletion failed due to error", hub_member_id=obj_id, error=e)
            return Err(e)

    async def fetch_admin_by_username(self, username: str) -> Result[HubAdmin, HubMemberNotFoundError | Exception]:
        try:
            LOG.info("Trying to get HUB admin by username...", username=username)

            hub_admin = await self._collection.find_one(filter={"username": username})

            if hub_admin is None:
                return Err(HubMemberNotFoundError())

            hub_admin["id"] = hub_admin.pop("_id")
            return Ok(HubAdmin(**hub_admin))

        except Exception as e:
            LOG.exception(f"Failed to fetch HUB admin due to err", error=e)
            return Err(e)
