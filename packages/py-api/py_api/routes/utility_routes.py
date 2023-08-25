from typing import Any, Dict

from fastapi import APIRouter
from py_api.utilities.memory import get_current_memory_usage_in_mbs


class UtilityRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        @router.get('/health')
        async def health() -> Dict[str, Any]:
            return {
                "status": "healthy",
                "currentMemoryUsage": f"{get_current_memory_usage_in_mbs()} MB",
            }
