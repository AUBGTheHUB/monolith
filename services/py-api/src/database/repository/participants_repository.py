from typing import Optional, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.errors import DuplicateKeyError
from result import Result, Ok, Err
from src.server.schemas.request_schemas.schemas import UpdateParticipantParams
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.database.model.participant_model import Participant
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import DuplicateEmailError, ParticipantNotFoundError

LOG = get_logger()


class ParticipantsRepository(CRUDRepository[Participant]):
    # TODO: Implement the rest of the methods
    def __init__(self, db_manager: DatabaseManager, collection_name: str) -> None:
        self._collection = db_manager.get_collection(collection_name)

    async def fetch_by_id(self, obj_id: str) -> Result[Participant, Exception]:
        # TODO The implementer should catch invalid ObjectID format
        raise NotImplementedError()

    async def fetch_all(self) -> Result[List[Participant], Exception]:
        raise NotImplementedError()

    async def update(
        self,
        obj_id: str,
        participant: UpdateParticipantParams,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Participant, Err]:
        raise NotImplementedError()

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Participant, ParticipantNotFoundError | Exception]:
        """
        Deletes the participant which corresponds to the provided object_id
        """
        try:

            LOG.debug("Deleting participant...", participant_obj_id=obj_id)

            # According to mongodb docs result is of type _DocumentType:
            # https://pymongo.readthedocs.io/en/4.8.0/api/pymongo/collection.html#pymongo.collection.Collection.find_one_and_delete
            # _id is projected because ObjectID is not serializable.
            # We use the Participant data class to represent the deleted participant.
            result = await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            # The result is None when the participant with the specified ObjectId is not found
            if result:
                return Ok(Participant(id=obj_id, **result))

            return Err(ParticipantNotFoundError())

        except Exception as e:
            LOG.exception("Participant deletion failed due to err {}".format(e))
            return Err(e)

    async def create(
        self,
        participant: Participant,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Participant, DuplicateEmailError | Exception]:
        try:
            LOG.debug("Inserting participant...", participant=participant.dump_as_json())
            await self._collection.insert_one(document=participant.dump_as_mongo_db_document(), session=session)
            return Ok(participant)
        except DuplicateKeyError:
            LOG.warning("Participant insertion failed due to duplicate email", email=participant.email)
            return Err(DuplicateEmailError(participant.email))
        except Exception as e:
            LOG.exception("Participant insertion failed due to err {}".format(e))
            return Err(e)

    async def get_verified_random_participants_count(self) -> int:
        """Returns the count of verified participants who are not assigned to any team."""
        # Ignoring mypy type due to mypy err: 'Returning Any from function declared to return "int"  [no-any-return]'
        # which is not true
        return await self._collection.count_documents({"email_verified": True, "team_id": None})  # type: ignore

    async def get_number_registered_teammates(self, team_id: str) -> int:
        """Returns the count of registered participants already in the team."""
        return await self._collection.count_documents({"team_id": ObjectId(team_id)})  # type: ignore
