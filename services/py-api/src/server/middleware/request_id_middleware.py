from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars

_REQUEST_ID_HEADER = "TheHubAUBG-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach a per-request UUID to structlog's contextvars and response headers.

    We inherit from BaseHTTPMiddleware to simplify our code, as the limitations it has do not apply for us. Should
    we start using contextvars.ContextVar, we must write this as a pure ASGI middleware.
    See: https://starlette.dev/middleware/#limitations
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Clear contextvars from the previous request
        clear_contextvars()
        # Generate a fresh UUID for this request
        request_id = uuid4().hex

        # Bind request_id to structlog contextvars.
        # We don't unbind here because uvicorn logs its access log after the response is returned.
        # The next request's clear_contextvars() will clean this up.
        # See: https://uvicorn.dev/settings/#logging
        bind_contextvars(request_id=request_id)

        response = await call_next(request)
        response.headers[_REQUEST_ID_HEADER] = request_id
        return response
