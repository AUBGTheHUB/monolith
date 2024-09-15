import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from result import Err
from structlog import get_logger

LOG = get_logger()

DB_NAME = "TheHubDev"


def ping_db() -> Err[str]:
    mongo_client = MongoClient(host=os.environ["DATABASE_URL"])

    try:
        LOG.debug("Pinging MongoDB...")
        mongo_client.DB_NAME.command("ping")
    except ConnectionFailure:
        return Err("Database is unavailable!")
    except OperationFailure:
        return Err("Database authentication failed!")

    LOG.debug("Pong")
    mongo_client.close()
