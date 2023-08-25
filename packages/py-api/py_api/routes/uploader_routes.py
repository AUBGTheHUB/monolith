from typing import Annotated, Any, Dict

from fastapi import APIRouter, Form, UploadFile
from py_api.controllers import UploaderController as c


class UploaderRoutes:
    @staticmethod
    def bind(router: APIRouter) -> None:

        @router.get('/uploader')
        async def get_objects() -> Dict[str, Any]:
            return c.dump_objects()

        @router.post('/uploader')
        async def upload_object(file: UploadFile, filename: Annotated[str, Form()]) -> Dict[str, Any]:
            """
                MyPy's capabilities are insufficient to detect the possibility that the
                upload_object controller could potentially return a JSONResponse instead
                of the expected typed Dict.

                It appears that the majority of codebases
                do not specify return types for their endpoints.

                However, due to our enforcement of rigorous --strict checking,
                we must manage with typed dictionaries.
            """
            return c.upload_object(file, filename)

        @router.delete('/uploader')
        async def delete_object() -> Dict[str, Any]:  # type: ignore
            pass
