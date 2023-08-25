from typing import Any, Dict

from fastapi import APIRouter, FastAPI, Request
from py_api.utilities.decorators import bind_router
from py_api.utilities.memory import get_current_memory_usage_in_mbs

router = APIRouter()

class UtilityRoutes:

    @staticmethod
    @bind_router(router)
    def bind(app: FastAPI) -> None:
        @router.get('/health')
        async def health() -> Dict[str, Any]:
            return {
                "status": "healthy",
                "currentMemoryUsage": f"{get_current_memory_usage_in_mbs()} MB",
            }

        @router.get('/routes')
        async def get_routes(request: Request) -> Dict[str, Dict[str, Any]]:
            routes: Dict[str, Any] = {}
            for route in request.app.routes:
                if not routes.get(route.path):
                    routes[route.path] = [*route.methods]
                else:
                    routes[route.path].append(*route.methods)

            return {
                "paths": routes,
            }
