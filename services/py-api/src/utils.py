from collections.abc import Callable
from os import environ
from threading import Lock
from typing import Any, Dict, cast
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError, decode, encode
import httpx
from result import Err, Ok, Result
from structlog.stdlib import get_logger

from src.server.schemas.jwt_schemas.jwt_user_data_schema import BaseTypedDict

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
    """A class providing generic methods for encoding data in with a predefined format into a JWT token, or decoding a JWT
    token into a predefined format (TypedDict)"""

    @staticmethod
    def encode_data[T: BaseTypedDict](data: T) -> str:
        return str(encode(payload=data, key=environ["SECRET_KEY"], algorithm="HS256"))

    @staticmethod
    def decode_data[T: BaseTypedDict](token: str, schema: Callable[..., T]) -> Result[T, str]:
        try:
            decoded_token: dict[str, Any] = decode(jwt=token, key=environ["SECRET_KEY"], algorithms=["HS256"])

            # schema.__annotations___.keys() gets all the defined fields of the TypedDict without initializing it
            # this will help us see if all the fields that we have defined in the schema are present in the decoded
            # jwt token
            for key in schema.__annotations__.keys():
                if key not in decoded_token:
                    return Err("The decoded token does not correspond with the provided schema.")

            # We check both sides since we dont know which of the dictionaries is bigger than the other
            for key in decoded_token:
                if key not in schema.__annotations__.keys():
                    return Err("The decoded token does not correspond with the provided schema.")

            return Ok(cast(T, decoded_token))

        except ExpiredSignatureError:
            return Err("The JWT token has expired.")

        except InvalidSignatureError:
            return Err("The JWT token has invalid signature.")

        except DecodeError:
            # We log the exception DecodeError as we want to be able to trace what exactly has caused the error
            LOG.exception("There was a a general error while decoding the JWT token.")
            return Err("There was a a general error while decoding the JWT token. Checks its format again.")
