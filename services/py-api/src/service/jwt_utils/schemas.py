"""Here we store the schemas which model the data stored in a JWT token for different use cases.

These schemas are different from the OpenAPI spec ones. They are used only for providing a more deterministic way of
knowing what the JWT token should contain depending on the use case.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypedDict, Self, TypeVar, Generic

from src.database.model.admin.hub_admin_model import ROLES
from src.database.model.admin.hub_member_model import MEMBER_TYPE


class DecodedJwtTokenBase(TypedDict):
    """
    A Type representing a DecodedJwtToken. This is just a Type and application developers should not create a
    DecodedJwtToken instance.
    """

    # The following wrapper around TypedDict is created so we can bind it to a generic type.
    # doing [T: TypedDict] throws an error: "typing.TypedDict" is not valid as a type.
    # Proceeding as suggested in https://stackoverflow.com/questions/78518728/how-to-specify-a-generic-over-typeddict
    sub: str
    exp: int


# TypedDicts are used only as type hints below, they should not be initialized or used outside of this file!
class _DecodedJwtParticipantVerificationToken(DecodedJwtTokenBase):
    """A Type representing a decoded JWT token used for verifying the emails of participants"""

    is_admin: bool


class _DecodedJwtInviteRegistrationToken(DecodedJwtTokenBase):
    """A Type representing a decoded JWT token used in the invite_link which is sent to every verified admin
    participant"""

    team_name: str
    team_id: str


class _DecodedJwtAdminToken(DecodedJwtTokenBase):
    """A Type representing a decoded JWT token used for authenticating HUB Admins"""

    member_type: MEMBER_TYPE = "admin"
    site_role: ROLES


class _RefreshJwtToken(DecodedJwtTokenBase):
    """A Type representing a decoded JWT token used for refreshing"""

    token_type: str = "refresh"


# We need the following dataclasses, because Python typing system is not that advanced, and even though we use Generics
# in the `JwtUtils.decode` method (passing a schema), if this schema was one of the following TypeDicts above, when the
# type is inferred, for example like this:
# result = JwtUtility.decode_data(token=jwt_token, schema=DecodedJwtToken)
# result is not of type DecodedJwtToken but is actually the standard dict type: dict[str, str | float], meaning
# when accessing the attributes of the schema (result["sub"]), they won't be autocompleted as the type is a normal dict
# and not a TypedDict

# Here we had to use the old Generics syntax, to tell my-py that this TypeVar is covariant explicitly, as otherwise it
# was giving incompatible type "JwtParticipantVerificationData"; expected "JwtBase[DecodedJwtTokenBase]", even though:
# JwtParticipantVerificationData is a subtype of JwtBase[DecodedJwtTokenBase]
# To learn more:
# https://typing.readthedocs.io/en/latest/spec/generics.html#variance-inference
# https://typing.readthedocs.io/en/latest/spec/generics.html#variance
T_co = TypeVar("T_co", bound=DecodedJwtTokenBase, covariant=True)


@dataclass(kw_only=True)
class JwtBase(Generic[T_co], ABC):
    """Generic Schema (model) representing the base fields that every JWT token issued by us includes"""

    sub: str
    """The ObjectID of the participant/user.
    https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims#registered-claims    """
    exp: int
    """Time after which the JWT expires (represented in Epoch time)"""

    @abstractmethod
    def serialize(self) -> T_co:
        """Creates a dict format of the schema. The format of the dict is the passed Type in the Generic class."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def deserialize(cls, decoded_token: T_co) -> Self:
        """Creates a Schema object from the passed decoded_token (raw dict).

        Implementations are not responsible for verifying if the passed decoded_token (raw dict) contains the same        fields as the schema object. This verification should happen in the caller (in an upper level)!
        """
        raise NotImplementedError()


@dataclass(kw_only=True)
class JwtParticipantVerificationData(JwtBase[_DecodedJwtParticipantVerificationToken]):
    is_admin: bool
    """If the participant we are verifying is an admin. If this is True, they will receive a special email containing
    an ``invite_link`` which they should share with other team members, who should join their team"""

    def serialize(self) -> _DecodedJwtParticipantVerificationToken:
        return _DecodedJwtParticipantVerificationToken(sub=self.sub, exp=self.exp, is_admin=self.is_admin)

    @classmethod
    def deserialize(cls, decoded_token: _DecodedJwtParticipantVerificationToken) -> Self:
        return cls(sub=decoded_token["sub"], is_admin=decoded_token["is_admin"], exp=decoded_token["exp"])


@dataclass(kw_only=True)
class JwtParticipantInviteRegistrationData(JwtBase[_DecodedJwtInviteRegistrationToken]):
    team_name: str
    """The name of the Team entity in Mongo. Used by the front-end when displaying special registration form"""
    team_id: str
    """The ObjectID of the Team entity in Mongo. This is the team which team members registering via the``invite_link``
    should join"""

    def serialize(self) -> _DecodedJwtInviteRegistrationToken:
        return _DecodedJwtInviteRegistrationToken(
            sub=self.sub, exp=self.exp, team_id=self.team_id, team_name=self.team_name
        )

    @classmethod
    def deserialize(cls, decoded_token: _DecodedJwtInviteRegistrationToken) -> Self:
        return cls(
            sub=decoded_token["sub"],
            team_id=decoded_token["team_id"],
            exp=decoded_token["exp"],
            team_name=decoded_token["team_name"],
        )


@dataclass(kw_only=True)
class JwtAdminToken(JwtBase[_DecodedJwtAdminToken]):
    member_type: MEMBER_TYPE = "admin"
    site_role: ROLES

    def serialize(self) -> _DecodedJwtAdminToken:
        return _DecodedJwtAdminToken(sub=self.sub, exp=self.exp, member_type=self.member_type, site_role=self.site_role)

    @classmethod
    def deserialize(cls, decoded_token: _DecodedJwtAdminToken) -> Self:
        return cls(
            sub=decoded_token["sub"],
            member_type=decoded_token["member_type"],
            exp=decoded_token["exp"],
            site_role=decoded_token["site_role"],
        )


@dataclass(kw_only=True)
class JwtRefreshToken(JwtBase[_RefreshJwtToken]):
    token_type: str = "refresh"

    def serialize(self) -> _RefreshJwtToken:
        return _RefreshJwtToken(sub=self.sub, exp=self.exp, token_type=self.token_type)

    @classmethod
    def deserialize(cls, decoded_token: _RefreshJwtToken) -> Self:
        return cls(sub=decoded_token["sub"], token_type=decoded_token["token_type"], exp=decoded_token["exp"])
