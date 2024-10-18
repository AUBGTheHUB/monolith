from logging import INFO
from pathlib import Path
from typing import Dict, Any

from structlog import configure, make_filtering_bound_logger, PrintLoggerFactory, WriteLoggerFactory
from structlog.contextvars import merge_contextvars
from structlog.dev import ConsoleRenderer
from structlog.processors import (
    TimeStamper,
    ExceptionPrettyPrinter,
    StackInfoRenderer,
    CallsiteParameterAdder,
    CallsiteParameter,
    JSONRenderer,
    format_exc_info,
    add_log_level,
)
from structlog.stdlib import PositionalArgumentsFormatter
from structlog.typing import EventDict, WrappedLogger
from uvicorn.config import LOGGING_CONFIG


class _CustomConsoleRenderer(ConsoleRenderer):
    def __call__(self, logger: WrappedLogger, name: str, event_dict: EventDict) -> str:
        event_dict["event"] = "{file}:{line} ({function}) {}".format(
            event_dict["event"],
            **{
                "file": event_dict.pop("filename"),
                "line": event_dict.pop("lineno"),
                "function": event_dict.pop("func_name"),
            },
        )
        return str(super().__call__(logger, name, event_dict))


def get_uvicorn_logger(env: str) -> Dict[str, Any]:
    prod_logging_config: Dict[str, Any] = {
        "version": 1,
        "formatters": {
            "logformatter": {
                "format": "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "logfile": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "filename": "shared/server.log",
                "formatter": "logformatter",
                "maxBytes": 10 * 1024 * 1024,  # 10 MB limit
                "backupCount": 2,  # 2 backup files
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["logfile"],
        },
        "loggers": {
            "uvicorn.error": {"level": "INFO"},
        },
    }

    # We save the incoming requests logs to a file like this:
    # [2024-10-16 14:07:11][INFO][uvicorn.access]: 127.0.0.1:52176 - "GET /api/v3/ping HTTP/1.1" 200
    if env in ("DEV", "PROD"):
        return prod_logging_config

    default_logging_config: Dict[str, Any] = LOGGING_CONFIG

    return default_logging_config


def configure_app_logger(env: str, simulating_prod_env: bool = False) -> None:
    """Configures structlog. This logger is intended for use in the application level, and it is different from
    uvicorn's default one"""
    configure(
        processors=[
            add_log_level,
            merge_contextvars,
            TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            ExceptionPrettyPrinter(),
            StackInfoRenderer(),
            format_exc_info,
            PositionalArgumentsFormatter(),
            CallsiteParameterAdder(
                {
                    CallsiteParameter.FILENAME,
                    CallsiteParameter.FUNC_NAME,
                    CallsiteParameter.LINENO,
                }
            ),
            # If the ENV is DEV or PROD we save the logs in a JSON format. This is done in order to have better
            # filtering and searchability
            (JSONRenderer() if env in ("DEV", "PROD") else _CustomConsoleRenderer()),
        ],
        logger_factory=(
            # For DEV and PROD as these are VMs we save the logs to a logfile, so that we can check them later
            # For LOCAL and TEST env we print the logs directly to the stdout
            WriteLoggerFactory(file=Path("shared/server").with_suffix(".log").open("a"))
            if env in ("DEV", "PROD")
            else PrintLoggerFactory()
        ),
        # For the PROD env we allow logs with logging level above INFO, in order not to clutter our log files
        # For every other env the logging level is DEBUG and above, in order to have better traceability if something
        # goes wrong during testing
        wrapper_class=None if env != "PROD" else make_filtering_bound_logger(INFO),
        cache_logger_on_first_use=True,
    )
