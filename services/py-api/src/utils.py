from os import environ
from threading import Lock
from typing import Any, Dict, TypedDict
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError, decode, encode
import httpx
import jwt
from structlog.stdlib import get_logger

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
    class UserData(TypedDict):
        id: int
        name: str
        email: str
        is_admin: bool
        email_verified: bool
        team_id: int
        created_at: str
        updated_at: str
         

    @staticmethod
    def encode(data: UserData) -> str:
            return encode(data,key=environ["SECRET_KEY"])
    
    @staticmethod
    def decode(token: str) -> Dict[str, Any]:
     try:
        decoded_payload=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
     except ExpiredSignatureError:
            print("The token has expired.")
            return {"error": "TokenExpired"}
     except InvalidSignatureError:
            print("The token has an invalid signature.")
            return {"error": "InvalidSignature"}
     except DecodeError:
            print("There was an error decoding the token.")
            return {"error": "DecodeError"}
    

print(JwtUtility.encode({"str":"fdsafsad"}))