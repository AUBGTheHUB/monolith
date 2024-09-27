from typing import Optional, Type

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from result import Result, Ok, Err
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.database.model.participant_model import Participant
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import DuplicateEmail
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody

LOG = get_logger()


class ParticipantsRepository(CRUDRepository):
    # TODO: Implement the rest of the methods
    def __init__(self, db_manager: DatabaseManager, collection: str) -> None:
        self._client = db_manager.client
        self._collection = self._client[db_manager.DB_NAME][collection]

    async def fetch_by_id(self, obj_id: str) -> Result:
        raise NotImplementedError()

    async def fetch_all(self) -> Result:
        raise NotImplementedError()

    async def update(
        self, obj_id: str, input_data: BaseModel, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result:
        raise NotImplementedError()

    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result:
        raise NotImplementedError()

    async def create(
        self, input_data: ParticipantRequestBody, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Ok[Participant] | Err[Type[DuplicateEmail]] | Err[Exception]:
        try:
            participant = Participant(
                _id=ObjectId(), name=input_data.name, email=input_data.email, is_admin=input_data.is_admin
            )
            LOG.debug("Inserting participant {}".format(participant.model_dump()))
            await self._collection.insert_one(document=participant.model_dump(), session=session)
            return Ok(participant)
        except DuplicateKeyError:
            LOG.warn("Participant insertion failed due to duplicate email {}".format(input_data.email))
            return Err(DuplicateEmail("Duplicate email"))
        except Exception as e:
            LOG.exception("Participant insertion failed due to err {}".format(e))
            return Err(e)
