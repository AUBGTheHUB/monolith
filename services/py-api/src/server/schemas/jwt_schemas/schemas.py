from typing import TypedDict

"""
The following wrapper around TypedDict is that so we can bind it to a generic type.
doing T = TypeVar('T', bound=TypedDcit) throws an error.
Proceeding as suggested in https://stackoverflow.com/questions/78518728/how-to-specify-a-generic-over-typeddict
"""


class BaseTypedDict(TypedDict):
    pass


# All the types within this should be required
class JwtBase(BaseTypedDict):
    sub: str
    exp: float


class JwtParticipantVerification(JwtBase):
    is_admin: bool


class JwtParticipantInviteRegistration(JwtBase):
    team_id: str
