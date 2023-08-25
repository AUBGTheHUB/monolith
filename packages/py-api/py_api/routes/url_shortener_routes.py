from typing import Any, Dict

from fastapi import APIRouter
from py_api.controllers import UrlShortenerController as c
from py_api.models import ShortenedURL


class UrlShortenerRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        @router.get("/shortener")
        def get_shortened_urls() -> Dict[str, Any]:
            return c.fetch_shortened_urls()

        @router.delete("/shortener/{endpoint}")
        def delete_shortened_url(endpoint: str) -> Dict[str, Any]:
            return c.delete_shortened_url(endpoint)

        @router.put("/shortener")
        async def upsert_shortener_url(body: ShortenedURL) -> Dict[str, Any]:
            return c.upsert_shortened_url(body)
