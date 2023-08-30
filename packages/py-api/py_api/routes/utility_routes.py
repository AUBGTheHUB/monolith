from logging import getLogger
from typing import Any, Dict

from fastapi import APIRouter, Request
from py_api.utilities.memory import get_current_memory_usage_in_mbs

router = APIRouter()
logger = getLogger("health")


def handle_exception(func):
    def wrapper(*arg, **kwargs):
        print("here")
        request = arg[0]
        try:
            response = func(*arg, **kwargs)
            print(response)
            return response
        except Exception as e:
            e.handle_body = request.body
            raise e

    return wrapper


@handle_exception
def health_controller(request: Request):
    raise Exception('/health')
    return {
        "status": "healthy",
        "currentMemoryUsage": f"{get_current_memory_usage_in_mbs()} MB",
    }


@router.get('/health')
# @handle_exception
async def health(request: Request) -> Dict[str, Any]:
    result = health_controller(request)
    return result


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
