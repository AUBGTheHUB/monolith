from typing import Optional
from bson import ObjectId
from pymongo import ReturnDocument
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from pymongo.errors import DuplicateKeyError
from pymongo.asynchronous.client_session import AsyncClientSession

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.tournament_collections import TOURNAMENT_TEAMS_COLLECTION
from src.database.model.tournament_registration.tournament_team_model import TournamentTeam, UpdateTournamentTeamParams
from src.exception import TournamentTeamNotFoundError, DuplicateTournamentTeamNameError

LOG = get_logger()


class TournamentTeamsRepository:

    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(TOURNAMENT_TEAMS_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[TournamentTeam, TournamentTeamNotFoundError | Exception]:
        try:
            LOG.debug("Fetching tournament team by ObjectID...", obj_id=obj_id)
            tournament_team = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )

            if tournament_team is None:
                LOG.warning("Did not find tournament team with ObjectID", obj_id=obj_id)
                return Err(TournamentTeamNotFoundError())

            return Ok(tournament_team)

        except Exception as error:
            LOG.exception("Failed to fetch tournament team with ObjectID", obj_id=obj_id, error=error)
            return Err(error)

    async def fetch_all(self) -> Result[list[TournamentTeam], Exception]:
        try:
            LOG.info("Fetching all tournament teams...")

            tournament_teams_data = await self._collection.find({}).to_list(length=None)

            tournament_teams = []
            for doc in tournament_teams_data:
                doc["id"] = doc.pop("_id")

                tournament_teams.append(TournamentTeam(**doc))

            LOG.debug(f"Fetched {len(tournament_teams)} tournament teams.")
            return Ok(tournament_teams)

        except Exception as e:
            LOG.exception(f"Failed to fetch all participants due to err {e}")
            return Err(e)

    async def create(
        self,
        tournament_team: TournamentTeam,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentTeam, Exception]:

        try:
            LOG.info("Inserting tournament team...", tournament_team=tournament_team.dump_as_json())
            await self._collection.insert_one(document=tournament_team.dump_as_mongo_db_document(), session=session)
            return Ok(tournament_team)

        except DuplicateKeyError:
            LOG.warning("Tournament team insertion failed due to duplicate name", name=tournament_team.name)
            return Err(DuplicateTournamentTeamNameError(tournament_team.name))

        except Exception as e:
            LOG.exception("Tournament team insertion failed due to error", team_id=str(tournament_team.id), error=e)
            return Err(e)

    async def update(
        self,
        obj_id: str,
        obj_fields: UpdateTournamentTeamParams,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentTeam, TournamentTeamNotFoundError | Exception]:
        try:
            LOG.info(f"Updating tournament team...", tournament_team_id=obj_id, updated_fields=obj_fields.model_dump())

            tournament_team = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump(exclude_none=True)},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if tournament_team is None:
                LOG.warning("Did not find tournament team with ObjectID", obj_id=obj_id)
                return Err(TournamentTeamNotFoundError())

            return Ok(tournament_team)
        except Exception as exc:
            LOG.exception("Failed to update tournament team to error", tournament_team_id=obj_id, error=exc)
            return Err(exc)

    async def delete(
        self,
        obj_id: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentTeam, TournamentTeamNotFoundError | Exception]:
        try:
            LOG.info("Deleting tournament team...", tournament_team_id=obj_id)

            document = await self._collection.find_one_and_delete(
                filter={"_id": ObjectId(obj_id)},
                projection={"_id": 0},
                session=session,
            )

            if document is None:
                LOG.warning("Did not find tournament team with ObjectID", obj_id=obj_id)
                return Err(TournamentTeamNotFoundError())

            return Ok(TournamentTeam(id=ObjectId(obj_id), **document))
        except Exception as exc:
            LOG.exception("tournament team deletion failed due to error", tournament_team_id=obj_id, error=exc)
            return Err(exc)

    async def find_by_code(
        self,
        code: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[TournamentTeam, Exception]:

        try:
            LOG.debug("Tryng to find a tournament team by team code...", team_code=code)

            tournament_team = await self._collection.find_one(
                filter={"code": code},
                session=session,
            )

            if tournament_team is None:
                LOG.warning("Did not find tournament team with code", team_code=code)
                return Err(TournamentTeamNotFoundError())

            tournament_team["id"] = tournament_team.pop("_id")

            return Ok(TournamentTeam(**tournament_team))

        except Exception as error:
            LOG.exception("Failed to fetch tournament team by code", team_code=code, error=error)
            return Err(error)
