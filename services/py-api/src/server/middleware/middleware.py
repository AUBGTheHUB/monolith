from typing import Callable

from fastapi import FastAPI
from starlette.types import ASGIApp

from src.server.middleware.enable_cors_middleware import cors_middleware_factory
from src.server.middleware.request_id_middleware import RequestIdMiddleware

# Middleware stack - ORDER MATTERS!
# The LAST middleware in this list will execute FIRST on the request path.
# Each middleware takes the next app in the chain and returns a wrapped app.
_MIDDLEWARE_STACK: list[Callable[[ASGIApp], ASGIApp]] = [
    cors_middleware_factory,  # 2nd: handles CORS headers
    RequestIdMiddleware,  # 1st: attaches request ID to logs and response
]


class Middlewares:

    @staticmethod
    def register_middlewares(app: FastAPI) -> None:
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

        See Also:
        https://fastapi.tiangolo.com/tutorial/middleware/?h=midd#multiple-middleware-execution-order

        https://starlette.dev/middleware/
        """
        for middleware in _MIDDLEWARE_STACK:
            app.add_middleware(middleware)
