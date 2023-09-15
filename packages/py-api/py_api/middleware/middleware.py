
from typing import Any, List

from fastapi import FastAPI
from py_api.middleware.analytics import AnalyticsMiddleware
from py_api.middleware.auth import AuthMiddleware
from py_api.middleware.exception_handler import ExceptionHandler


class Middleware:
    _middlewares: List[Any] = [
        AuthMiddleware,
        ExceptionHandler,
    ]

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        for middleware in cls._middlewares:
            middleware(app)
