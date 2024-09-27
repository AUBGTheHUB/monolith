import os
from typing import Callable, Any, Final, Tuple, Literal

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware:
    """This middleware is responsible for checking if the requests are coming from PY-API"""

    _BYPASSED_ENDPOINTS: Final = {"/ping": ["GET"]}

    def __init__(self, app: FastAPI) -> None:
        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            _, is_bypassed = self._check_bypassed_endpoint(request.url)
            if is_bypassed:
                response = await call_next(request)
                return response

            if os.environ["ENV"] != "PROD":
                if request.headers.get("X-PY-API-MACHINE-AUTHORIZATION") == "DEV":
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
            else:
                # TODO: Implement computing digest of request and comparing it with the incoming one
                pass

    @classmethod
    def _check_bypassed_endpoint(cls, url: Request.url) -> Tuple[str, Literal[True]] | Tuple[None, Literal[False]]:
        for endpoint in cls._BYPASSED_ENDPOINTS.keys():
            if endpoint in str(url):
                return endpoint, True
        return None, False
