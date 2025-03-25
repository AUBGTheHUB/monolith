from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.server.schemas.response_schemas.schemas import Response, ErrResponse


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        @app.exception_handler(HTTPException)
        async def custom_exception_handler(request: Request, exc: HTTPException) -> Response:
            """This is needed to keep consistency in Error format in Swagger. Instead of "error", the default key is
            the JSON response is "detail"
            """
            return Response(status_code=exc.status_code, response_model=ErrResponse(error=exc.detail))
