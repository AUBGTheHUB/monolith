from traceback import format_exc

from bson.errors import InvalidId
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from py_api.environment import IS_OFFLINE
from py_api.utilities.parsers import eval_bool


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        @app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
            content = {
                "message": "Something went wrong! Please, contact The Hub!",
            }

            if eval_bool(IS_OFFLINE):
                content = {
                    "message": "Hey there, bud! Don't be sad! Here's some info which might help you debug your issue 🎉",
                    "exception": str(exc),
                    "http_method": request.method,
                    "url": str(request.url),
                    "stacktrace": format_exc(),

                }

            return JSONResponse(
                status_code=500,
                content=content,
            )

        @app.exception_handler(InvalidId)
        async def handle_invalid_object_id(request: Request, exc: InvalidId) -> JSONResponse:
            return JSONResponse(content={"message": "Invalid object_id format!"}, status_code=400)
