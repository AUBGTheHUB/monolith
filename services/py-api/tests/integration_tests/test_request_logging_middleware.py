from unittest import mock

import pytest
from httpx import AsyncClient
from structlog.testing import LogCapture

PING_ENDPOINT_URL = "/api/v3/ping"


@pytest.mark.asyncio
async def test_request_logging_middleware_logs_request_details(async_client: AsyncClient) -> None:
    """Test that the request logging middleware logs detailed request information"""
    # Given: A log capture to intercept logs
    log_capture = LogCapture()

    with mock.patch("src.server.middleware.request_logging_middleware.LOG", log_capture):
        # When: Making a request
        resp = await async_client.get(PING_ENDPOINT_URL)

        # Then: The response is successful
        assert resp.status_code == 200

        # And: The middleware logged the request with detailed information
        assert len(log_capture.entries) > 0

        # Find the HTTP Request log entry
        http_request_logs = [entry for entry in log_capture.entries if entry.get("event") == "HTTP Request"]
        assert len(http_request_logs) > 0

        # Verify the reqPayload contains all required fields
        log_entry = http_request_logs[0]
        req_payload = log_entry["reqPayload"]

        # Verify all expected fields are present
        assert "ip" in req_payload
        assert "startTime" in req_payload
        assert "endTime" in req_payload
        assert "latency" in req_payload
        assert "method" in req_payload
        assert "resource" in req_payload
        assert "httpVersion" in req_payload
        assert "status" in req_payload
        assert "responseSize" in req_payload
        assert "host" in req_payload
        assert "traceId" in req_payload

        # Verify specific values
        assert req_payload["method"] == "GET"
        assert req_payload["resource"] == "/api/v3/ping"
        assert req_payload["status"] == 200
        assert req_payload["latency"].endswith("s")  # Should end with 's' for seconds
