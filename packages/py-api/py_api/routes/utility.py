from typing import Any, Dict

from fastapi import FastAPI


class UtilityRoutes:
    @staticmethod
    def bind(app: FastAPI) -> None:
        @app.get('/health')  # type: ignore
        async def health() -> Dict[str, Any]:
            return {"status": "healthy"}
