from typing import Any, List

from fastapi import FastAPI

from src.server.middleware.enable_cors_middleware import EnableCorsMiddleware
from src.server.middleware.exception_handler import ExceptionHandler
from src.server.middleware.request_logging_middleware import setup_request_logging_middleware


class Middleware:

    _middlewares: List[Any] = [EnableCorsMiddleware, ExceptionHandler, setup_request_logging_middleware]

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        """Bind all middlewares to the app"""
        for middleware in cls._middlewares:
            middleware(app)
