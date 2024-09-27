from fastapi import FastAPI

from src.server.middleware.auth_middleware import AuthMiddleware


class Middleware:
    _middlewares = [AuthMiddleware]

    @classmethod
    def register_middlewares(cls, app: FastAPI) -> None:
        for middleware in cls._middlewares:
            middleware(app)
