from typing import Any, Dict

from fastapi import APIRouter
from py_api.controllers import UrlShortenerController as c


class UrlShortenerRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        @router.get("/shortener")
        def get_shortened_urls() -> Dict[str, Any]:
            return c.fetch_shortened_urls()
