from os import getenv

from dotenv import load_dotenv
from py_api.utilities.parsers import eval_bool

load_dotenv()

MONGO_URI = getenv("MONGOURI", "")

IS_OFFLINE = eval_bool(getenv("IS_OFFLINE", False))

OFFLINE_TOKEN = "OFFLINE_TOKEN"
