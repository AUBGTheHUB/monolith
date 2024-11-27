from typing import TypedDict, Required

"""
The following wrapper around TypedDict is that so I can bind it to a generic type.
doing T = TypeVar('T', bound=TypedDcit) throws an error.
Proceeding as suggested in https://stackoverflow.com/questions/78518728/how-to-specify-a-generic-over-typeddict
"""


class BaseTypedDict(TypedDict):
    pass


# All the types within this should be required
class JwtUserData(BaseTypedDict):
    sub: Required[str]
    is_admin: Required[bool]
    team_id: Required[str]
