from dataclasses import dataclass
from os import cpu_count

from structlog.stdlib import get_logger
from uvicorn import run

from src.environment import DOMAIN, PORT, ADDRESS, ENV
from src.logger.logger_factory import get_uvicorn_logger
from src.utils import singleton

LOG = get_logger()


def _get_ssl_config() -> tuple[None, None] | tuple[str, str]:
    """Returns ssl_certfile, ssl_keyfile based on the ENV"""

    # In deployed environments we are behind Caddy, which takes care of TLS Termination. This is because the traffic
    # between Caddy and the py-api happens over the internal Docker overlay network, created by Docker Swarm, which is
    # already isolated. Adding TLS here would create unnecessary complexity, and overhead.
    # See:
    # https://docs.docker.com/engine/swarm/networking/
    # https://docs.docker.com/engine/network/drivers/overlay/
    # https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#examples
    if DOMAIN != "localhost":
        return None, None

    return "src/server/certs/localhost.crt", "src/server/certs/localhost.key"


@dataclass
class _ServerConfig:
    ENV = ENV
    ADDRESS = ADDRESS
    SSL_CERT, SSL_KEY = _get_ssl_config()


@singleton
def _load_server_config() -> "_ServerConfig":
    """Returns a Singleton Server Config"""
    return _ServerConfig()


def start_server() -> None:
    """Starts the Uvicorn server with different config based on the environment we are in"""
    server_config = _load_server_config()

    if server_config.ENV == "LOCAL":
        LOG.debug("To open swagger/docs of the API visit: https://localhost:8080/api/v3/docs")

    run(
        app="src.app_entrypoint:app",
        host=server_config.ADDRESS,
        port=PORT,
        reload=server_config.ENV == "LOCAL",
        log_config=get_uvicorn_logger(server_config.ENV),
        ssl_certfile=server_config.SSL_CERT,
        ssl_keyfile=server_config.SSL_KEY,
        # https://docs.gunicorn.org/en/stable/design.html#how-many-workers
        # https://stackoverflow.com/questions/65278110/how-does-gunicorn-distribute-requests-across-sync-workers
        # As cpu_count could return None we use 0 instead, as 2 * None would produce an error
        # Also "workers" flag is ignored when reloading is enabled (It is ignored for LOCAL env)
        workers=2 * (cpu_count() or 0) + 1,
    )
