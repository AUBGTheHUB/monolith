import os

from pymongo import MongoClient
from structlog import get_logger

LOG = get_logger()

DB_NAME = "TheHubDev"


def ping_db() -> None:
    """
    Raises:
        pymongo ConnectionFailure: if we cannot connect to the database
        pymongo OperationFailure: If database Authentication fails
    """
    mongo_client = MongoClient(host=os.environ["DATABASE_URL"])
    LOG.debug("Pinging MongoDB...")
    mongo_client.DB_NAME.command("ping")
    LOG.debug("Pong")
    mongo_client.close()
