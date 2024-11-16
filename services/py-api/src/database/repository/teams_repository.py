from typing import Optional, Any, Dict

from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.database.model.team_model import Team
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import DuplicateTeamNameError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody

LOG = get_logger()


class TeamsRepository(CRUDRepository):
    def __init__(self, db_manager: DatabaseManager, collection_name: str) -> None:
        self._collection = db_manager.get_collection(collection_name)

    async def create(
        self,
        input_data: ParticipantRequestBody,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Dict[str, Any]
    ) -> Result[Team, DuplicateTeamNameError | Exception]:

        try:
            team = Team(name=input_data.team_name)
            LOG.debug("Inserting team...", team=team.dump_as_json())
            await self._collection.insert_one(document=team.dump_as_mongo_db_document(), session=session)
            return Ok(team)

        except DuplicateKeyError:
            LOG.warning("Team insertion failed due to duplicate team name", team_name=input_data.team_name)
            return Err(DuplicateTeamNameError(input_data.team_name))

        except Exception as e:
            LOG.exception("Team insertion failed due to err {}".format(e))
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result:
        raise NotImplementedError()

    async def fetch_all(self) -> Result:
        raise NotImplementedError()

    async def update(
        self,
        obj_id: str,
        input_data: BaseModel,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Dict[str, Any]
    ) -> Result:
        raise NotImplementedError()

    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result:
        raise NotImplementedError()
    
    async def get_number_registered_teams(self):
        return self._collection.find({"is_verified": "true"}).count()
