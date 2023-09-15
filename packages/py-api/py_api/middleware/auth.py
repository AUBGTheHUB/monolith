from logging import getLogger
from typing import Any, Callable, Final, Literal, Tuple

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from py_api.environment import IS_OFFLINE, OFFLINE_TOKEN
from py_api.utilities.parsers import AttrDict
from requests import post

logger = getLogger(__name__)


# add endpoints which need to bypass the request verification in this dict
# with their appropriate method type or "*" in order to allow all types

# an endpoint which allows all methods to bypass verification will be declared
# as follows: "/users": ["*"]

# an endpoint which allows only GET and PUT methods to bypass verification
# will be declared as follows: "/users": ["GET", "PUT"]

class AuthMiddleware:
    """Utility class for easily initializing all authentication middleware"""
    _BYPASSED_ENDPOINTS: Final = {
        "/health": ["GET"], "/routes": ["GET"], "/fswitches": ["GET"],
    }

    def __init__(self, app: FastAPI) -> None:
        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            endpoint, is_bypassed = self._check_bypassed_endpoint(request.url)

            if not is_bypassed or (
                    # autopep8: off
                    request.method not in self._BYPASSED_ENDPOINTS[endpoint]  # type: ignore
                    and self._BYPASSED_ENDPOINTS[endpoint][0] != "*"  # type: ignore
                    # autopep8: on
            ):
                # localhost or hostname aliases such as local.thehub-aubg.com
                if ':' in request.base_url.hostname:
                    host = request.base_url.netloc.split(":")[0] + ":8000"
                else:
                    host = "api:8000"

                validate_url = f"{request.url.components.scheme}://{host}/api/validate"

                try:
                    # passing all headers breaks the APIs when using formdata
                    header_key = 'BEARER-TOKEN'
                    request_token = request.headers.get(header_key, '')

                    if not IS_OFFLINE:
                        headers = {
                            header_key: request_token,
                        }
                        res = post(
                            url=validate_url, headers=headers,
                            # since request's hostname doesn't match the server's certificates
                            # we need to explicitly pass the certificates
                            verify="./certs/devenv.crt",
                        )
                    else:
                        res = AttrDict(
                            status_code=200 if request_token == OFFLINE_TOKEN else 401,
                        )

                except Exception as e:
                    return self._generate_bad_auth_response(exception=e)

                if res.status_code != 200:
                    return self._generate_bad_auth_response(res.status_code)

            response = await call_next(request)
            return response

    @classmethod
    def _generate_bad_auth_response(cls, status_code: int = 401, exception: Exception | None = None) -> JSONResponse:

        content = {
            "message": "User doesn't have permissions to access this resource!",
        }

        if exception:
            content = {
                "message": "Something went wrong when verifying the request!",
                "exception": str(exception),
            }

            status_code = 500
            logger.error(
                f"Validation request failed with status code: {status_code} and exception: {str(exception)}",
            )

        return JSONResponse(content=content, status_code=status_code)

    @classmethod
    def _check_bypassed_endpoint(cls, url: Request.url) -> Tuple[str, Literal[True]] | Tuple[None, Literal[False]]:
        for endpoint in cls._BYPASSED_ENDPOINTS.keys():
            if endpoint in str(url):
                return endpoint, True
        return None, False
