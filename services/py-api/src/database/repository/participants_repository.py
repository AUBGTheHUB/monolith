from typing import Optional, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from result import Result, Ok, Err
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.database.model.participant_model import Participant, UpdateParticipantParams
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import DuplicateEmailError, ParticipantNotFoundError

LOG = get_logger()


class ParticipantsRepository(CRUDRepository[Participant]):
    # TODO: Implement the rest of the methods
    def __init__(self, db_manager: DatabaseManager, collection_name: str) -> None:
        self._collection = db_manager.get_collection(collection_name)

    async def fetch_by_id(self, obj_id: str) -> Result[Participant, ParticipantNotFoundError | Exception]:
        try:
            LOG.debug("Fetching participant by ObjectID...", participant_id=obj_id)

            # Query the database for the participant with the given object id
            participant = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if participant is None:  # If no participant is found, return an Err
                return Err(ParticipantNotFoundError())

            return Ok(Participant(id=obj_id, **participant))

        except Exception as e:
            LOG.exception("Failed to fetch participant due to error", participant_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self) -> Result[List[Participant], Exception]:
        try:
            LOG.info("Fetching all participants...")

            participants_data = await self._collection.find({}).to_list(length=None)

            participants = []
            for doc in participants_data:
                doc_copy = dict(doc)

                doc_copy["id"] = str(doc_copy.pop("_id"))

                participants.append(Participant(**doc_copy))

            LOG.debug(f"Fetched {len(participants)} participants.")
            return Ok(participants)

        except Exception as e:
            LOG.exception(f"Failed to fetch all participants due to err {e}")
            return Err(e)

    async def update(
        self,
        obj_id: str,
        obj_fields: UpdateParticipantParams,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Participant, ParticipantNotFoundError | Exception]:
        try:
            LOG.info(f"Updating participant...", participant_obj_id=obj_id, updated_fields=obj_fields.model_dump_json())

            # ReturnDocument.AFTER returns the updated document instead of the orignal document which is the
            # default behaviour.
            result = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            # The result is None when the participant with the specified ObjectId is not found
            if result is None:
                return Err(ParticipantNotFoundError())

            return Ok(Participant(id=obj_id, **result))

        except Exception as e:
            LOG.exception("Failed to update participant", participant_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Participant, ParticipantNotFoundError | Exception]:
        """
        Deletes the participant which corresponds to the provided object_id
        """
        try:

            LOG.info("Deleting participant...", participant_id=obj_id)

            # According to mongodb docs result is of type _DocumentType:
            # https://pymongo.readthedocs.io/en/4.8.0/api/pymongo/collection.html#pymongo.collection.Collection.find_one_and_delete
            # _id is projected because ObjectID is not serializable.
            # We use the Participant data class to represent the deleted participant.
            result = await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            # The result is None when the participant with the specified ObjectId is not found
            if result is None:
                return Err(ParticipantNotFoundError())

            return Ok(Participant(id=obj_id, **result))

        except Exception as e:
            LOG.exception("Participant deletion failed due to error", participant_id=obj_id, error=e)
            return Err(e)

    async def create(
        self,
        participant: Participant,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Participant, DuplicateEmailError | Exception]:
        try:
            LOG.info("Inserting participant...", participant=participant.dump_as_json())
            await self._collection.insert_one(document=participant.dump_as_mongo_db_document(), session=session)
            return Ok(participant)
        except DuplicateKeyError:
            LOG.warning("Participant insertion failed due to duplicate email", email=participant.email)
            return Err(DuplicateEmailError(participant.email))
        except Exception as e:
            LOG.exception("Participant insertion failed due to error", participant_id=str(participant.id), error=e)
            return Err(e)

    async def get_verified_random_participants_count(self) -> int:
        """Returns the count of verified participants who are not assigned to any team."""
        # Ignoring mypy type due to mypy err: 'Returning Any from function declared to return "int"  [no-any-return]'
        # which is not true
        return await self._collection.count_documents({"email_verified": True, "team_id": None})  # type: ignore

    async def get_number_registered_teammates(self, team_id: str) -> int:
        """Returns the count of registered participants already in the team."""
        return await self._collection.count_documents({"team_id": ObjectId(team_id)})  # type: ignore
