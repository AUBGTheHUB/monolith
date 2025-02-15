from os import environ
from dotenv import load_dotenv

# Something to keep in mind is that in deployed env, we don't use .env files, but for local development we use them.
load_dotenv(override=True)


def _read_docker_secret(secret_path: str) -> str | None:
    """
    Reads the decrypted secret value from a Docker-managed secret file.

    Docker mounts secrets as files in an in-memory filesystem, typically under /run/secrets/.
    This function reads the content of the specified file if it exists.

    Args:
        secret_path (str): The full path to the Docker secret file.

    Returns:
        str: The decrypted secret value if the file exists and can be read.
        None: If the file does not exist (e.g., when running outside a Docker Swarm environment).

    Notes:
        - This function handles the FileNotFoundError silently, as secrets may not be available
          in non-Docker environments (e.g., local development).
        - For more information, refer to:
          https://docs.docker.com/engine/swarm/secrets/#how-docker-manages-secrets
    """
    try:
        with open(secret_path, "r") as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        return None


def _load_docker_secrets() -> None:
    # Secrets here are from the docker-stack.yml and are set on the PROD and DEV VMs (aka Nodes)
    secrets = {
        "ENV": "/run/secrets/env",
        "DATABASE_URL": "/run/secrets/db-url",
        "SECRET_KEY": "/run/secrets/secret-key",
        "SECRET_AUTH_TOKEN": "/run/secrets/secret-auth-key",
        "RESEND_API_KEY": "/run/secrets/resend-api-key",
    }

    # We set the env var value only if we are in a deployed env, and the env var has been set on the given Node
    for key, path in secrets.items():
        if value := _read_docker_secret(path):
            environ[key] = value


def load_env() -> None:
    """This should be called first (top of the file) in the entrypoint of the app because the env variables should be
    loaded into the process before we start using them across our codebase."""
    _load_docker_secrets()

    if environ["ENV"] not in ("PROD", "DEV", "LOCAL", "TEST"):
        raise ValueError(
            f"The ENV environment variable should be PROD, DEV, LOCAL OR TEST. Actual value: {environ["ENV"]}"
        )


def is_prod_env() -> bool:
    return environ["ENV"] == "PROD"


def is_dev_env() -> bool:
    return environ["ENV"] == "DEV"


def is_test_env() -> bool:
    return environ["ENV"] == "TEST"


def is_local_env() -> bool:
    return environ["ENV"] == "LOCAL"


DOMAIN = environ["DOMAIN"]
PORT = int(environ["PORT"])
SUBDOMAIN = "dev"
