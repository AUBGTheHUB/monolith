from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.server.schemas.response_schemas.schemas import ErrResponse, Response


async def _http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """
    This is needed to keep consistency in Error format in Swagger. Instead of "error", the default key in
    the JSON response is "detail" when we raise an HTTPException. This handler changes this key to "error".
    """
    return Response(status_code=exc.status_code, response_model=ErrResponse(error=exc.detail))


def _format_validation_errors(errors: list[dict]) -> tuple[int, str]:
    """Formats validation errors and determines the appropriate status code."""
    # Check if the error is about missing Authorization header
    for error in errors:
        if error.get("loc") and "Authorization" in str(error.get("loc")):
            return (401, "Unauthorized")
    
    # Format validation errors into a readable message
    error_messages = []
    for error in errors:
        loc = " -> ".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "Validation error")
        error_messages.append(f"{loc}: {msg}")
    
    error_message = "; ".join(error_messages) if error_messages else "Validation error"
    return (400, error_message)


async def _request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    """
    Converts Pydantic validation errors (422) to 400 for consistency.
    Also handles missing Authorization header as 401 instead of 422.
    """
    status_code, error_message = _format_validation_errors(exc.errors())
    return Response(
        status_code=status_code,
        response_model=ErrResponse(error=error_message)
    )


async def _pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> Response:
    """
    Handles Pydantic ValidationError directly (in case FastAPI doesn't convert it to RequestValidationError).
    """
    errors = exc.errors()
    status_code, error_message = _format_validation_errors(errors)
    return Response(
        status_code=status_code,
        response_model=ErrResponse(error=error_message)
    )


async def _global_exception_handler(request: Request, exc: Exception) -> Response:
    """Catches all unhandled exceptions and returns a 500 error."""
    import traceback
    from structlog.stdlib import get_logger
    LOG = get_logger()
    LOG.exception("Unhandled exception in request handler", exc=exc, exc_type=type(exc).__name__)
    traceback.print_exc()
    return Response(
        status_code=500,
        response_model=ErrResponse(error=f"An unexpected error occurred: {type(exc).__name__}: {str(exc)}")
    )


class ExceptionHandlers:
    @staticmethod
    def register_exception_handlers(app: FastAPI) -> None:
        """Register all custom exception handlers for the application."""
        # FastAPI converts Pydantic ValidationError to RequestValidationError, so we only need RequestValidationError handler
        app.add_exception_handler(RequestValidationError, _request_validation_exception_handler)
        app.add_exception_handler(HTTPException, _http_exception_handler)
        # Keep ValidationError handler as fallback in case FastAPI doesn't convert it
        app.add_exception_handler(ValidationError, _pydantic_validation_exception_handler)
        app.add_exception_handler(Exception, _global_exception_handler)
