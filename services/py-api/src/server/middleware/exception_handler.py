from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from src.server.schemas.response_schemas.schemas import Response, ErrResponse


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        @app.exception_handler(HTTPException)
        async def custom_exception_handler(request: Request, exc: HTTPException) -> Response:
            """Normalizes HTTPException responses to use 'error' key instead of 'detail'."""
            return Response(status_code=exc.status_code, response_model=ErrResponse(error=exc.detail))

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
            """Converts Pydantic validation errors (422) to 400 with formatted error messages."""
            error_messages = []
            for error in exc.errors():
                if "msg" in error:
                    field = " -> ".join(str(loc) for loc in error.get("loc", []))
                    msg = error["msg"]
                    if field:
                        error_messages.append(f"{field}: {msg}")
                    else:
                        error_messages.append(msg)
            
            error_message = "; ".join(error_messages) if error_messages else "Validation error"
            return Response(status_code=400, response_model=ErrResponse(error=error_message))
