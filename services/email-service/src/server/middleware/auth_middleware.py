import os
from typing import Callable, Any

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware:
    """This middleware is responsible for checking if the requests are coming from PY-API"""

    def __init__(self, app: FastAPI) -> None:
        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            if os.environ["ENV"] != "PROD":
                if request.headers.get("X-PY-API-MACHINE-AUTHORIZATION") == "DEV":
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
            else:
                # TODO: Implement computing digest of request and comparing it with the incoming one
                pass
