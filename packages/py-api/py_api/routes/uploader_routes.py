from typing import Annotated, Any, Dict

from fastapi import APIRouter, Form, UploadFile
from py_api.controllers import UploaderControllers


class UploaderRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:

        @router.get('/uploader')
        async def get_objects() -> Dict[str, Any]:
            return UploaderControllers.dump_objects()

        @router.post('/uploader')
        async def upload_object(file: UploadFile, filename: Annotated[str, Form()]) -> Dict[str, Any]:
            return UploaderControllers.upload_object(file, filename)

        @router.delete('/uploader')
        async def delete_object() -> Dict[str, Any]:  # type: ignore
            pass
