from dataclasses import dataclass
from os import environ, cpu_count

from typing import Tuple
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


def _get_ssl_config(env: str) -> Tuple[str, str]:
    """Returns ssl_certfile, ssl_keyfile based on the ENV"""
    # TODO: these paths will definitely change depending on the web server we choose, disused in
    #  https://github.com/AUBGTheHUB/monolith/issues/737
    #  The paths are set according to the current DEV/PROD VMs

    letsencrypt_path = "/etc/letsencrypt/live"

    if env == "DEV":
        return (
            f"{letsencrypt_path}/dev.thehub-aubg.com/fullchain.pem",
            f"{letsencrypt_path}/dev.thehub-aubg.com/privkey.pem",
        )
    if env == "PROD":
        return f"{letsencrypt_path}/thehub-aubg.com/fullchain.pem", f"{letsencrypt_path}/thehub-aubg.com/privkey.pem"

    return "src/server/certs/localhost.crt", "src/server/certs/localhost.key"


@dataclass
class ServerConfig(metaclass=SingletonMeta):
    ENV = environ["ENV"]
    PORT = int(environ["PORT"])
    ADDRESS = environ["ADDRESS"]
    SSL_CERT, SSL_KEY = _get_ssl_config(ENV)


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
            ssl_certfile=server_config.SSL_CERT,
            ssl_keyfile=server_config.SSL_KEY,
            # https://docs.gunicorn.org/en/stable/design.html#how-many-workers
            # https://stackoverflow.com/questions/65278110/how-does-gunicorn-distribute-requests-across-sync-workers
            # As cpu_count could return None we use 0 instead, as 2 * None would produce an error
            # Also "workers" flag is ignored when reloading is enabled (It is ignored for LOCAL)
            workers=2 * (cpu_count() or 0) + 1,
        )
    else:
        raise ValueError("The ENV environment variable should be PROD, DEV, LOCAL OR TEST")
