from dataclasses import dataclass
from os import environ

from dotenv import load_dotenv
from uvicorn import run

from src.server.logger.logger_factory import configure_app_logger, get_uvicorn_logger
from src.server.utils import SingletonMeta

load_dotenv()


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

    if server_config.ENV in ("PROD", "DEV", "TEST"):
        configure_app_logger(server_config.ENV)

        # If the ENV is PROD or TEST we don't want to have hot reloading
        run(
            app="src.server.app_entrypoint:app",
            host=server_config.ADDRESS,
            port=server_config.PORT,
            reload=server_config.ENV == "DEV",
            log_config=get_uvicorn_logger(server_config.ENV),
            # TODO: Add those to ServerConfig in order for them to be loaded dynamically based on ENV
            ssl_certfile="src/server/certs/localhost.crt",
            ssl_keyfile="src/server/certs/localhost.key",
        )
    else:
        raise ValueError("The ENV environment variable should be PROD, DEV OR TEST")
