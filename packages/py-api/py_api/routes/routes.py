from fastapi import APIRouter
from py_api.routes.uploader_routes import UploaderRoutes
from py_api.routes.url_shortener_routes import UrlShortenerRoutes
from py_api.routes.utility_routes import UtilityRoutes

"""
    If you need to disable request verification for a particular endpoint,
    you can do that in packages/py-api/py_api/middleware/auth.py
    by adding them to the BYPASSED_ENDPOINTS dictionary.
"""


class Routes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        UtilityRoutes.bind(router)
        UploaderRoutes.bind(router)
        UrlShortenerRoutes.bind(router)
