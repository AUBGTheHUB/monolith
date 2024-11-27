from threading import Lock
from typing import Any, Dict, cast
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError, decode, encode
import httpx
from result import Err, Ok, Result
from structlog.stdlib import get_logger
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData

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
    """A class providing methods for encoding data in with a predefined format into a JWT token, or decoding a JWT
    token into a predefined format (TypedDict)"""

    @staticmethod
    def encode_data(data: JwtUserData) -> str:
        return str(encode(data, key="secret", algorithm="HS256"))

    @staticmethod
    def decode_data(token: str) -> Result[JwtUserData, str]:
        try:
            decoded_token: dict[str, Any] = decode(token, "secret", algorithms=["HS256"])

            if "sub" in decoded_token and "is_admin" in decoded_token and "team_id" in decoded_token:
                return Ok(cast(JwtUserData, decoded_token))

            LOG.warning(
                "Decoded token is missing some or all of the required fields: `sub`, `is_admin`, `team_id`",
                decoded_token=decoded_token,
            )
            return Err("The decoded token is missing some or all of the required fields: `sub`, `is_admin`, `team_id`")

        except ExpiredSignatureError:
            LOG.warning("The JWT token has expired.")
            return Err("The JWT token has expired.")

        except InvalidSignatureError:
            LOG.warning("The JWT token has an invalid signature.")
            return Err("The JWT token has invalid signature.")

        except DecodeError:
            # We log the exception as DecodeError is a more generic one, and we want to be able to trace what exactly
            # has cause the error
            LOG.exception("There was a a general error while decoding the JWT token.")
            return Err("There was a a general error while decoding the JWT token. Checks its format again.")
