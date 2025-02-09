from abc import ABC
from typing import Any, Dict, Tuple, Type
from starlette import status
from pymongo.errors import DuplicateKeyError

ERROR_MAPPING: Dict[Type[BaseException], Tuple[str, int]] = {}
"""Maps custom errors to their representation (message, status_code), dynamically populated once a subclass of
CustomError is instantiated."""


class CustomError(ABC, BaseException):
    """Base class for all custom errors. Inheritors should override ``message`` and ``status_code``"""

    message: str
    status_code: int

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        This method is called when a class is subclassed.
        The default implementation does nothing. It may be overridden to extend subclasses.
        """
        super().__init_subclass__(**kwargs)

        # Add to the error mapping
        ERROR_MAPPING[cls] = (cls.message, cls.status_code)


class DuplicateEmailError(CustomError, DuplicateKeyError):
    message = "Participant with this email already exists"
    status_code = status.HTTP_409_CONFLICT


class DuplicateTeamNameError(CustomError, DuplicateKeyError):
    message = "Team with this name already exists"
    status_code = status.HTTP_409_CONFLICT


class HackathonCapacityExceededError(CustomError):
    """Exception raised when hackathon capacity has been reached."""

    message = "Max hackathon capacity has been reached"
    status_code = status.HTTP_409_CONFLICT


class ParticipantNotFoundError(CustomError):
    """Exception raised when there are no participants that match the query to the database"""

    message = "The specified participant was not found"
    status_code = status.HTTP_404_NOT_FOUND


class TeamNotFoundError(CustomError):
    """Exception raised when there are no teams that match the query to the database"""

    message = "The specified team was not found"
    status_code = status.HTTP_404_NOT_FOUND


class TeamCapacityExceededError(CustomError):
    """Exception raised when team capacity has been reached"""

    message = "Max team capacity has been reached"
    status_code = status.HTTP_409_CONFLICT


class TeamNameMissmatchError(CustomError):
    """Exception raised when the ``team_name`` passed in the request body is different from the ``team_name`` in the
    decoded JWT token, when a participant is registering via an invitation link.
    """

    message = "team_name passed in the request body is different from the team_name in the decoded JWT token"
    status_code = status.HTTP_400_BAD_REQUEST


class JwtDecodeSchemaMismatch(CustomError):
    """Exception raised when the decoded token does not match the structure of the defined JWT schema"""

    message = "The decoded token does not match the Jwt schema"
    status_code = status.HTTP_400_BAD_REQUEST


class JwtInvalidSignatureError(CustomError):
    """Exception raised by the Jwt Utility when the token has an invalid signature"""

    message = "The JWT token has invalid signature."
    status_code = status.HTTP_400_BAD_REQUEST


class JwtExpiredSignatureError(CustomError):
    """Exception raised by the Jwt Utility when the token has expired"""

    message = "The JWT token has expired."
    status_code = status.HTTP_400_BAD_REQUEST


class JwtDecodeError(CustomError):
    """Exception raised by the Jwt Utility when the token cannot be decoded"""

    message = "There was a a general error while decoding the JWT token. Checks its format again."
    status_code = status.HTTP_400_BAD_REQUEST

class FeatureSwitchNotFoundError(CustomError):
    message = "The feature switch was not found."
    status_code = status.HTTP_404_NOT_FOUND
