from typing import Any, List

from fastapi import FastAPI

from src.server.middleware.enable_cors_middleware import EnableCorsMiddleware


class Middleware:

    _middlewares: List[Any] = [EnableCorsMiddleware]

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        """Bind all middlewares to the app"""
        for middleware in cls._middlewares:
            middleware(app)
