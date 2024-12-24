from typing import Any, List

from fastapi import FastAPI


class Middleware:

    _middlewares: List[Any] = []

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        for middleware in cls._middlewares:
            middleware(app)
