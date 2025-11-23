from logging import INFO, Filter, LogRecord
from logging.handlers import RotatingFileHandler
from os import path, rename
from pathlib import Path
from typing import Dict, Any

from structlog import (
    configure,
    make_filtering_bound_logger,
    PrintLoggerFactory,
    WriteLoggerFactory,
)
from structlog.contextvars import merge_contextvars, get_contextvars
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


class _CustomRotatingFileHandler(RotatingFileHandler):
    """
    By default, the Rotating file handler, closes the current logfile (stream), renames the file by adding .1, .2, .3,
    ...etc. and then creates a new server.log to start logging there (opens a new stream). However, with this logic we
    could not synchronize both structlog and uvicorn to log at the new server.log file, since structlog had the stream
    opened to the old file which was renamed to i.e. server.log.1 by the handler used by uvicorn. To go around it, we
    are changing how the rollover of files is happening. Here we copy the contents of the server.log once it reaches
    the limit. We create a new file with the extension .1, .2, .3, ...etc. We paste the contents of the server.log to
    the new file i.e. server.log.1 and then delete whatever server.log had. This way structlog and uvicorn keep writing
    to the same file (the original server.log) using their originally opened streams.

    To achieve this we override the doRollover() method of the logging.RotatingFileHandler.

    Inspiration for the new implementation was gotten from an amazing tool called 'logrotate' that performs rotation of
    logs in this manner.

    Thank you 'logrotate'!
    """

    def _get_new_rollover_filename(self) -> str:
        """
        Generate the next available rollover file name in the sequence `.1`, `.2`, `.3`, etc.
        """
        for i in range(1, self.backupCount + 1):
            rollover_filename = f"{self.baseFilename}.{i}"
            if not path.exists(rollover_filename):
                return rollover_filename

        # If all filenames are in use, overwrite the oldest file by cycling back to `.1`
        # This function renames the files so that the oldest one is .1 and the newest
        # is the .{backupCount}.
        for i in range(1, self.backupCount + 1):
            if i == 1:
                rename(f"{self.baseFilename}.1", f"{self.baseFilename}.{self.backupCount}")
            else:
                rename(f"{self.baseFilename}.{i}", f"{self.baseFilename}.{i-1}")

        return f"{self.baseFilename}.{self.backupCount}"

    def doRollover(self) -> None:
        """
        Perform a rollover by copying the contents to a new file and truncating the original file in place.
        """
        # Get the next available rollover filename
        rollover_filename = self._get_new_rollover_filename()

        # Copy contents to the new rollover file
        with open(self.baseFilename, "r") as original_file, open(rollover_filename, "w") as rollover_file:
            rollover_file.write(original_file.read())

        # Truncate the original file in place without reopening
        with open(self.baseFilename, "w") as original_file:
            original_file.truncate()


class RequestIdFilter(Filter):
    """
    Logging filter that injects `request_id` into log records
    based on structlog's contextvars.
    """

    def filter(self, record: LogRecord) -> bool:
        try:
            ctx = get_contextvars()
        except Exception:
            ctx = {}

        request_id = ctx.get("request_id")
        # Empty string so formatter with %(request_id)s never explodes
        record.request_id = request_id or ""
        return True


def get_uvicorn_logger(env: str) -> Dict[str, Any]:
    prod_logging_config: Dict[str, Any] = {
        "version": 1,
        "formatters": {
            "logformatter": {
                "format": (
                    '{"timestamp":"%(asctime)s",'
                    '"level":"%(levelname)s",'
                    '"logger":"%(name)s",'
                    '"request_id":"%(request_id)s",'
                    '"message":"%(message)s"}'
                ),
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "filters": {
            "request_id_filter": {
                "()": "src.logger.logger_factory.RequestIdFilter",
            },
        },
        "handlers": {
            "logfile": {
                "class": "src.logger.logger_factory._CustomRotatingFileHandler",
                "level": "INFO",
                "filename": "shared/server.log",
                "formatter": "logformatter",
                "maxBytes": 10 * 1024 * 1024,  # 10 MB limit
                "backupCount": 2,  # 2 backup files
                "filters": ["request_id_filter"],
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

    # In DEV/PROD we log uvicorn output to shared/server.log as JSON-like lines
    if env in ("DEV", "PROD"):
        return prod_logging_config

    # For LOCAL/TEST fall back to uvicorn's default logging config
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
