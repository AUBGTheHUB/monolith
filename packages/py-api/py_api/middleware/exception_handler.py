from os import getenv
from traceback import format_exc

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from py_api.utilities.parsers import parse_request_body


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        @app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
            content = {
                "message": "Something went wrong! Please, contact The Hub!",
            }

            body = {}

            if hasattr(exc, "handle_body"):
                body = await parse_request_body(exc.handle_body)

            if bool(getenv("IS_OFFLINE")):
                content = {
                    "message": "Hey there, bud! Don't be sad! Here's some info which might help you debug your issue 🎉",
                    "exception": str(exc),
                    "body": body,
                    "stacktrace": format_exc(),
                }

            return JSONResponse(
                status_code=500,
                content=content,
            )
