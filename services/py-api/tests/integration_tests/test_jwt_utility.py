import os
from unittest.mock import patch
from result import Err, Ok
from src.exception import JwtDecodeSchemaMismatch, JwtExpiredSignatureError, JwtInvalidSignatureError
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from src.service.jwt_utils.codec import JwtUtility


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_decode_success(
    jwt_utility_mock: JwtUtility, invite_link_jwt_payload_mock: JwtParticipantInviteRegistrationData
) -> None:
    # Given
    encoded_data = jwt_utility_mock.encode_data(data=invite_link_jwt_payload_mock)

    # When
    decoded_data = jwt_utility_mock.decode_data(token=encoded_data, schema=JwtParticipantInviteRegistrationData)

    # Then
    assert isinstance(encoded_data, str)
    assert isinstance(decoded_data, Ok)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_failure_missing_keys(
    jwt_utility_mock: JwtUtility, participant_verification_jwt_payload_mock: JwtParticipantVerificationData
) -> None:
    """Tests the case when the token is encoded with a schema that has less keys than our target"""

    # Given
    encoded_data = jwt_utility_mock.encode_data(data=participant_verification_jwt_payload_mock)

    # When
    decoded_data = jwt_utility_mock.decode_data(token=encoded_data, schema=JwtParticipantInviteRegistrationData)

    # Then
    assert isinstance(encoded_data, str)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtDecodeSchemaMismatch)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_encode_failure_additional_keys(
    invite_link_jwt_payload_mock: JwtParticipantInviteRegistrationData, jwt_utility_mock: JwtUtility
) -> None:
    """Tests the case when the token is encoded with a schema that has more keys than our target"""

    # Given
    encoded_data = jwt_utility_mock.encode_data(data=invite_link_jwt_payload_mock)

    # When
    decoded_data = jwt_utility_mock.decode_data(token=encoded_data, schema=JwtParticipantVerificationData)

    # Then
    assert isinstance(encoded_data, str)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtDecodeSchemaMismatch)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
def test_decode_failure_expired_token(
    expired_jwt_payload_mock: JwtParticipantInviteRegistrationData, jwt_utility_mock: JwtUtility
) -> None:
    # Given
    encoded_data = jwt_utility_mock.encode_data(data=expired_jwt_payload_mock)

    # When
    decoded_data = jwt_utility_mock.decode_data(token=encoded_data, schema=JwtParticipantInviteRegistrationData)

    # Then
    assert isinstance(encoded_data, str)
    assert isinstance(decoded_data, Err)
    assert isinstance(decoded_data.err_value, JwtExpiredSignatureError)


def test_encode_decode_secret_key_mismatch(invite_link_jwt_payload_mock: JwtParticipantInviteRegistrationData) -> None:
    # Given
    # Mock the SECRET_KEY environment variable for encoding
    with patch.dict(os.environ, {"SECRET_KEY": "abcdefghijklmnopqrst"}):
        # Create the mock_jwt_utility object under this context so that it has the given SECRET_KEY
        mock_jwt_utility = JwtUtility()
        encoded_data = mock_jwt_utility.encode_data(data=invite_link_jwt_payload_mock)
        assert isinstance(encoded_data, str)  # Verify token is a string

    # When
    # Mock a different SECRET_KEY environment variable for decoding
    with patch.dict(os.environ, {"SECRET_KEY": "tsrqponmlkjihgfedcab"}):
        # Re-create the jwt utility object so that we can produce the desired case
        mock_jwt_utility = JwtUtility()
        decoded_data = mock_jwt_utility.decode_data(token=encoded_data, schema=JwtParticipantInviteRegistrationData)
        # Then
        assert isinstance(decoded_data, Err)  # Ensure the result is an error object
        assert isinstance(decoded_data.err_value, JwtInvalidSignatureError)
