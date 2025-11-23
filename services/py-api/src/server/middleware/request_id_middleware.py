import uuid
from typing import Awaitable, Callable

from fastapi import FastAPI, Request
from starlette.responses import Response

from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    unbind_contextvars,
)

REQUEST_ID_HEADER = "X-Request-ID"
REQUEST_ID_CTX_KEY = "request_id"


def register_request_id_middleware(app: FastAPI) -> None:
    """
    Attach a per-request UUID to structlog's contextvars and response headers.

    - Clears structlog contextvars at the start of each request;
    - Reuses X-Request-ID if present, otherwise generates a new UUID (hex, no dashes);
    - Binds `request_id` into structlog's contextvars so all logs during this request include it;
    - Adds X-Request-ID to the response headers.
    """

    @app.middleware("http")
    async def request_id_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # Make sure we start from a clean context for this request
        clear_contextvars()

        # Reuse incoming header if present, otherwise generate a fresh UUID
        request_id = request.headers.get(REQUEST_ID_HEADER) or uuid.uuid4().hex

        # Expose request_id to downstream code if needed
        request.state.request_id = request_id

        # Bind into structlog's contextvars so all logs during this request
        # include "request_id": "<uuid>"
        bind_contextvars(**{REQUEST_ID_CTX_KEY: request_id})

        try:
            response = await call_next(request)
        finally:
            # Avoid leaking the request_id into unrelated contexts
            unbind_contextvars(REQUEST_ID_CTX_KEY)

        # Make sure clients can see / report this ID back if needed
        if REQUEST_ID_HEADER not in response.headers:
            response.headers[REQUEST_ID_HEADER] = request_id

        return response
