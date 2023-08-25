from os import getenv
from traceback import format_exc

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ExceptionHandler:
    @staticmethod
    def bind(app: FastAPI) -> None:
        @app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
            content = {
                "message": "Something went wrong! Please, contact The Hub!",
            }

            if bool(getenv("IS_OFFLINE")):
                content = {
                    "message": "Hey there, bud! Don't be sad! Here's some info which might help you debug your issue 🎉",
                    "exception": str(exc),
                    "stacktrace": str(format_exc()) if bool(getenv("IS_OFFLINE")) else "<REDACTED>",
                }
            else:
                # TODO: write exception in file used for logging
                # this will help with debugging failing deployed APIs
                pass

            return JSONResponse(
                status_code=500,
                content=content,
            )
