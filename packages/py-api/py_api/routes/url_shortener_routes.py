from typing import Any, Dict

from fastapi import APIRouter, FastAPI
from py_api.controllers import UrlShortenerController as c
from py_api.models import ShortenedURL
from py_api.routes.base import RoutesBase
from py_api.utilities.decorators import bind_router

router = APIRouter(prefix="/shortener")


class UrlShortenerRoutes(RoutesBase):
    def __init__(self, app: FastAPI):
        self.bind(app)

    @staticmethod
    @bind_router(router)
    def bind(app: FastAPI) -> None:
        @router.get("")
        def get_shortened_urls() -> Dict[str, Any]:
            return c.fetch_shortened_urls()

        @router.delete("/{endpoint}")
        def delete_shortened_url(endpoint: str) -> Dict[str, Any]:
            return c.delete_shortened_url(endpoint)

        @router.put("")
        async def upsert_shortener_url(body: ShortenedURL) -> Dict[str, Any]:
            return c.upsert_shortened_url(body)
