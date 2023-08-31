from os import getenv
from typing import Dict

from dotenv import load_dotenv
from py_api.utilities.parsers import eval_bool

load_dotenv()

MONGO_URI = getenv("MONGOURI", "")

IS_OFFLINE = eval_bool(getenv("IS_OFFLINE", False))
IS_PROD = eval_bool(getenv("IS_PROD", False))
IS_LOCAL_COMPOSE = eval_bool(getenv("IS_LOCAL_COMPOSE", False))

OFFLINE_TOKEN = "OFFLINE_TOKEN"

SSL_FILES: Dict[str, str] = {
    "ssl_keyfile": "certs/devenv.key",
    "ssl_certfile": "certs/devenv.crt",
}
