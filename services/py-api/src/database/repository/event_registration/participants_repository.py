from typing import Optional

from datetime import datetime, timezone
from pymongo import ReturnDocument

from src.database.model.base_model import SerializableObjectId
from pymongo.asynchronous.client_session import AsyncClientSession
from result import Result, Ok, Err
from src.database.model.base_model import SerializableObjectId
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.event_registration_collections import (
    PARTICIPANTS_COLLECTION,
)
from src.database.model.event_registration.participant_model import Participant


class ParticipantsRepository:

    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(PARTICIPANTS_COLLECTION)

    async def assign_solo_to_team(
        self,
        participant_id: SerializableObjectId,
        team_id: SerializableObjectId,
        assigned_role: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            document = await self._collection.find_one_and_update(
                filter={
                    "_id": participant_id,
                    "team_id": None,
                    "is_team_leader": False,
                },
                update={
                    "$set": {
                        "team_id": team_id,
                        "assigned_role": assigned_role,
                        "updated_at": datetime.now(timezone.utc),
                    },
                },
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            return Ok(document)

        except Exception as error:
            return Err(error)

    async def create(
        self,
        participant: Participant,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Participant, Exception]:

        try:
            await self._collection.insert_one(
                document=participant.dump_as_mongo_db_document(),
                session=session,
            )

            return Ok(participant)

        except Exception as error:
            return Err(error)

    async def find_by_email(
        self,
        email: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            document = await self._collection.find_one(
                filter={"email": email},
                session=session,
            )

            return Ok(document)

        except Exception as error:
            return Err(error)

    async def find_by_id(
        self,
        participant_id: SerializableObjectId,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            document = await self._collection.find_one(
                filter={"_id": participant_id},
                session=session,
            )

            return Ok(document)

        except Exception as error:
            return Err(error)
