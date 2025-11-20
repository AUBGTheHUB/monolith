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


def test_json_formatter_uvicorn_access_log():
    """Test that uvicorn.access logs are parsed into detailed reqPayload structure"""
    formatter = _JSONFormatter()

    # Create a mock uvicorn access log record
    record = LogRecord(
        name="uvicorn.access",
        level=20,  # INFO level
        pathname="/path/to/uvicorn.py",
        lineno=100,
        msg='127.0.0.1:52176 - "GET /api/v3/ping HTTP/1.1" 200',
        args=(),
        exc_info=None,
    )

    # Format the record
    result = formatter.format(record)

    # Parse the JSON to verify it's valid
    log_data = json.loads(result)

    # Verify base fields
    assert "timestamp" in log_data
    assert "level" in log_data
    assert log_data["level"] == "INFO"
    assert "logger" in log_data
    assert log_data["logger"] == "uvicorn.access"

    # Verify reqPayload structure
    assert "reqPayload" in log_data
    req_payload = log_data["reqPayload"]

    assert req_payload["ip"] == "127.0.0.1"
    assert req_payload["method"] == "GET"
    assert req_payload["resource"] == "/api/v3/ping"
    assert req_payload["httpVersion"] == "HTTP/1.1"
    assert req_payload["status"] == 200


def test_json_formatter_uvicorn_access_log_with_custom_fields():
    """Test that uvicorn.access logs include custom fields when available"""
    formatter = _JSONFormatter()

    # Create a mock uvicorn access log record with custom attributes
    record = LogRecord(
        name="uvicorn.access",
        level=20,  # INFO level
        pathname="/path/to/uvicorn.py",
        lineno=100,
        msg='104.23.160.2:52176 - "GET /api/v3/ping HTTP/1.1" 200',
        args=(),
        exc_info=None,
    )

    # Add custom attributes that might be added by middleware
    record.startTime = "2025-10-02T10:36:08.769100Z"
    record.endTime = "2025-10-02T10:36:08.850535Z"
    record.latency = "0.081435s"
    record.host = "thehub-aubg.com"
    record.traceId = "7daae9306acb60d81ae73c79864932df"

    # Format the record
    result = formatter.format(record)

    # Parse the JSON
    log_data = json.loads(result)

    # Verify reqPayload includes custom fields
    assert "reqPayload" in log_data
    req_payload = log_data["reqPayload"]

    assert req_payload["ip"] == "104.23.160.2"
    assert req_payload["method"] == "GET"
    assert req_payload["resource"] == "/api/v3/ping"
    assert req_payload["httpVersion"] == "HTTP/1.1"
    assert req_payload["status"] == 200
    assert req_payload["startTime"] == "2025-10-02T10:36:08.769100Z"
    assert req_payload["endTime"] == "2025-10-02T10:36:08.850535Z"
    assert req_payload["latency"] == "0.081435s"
    assert req_payload["host"] == "thehub-aubg.com"
    assert req_payload["traceId"] == "7daae9306acb60d81ae73c79864932df"


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
