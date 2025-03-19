from os import environ

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from result import Err
from structlog.stdlib import get_logger

LOG = get_logger()

_DB_NAME = {"TEST": "TheHubTESTS", "PROD": "TheHubPROD", "DEV": "TheHubDEV", "LOCAL": "TheHubDEV"}[environ["ENV"]]

PARTICIPANTS_COLLECTION = "participants"
TEAMS_COLLECTION = "teams"
FEATURE_SWITCH_COLLECTION = "feature-switches"


class MongoDatabaseManager:
    """Provides utils for pinging the database, closing connections, and getting access to a particular collection in
    our Mongo database"""

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

    async def async_ping_db(self) -> Err[ConnectionFailure | OperationFailure | ConfigurationError] | None:
        try:
            LOG.debug("Pinging MongoDB...")
            await self._client.get_database(name=_DB_NAME).command("ping")
            LOG.debug("Pong")

            return None

        except ConnectionFailure as cf:
            LOG.exception("Pinging db failed due to err", error=cf)
            return Err(cf)

        except (OperationFailure, ConfigurationError) as err:
            LOG.exception("Pinging db failed due to err", error=err)
            return Err(err)

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-database
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection
        return self._client.get_database(name=_DB_NAME).get_collection(name=collection_name)


def ping_db() -> Err[ConnectionFailure | OperationFailure | ConfigurationError] | None:
    """This method is used only on application startup. It is different from the async_ping_db defined in the
    DatabaseManager as it uses the synchronous MongoClient. We need this method because if we used the async_ping_db we
    had to await it. The await keyword is used only is async ctx and the start() method should not and cannot be async,
    as we are using it as a poetry script."""
    mongo_client = MongoClient(host=environ["DATABASE_URL"])
    try:
        LOG.debug("Pinging MongoDB...")
        mongo_client.get_database(name=_DB_NAME).command("ping")
        LOG.debug("Pong")

        return None
    except ConnectionFailure as cf:
        LOG.exception("Pinging db failed due to err", error=cf)
        return Err(cf)

    except (OperationFailure, ConfigurationError) as err:
        LOG.exception("Pinging db failed due to err", error=err)
        return Err(err)

    finally:
        mongo_client.close()


def mongo_db_manager_provider(client: AsyncIOMotorClient) -> MongoDatabaseManager:
    """
    Args:
        client: A singleton AsyncIOMotorClient instance

    Returns:
        A MongoDatabaseManager instance
    """
    return MongoDatabaseManager(client=client)
