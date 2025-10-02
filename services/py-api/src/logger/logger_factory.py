import json
import re
from datetime import datetime
from logging import INFO, Formatter, LogRecord
from logging.handlers import RotatingFileHandler
from os import path, rename
from pathlib import Path
from typing import Dict, Any, Optional

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


class _JSONFormatter(Formatter):
    """Custom JSON formatter for Python's standard logging module.
    This is used for Uvicorn logs to output in JSON format for DEV and PROD environments.

    For uvicorn.access logs, the formatter parses the log message and creates a structured reqPayload.

    Basic fields extracted from the log message:
    - ip: Client IP address
    - method: HTTP method (GET, POST, etc.)
    - resource: Request path
    - httpVersion: HTTP version (HTTP/1.1, etc.)
    - status: HTTP status code
    - responseSize: Response size in bytes (if available)

    Additional fields can be added to the log record by middleware:
    - startTime: Request start time (ISO format)
    - endTime: Request end time (ISO format)
    - latency: Request processing time
    - host: Host header value
    - traceId: Trace ID for request tracking

    Example output:
    {
      "timestamp": "2025-10-02T10:36:08.769100Z",
      "level": "INFO",
      "logger": "uvicorn.access",
      "reqPayload": {
        "ip": "104.23.160.2",
        "method": "GET",
        "resource": "/api/v3/ping",
        "httpVersion": "HTTP/1.1",
        "status": 200,
        "responseSize": "559",
        "startTime": "2025-10-02T10:36:08.769100Z",
        "endTime": "2025-10-02T10:36:08.850535Z",
        "latency": "0.081435s",
        "host": "thehub-aubg.com",
        "traceId": "7daae9306acb60d81ae73c79864932df"
      }
    }
    """

    # Regex pattern to parse Uvicorn access logs
    # Example: 127.0.0.1:52176 - "GET /api/v3/ping HTTP/1.1" 200
    ACCESS_LOG_PATTERN = re.compile(
        r'^(?P<ip>[\d\.:a-fA-F]+):(?P<port>\d+) - "(?P<method>\w+) (?P<path>[^\s]+) (?P<http_version>HTTP/[\d\.]+)" (?P<status>\d+)(?:\s+(?P<response_size>\d+))?'
    )

    def _parse_access_log(self, message: str) -> Optional[Dict[str, Any]]:
        """Parse Uvicorn access log message and extract structured fields."""
        match = self.ACCESS_LOG_PATTERN.match(message)
        if match:
            data = match.groupdict()
            return {
                "ip": data["ip"],
                "method": data["method"],
                "resource": data["path"],
                "httpVersion": data["http_version"],
                "status": int(data["status"]),
                "responseSize": data.get("response_size"),
            }
        return None

    def format(self, record: LogRecord) -> str:
        message = record.getMessage()
        timestamp = datetime.fromtimestamp(record.created).isoformat() + "Z"

        # Base log structure
        log_data: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
        }

        # For uvicorn.access logs, parse and structure the request payload
        if record.name == "uvicorn.access":
            parsed = self._parse_access_log(message)
            if parsed:
                # Build detailed request payload
                req_payload = {
                    "ip": parsed["ip"],
                    "method": parsed["method"],
                    "resource": parsed["resource"],
                    "httpVersion": parsed["httpVersion"],
                    "status": parsed["status"],
                }

                # Add optional fields if available
                if parsed.get("responseSize"):
                    req_payload["responseSize"] = parsed["responseSize"]

                # Try to extract additional fields from the log record attributes
                if hasattr(record, "startTime"):
                    req_payload["startTime"] = record.startTime
                if hasattr(record, "endTime"):
                    req_payload["endTime"] = record.endTime
                if hasattr(record, "latency"):
                    req_payload["latency"] = record.latency
                if hasattr(record, "host"):
                    req_payload["host"] = record.host
                if hasattr(record, "traceId"):
                    req_payload["traceId"] = record.traceId

                log_data["reqPayload"] = req_payload
            else:
                # Fallback to original message if parsing fails
                log_data["message"] = message
        else:
            # For non-access logs, just include the message
            log_data["message"] = message

        # Add exception info if present
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


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
                rename(f"{self.baseFilename}.{1}", f"{self.baseFilename}.{self.backupCount}")
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


def get_uvicorn_logger(env: str) -> Dict[str, Any]:
    prod_logging_config: Dict[str, Any] = {
        "version": 1,
        "formatters": {
            "json_formatter": {
                "()": "src.logger.logger_factory._JSONFormatter",
            },
        },
        "handlers": {
            "logfile": {
                "class": "src.logger.logger_factory._CustomRotatingFileHandler",
                "level": "INFO",
                "filename": "shared/server.log",
                "formatter": "json_formatter",
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

    # We save the incoming requests logs to a file in JSON format for DEV and PROD environments
    # Example: {"timestamp": "2024-10-16 14:07:11", "level": "INFO", "logger": "uvicorn.access", "message": "127.0.0.1:52176 - \"GET /api/v3/ping HTTP/1.1\" 200"}
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
