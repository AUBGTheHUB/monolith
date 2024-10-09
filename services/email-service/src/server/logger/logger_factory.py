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
                "filename": "email_service.log",
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

    if env == "PROD":
        return prod_logging_config

    default_logging_config: Dict[str, Any] = LOGGING_CONFIG

    return default_logging_config


def configure_app_logger(env: str) -> None:
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
            _CustomConsoleRenderer() if env == "DEV" else JSONRenderer(),
        ],
        logger_factory=(
            PrintLoggerFactory()
            if env != "PROD"
            else WriteLoggerFactory(file=Path("email_service").with_suffix(".log").open("a"))
        ),
        wrapper_class=None if env != "PROD" else make_filtering_bound_logger(INFO),
        cache_logger_on_first_use=True,
    )
