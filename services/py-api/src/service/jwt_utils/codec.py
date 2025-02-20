from os import environ
from typing import Callable, Any, cast

from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.exception import JwtDecodeSchemaMismatch, JwtExpiredSignatureError, JwtInvalidSignatureError, JwtDecodeError
from src.service.jwt_utils.schemas import BaseTypedDict

LOG = get_logger()


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
