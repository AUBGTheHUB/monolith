from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.server.schemas.response_schemas.schemas import ErrResponse, Response


async def _http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """
    This is needed to keep consistency in Error format in Swagger. Instead of "error", the default key in
    the JSON response is "detail" when we raise an HTTPException. This handler changes this key to "error".
    """
    return Response(status_code=exc.status_code, response_model=ErrResponse(error=exc.detail))


class ExceptionHandlers:
    @staticmethod
    def register_exception_handlers(app: FastAPI) -> None:
        """Register all custom exception handlers for the application."""
        app.add_exception_handler(HTTPException, _http_exception_handler)
