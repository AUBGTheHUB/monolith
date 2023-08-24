from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Final
from requests import post


class AuthMiddleware:
    """Utility class for easily initializing all authentication middleware"""

    # add endpoints which need to bypass the request verification in this list
    BYPASSED_ENDPOINTS: Final = ["/health"]

    def __init__(self, app):
        @app.middleware("http")
        async def verify_request(request: Request, call_next):
            current_endpoint = f"/{str(request.url).rsplit('/', 1)[-1]}"

            if current_endpoint not in self.BYPASSED_ENDPOINTS:
                validate_url = f"{request.url.components.scheme}://{request.base_url if not request.base_url.netloc.find(':') else request.base_url.netloc.split(':')[0]}:8000/api/validate"

                try:
                    res = post(url=validate_url, headers=request.headers)
                except Exception as e:
                    return self._generate_bad_auth_response(exception=e)

                if res.status_code != 200:
                    return self._generate_bad_auth_response()

            response = await call_next(request)
            return response

    def _generate_bad_auth_response(self, exception=None):
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

        return JSONResponse(content=jsonable_encoder(content),
                            status_code=status_code)
