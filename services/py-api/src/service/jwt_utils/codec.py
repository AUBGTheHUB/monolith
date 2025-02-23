from dataclasses import fields
from os import environ
from typing import Any, Type, cast, Dict

from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from result import Result, Err, Ok

from src.exception import JwtDecodeSchemaMismatch, JwtExpiredSignatureError, JwtInvalidSignatureError, JwtDecodeError
from src.service.jwt_utils.schemas import JwtBase, DecodedJwtTokenBase


class JwtUtility:
    """A class providing generic methods for encoding data with predefined format into a JWT token, or decoding a
    JWT token into a predefined schema format"""

    def __init__(self) -> None:
        self._key = environ["SECRET_KEY"]
        """Key used for encoding and decoding the JWT token"""

    def encode_data[T: JwtBase[DecodedJwtTokenBase]](self, data: T) -> str:
        return str(encode(payload=data.serialize(), key=self._key, algorithm="HS256"))

    def decode_data[
        T: JwtBase[DecodedJwtTokenBase]
    ](self, token: str, schema: Type[T]) -> Result[
        T, JwtDecodeSchemaMismatch | JwtExpiredSignatureError | JwtInvalidSignatureError | JwtDecodeError
    ]:
        try:
            decoded_token: Dict[str, Any] = decode(jwt=token, key=self._key, algorithms=["HS256"])

            # https://www.cuemath.com/algebra/equal-sets/
            expected_keys_set = {key.name for key in fields(schema)}
            decoded_token_keys_set = set(decoded_token.keys())

            if not expected_keys_set.issubset(decoded_token_keys_set):
                return Err(JwtDecodeSchemaMismatch())

            if not decoded_token_keys_set.issubset(expected_keys_set):
                return Err(JwtDecodeSchemaMismatch())

            # By this point decoded_token should be in the expected format type which is a subclass of
            # DecodedJwtTokenBase, and we create a populated Schema object from the data stored in the decoded_token
            return Ok(schema.deserialize(decoded_token=cast(DecodedJwtTokenBase, decoded_token)))

        except ExpiredSignatureError:
            return Err(JwtExpiredSignatureError())

        except InvalidSignatureError:
            return Err(JwtInvalidSignatureError())

        except DecodeError:
            return Err(JwtDecodeError())


def jwt_utility_provider() -> JwtUtility:
    """
    Returns:
        A JwtUtility instance
    """
    return JwtUtility()
