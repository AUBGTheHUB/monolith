from typing import List

from fastapi import APIRouter, FastAPI
from py_api.routes.feature_switches_routes import router as feature_switches_router
from py_api.routes.getting_logs_routes import router as get_logs_router
from py_api.routes.uploader_routes import router as uploader_router
from py_api.routes.url_shortener_routes import router as url_shortener_router
from py_api.routes.utility_routes import router as utility_router

"""
    If you need to disable request verification for a particular endpoint,
    you can do that in packages/py-api/py_api/middleware/auth.py
    by adding them to the BYPASSED_ENDPOINTS dictionary.
"""

routers: List[APIRouter] = [
    uploader_router,
    url_shortener_router,
    utility_router,
    feature_switches_router,
    get_logs_router,
]


class Routes:
    def bind(app: FastAPI) -> None:
        for router in routers:
            app.include_router(router)
