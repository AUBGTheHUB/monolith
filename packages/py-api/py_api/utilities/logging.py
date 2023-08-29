import logging
from copy import copy
from logging import Formatter
from typing import Any, Dict

from py_api.environment import IS_OFFLINE
from py_api.utilities.parsers import eval_bool
from uvicorn.config import LOGGING_CONFIG
from uvicorn.logging import ColourizedFormatter

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

# Overwrite uvicorn's default logging config in order to be able to log INFO level messages
# from within our app
LOGGING_CONFIG["loggers"]["root"] = {
    "handlers": [
        "default",
    ], "level": "INFO", "propagate": False,
}


def get_log_config() -> Dict[str, Any]:
    log_config: Dict[str, Any] = PROD_LOGGING_CONFIG if not eval_bool(
        IS_OFFLINE,
    ) else LOGGING_CONFIG

    return log_config


fmt = Formatter(fmt="[%(levelprefix)s] [%(name)s]: %(message)s")


def formatMessage(self: ColourizedFormatter, record: logging.LogRecord) -> str:
    recordcopy = copy(record)
    levelname = recordcopy.levelname
    if self.use_colors:
        levelname = self.color_level_name(levelname, recordcopy.levelno)
        if "color_message" in recordcopy.__dict__:
            recordcopy.msg = recordcopy.__dict__["color_message"]
            recordcopy.__dict__["message"] = recordcopy.getMessage()
    recordcopy.__dict__["levelprefix"] = levelname
    return fmt.formatMessage(recordcopy)


ColourizedFormatter.formatMessage = formatMessage
