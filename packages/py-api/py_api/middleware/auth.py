from typing import Any, Callable, Final

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from py_api.database import db
from requests import post

# add endpoints which need to bypass the request verification in this dict
# with their appropriate method type or "*" in order to allow all types

# an endpoint which allows all methods to bypass verification will be declared
# as follows: "/users": ["*"]

# an endpoint which allows only GET and PUT methods to bypass verification
# will be declared as follows: "/users": ["GET", "PUT"]

BYPASSED_ENDPOINTS: Final = {"/health": ["GET"]}


class AuthMiddleware:
    """Utility class for easily initializing all authentication middleware"""

    @classmethod
    def bind(cls, app: FastAPI) -> None:
        db.jobs.find_one()

        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            for endpoint, methods in BYPASSED_ENDPOINTS.items():
                if endpoint not in str(request.url) or (
                    request.method not in methods and methods[0] != "*"
                ):
                    if not request.base_url.netloc.find(":"):
                        host = request.base_url
                    else:
                        host = request.base_url.netloc.split(":")[0] + ":8000"

                    validate_url = (
                        f"{request.url.components.scheme}://{host}/api/validate"
                    )

                    try:
                        res = post(url=validate_url, headers=request.headers)
                    except Exception as e:
                        return cls._generate_bad_auth_response(exception=e)

                    if res.status_code != 200:
                        return cls._generate_bad_auth_response()

            response = await call_next(request)
            return response

    @classmethod
    def _generate_bad_auth_response(cls, exception: Exception | None = None) -> JSONResponse:

        content = {
            "message": "User doesn't have permissions to access this resource!",
        }
        status_code = 401

        if exception:
            content = {
                "message": "Something went wrong when verifying the request!",
                "exception": str(exception),
            }

            status_code = 500

        return JSONResponse(content=jsonable_encoder(content), status_code=status_code)
