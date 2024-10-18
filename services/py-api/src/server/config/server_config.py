from dataclasses import dataclass
from os import environ, cpu_count

from dotenv import load_dotenv
from uvicorn import run

from src.database.db_manager import ping_db
from src.server.logger.logger_factory import get_uvicorn_logger, configure_app_logger
from src.utils import SingletonMeta

# This should be called first because the env variables should be loaded into the process before we start using them
# across our codebase
load_dotenv()

# We also configure the logger here. This should be done before calling LOG = get_logger(), which we use in almost
# every file, in order for the logger to function properly. Otherwise, it uses the default logging config.
configure_app_logger(environ["ENV"])


@dataclass
class ServerConfig(metaclass=SingletonMeta):
    ENV = environ["ENV"]
    PORT = int(environ["PORT"])
    ADDRESS = environ["ADDRESS"]


def load_server_config() -> ServerConfig:
    """Returns a Singleton Server Config"""
    return ServerConfig()


def start() -> None:
    """Starts the Uvicorn server with different config based on the env we are in"""
    server_config = load_server_config()

    if server_config.ENV in ("PROD", "DEV", "LOCAL", "TEST"):
        err = ping_db()
        if err:
            raise RuntimeError(err.err_value)

        run(
            app="src.server.app_entrypoint:app",
            host=server_config.ADDRESS,
            port=server_config.PORT,
            reload=server_config.ENV == "LOCAL",
            log_config=get_uvicorn_logger(server_config.ENV),
            # TODO: Add those to ServerConfig in order for them to be loaded dynamically based on ENV. This should be
            # done before deploying to PROD
            ssl_certfile="src/server/certs/localhost.crt",
            ssl_keyfile="src/server/certs/localhost.key",
            # https://docs.gunicorn.org/en/stable/design.html#how-many-workers
            # https://stackoverflow.com/questions/65278110/how-does-gunicorn-distribute-requests-across-sync-workers
            # As cpu_count could return None we use 0 instead, as 2 * None would produce an error
            # Also "workers" flag is ignored when reloading is enabled (It is ignored for LOCAL)
            workers=2 * (cpu_count() or 0) + 1,
        )
    else:
        raise ValueError("The ENV environment variable should be PROD, DEV, LOCAL OR TEST")
