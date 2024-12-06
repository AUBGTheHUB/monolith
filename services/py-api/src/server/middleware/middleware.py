from typing import Any, List

from fastapi import FastAPI
from src.server.middleware.auth import AuthMiddleware


class Middleware:

    _middlewares: List[Any] = [AuthMiddleware]

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        for middleware in cls._middlewares:
            middleware(app)
