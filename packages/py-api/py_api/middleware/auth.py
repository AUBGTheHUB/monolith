from typing import Any, Callable, Final, Literal, Tuple

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from requests import post

# add endpoints which need to bypass the request verification in this dict
# with their appropriate method type or "*" in order to allow all types

# an endpoint which allows all methods to bypass verification will be declared
# as follows: "/users": ["*"]

# an endpoint which allows only GET and PUT methods to bypass verification
# will be declared as follows: "/users": ["GET", "PUT"]

BYPASSED_ENDPOINTS: Final = {
    "/health": ["GET"], "/routes": ["GET"], "/fswitches": ["GET"],
}


class AuthMiddleware:
    """Utility class for easily initializing all authentication middleware"""

    @classmethod
    def bind(cls, app: FastAPI) -> None:

        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            endpoint, is_bypassed = cls.check_bypassed_endpoint(request.url)

            if not is_bypassed or (
                # autopep8: off
                request.method not in BYPASSED_ENDPOINTS[endpoint]  # type: ignore
                and BYPASSED_ENDPOINTS[endpoint][0] != "*"  # type: ignore
                # autopep8: on
            ):

                if not request.base_url.netloc.find(":"):
                    host = request.base_url
                else:
                    host = request.base_url.netloc.split(":")[0] + ":8000"

                validate_url = (
                    f"{request.url.components.scheme}://{host}/api/validate"
                )

                try:
                    # passing all headers breaks the APIs when using formdata
                    header_key = 'BEARER-TOKEN'
                    headers = {
                        header_key: request.headers.get(header_key, ''),
                    }
                    res = post(url=validate_url, headers=headers)
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

        return JSONResponse(content=content, status_code=status_code)

    @classmethod
    def check_bypassed_endpoint(cls, url: Request.url) -> Tuple[str, Literal[True]] | Tuple[None, Literal[False]]:
        for endpoint in BYPASSED_ENDPOINTS.keys():
            if endpoint in str(url):
                return endpoint, True
        return None, False
