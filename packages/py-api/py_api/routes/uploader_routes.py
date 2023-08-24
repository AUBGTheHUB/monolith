from typing import Any, Dict

from fastapi import APIRouter, Request
from py_api.controllers import UploaderControllers


class UploaderRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:
        # @router.post('/uploader')
        # async def upload_object() -> Dict[str, Any]:
        #     return {"message": "here"}
        #     # return UploaderControllers.upload_object()

        @router.get('/uploader')
        async def get_objects() -> Dict[str, Any]:
            return UploaderControllers.dump_objects()
