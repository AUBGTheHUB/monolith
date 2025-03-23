"""Here we store clients for different databases. It's recommended that these clients are Singletons."""

from math import ceil
from os import environ

from motor.motor_asyncio import AsyncIOMotorClient

from src.utils import singleton


## Note:
# Usually it is a good idea to write a common interface which all Db clients should adhere to, so that you could swap
# them easily for one another (Dependency Inversion). For ease of use and faster development we don't do that at the
# moment.


@singleton
def mongo_db_client_provider() -> AsyncIOMotorClient:
    """
    This method could be used as the global access point for the async MongoDB client.

    Returns:
         A preconfigured Singleton thread-safe AsyncIOMotorClient instance.
    """

    # The mongo client is thread-safe and has a conn pool under the hood. We set a min number of idle connections that
    # the pool has to maintain, the default is 0. This is in order to have some connections ready to be used instead of
    # waiting for a socket connection to be opened.
    # After maxIdleTimeMS the connection pool replaces the idle conn with a new one. By default, the value is 0
    # which means a connection can remain idle indefinitely, but this can cause the connection to become stale.
    # The config values are set according to the articles below.
    # https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
    # https://alexedwards.net/blog/configuring-sqldb
    # https://medium.com/@dhanushkasampath.mtr/what-are-the-default-values-for-hikari-connection-pool-if-we-do-not-override-in-application-properti-11932cdbe321
    # https://www.mongodb.com/docs/languages/python/pymongo-driver/current/faq/#how-does-connection-pooling-work-in-pymongo-
    return AsyncIOMotorClient(
        host=environ["DATABASE_URL"], minPoolSize=ceil(0.1 * 25), maxConnecting=25, maxIdleTimeMS=5 * 60 * 1000
    )
