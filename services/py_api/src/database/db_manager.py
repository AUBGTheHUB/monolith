import os
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from result import Err
from structlog import get_logger

from src.utils import SingletonMeta

LOG = get_logger()


class DatabaseManager(metaclass=SingletonMeta):
    """Creates a Thread-safe singleton Database manager. It provides a wrapper over the AsyncIOMotorClient and utils for
    pinging the database. The singleton behaviour allows us to have one instance of the AsyncIOMotorClient which we
    could safely use across our application through the interface of the DatabaseManager"""

    DB_NAME = "TheHubDEV"

    def __init__(self) -> None:
        self._client = AsyncIOMotorClient(host=os.environ["DATABASE_URL"])

    def close_all_connections(self) -> Err[str]:
        """Closes all connections in the pool managed by Mongo"""
        if not self._client:
            return Err("The database client is not initialized!")

        LOG.debug("Closing all database connections")
        self._client.close()

    async def async_ping_db(self) -> Err[str]:
        try:
            LOG.debug("Pinging MongoDB...")
            await self._client.admin.command("ping")
        except ConnectionFailure:
            return Err("Database is unavailable!")
        except (OperationFailure, ConfigurationError):
            return Err("Database authentication failed!")

        LOG.debug("Pong")

    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client


def ping_db() -> Err[str]:
    """This method is used on application startup. It is not async as I cannot await the start() method"""
    mongo_client = MongoClient(host=os.environ["DATABASE_URL"])

    try:
        LOG.debug("Pinging MongoDB...")
        mongo_client.admin.command("ping")
    except ConnectionFailure:
        return Err("Database is unavailable!")
    except (OperationFailure, ConfigurationError):
        return Err("Database authentication failed!")

    LOG.debug("Pong")
    mongo_client.close()


def get_db_manager() -> DatabaseManager:
    """Returns a Singleton Database Manager
    This method could be used as the global access point to the Database Manager across the application.
    The method is also needed because Annotated[DatabaseManager, Depends(DatabaseManager)] does not work as expected due
    to the SingletonMeta class used in the DatabaseManager.
    For more info: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
    """
    return DatabaseManager()


DB_MANAGER = Annotated[DatabaseManager, Depends(get_db_manager)]
"""Global FastAPI dependency used across routes and handlers."""

# To learn more about FastAPI Dependency injection system, visit:
# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
