from dataclasses import dataclass
from os import environ

from dotenv import load_dotenv
from uvicorn import run

from src.utils import SingletonMeta

load_dotenv()


@dataclass
class ServerConfig(metaclass=SingletonMeta):
    ENV = environ["ENV"]
    PORT = int(environ["PORT"])
    ADDRESS = environ["ADDRESS"]


def load_server_config() -> ServerConfig:
    """Returns a Singleton Server Config"""
    return ServerConfig()


def start(server_config: ServerConfig) -> None:
    """Starts the Uvicorn server with different config based on the env we are in"""

    # TODO: ADD ssl and logging levels/config
    if server_config.ENV == "PROD":
        run(
            app="src.server.main:app",
            host=server_config.ADDRESS,
            port=server_config.PORT,
            reload=False,
            root_path="/api/v3",
        )
    elif server_config.ENV == "DEV":
        run(
            app="src.server.main:app",
            host=server_config.ADDRESS,
            port=server_config.PORT,
            reload=True,
            root_path="/api/v3",
        )
    # TODO: ADD ENV = TEST case
    else:
        raise ValueError("The ENV environment variable should be PROD, DEV OR TEST")
