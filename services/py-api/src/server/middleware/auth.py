from os import environ
from typing import Callable, Any, Final

from fastapi.applications import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware:
    """This middleware is responsible for handling authorization for incoming requests."""

    _BYPASSED_ENDPOINTS: Final = {
        "/ping": ["GET"],
        "/docs": ["GET"],
        "/openapi.json": ["GET"],
        "/hackathon/participants": ["POST"],
    }
    """
    This dictionary maps endpoint paths to allowed HTTP methods. It contains endpoints which do not require Bearer token
    to access (public endpoints).

    Paths ending with `/*` act as wildcards, matching any sub-path. For example:

    - `"/hackathon/teams/*": ["GET", "POST"]` matches paths like `/hackathon/teams/id` or `/hackathon/teams/isak/test`
    with the specified methods (GET, POST).
    - `"/hackathon/participants": ["POST"]` matches only `/hackathon/participants` with the POST method.
    """

    def __init__(self, app: FastAPI) -> None:

        _base_url: str = app.root_path

        @app.middleware("http")
        async def verify_request(request: Request, call_next: Callable[[Any], Any]) -> JSONResponse:
            """
            Verifies the incoming request for authorization:
            - If the request is made to a bypassed endpoint, it is allowed to proceed.
            - If not, it checks for a Bearer token in the request headers for authorization.
            - If neither condition is met, it returns a 401 Unauthorized status code.

            Args:
                request: The incoming HTTP request.
                call_next: The next handler in the stack.
                    Passing the request to the next handler, either the next middleware in the stack or a route which
                    matches the URL pattern is handled internally by the `middleware` decorator

            For more info visit:
            https://fastapi.tiangolo.com/tutorial/middleware/
            https://www.starlette.io/middleware/
            https://github.com/encode/starlette/blob/8a99adfb5839b37efee33f2f49c1ba27a954fcbd/starlette/middleware/base.py#L108
            """
            if _is_bypassed(request):
                return await call_next(request)

            # FIXME: Currently the token is hardcoded as a secret for DEV and TEST environments, we will fix it before
            #  deploying to PROD
            if environ["ENV"] != "PROD":
                auth_header = request.headers.get("Authorization")
                if (
                    auth_header
                    and auth_header.startswith("Bearer ")
                    and auth_header[len("Bearer ") :] == environ["SECRET_AUTH_TOKEN"]
                ):
                    return await call_next(request)

                return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

            # TODO: Implement JWT Bearer token authorization logic if we decide on an admin panel.
            #  For now every effort to access protected routes in a PROD env will not be authorized!
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

        def _is_bypassed(req: Request) -> bool:
            """Checks if the request is towards a bypassed endpoints.

            Returns:
                True: if the request is made towards a bypassed endpoint
                False: otherwise
            """
            path = req.url.path.removeprefix(_base_url)
            method = req.method

            for allowed_path, allowed_methods in self._BYPASSED_ENDPOINTS.items():
                # Check for exact match
                if allowed_path == path and method in allowed_methods:
                    return True

                # Check for wildcard match
                if allowed_path.endswith("/*") and path.startswith(allowed_path[:-2]) and method in allowed_methods:
                    return True

            return False
