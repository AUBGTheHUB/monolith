from os import getenv
from typing import Dict

from dotenv import load_dotenv
from py_api.utilities.parsers import eval_bool

load_dotenv()

MONGO_URI = getenv("MONGOURI", "")

IS_OFFLINE = eval_bool(getenv("IS_OFFLINE", False))
ENABLE_ANALYTICS = eval_bool(getenv("ENABLE_ANALYTICS", False))
IS_LOCAL_COMPOSE = eval_bool(getenv("IS_LOCAL_COMPOSE", False))
SECRET_KEY = getenv("SECRET_KEY")
HUB_MAIL = getenv("HUB_MAIL")
HUB_PSW = getenv("HUB_PSW")
HUB_WEB_URL = getenv("HUB_WEB_URL", "")
DOCK_ENV = getenv("DOCK_ENV", "")

OFFLINE_TOKEN = "OFFLINE_TOKEN"

SSL_FILES: Dict[str, str] = {
    "ssl_keyfile": "certs/devenv.key",
    "ssl_certfile": "certs/devenv.crt",
} if not IS_OFFLINE else {}
