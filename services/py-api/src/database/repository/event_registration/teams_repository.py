from typing import Optional

from datetime import datetime, timezone
from pymongo import ReturnDocument
from result import Result, Ok, Err
from pymongo.asynchronous.client_session import AsyncClientSession

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.event_registration_collections import (
    TEAMS_COLLECTION,
)
from src.database.model.event_registration.team_model import Team


class TeamsRepository:

    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(TEAMS_COLLECTION)

    async def create(
        self,
        team: Team,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Team, Exception]:

        try:
            await self._collection.insert_one(
                document=team.dump_as_mongo_db_document(),
                session=session,
            )

            return Ok(team)

        except Exception as error:
            return Err(error)

    async def find_by_code(
        self,
        code: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            document = await self._collection.find_one(
                filter={"code": code},
                session=session,
            )

            return Ok(document)

        except Exception as error:
            return Err(error)

    async def reserve_slot(
        self,
        code: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            document = await self._collection.find_one_and_update(
                filter={
                    "code": code,
                    "member_count": {"$lt": 5},
                },
                update={
                    "$inc": {"member_count": 1},
                },
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            return Ok(document)

        except Exception as error:
            return Err(error)

    async def mark_completed(
        self,
        code: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Optional[dict], Exception]:

        try:
            document = await self._collection.find_one_and_update(
                filter={
                    "code": code,
                    "member_count": 5,
                    "completed_at": None,
                },
                update={
                    "$set": {
                        "completed_at": datetime.now(timezone.utc),
                    },
                },
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            return Ok(document)

        except Exception as error:
            return Err(error)

    async def mark_completion_email_sent(
        self,
        code: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[bool, Exception]:

        try:
            result = await self._collection.update_one(
                filter={
                    "code": code,
                    "completed_at": {"$ne": None},
                    "completion_email_sent_at": None,
                },
                update={
                    "$set": {
                        "completion_email_sent_at": datetime.now(timezone.utc),
                    },
                },
                session=session,
            )

            return Ok(result.modified_count == 1)

        except Exception as error:
            return Err(error)

    async def find_pending_completion_emails(
        self,
        limit: int = 50,
    ) -> Result[list[dict], Exception]:

        try:
            cursor = self._collection.find(
                filter={
                    "completed_at": {"$ne": None},
                    "completion_email_sent_at": None,
                },
                sort=[("completed_at", 1)],
                limit=limit,
            )

            documents = await cursor.to_list(length=limit)

            return Ok(documents)

        except Exception as error:
            return Err(error)
