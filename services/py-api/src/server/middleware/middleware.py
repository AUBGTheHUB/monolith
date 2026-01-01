from typing import Callable

from fastapi import FastAPI
from starlette.types import ASGIApp

from src.server.middleware.enable_cors_middleware import cors_middleware_factory
from src.server.middleware.exception_handler import register_exception_handlers
from src.server.middleware.request_id_middleware import RequestIdMiddleware

# Type alias for middleware: a callable that takes an ASGIApp and returns an ASGIApp
type MiddlewareFactory = Callable[[ASGIApp], ASGIApp]

# Middleware stack defined in REQUEST execution order (first to last).
# Starlette's add_middleware prepends to the list, and then reverses when building
# the stack, so the LAST middleware added via add_middleware becomes OUTERMOST.
# Therefore, we list middlewares in REVERSE execution order here.
MIDDLEWARE_STACK: list[MiddlewareFactory] = [
    cors_middleware_factory,  # Added first → innermost → executes SECOND on request
    RequestIdMiddleware,  # Added last → outermost → executes FIRST on request
]


def register_all_exception_handlers(app: FastAPI) -> None:
    """
    Register all custom exception handlers for the application.

    Exception handlers are registered with FastAPI's internal ExceptionMiddleware
    and are invoked when matching exceptions are raised during request processing.
    """
    register_exception_handlers(app)


def register_all_middlewares(app: FastAPI) -> None:
    """
    Register all middlewares for the application.

    MIDDLEWARE EXECUTION ORDER:
    ==========================
    Starlette's add_middleware(M) prepends M to an internal list, then reverses
    that list when building the middleware stack. This means:
    - The LAST middleware added becomes the OUTERMOST (runs first on request)
    - The FIRST middleware added becomes the INNERMOST (runs last on request)

    MIDDLEWARE_STACK is defined in REQUEST execution order. We iterate in order,
    so the last item added (last in list) becomes outermost (runs first).

    Request flow:  Client → RequestIdMiddleware → CORSMiddleware → Route Handler
    Response flow: Route Handler → CORSMiddleware → RequestIdMiddleware → Client
    """
    for middleware in MIDDLEWARE_STACK:
        app.add_middleware(middleware)
