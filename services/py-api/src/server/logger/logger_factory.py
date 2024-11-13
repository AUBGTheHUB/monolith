from logging import INFO, FileHandler
from pathlib import Path
from typing import Dict, Any

from structlog import configure, make_filtering_bound_logger, PrintLoggerFactory, WriteLoggerFactory
from structlog.contextvars import merge_contextvars
from structlog.dev import ConsoleRenderer
from structlog.processors import (
    TimeStamper,
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
    """We override the standard ConsoleRenderer in order to have the logs displayed like this in the console:
    "2024-10-23 13:18:22 [debug    ] db_manager.py:83 (ping_db) Pong"
    """

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

import os
from logging import FileHandler

class CustomRotatingFileHandler(FileHandler):
    def __init__(self, filename, max_bytes, backup_count=1, encoding=None, delay=False):
        super().__init__(filename, mode='a', encoding=encoding, delay=delay)
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def shouldRollover(self, record):
        """
        Determine if rollover should occur by checking the current file size.
        """
        if self.stream is None:  # Delay was set to True, open the stream now.
            self.stream = self._open()
        if self.max_bytes > 0:  # Check file size if max_bytes is set.
            self.stream.seek(0, os.SEEK_END)  # Move to end of file.
            if self.stream.tell() >= self.max_bytes:
                return True
        return False

    def get_new_rollover_filename(self):
        """
        Generate the next available rollover file name in the sequence `.1`, `.2`, `.3`, etc.
        """
        for i in range(1, self.backup_count + 1):
            rollover_filename = f"{self.baseFilename}.{i}"
            if not os.path.exists(rollover_filename):
                return rollover_filename
        # If all filenames are in use, overwrite the oldest file by cycling back to `.1`
        return f"{self.baseFilename}.1"

    def doRollover(self):
        """
        Perform a rollover by copying the contents to a new file and truncating the original file in place.
        """
        # Get the next available rollover filename
        rollover_filename = self.get_new_rollover_filename()

        # Copy contents to the new rollover file
        with open(self.baseFilename, 'r') as original_file, open(rollover_filename, 'w') as rollover_file:
            rollover_file.write(original_file.read())

        # Truncate the original file in place without reopening
        with open(self.baseFilename, 'w') as original_file:
            original_file.truncate()

    def emit(self, record):
        """
        Emit a record, performing a rollover if needed.
        """
        if self.shouldRollover(record):
            self.doRollover()
        super().emit(record)


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
                "class": "src.server.logger.logger_factory.CustomRotatingFileHandler",
                "level": "INFO",
                "filename": "shared/server.log",
                "formatter": "logformatter",
                "max_bytes": 10000,  # 10 MB limit
                "backup_count": 2,  # 2 backup files
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


def configure_app_logger(env: str) -> None:
    """Configures structlog. This logger is intended for use in the application level, and it is different from
    uvicorn's default one"""
    configure(
        processors=[
            add_log_level,
            merge_contextvars,
            TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            format_exc_info,
            StackInfoRenderer(),
            PositionalArgumentsFormatter(),
            CallsiteParameterAdder(
                {
                    CallsiteParameter.FILENAME,
                    CallsiteParameter.FUNC_NAME,
                    CallsiteParameter.LINENO,
                }
            ),
            # If the ENV is DEV or PROD we save the logs in a JSON format. This is done in order to have better
            # filtering and searching of logs if we use something like the ELK stack in the future
            # https://www.elastic.co/elastic-stack
            (JSONRenderer() if env in ("DEV", "PROD") else _CustomConsoleRenderer()),
        ],
        logger_factory=(
            # For DEV and PROD as these are VMs we save the logs to a logfile, so that we can check them later
            # For LOCAL and TEST env we print the logs directly to the stdout
            # FIXME: This could create an issue as the uvicorn logger will eventually create a server.log.1 file but
            #  these logs will continue to be written to the old server.log file
            WriteLoggerFactory(file=Path("shared/server").with_suffix(".log").open("a"))
            if env in ("DEV", "PROD")
            else PrintLoggerFactory()
        ),
        # For the PROD env we allow logs with logging level INFO and above, in order not to clutter our log files
        # For every other env the logging level is DEBUG and above, in order to have better traceability if something
        # goes wrong during testing
        wrapper_class=None if env != "PROD" else make_filtering_bound_logger(INFO),
        cache_logger_on_first_use=True,
    )
