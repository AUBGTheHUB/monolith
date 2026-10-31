from typing import Optional
from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from src.database.model.base_model import SerializableObjectId
from src.exception import DuplicateTournamentParticipantError, TournamentParticipantNotFoundError
from structlog.stdlib import get_logger
from result import Result, Ok, Err
from pymongo.asynchronous.client_session import AsyncClientSession

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.tournament_collections import TOURNAMENT_PARTICIPANTS_COLLECTION
from src.database.model.tournament_registration.tournament_participant_model import (
    TournamentParticipant,
    UpdateTournamentParticipantParams,
)
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class TournamentParticipantsRepository(CRUDRepository[TournamentParticipant]):

    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(TOURNAMENT_PARTICIPANTS_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[TournamentParticipant, TournamentParticipantNotFoundError | Exception]:
        try:
            LOG.debug("Fetching tournament participant by ObjectID...", obj_id=obj_id)
            tournament_participant = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}
            )

            if tournament_participant is None:
                LOG.warning("Did not find tournament participant with ObjectID", obj_id=obj_id)
                return Err(TournamentParticipantNotFoundError())

            return Ok(tournament_participant)

        except Exception as error:
            LOG.exception("Failed to fetch tournament participant by ObjectID", obj_id=obj_id, error=error)
            return Err(error)

    async def fetch_all(self) -> Result[list[TournamentParticipant], Exception]:
        try:
            LOG.info("Fetching all tournament participants...")

            tournament_participants_data = await self._collection.find({}).to_list(length=None)

            tournament_participants = []
            for doc in tournament_participants_data:
                doc["id"] = doc.pop("_id")

                tournament_participants.append(TournamentParticipant(**doc))

            LOG.debug(f"Fetched {len(tournament_participants)} tournament participants.")
            return Ok(tournament_participants)

        except Exception as e:
            LOG.exception(f"Failed to fetch all tournament participants due to err {e}")
            return Err(e)

    async def create(
        self,
        tournament_participant: TournamentParticipant,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentParticipant, Exception]:

        try:
            LOG.info(
                "Inserting tournament participant...", tournament_participant=tournament_participant.dump_as_json()
            )
            await self._collection.insert_one(
                document=tournament_participant.dump_as_mongo_db_document(), session=session
            )
            return Ok(tournament_participant)

        except DuplicateKeyError:
            LOG.warning(
                "Tournament participant insertion failed due to duplicate email", email=tournament_participant.email
            )
            return Err(DuplicateTournamentParticipantError(tournament_participant.email))

        except Exception as e:
            LOG.exception(
                "Tournament Participant insertion failed due to error",
                participant_id=str(tournament_participant.id),
                error=e,
            )
            return Err(e)

    async def update(
        self,
        obj_id: str,
        obj_fields: UpdateTournamentParticipantParams,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentParticipant, TournamentParticipantNotFoundError | Exception]:
        try:
            LOG.info(
                f"Updating tournament participant...",
                tournament_participant_id=obj_id,
                updated_fields=obj_fields.model_dump(),
            )

            tournament_participant = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump(exclude_none=True)},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if tournament_participant is None:
                LOG.warning("Did not find tournament participant with ObjectID", obj_id=obj_id)
                return Err(TournamentParticipantNotFoundError())

            return Ok(tournament_participant)
        except Exception as exc:
            LOG.exception(
                "Failed to update tournament participant to error", tournament_participant_id=obj_id, error=exc
            )
            return Err(exc)

    async def delete(
        self,
        obj_id: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentParticipant, Exception]:
        try:
            LOG.info("Deleting tournament participant...", tournament_participant_id=obj_id)

            document = await self._collection.find_one_and_delete(
                filter={"_id": ObjectId(obj_id)},
                projection={"_id": 0},
                session=session,
            )

            if document is None:
                LOG.warning("Did not find tournament participant with ObjectID", obj_id=obj_id)
                return Err(TournamentParticipantNotFoundError())

            return Ok(TournamentParticipant(id=ObjectId(obj_id), **document))
        except Exception as exc:
            LOG.exception(
                "Tournament participant deletion failed due to error", tournament_participant_id=obj_id, error=exc
            )
            return Err(exc)

    async def find_by_email(
        self,
        email: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            LOG.debug("Trying to find tournament participant by email", email=email)
            tournament_participant = await self._collection.find_one(
                filter={"email": email},
                projection={"_id": 0},
                session=session,
            )

            return Ok(tournament_participant)

        except Exception as error:
            LOG.exception("Failed to fetch tournament participant by email", email=email, error=error)
            return Err(error)

    async def check_team_members_count_by_team_id(
        self,
        team_id: SerializableObjectId,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[int, Exception]:
        try:
            LOG.debug("Finding team participants count by team id...", team_id=team_id)

            count = await self._collection.count_documents(
                filter={"team_id": team_id},
                session=session,
            )

            return Ok(count)

        except Exception as error:
            LOG.exception("Failed to count team participants", team_id=team_id, error=error)
            return Err(error)
