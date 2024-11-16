import os

from threading import Lock
from typing import Any, Dict

import httpx
from structlog.stdlib import get_logger

import jwt

JWT_SECRET = os.environ["SECRET_KEY"]
LOG = get_logger()


class SingletonMeta(type):
    """
    Thread-safe implementation of Singleton. As a metaclass in provides the singleton behaviour to classes using it.
    https://refactoring.guru/design-patterns/singleton/python/example#example-1
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
    # TODO: Finish implementation. we use this wrapper class to provide an abstraction over the async http library we
    #  use. It is somewhat of a [Facade Pattern](https://refactoring.guru/design-patterns/facade) so that if we decide
    #  to swap the underlying library for another one we do it only here, and all of the callers which use this class
    #  won't break. If we use the library directly we get coupled to the interface and implementations of the given
    #  libray, which makes our code harder to change in the future.

    def __init__(self) -> None:
        self._async_client = httpx.AsyncClient()

    async def stop(self) -> None:
        """Raises RuntimeError if the client has not been initialized"""
        if self._async_client is None:
            raise RuntimeError("The AsyncClient has not been initialized!")

        await self._async_client.aclose()


class JwtUtility:
    async def encode(payload) -> Any:
        try:
            encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            return encoded
        except RuntimeError as e:
            LOG.warning(e)

    async def decode(token) -> Any:
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithm="HS256")
            return decoded
        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidSignatureError) as e:
            LOG.error(e)
