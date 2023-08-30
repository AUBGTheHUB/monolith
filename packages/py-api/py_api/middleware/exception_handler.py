from os import getenv
from traceback import format_exc

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:

        @app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
            content = {
                "message": "Something went wrong! Please, contact The Hub!",
            }

            if bool(getenv("IS_OFFLINE")):
                content = {
                    "message": "Hey there, bud! Don't be sad! Here's some info which might help you debug your issue 🎉",
                    "exception": str(exc),
                    "http_method": request.method,
                    "url": str(request.url),
                    # "body": str(),
                    "stacktrace": format_exc(),

                }

            return JSONResponse(
                status_code=500,
                content=content,
            )
