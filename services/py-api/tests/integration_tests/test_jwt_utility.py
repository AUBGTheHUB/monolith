import os
from unittest.mock import patch
from result import Err, Ok
from src.server.exception import JwtDecodeSchemaMismatch, JwtExpiredSignatureError, JwtInvalidSignatureError
from src.server.schemas.jwt_schemas.schemas import JwtBase, JwtParticipantVerification
from datetime import datetime, timezone
from src.utils import JwtUtility


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_decode_success(mock_obj_id: str, thirty_sec_jwt_exp_limit: float) -> None:
    payload = JwtBase(sub=mock_obj_id, exp=thirty_sec_jwt_exp_limit)
    encoded_data = JwtUtility.encode_data(data=payload)
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtBase)
    assert isinstance(decoded_data, Ok)
    assert decoded_data.ok_value == payload


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_failure_missing_keys(mock_obj_id: str, thirty_sec_jwt_exp_limit: float) -> None:
    """Tests the case when the token is encoded with a schema that has less keys than our target"""
    encoded_data = JwtUtility.encode_data(data=JwtBase(sub=mock_obj_id, exp=thirty_sec_jwt_exp_limit))
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtParticipantVerification)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtDecodeSchemaMismatch)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_failure_additional_keys(mock_obj_id: str, thirty_sec_jwt_exp_limit: float) -> None:
    """Tests the case when the token is encoded with a schema that has more keys than our target"""
    encoded_data = JwtUtility.encode_data(
        data=JwtParticipantVerification(sub=mock_obj_id, is_admin=True, exp=thirty_sec_jwt_exp_limit)
    )
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtBase)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtDecodeSchemaMismatch)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_decode_failure_expired_token(mock_obj_id: str) -> None:
    encoded_data = JwtUtility.encode_data(
        data=JwtBase(sub=mock_obj_id, exp=(datetime.now(tz=timezone.utc)).timestamp())
    )
    assert isinstance(encoded_data, str)

    decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtBase)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtExpiredSignatureError)


def test_encode_decode_secret_key_mismatch(mock_obj_id: str, thirty_sec_jwt_exp_limit: float) -> None:
    # Mock the SECRET_KEY environment variable for encoding
    with patch.dict(os.environ, {"SECRET_KEY": "abcdefghijklmnopqrst"}):
        encoded_data = JwtUtility.encode_data(data=JwtBase(sub=mock_obj_id, exp=thirty_sec_jwt_exp_limit))
        assert isinstance(encoded_data, str)  # Verify token is a string

    # Mock a different SECRET_KEY environment variable for decoding
    with patch.dict(os.environ, {"SECRET_KEY": "tsrqponmlkjihgfedcab"}):
        decoded_data = JwtUtility.decode_data(token=encoded_data, schema=JwtBase)
        assert isinstance(decoded_data, Err)  # Ensure the result is an error object
        assert isinstance(decoded_data.err_value, JwtInvalidSignatureError)
