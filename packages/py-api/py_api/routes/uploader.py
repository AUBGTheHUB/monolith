from typing import Any, Dict

from fastapi import APIRouter


class UploaderRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        @router.post('/uploader')
        async def upload_object() -> Dict[str, Any]:
            return {}

        @router.get('/uploader')
        async def get_objects() -> Dict[str, Any]:
            return {}
