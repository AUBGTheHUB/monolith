from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err
from structlog.stdlib import get_logger

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.admin_collections import TEAM_MEMBERS_COLLECTION
from src.database.model.admin.team_member_model import TeamMember, UpdateTeamMemberParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class TeamMembersRepository(CRUDRepository[TeamMember]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(TEAM_MEMBERS_COLLECTION)

    async def create(
        self, obj: TeamMember, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[List[TeamMember], Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj_fields: UpdateTeamMemberParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[TeamMember, Exception]:
        return Err(NotImplementedError())
