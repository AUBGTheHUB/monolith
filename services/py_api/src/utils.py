from threading import Lock
from typing import Any, Dict

import httpx
from structlog.stdlib import get_logger

LOG = get_logger()


class SingletonMeta(type):
    """
    Thread-safe implementation of Singleton. As a metaclass in provides the singleton behaviour to classes using it.
    """

    _instances: Dict[Any, Any] = {}
    _lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # On the first call a thread acquires the lock
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]


class AsyncClient(metaclass=SingletonMeta):
    # https://stackoverflow.com/questions/71031816/how-do-you-properly-reuse-an-httpx-asyncclient-within-a-fastapi-application
    # TODO: TBD
    _async_client = None

    def __init__(self) -> None:
        self._async_client = httpx.AsyncClient()

    async def stop(self) -> None:
        """Raises RuntimeError if the client has not been initialized"""
        if not self._async_client:
            raise RuntimeError("The AsyncClient has not been initialized")

        await self._async_client.aclose()
