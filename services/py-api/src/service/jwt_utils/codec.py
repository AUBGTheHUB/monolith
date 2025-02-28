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
        # TODO: Rotate key on DEV and PROD: https://github.com/AUBGTheHUB/monolith/issues/937
        self._key = environ["SECRET_KEY"]
        """Key used for encoding and decoding the JWT token"""

        self._algorithm = "HS256"
        """We use HS256, a single-key (symmetric) hashing algorithm, as it's simpler to use when compared to RS256.
        Note in the future this might change, and probably should if we have other use-cases or a more complex system
        (e.g. multiple instances hosted across multiple nodes)
        To learn more: https://auth0.com/blog/rs256-vs-hs256-whats-the-difference/
        """

    def encode_data[T: JwtBase[DecodedJwtTokenBase]](self, data: T) -> str:
        return str(encode(payload=data.serialize(), key=self._key, algorithm=self._algorithm))

    def decode_data[
        T: JwtBase[DecodedJwtTokenBase]
    ](self, token: str, schema: Type[T]) -> Result[
        T, JwtDecodeSchemaMismatch | JwtExpiredSignatureError | JwtInvalidSignatureError | JwtDecodeError
    ]:
        try:
            decoded_token: Dict[str, Any] = decode(jwt=token, key=self._key, algorithms=[self._algorithm])

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
