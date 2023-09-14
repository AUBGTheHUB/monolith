from logging import getLogger
from typing import Any, Callable, Dict, Tuple

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from py_api.database import db
from py_api.environment import ENABLE_ANALYTICS
from requests import get
from starlette.background import BackgroundTask

logger = getLogger("analytics")


class AnalyticsMiddleware:
    an_col = db.analytics

    def __init__(self, app: FastAPI) -> None:
        @app.middleware('http')
        async def run_analytics(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            response = await call_next(request)
            if ENABLE_ANALYTICS:
                response.background = BackgroundTask(
                    self._update_entries, request,
                )

            return response

    @classmethod
    async def _update_entries(cls, request: Request) -> None:
        country, city = None, None
        projection = {"_id": 0}
        analytics = cls.an_col.find_one({}, projection)

        if request.client:
            country, city = cls.get_country_and_city_from_ip(request.client)

        analytics = cls._update_analytics(analytics, country, city)

        update_operation = cls._create_update_operation(analytics)
        status = cls.an_col.update_one({}, update_operation, upsert=True)

        if status.modified_count != 1 and not status.acknowledged:
            logger.error("Couldn't update analytics")

    @staticmethod
    def get_country_and_city_from_ip(ip_address: str) -> Tuple[str, str]:
        response = get(
            f"https://geolocation-db.com/json/{ip_address}",
        ).json()
        return response["country_name"], response["city"]

    @staticmethod
    def _create_update_operation(locations: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        update_operation: Dict[str, Dict[str, Any]] = {
            "$set": {},
        }

        for key, item in locations.items():
            update_operation["$set"][key] = item

        return update_operation

    @staticmethod
    def _update_analytics(analytics: Dict[str, Any] | None, country: str | None, city: str | None) -> Dict[str, Any]:
        if not analytics:
            analytics = {
                "total_requests": 0,
                "locations": {},
            }

        analytics["total_requests"] = analytics["total_requests"] + 1

        if not country or not city:
            return analytics

        if country_dict := analytics["locations"].get(country):
            if current_count := country_dict.get(city):
                analytics["locations"][country][city] = current_count + 1
            else:
                analytics["locations"][country][city] = 1
        else:
            analytics["locations"][country] = {
                city: 1,
            }

        return analytics
