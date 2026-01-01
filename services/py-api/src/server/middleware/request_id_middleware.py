import uuid

from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from structlog.contextvars import bind_contextvars, clear_contextvars, unbind_contextvars

REQUEST_ID_HEADER = "TheHubAUBG-Request-ID"
REQUEST_ID_CTX_KEY = "request_id"


class RequestIdMiddleware:
    """Attach a per-request UUID to structlog's contextvars and response headers."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Make sure we start from a clean context for this request
        clear_contextvars()

        request = Request(scope)

        # Generate a fresh UUID for this request
        request_id = uuid.uuid4().hex

        # Expose request_id to downstream code if needed
        request.state.request_id = request_id

        async def _send(message: Message) -> None:
            # Only inject header in http.response.start (not http.response.body)
            if message["type"] == "http.response.start":
                response_headers = list(message.get("headers", []))
                response_headers.append((REQUEST_ID_HEADER.encode(), request_id.encode()))
                message["headers"] = response_headers
            await send(message)

        # Bind request_id into structlog's contextvars so all logs during this request
        # include "request_id": "<uuid>".
        bind_contextvars(**{REQUEST_ID_CTX_KEY: request_id})
        try:
            await self.app(scope, receive, _send)
        finally:
            unbind_contextvars(REQUEST_ID_CTX_KEY)
