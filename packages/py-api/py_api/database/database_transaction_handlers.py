from functools import wraps
from typing import Any, Callable

from fastapi.responses import JSONResponse
from py_api.database.initialize import client


def handle_database_session_transaction(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            # Assuming `client` is an instance of MongoClient
            with client.start_session() as session:
                with session.start_transaction():
                    return func(*args, session=session, **kwargs)

        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    return wrapper
