from typing import Any, Dict

from fastapi import APIRouter


class UtilityRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        @router.get('/health')
        async def health() -> Dict[str, Any]:
            return {"status": "healthy"}
