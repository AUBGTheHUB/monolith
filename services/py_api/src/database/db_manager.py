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


# DB_NAME = "TheHubDev"


class DatabaseManager(metaclass=SingletonMeta):
    """Creates a Thread-safe singleton Database manager. This manager is created once in the app_factory and used
    across the whole application. It provides a Singleton db client and utils for pinging the database"""

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(host=os.environ["DATABASE_URL"])

    def close_all_connections(self) -> Err[str]:
        """Closes all connections in the pool managed by Mongo"""
        if not self.client:
            return Err("The database client is not initialized!")

        LOG.debug("Closing all database connections")
        self.client.close()

    async def async_ping_db(self) -> Err[str]:
        try:
            LOG.debug("Pinging MongoDB...")
            await self.client.admin.command("ping")
        except ConnectionFailure:
            return Err("Database is unavailable!")
        except (OperationFailure, ConfigurationError):
            return Err("Database authentication failed!")

        LOG.debug("Pong")


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


def create_db_manager() -> DatabaseManager:
    """Returns a Singleton Database Manager"""
    return DatabaseManager()


DB_MANAGER = Annotated[DatabaseManager, Depends(create_db_manager)]
"""Global FastAPI dependency used across routes and handlers"""

# To learn more about FastAPI Dependency injection system, visit:
# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
