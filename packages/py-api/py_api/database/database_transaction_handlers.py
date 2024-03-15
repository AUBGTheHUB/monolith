from functools import wraps
from typing import Any, Callable

from py_api.database.initialize import client


# https://pymongo.readthedocs.io/en/stable/api/pymongo/client_session.html
def handle_database_session_transaction(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Upon normal completion of with session.start_transaction() block, the transaction automatically
        calls ClientSession.commit_transaction().
        If the block exits with an exception, the transaction automatically calls ClientSession.abort_transaction()."""
        with client.start_session() as session:
            with session.start_transaction():
                return func(*args, session=session, **kwargs)

    return wrapper
