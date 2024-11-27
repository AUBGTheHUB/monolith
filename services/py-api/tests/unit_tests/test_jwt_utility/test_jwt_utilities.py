import pytest
from typing import TypedDict
from unittest.mock import patch
from jwt import ExpiredSignatureError, InvalidSignatureError, DecodeError
from os import environ
from result import Ok, Err
from src.utils import JwtUtility


# Define a sample TypedDict schema
class TestSchema(TypedDict):
    sub: str
    is_admin: bool
    team_id: str


@pytest.fixture
def setup_secret_key():
    # Mock environment variable for the secret key
    environ["SECRET_KEY"] = "test-secret-key"


def test_encode_data(setup_secret_key):
    data = TestSchema(sub="test", is_admin=True, team_id="test")
    token = JwtUtility.encode_data(data)
    assert isinstance(token, str)  # Check if the token is a string


def test_decode_data_success(setup_secret_key):
    data = TestSchema(sub="test", is_admin=True, team_id="test")
    token = JwtUtility.encode_data(data)

    result = JwtUtility.decode_data(token, TestSchema)
    assert isinstance(result, Ok)  # Ensure result is successful
    assert result.ok_value == data  # Verify decoded data matches the input


def test_decode_data_missing_fields(setup_secret_key):
    data = {"user_id": 1}  # Incomplete data
    token = JwtUtility.encode_data(data)

    result = JwtUtility.decode_data(token, TestSchema)
    assert isinstance(result, Err)  # Ensure result indicates an error
    assert result.err_value == "The decoded token is missing some or all of the required fields."


def test_decode_data_expired_token(setup_secret_key):
    with patch("jwt.decode", side_effect=ExpiredSignatureError):
        token = "fake.token.string"
        result = JwtUtility.decode_data(token, TestSchema)
        assert isinstance(result, Err)
        assert result.err_value == "The JWT token has expired."


def test_decode_data_invalid_signature(etup_secret_key):
    with patch("jwt.decode", side_effect=InvalidSignatureError):
        token = "fake.token.string"
        result = JwtUtility.decode_data(token, TestSchema)
        assert isinstance(result, Err)
        assert result.err_value == "The JWT token has invalid signature."


def test_decode_data_general_error(setup_secret_key):
    with patch("jwt.decode", side_effect=DecodeError):
        token = "fake.token.string"
        result = JwtUtility.decode_data(token, TestSchema)
        assert isinstance(result, Err)
        assert result.err_value == "There was a a general error while decoding the JWT token. Checks its format again."
