from typing import Any, Dict

from fastapi import Request
from py_api.utilities.decorators import handle_exception
from py_api.utilities.memory import get_current_memory_usage_in_mbs


class UtilitiesController:
    @handle_exception
    def health(request: Request) -> Dict[str, str]:
        return {
            "status": "healthy",
            "currentMemoryUsage": f"{get_current_memory_usage_in_mbs()} MB",
        }

    @handle_exception
    def get_routes(request: Request) -> Dict[str, Dict[str, Any]]:
        routes: Dict[str, Any] = {}
        for route in request.app.routes:
            if not routes.get(route.path):
                routes[route.path] = [*route.methods]
            else:
                routes[route.path].append(*route.methods)

        return {
            "paths": routes,
        }
