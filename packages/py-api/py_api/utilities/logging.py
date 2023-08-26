from os import getenv
from typing import Any, Dict

from py_api.environment import IS_OFFLINE
from py_api.utilities.parsers import eval_bool
from uvicorn.config import LOGGING_CONFIG

PROD_LOGGING_CONFIG: Dict[str, Any] = {
    'version': 1,
    'formatters': {
        'logformatter': {
            'format': '[%(asctime)s][%(levelname)s][%(name)s]: %(message)s',
            'datefmt': '%H:%M',
        },
    },
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'filename': 'py_api/shared/logfile.log',
            'formatter': 'logformatter',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB limit
            'backupCount': 2,  # 2 backup files
        },
    },
    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['logfile'],
        },
        "uvicorn.error": {"level": "ERROR"},
    },
}


def get_log_config() -> Dict[str, Any]:
    log_config: Dict[str, Any] = PROD_LOGGING_CONFIG if not eval_bool(
        IS_OFFLINE,
    ) else LOGGING_CONFIG

    return log_config
