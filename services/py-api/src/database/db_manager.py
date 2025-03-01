from math import ceil
from os import environ
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from result import Err
from structlog.stdlib import get_logger

from src.environment import ENV
from src.utils import SingletonMeta

LOG = get_logger()


class DatabaseManager(metaclass=SingletonMeta):
    """Creates a Thread-safe singleton Database manager. It provides a wrapper over the AsyncIOMotorClient and utils for
    pinging the database. The singleton behaviour allows us to have one instance of the AsyncIOMotorClient which we
    could safely use across our application through the interface of the DatabaseManager"""

    _DB_NAME = {"TEST": "TheHubTESTS", "PROD": "TheHubPROD", "DEV": "TheHubDEV", "LOCAL": "TheHubDEV"}[ENV]

    def __init__(self) -> None:
        # The mongo client has a conn pool under the hood. We set a min number of idle connections that the pool has
        # to maintain, the default is 0. This is in order to have some connections ready to be used instead of waiting
        # for a socket conn to be opened.
        # After maxIdleTimeMS the connection pool replaces the idle conn with a new one. By default, the value is 0
        # which means a connection can remain idle indefinitely, but this can cause the connection to become stale.
        # The config values are set according to the articles below.
        # https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
        # https://alexedwards.net/blog/configuring-sqldb
        # https://medium.com/@dhanushkasampath.mtr/what-are-the-default-values-for-hikari-connection-pool-if-we-do-not-override-in-application-properti-11932cdbe321
        # https://www.mongodb.com/docs/languages/python/pymongo-driver/current/faq/#how-does-connection-pooling-work-in-pymongo-
        self._client = AsyncIOMotorClient(
            host=environ["DATABASE_URL"], minPoolSize=ceil(0.1 * 25), maxConnecting=25, maxIdleTimeMS=5 * 60 * 1000
        )

    def close_all_connections(self) -> Err[str]:
        """Closes all connections in the pool managed by Mongo"""
        if self._client is None:
            LOG.error("The database client is not initialized!")
            return Err("The database client is not initialized!")

        LOG.debug("Closing all database connections")
        self._client.close()

    async def async_ping_db(self) -> Err[str]:
        try:
            LOG.debug("Pinging MongoDB...")
            await self._client.admin.command("ping")
            LOG.debug("Pong")
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


def ping_db() -> Err[str]:
    """This method is used only on application startup. It is different from the async_ping_db defined in the
    DatabaseManager as it uses the synchronous MongoClient. We need this method because if we used the async_ping_db we
    had to await it. The await keyword is used only is async ctx and the start() method should not and cannot be async,
    as we are using it as a poetry script."""
    mongo_client = MongoClient(host=environ["DATABASE_URL"])

    try:
        LOG.debug("Pinging MongoDB...")
        mongo_client.admin.command("ping")
        LOG.debug("Pong")
    except ConnectionFailure as cf:
        LOG.exception("Pinging db failed due to err {}".format(cf))
        return Err("Database is unavailable!")
    except (OperationFailure, ConfigurationError) as err:
        LOG.exception("Pinging db failed due to err {}".format(err))
        return Err("Database authentication failed!")
    finally:
        mongo_client.close()


def get_db_manager() -> DatabaseManager:
    """Returns a Singleton Database Manager
    This method could be used as the global access point to the Database Manager across the application.
    The method is also needed because Annotated[DatabaseManager, Depends(DatabaseManager)] does not work as expected due
    to the SingletonMeta class used in the DatabaseManager.
    For more info: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
    """
    return DatabaseManager()


# Global FastAPI dependencies used across routes and handlers.
DB_MANAGER = Annotated[DatabaseManager, Depends(get_db_manager)]
PARTICIPANTS_COLLECTION = "participants"
TEAMS_COLLECTION = "teams"
FEATURE_SWITCH_COLLECTION = "feature-switches"

# To learn more about FastAPI Dependency injection system, visit:
# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
