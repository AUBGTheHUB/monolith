from os import environ
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from result import Err
from structlog.stdlib import get_logger

from src.database.db_clients import MotorClientDep

LOG = get_logger()

PARTICIPANTS_COLLECTION_NAME = "participants"
TEAMS_COLLECTION_NAME = "teams"


class MongoDatabaseManager:
    """Provides utils for pinging the database, closing connections, and getting access to a particular collection in
    our Mongo database"""

    _DB_NAME = {"TEST": "TheHubTESTS", "PROD": "TheHubPROD", "DEV": "TheHubDEV", "LOCAL": "TheHubDEV"}[environ["ENV"]]

    def __init__(self, client: AsyncIOMotorClient) -> None:
        self._client = client

    def close_all_connections(self) -> Err[str] | None:
        """Closes all connections in the pool managed by Mongo"""
        if self._client is None:
            LOG.error("The database client is not initialized!")
            return Err("The database client is not initialized!")

        LOG.debug("Closing all database connections")
        self._client.close()

        return None

    async def async_ping_db(self) -> Err[str] | None:
        try:
            LOG.debug("Pinging MongoDB...")
            await self._client.admin.command("ping")
            LOG.debug("Pong")

            return None
        except ConnectionFailure as cf:
            LOG.exception("Pinging db failed due to err {}".format(cf))
            return Err("Database is unavailable!")
        except (OperationFailure, ConfigurationError) as err:
            LOG.exception("Pinging db failed due to err {}".format(err))
            return Err("Database authentication failed!")

    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-database
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection
        return self._client[self._DB_NAME][collection_name]


def ping_db() -> Err[str] | None:
    """This method is used only on application startup. It is different from the async_ping_db defined in the
    DatabaseManager as it uses the synchronous MongoClient. We need this method because if we used the async_ping_db we
    had to await it. The await keyword is used only is async ctx and the start() method should not and cannot be async,
    as we are using it as a poetry script."""
    mongo_client = MongoClient(host=environ["DATABASE_URL"])

    try:
        LOG.debug("Pinging MongoDB...")
        mongo_client.admin.command("ping")
        LOG.debug("Pong")

        return None
    except ConnectionFailure as cf:
        LOG.exception("Pinging db failed due to err {}".format(cf))
        return Err("Database is unavailable!")
    except (OperationFailure, ConfigurationError) as err:
        LOG.exception("Pinging db failed due to err {}".format(err))
        return Err("Database authentication failed!")
    finally:
        mongo_client.close()


def mongo_db_manager_provider(client: MotorClientDep) -> MongoDatabaseManager:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "provider" of an
    instance. ``fastapi.Depends`` will automatically inject the MongoDatabaseManager instance into its intended
    consumers by calling this provider.

    Args:
        client: An automatically injected singleton AsyncIOMotorClient instance by FastAPI using ``fastapi.Depends``

    Returns:
        A MongoDatabaseManager instance
    """
    return MongoDatabaseManager(client=client)


# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
MongoDatabaseManagerDep = Annotated[MongoDatabaseManager, Depends(mongo_db_manager_provider)]
"""FastAPI dependency for automatically injecting a MongoDatabaseManagerDep instance into consumers"""
