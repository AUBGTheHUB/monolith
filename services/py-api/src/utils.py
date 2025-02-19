from collections.abc import Callable
from os import environ
from threading import Lock
from typing import Any, Dict, cast
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError, decode, encode
from src.server.exception import (
    JwtDecodeError,
    JwtDecodeSchemaMismatch,
    JwtExpiredSignatureError,
    JwtInvalidSignatureError,
)
from result import Err, Ok, Result
from structlog.stdlib import get_logger

from src.server.schemas.jwt_schemas.schemas import BaseTypedDict

LOG = get_logger()


def singleton[T](provider_func: Callable[..., T]) -> Callable[..., T]:
    """
    Thread-safe implementation of Singleton. Should be as a decorator of a "provider" function. A "provider" function
    is one which provides an instance of a class.
    Notes:
        The lock in the singleton decorator ensures that only one thread at a time can create an instance. However, it
        does not automatically make the created instance of the underlying class thread-safe!
    """
    providers = {}
    lock = Lock()

    def get_instance(*args: Any, **kwargs: Any) -> T:
        # As multiple threads could access `if cls not in instances` at the same time, this creates a race condition,
        # and we could have two different instances created. By using a lock, only ont thread at a time could execute
        # the check below.
        with lock:
            # if the provider func is not in the dict
            if provider_func not in providers:
                # We set in the dict: the provider type as key, and the provided instance as value
                providers[provider_func] = provider_func(*args, **kwargs)

        # we return the value from the dict (a.k.a the instance of the class)
        return providers[provider_func]

    return get_instance


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


class JwtUtility:
    """A class providing generic methods for encoding data in with a predefined format into a JWT token, or decoding a JWT
    token into a predefined format (TypedDict)"""

    @staticmethod
    def encode_data[T: BaseTypedDict](data: T) -> str:
        return str(encode(payload=data, key=environ["SECRET_KEY"], algorithm="HS256"))

    @staticmethod
    def decode_data[
        T: BaseTypedDict
    ](token: str, schema: Callable[..., T]) -> Result[
        T, JwtDecodeSchemaMismatch | JwtExpiredSignatureError | JwtInvalidSignatureError | JwtDecodeError
    ]:
        try:
            decoded_token: dict[str, Any] = decode(jwt=token, key=environ["SECRET_KEY"], algorithms=["HS256"])

            # schema.__annotations___.keys() gets all the defined fields of the TypedDict without initializing it
            # this will help us see if all the fields that we have defined in the schema are present in the decoded
            # jwt token
            for key in schema.__annotations__.keys():
                if key not in decoded_token:
                    return Err(JwtDecodeSchemaMismatch())

            # We check both sides since we dont know which of the dictionaries is bigger than the other
            for key in decoded_token:
                if key not in schema.__annotations__.keys():
                    return Err(JwtDecodeSchemaMismatch())

            return Ok(cast(T, decoded_token))

        except ExpiredSignatureError:
            return Err(JwtExpiredSignatureError())

        except InvalidSignatureError:
            return Err(JwtInvalidSignatureError())

        except DecodeError:
            # We log the exception DecodeError as we want to be able to trace what exactly has caused the error
            LOG.exception("There was a a general error while decoding the JWT token.")
            return Err(JwtDecodeError())
