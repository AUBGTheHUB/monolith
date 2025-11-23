from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import HUB_MEMBERS_COLLECTION
from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class HubMembersRepository(CRUDRepository[HubMember]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(HUB_MEMBERS_COLLECTION)

    async def create(
        self, obj: HubMember, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[list[HubMember], Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj_fields: UpdateHubMemberParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[HubMember, Exception]:
        return Err(NotImplementedError())
