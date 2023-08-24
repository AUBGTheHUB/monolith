from fastapi import Request
from logging import getLogger
from typing import Final

logger = getLogger("auth")

class AuthMiddleware:
    """ Utility class for easily initializing all authentication middleware """

    BYPASSED_ENDPOINTS: Final = [
        "/health"
    ]

    def __init__(self, app):
        @app.middleware("http")
        async def verify_request(request: Request, call_next):
            current_endpoint = f"/{str(request.url).rsplit('/', 1)[-1]}"

            if not current_endpoint in self.BYPASSED_ENDPOINTS:
                # TODO: Verify request
                pass

            response = await call_next(request)
            return response
            

