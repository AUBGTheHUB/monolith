from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from src.server.schemas.response_schemas.schemas import ErrResponse, Response


async def _http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """
    This is needed to keep consistency in Error format in Swagger. Instead of "error", the default key in
    the JSON response is "detail" when we raise an HTTPException. This handler changes this key to "error".
    """
    return Response(status_code=exc.status_code, response_model=ErrResponse(error=exc.detail))


async def _request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    """
    Converts Pydantic validation errors (422) to 400 for consistency.
    Also handles missing Authorization header as 401 instead of 422.
    """
    errors = exc.errors()
    
    # Check if the error is about missing Authorization header
    for error in errors:
        if error.get("loc") and "Authorization" in str(error.get("loc")):
            return Response(
                status_code=401,
                response_model=ErrResponse(error="Unauthorized")
            )
    
    # Format validation errors into a readable message
    error_messages = []
    for error in errors:
        loc = " -> ".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "Validation error")
        error_messages.append(f"{loc}: {msg}")
    
    error_message = "; ".join(error_messages) if error_messages else "Validation error"
    
    return Response(
        status_code=400,
        response_model=ErrResponse(error=error_message)
    )


class ExceptionHandlers:
    @staticmethod
    def register_exception_handlers(app: FastAPI) -> None:
        """Register all custom exception handlers for the application."""
        app.add_exception_handler(HTTPException, _http_exception_handler)
        app.add_exception_handler(RequestValidationError, _request_validation_exception_handler)
