from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bound_contextvars, clear_contextvars

_REQUEST_ID_HEADER = "TheHubAUBG-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach a per-request UUID to structlog's contextvars and response headers.

    We inherit from BaseHTTPMiddleware to simplify our code, as the limitations it has do not apply for us. Should
    we start using contextvars.ContextVar, we must write this as a pure ASGI middleware.
    See: https://starlette.dev/middleware/#limitations
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Make sure we start from a clean context for this request
        clear_contextvars()
        # Generate a fresh UUID for this request
        request_id = uuid4().hex

        # Bind request_id to structlog contextvars for the duration of the request.
        # Type ignore: bound_contextvars is a sync context manager that works in async code.
        # noinspection PyTypeChecker
        with bound_contextvars(request_id=request_id):
            response = await call_next(request)
            # Attach the RequestID to the headers so that frontend can report it back to the client in case of an error
            response.headers[_REQUEST_ID_HEADER] = request_id
            return response
