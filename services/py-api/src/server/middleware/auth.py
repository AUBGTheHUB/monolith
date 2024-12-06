import os
import re
from typing import Callable, Any, Final, Tuple, Literal

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware:
    """This middleware is responsible for checking if the requests are coming from PY-API"""

    _BYPASSED_REQUESTS: Final = {
        "/ping": ["GET"],
        "/docs": ["GET"],
        "/openapi.json": ["GET"],
        "/hackathon/participants": ["POST"],
    }

    def __init__(self, app: FastAPI) -> None:

        _BASE_URL = app.root_path

        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            # Bypass any request towards an endpoint with a specified method that is declared in the
            # _BYPASSED_ENDPOINTS dict

            # If you the syntax below is new to you,
            # read more about upacking of touples: https://www.w3schools.com/python/python_tuples_unpack.asp
            _, is_bypassed = self._check_bypassed_request(request.url.path.removeprefix(_BASE_URL), request.method)
            if is_bypassed:
                response = await call_next(request)
                return response

            # Provides way of authorizing the incoming request based on the environment
            if os.environ["ENV"] != "PROD":
                if request.headers.get("X-Auth-Token") == "DEV":
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
            else:
                # TODO: Implement token authentication logic if we decide on an admin panel
                # For now every effort to access authenticated routes in a PROD env will not be authorized!
                return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

    @classmethod
    def _check_bypassed_request(
        cls, url_path: str, request_method: str
    ) -> Tuple[str, Literal[True]] | Tuple[None, Literal[False]]:
        # TODO: Strip the url from path params where there are such

        # Check if the url_path matches any of the endpoints
        endpoint, is_bypassed = cls._check_bypassed_endpoint(url_path)

        # If we have a url_path match, check if the current 'request_method' matches any of the allowed url methods
        if is_bypassed:
            # If both the endpoint and methods are allowed, bypass request authorization
            if request_method in cls._BYPASSED_REQUESTS[str(endpoint)]:
                return url_path, True

        return None, False

    @classmethod
    def _check_bypassed_endpoint(cls, url_path: str) -> Tuple[str, Literal[True]] | Tuple[None, Literal[False]]:

        # Tokenize the url string using '/' as a delimiter
        url_path_tokens = url_path.split("/")

        for endpoint in cls._BYPASSED_REQUESTS.keys():
            # Tokenize the endpoint string using '/' as a delimiter
            endpoint_tokens = endpoint.split("/")

            # Reset Sentinel Value/Flag to True
            endpoints_match = True

            # If the length of the endpoints doesnt match, they are not the same
            # Skip whatever is below and continue to the next iteration
            if len(url_path_tokens) != len(endpoint_tokens):
                continue

            for itr in range(len(endpoint_tokens)):
                # Do not include the path parameters in the validation
                # The regex expression checks for strings in the format '{...}'
                if re.match(r"^\{.*\}$", endpoint_tokens[itr]):
                    continue

                # If there is one token mismatch the endpoints don't match
                if endpoint_tokens[itr] != url_path_tokens[itr]:
                    endpoints_match = False
                    break

            if endpoints_match:
                return endpoint, True

        return None, False
