import os
from unittest.mock import patch
from result import Err, Ok
from src.server.exception import JwtDecodeSchemaMismatch, JwtExpiredSignatureError, JwtInvalidSignatureError
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData, JwtUserVerification
from datetime import datetime, timedelta, timezone
from src.utils import JwtUtility

sufficient_expiration_time = (datetime.now(tz=timezone.utc) + timedelta(seconds=30)).timestamp()
instant_expiration_time = (datetime.now(tz=timezone.utc)).timestamp()


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_decode_success(mock_obj_id: str) -> None:
    payload = JwtUserData(sub=mock_obj_id, exp=sufficient_expiration_time)
    encoded_data = JwtUtility.encode_data(data=payload)
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtUserData)
    assert isinstance(decoded_data, Ok)
    assert decoded_data.ok_value == payload


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_failure_missing_keys(mock_obj_id: str) -> None:
    """Tests the case when the token is encoded with a schema that has less keys than our target"""
    encoded_data = JwtUtility.encode_data(data=JwtUserData(sub=mock_obj_id, exp=sufficient_expiration_time))
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtUserVerification)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtDecodeSchemaMismatch)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_failure_additional_keys(mock_obj_id: str) -> None:
    """Tests the case when the token is encoded with a schema that has more keys than our target"""
    encoded_data = JwtUtility.encode_data(
        data=JwtUserVerification(sub=mock_obj_id, is_admin=True, exp=sufficient_expiration_time)
    )
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtUserData)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtDecodeSchemaMismatch)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_decode_failure_expired_token(mock_obj_id: str) -> None:
    encoded_data = JwtUtility.encode_data(data=JwtUserData(sub=mock_obj_id, exp=instant_expiration_time))
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtUserData)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtExpiredSignatureError)


def test_encode_decode_secret_key_mismatch(mock_obj_id: str) -> None:
    # Mock the SECRET_KEY environment variable for encoding
    with patch.dict(os.environ, {"SECRET_KEY": "abcdefghijklmnopqrst"}):
        encoded_data = JwtUtility.encode_data(data=JwtUserData(sub=mock_obj_id, exp=sufficient_expiration_time))
        assert isinstance(encoded_data, str)  # Verify token is a string

    # Mock a different SECRET_KEY environment variable for decoding
    with patch.dict(os.environ, {"SECRET_KEY": "tsrqponmlkjihgfedcab"}):
        decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtUserData)
        assert isinstance(decoded_data, Err)  # Ensure the result is an error object
        assert isinstance(decoded_data.err_value, JwtInvalidSignatureError)
