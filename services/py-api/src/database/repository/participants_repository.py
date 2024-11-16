from typing import Optional, Any, Dict

from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from result import Result, Ok, Err
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.database.model.participant_model import Participant
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import DuplicateEmailError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody

LOG = get_logger()


class ParticipantsRepository(CRUDRepository):
    # TODO: Implement the rest of the methods
    def __init__(self, db_manager: DatabaseManager, collection_name: str) -> None:
        self._collection = db_manager.get_collection(collection_name)

    async def fetch_by_id(self, obj_id: str) -> Result:
        raise NotImplementedError()

    async def fetch_all(self) -> Result:
        raise NotImplementedError()

    async def update(
        self, obj_id: str, input_data: BaseModel, session: Optional[AsyncIOMotorClientSession] = None, **kwargs: Any
    ) -> Result:
        raise NotImplementedError()

    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result:
        raise NotImplementedError()

    async def create(
        self,
        input_data: ParticipantRequestBody,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Dict[str, Any]
    ) -> Result[Participant, DuplicateEmailError | Exception]:
        try:
            participant = Participant(
                name=input_data.name,
                email=input_data.email,
                is_admin=input_data.is_admin,
                # If the team_id is passed as a kwarg the participant will be inserted in the given team
                team_id=kwargs.get("team_id"),
            )
            LOG.debug("Inserting participant...", participant=participant.dump_as_json())
            await self._collection.insert_one(document=participant.dump_as_mongo_db_document(), session=session)
            return Ok(participant)
        except DuplicateKeyError:
            LOG.warning("Participant insertion failed due to duplicate email", email=input_data.email)
            return Err(DuplicateEmailError(input_data.email))
        except Exception as e:
            LOG.exception("Participant insertion failed due to err {}".format(e))
            return Err(e)

    async def get_verified_random_participants_count(self) -> int:
        """Returns the count of verified participants who are not assigned to any team."""
        # Ignoring mypy type due to Returning Any from function declared to return "int"  [no-any-return] which is not true
        return await self._collection.count_documents({"email_verified": True, "team_id": None})  # type: ignore
