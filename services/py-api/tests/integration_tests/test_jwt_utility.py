from src.utils import JwtUtility, JwtUserData
from structlog import get_logger
from result import Ok

LOG = get_logger()


def test_jwt_encoding_decoding():
    payload = JwtUserData(sub="6719238430fe63030b3e73a5", team_id="67193455ee2785ecafca24e2", is_admin=True)
    encoded_msg = JwtUtility.encode_data(payload)
    LOG.debug(encoded_msg)
    assert isinstance(encoded_msg, str)

    decoded_msg = JwtUtility.decode_data(token=encoded_msg, schema=JwtUserData)
    assert isinstance(decoded_msg, Ok)
    assert decoded_msg.ok_value == payload
