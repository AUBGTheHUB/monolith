import time
import uuid
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from structlog.stdlib import get_logger

LOG = get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log detailed HTTP request information.
    Logs include: ip, startTime, endTime, latency, method, resource, httpVersion, status, responseSize, host, traceId
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Generate a unique trace ID for this request
        trace_id = uuid.uuid4().hex

        # Capture start time
        start_time = time.perf_counter()
        start_time_iso = datetime.now(timezone.utc).isoformat()

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Process the request
        response = await call_next(request)

        # Capture end time
        end_time = time.perf_counter()
        end_time_iso = datetime.now(timezone.utc).isoformat()

        # Calculate latency
        latency = end_time - start_time

        # Extract response size from headers if available
        response_size = response.headers.get("content-length", "0")

        # Build the request payload log
        req_payload = {
            "ip": client_ip,
            "startTime": start_time_iso,
            "endTime": end_time_iso,
            "latency": f"{latency:.6f}s",
            "method": request.method,
            "resource": str(request.url.path),
            "httpVersion": request.scope.get("http_version", "HTTP/1.1"),
            "status": response.status_code,
            "responseSize": response_size,
            "host": request.headers.get("host", "unknown"),
            "traceId": trace_id,
        }

        # Log the request payload
        LOG.info("HTTP Request", reqPayload=req_payload)

        return response


def setup_request_logging_middleware(app: FastAPI) -> None:
    """Setup function to add the request logging middleware to the FastAPI app"""
    app.add_middleware(RequestLoggingMiddleware)
