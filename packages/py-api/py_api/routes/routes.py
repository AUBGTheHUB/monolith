from typing import List

from fastapi import APIRouter, FastAPI
from py_api.controllers.hackathon import verification_controller
from py_api.routes.feature_switches_routes import router as feature_switches_router
from py_api.routes.hackathon.participants_routes import (
    router as hackathon_participants_routes,
)
from py_api.routes.hackathon.teams_routes import router as teams_router
from py_api.routes.hackathon.verification_routes import router as verification_router
from py_api.routes.logs_routes import router as logs_router
from py_api.routes.questionnaires_routes import router as questionnaires_router
from py_api.routes.uploader_routes import router as uploader_router
from py_api.routes.url_shortener_routes import router as url_shortener_router
from py_api.routes.utility_routes import router as utility_router

"""
    If you need to disable request verification for a particular endpoint,
    you can do that in packages/py-api/py_api/middleware/auth.py
    by adding them to the BYPASSED_ENDPOINTS dictionary.
"""


class Routes:
    _routers: List[APIRouter] = [
        uploader_router,
        url_shortener_router,
        utility_router,
        feature_switches_router,
        logs_router,
        questionnaires_router,
        teams_router,
        hackathon_participants_routes,
        verification_router,
    ]

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        for router in cls._routers:
            app.include_router(router)
