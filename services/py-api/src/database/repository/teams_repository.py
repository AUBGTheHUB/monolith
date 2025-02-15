from copy import deepcopy
from typing import Optional, List, Annotated, cast

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.db_managers import MongoDatabaseManager, TEAMS_COLLECTION_NAME, MongoDatabaseManagerDep
from src.database.model.team_model import Team, UpdateTeamParams
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import DuplicateTeamNameError, TeamNotFoundError

LOG = get_logger()


class TeamsRepository(CRUDRepository[Team]):

    def __init__(self, db_manager: MongoDatabaseManager, collection_name: str) -> None:
        self._collection = db_manager.get_collection(collection_name)

    async def create(
        self,
        team: Team,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Team, DuplicateTeamNameError | Exception]:

        try:
            LOG.info("Inserting team...", team=team.dump_as_json())
            await self._collection.insert_one(document=team.dump_as_mongo_db_document(), session=session)
            return Ok(team)

        except DuplicateKeyError:
            LOG.warning("Team insertion failed due to duplicate team name", team_name=team.name)
            return Err(DuplicateTeamNameError(team.name))

        except Exception as e:
            LOG.exception("Team insertion failed due to error", team_id=str(team.id), error=e)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[Team, TeamNotFoundError | Exception]:
        """
        Fetches a team by ObjectId
        """
        try:
            LOG.debug("Fetching team by ObjectId...", team_id=obj_id)

            # Query the database for the team with the given ObjectId
            team = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if team is None:  # If no team is found, return an Err
                return Err(TeamNotFoundError())

            return Ok(Team(id=obj_id, **team))

        except Exception as e:
            LOG.exception("Failed to fetch team due to error", team_id=obj_id, error=e)
            return Err(e)

    # TODO: FIX .find is NOT async, Read the docs!!!!!
    async def fetch_all(self) -> Result[List[Team], Exception]:
        raise NotImplementedError()
        # try:
        #     LOG.debug("Fetching all teams...")
        #
        #     teams_data = await self._collection.find({})
        #
        #     teams = []
        #     for doc in teams_data:
        #         doc_copy = dict(doc)
        #
        #         doc_copy["id"] = str(doc_copy.pop("_id"))
        #
        #         teams.append(Team(**doc_copy))
        #
        #     LOG.debug(f"Fetched {len(teams)} teams.")
        #     return Ok(teams)
        #
        # except Exception as e:
        #     LOG.exception(f"Failed to fetch all teams due to err {e}")
        #     return Err(e)

    async def update(
        self,
        obj_id: str,
        obj_fields: UpdateTeamParams,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[Team, TeamNotFoundError | Exception]:
        try:

            LOG.info(f"Updating team...", team_id=obj_id, updated_fields=obj_fields.model_dump_json())

            result = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                return_document=ReturnDocument.AFTER,
                projection={"_id": 0},
                session=session,
            )

            # The result is None when the team with the specified ObjectId is not found
            if result is None:
                return Err(TeamNotFoundError())

            return Ok(Team(id=obj_id, **result))

        except Exception as e:
            LOG.exception(f"Failed to update team due to error", team_id=obj_id, error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Team, TeamNotFoundError | Exception]:
        """
        Deletes the team which corresponds to the provided object_id
        """
        try:

            LOG.info("Deleting team...", team_id=obj_id)
            """
            According to mongodb docs result is of type _DocumentType:
            https://pymongo.readthedocs.io/en/4.8.0/api/pymongo/collection.html#pymongo.collection.Collection.find_one_and_delete
            _id is projected because ObjectID is not serializable.
            We use the Team data class to represent the deleted participant.
            """
            result = await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            """
            The result is None when the team with the specified ObjectId is not found
            """
            if result is None:
                return Err(TeamNotFoundError())

            return Ok(Team(id=obj_id, **result))

        except Exception as e:
            LOG.exception("Team deletion failed due to error", team_id=obj_id, error=e)
            return Err(e)

    async def get_verified_registered_teams_count(self) -> int:
        """Returns the count of verified teams."""
        # Ignoring mypy type due to mypy err: 'Returning Any from function declared to return "int"  [no-any-return]'
        # which is not true
        return await self._collection.count_documents({"is_verified": True})  # type: ignore

    async def fetch_by_team_name(self, team_name: str) -> Result[Team, TeamNotFoundError | Exception]:
        """
        Fetches a team by the team_name from the participant
        """
        try:
            LOG.debug("Fetching team by name...", team_name=team_name)

            # Query the database for the team with the given name
            team = await self._collection.find_one({"name": team_name})

            # If no team is found, return an Err
            if team is None:
                return Err(TeamNotFoundError())

            # Since the `Team` class has a parameter named `id` instead of `_id`,
            # we make the following operations in order to rename the key appropriately

            # Make a deep copy of the team dictionary
            team_copy = cast(deepcopy(team), dict)

            # Rename `_id` to `id`
            team_copy["id"] = str(team_copy.pop("_id"))

            return Ok(Team(**team_copy))

        except Exception as e:
            LOG.exception(f"Failed to fetch team due to err", team_name=team_name, error=e)
            return Err(e)


def teams_repo_provider(db_manager: MongoDatabaseManagerDep) -> TeamsRepository:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "provider" of an
    instance. ``fastapi.Depends`` will automatically inject the TeamsRepository instance into its intended consumers
    by calling this provider.

    Args:
        db_manager: An automatically injected MongoDatabaseManager instance by FastAPI using ``fastapi.Depends``

    Returns:
        A TeamsRepository instance
    """
    return TeamsRepository(db_manager, TEAMS_COLLECTION_NAME)


# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
TeamsRepoDep = Annotated[TeamsRepository, Depends(teams_repo_provider)]
"""FastAPI dependency for automatically injecting a TeamsRepository instance into consumers"""
