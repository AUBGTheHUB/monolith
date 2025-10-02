import json
from logging import LogRecord

from src.logger.logger_factory import _JSONFormatter


def test_json_formatter_basic():
    """Test that the JSON formatter produces valid JSON output with expected fields"""
    formatter = _JSONFormatter()

    # Create a mock log record
    record = LogRecord(
        name="test.logger",
        level=20,  # INFO level
        pathname="/path/to/file.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # Format the record
    result = formatter.format(record)

    # Parse the JSON to verify it's valid
    log_data = json.loads(result)

    # Verify expected fields are present
    assert "timestamp" in log_data
    assert "level" in log_data
    assert "logger" in log_data
    assert "message" in log_data

    # Verify values
    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "test.logger"
    assert log_data["message"] == "Test message"


def test_json_formatter_with_exception():
    """Test that the JSON formatter includes exception info when present"""
    formatter = _JSONFormatter()

    try:
        raise ValueError("Test exception")
    except ValueError:
        import sys

        exc_info = sys.exc_info()

        record = LogRecord(
            name="test.logger",
            level=40,  # ERROR level
            pathname="/path/to/file.py",
            lineno=42,
            msg="Error occurred",
            args=(),
            exc_info=exc_info,
        )

        result = formatter.format(record)
        log_data = json.loads(result)

        # Verify exception info is included
        assert "exc_info" in log_data
        assert "ValueError: Test exception" in log_data["exc_info"]


def test_get_uvicorn_logger_uses_json_formatter():
    """Test that get_uvicorn_logger returns config with JSON formatter for DEV and PROD"""
    from src.logger.logger_factory import get_uvicorn_logger

    # Test DEV environment
    dev_config = get_uvicorn_logger("DEV")
    assert "formatters" in dev_config
    assert "json_formatter" in dev_config["formatters"]
    assert dev_config["formatters"]["json_formatter"]["()"] == "src.logger.logger_factory._JSONFormatter"

    # Test PROD environment
    prod_config = get_uvicorn_logger("PROD")
    assert "formatters" in prod_config
    assert "json_formatter" in prod_config["formatters"]
    assert prod_config["formatters"]["json_formatter"]["()"] == "src.logger.logger_factory._JSONFormatter"

    # Verify handler uses the json formatter
    assert dev_config["handlers"]["logfile"]["formatter"] == "json_formatter"
    assert prod_config["handlers"]["logfile"]["formatter"] == "json_formatter"
